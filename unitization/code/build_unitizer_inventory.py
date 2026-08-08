#!/usr/bin/env python3
"""U-mod's inventory: a model family used neither as operator nor as adjudicator.

The unitizer sees the document and the declared unit rule. It is not told what
the division will be used for, that another division of the same document
exists, or that anything will be compared.

Long documents are divided in passes over blank-line blocks, so that no single
call has to re-emit an 11,000-word text: each pass covers a contiguous run of
blocks, the units it returns are located back in the source by search, and the
run continues from where the last located unit ended. A block whose units
cannot be located is recorded as UNLOCATED rather than dropped silently.

Run (keys injected, never printed):
    bws run -- uv run --with httpx --with pyyaml python \\
        code/build_unitizer_inventory.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402

BLOCK_CHARS = 3000  # per call: enough context to divide, small enough to re-emit


def blocks(text: str) -> list[tuple[int, int]]:
    """Contiguous passes over the text, cut only at blank lines."""
    spans, start = [], 0
    for m in re.finditer(r"\n[ \t]*\n", text):
        if m.end() - start >= BLOCK_CHARS:
            spans.append((start, m.start()))
            start = m.end()
    if start < len(text):
        spans.append((start, len(text)))
    return spans


def _normalized(text: str) -> tuple[str, list[int]]:
    """Whitespace-collapsed text plus a map from each collapsed char to its source offset.

    The unitizer re-emits the text, and re-emission normalizes whitespace: a
    displayed expression that sits between blank lines in the source comes back
    joined by a single space. Matching on the raw text therefore loses whole
    units of a mathematical document -- 11 of 21 in one block on the first pass
    -- for a reason that has nothing to do with how the model divided it.
    """
    out, idx = [], []
    prev_ws = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev_ws:
                out.append(" ")
                idx.append(i)
            prev_ws = True
        else:
            out.append(ch)
            idx.append(i)
            prev_ws = False
    idx.append(len(text))
    return "".join(out), idx


def locate(
    units: list[str], text: str, frm: int, to: int
) -> tuple[list[list[int]], int]:
    """Map returned unit strings back onto source offsets; count what will not map."""
    norm, idx = _normalized(text)
    # offsets into `norm` for the block boundaries
    lo = next((k for k, src in enumerate(idx) if src >= frm), 0)
    hi = next((k for k, src in enumerate(idx) if src >= to), len(norm))
    spans, pos, unlocated = [], lo, 0
    for u in units:
        needle = " ".join(str(u).split())
        if not needle:
            continue
        at = norm.find(needle, pos, hi + 400)
        if at < 0:  # fall back to the head, which survives a paraphrased tail
            head = " ".join(needle.split()[:8])
            at = norm.find(head, pos, hi + 400)
            if at < 0:
                unlocated += 1
                continue
            end_n = at + len(head)
        else:
            end_n = at + len(needle)
        start = idx[at]
        end = idx[min(end_n, len(idx) - 1)]
        spans.append([start, min(end, to)])
        pos = end_n
    return spans, unlocated


def _returned_from_logs(doc: str) -> dict[int, list[str]]:
    """Recover what the unitizer returned, per block, from the append-only call log.

    The first pass cached spans but not the strings they came from, and a
    correction to the LOCATOR must not cost a second set of calls: the model's
    answer is already on disk, in the log, which is what an append-only log is
    for.
    """
    import json
    import re as _re

    out: dict[int, list[str]] = {}
    for f in sorted((L.LOGS_DIR).glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except Exception:  # noqa: BLE001 -- a partial line is not a failure
                continue
            m = _re.match(
                rf"unitize\|[^|]+\|{_re.escape(doc)}\|b(\d+)$",
                str(row.get("operation", "")),
            )
            if not m:
                continue
            try:
                units = (
                    L.parse_json_block(str(row.get("response") or "")).get("units")
                    or []
                )
            except Exception:  # noqa: BLE001
                continue
            if units:
                out[int(m.group(1))] = units
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="*")
    ap.add_argument(
        "--relocate",
        action="store_true",
        help="re-derive spans from what the unitizer already returned, without calling it again",
    )
    args = ap.parse_args()

    proto = L.protocol()
    uni = proto["unitizer"]
    docs = [d for d in proto["specimens"] if not args.docs or d in args.docs]

    for doc in docs:
        path = L.inventory_path(doc, "unitizer")
        text = L.specimen_text(doc)
        state = (
            L.load_json(path)
            if path.exists()
            else {
                "document": doc,
                "source": "unitizer",
                "model": uni["model"],
                "family": uni["family"],
                "prompt_version": L.PROMPT_VERSION,
                "block_chars": BLOCK_CHARS,
                "passes": {},
            }
        )
        bs = blocks(text)
        if args.relocate:
            returned = _returned_from_logs(doc)
            for key, p in state["passes"].items():
                units = p.get("returned_units") or returned.get(int(key)) or []
                frm, to = p["range"]
                spans, unlocated = locate(
                    [u for u in units if str(u).strip()], text, frm, to
                )
                p["returned_units"] = units
                p["spans"], p["located"], p["unlocated"] = spans, len(spans), unlocated
            L.write_json(path, state)
        for i, (frm, to) in enumerate(bs):
            key = str(i)
            if key in state["passes"]:
                continue
            try:
                raw = L.call_model(
                    uni["model"],
                    uni["family"],
                    L.UNITIZE_SYSTEM,
                    L.UNITIZE_USER.format(text=text[frm:to]),
                    role="unitizer",
                    operation=f"unitize|{uni['id']}|{doc}|b{i}",
                    phase="unitization_umod_inventory",
                    max_out=16000,
                    reasoning="low",
                )
                units = L.parse_json_block(raw).get("units") or []
            except Exception as exc:  # noqa: BLE001
                # A block whose answer will not parse is recorded as unparsed
                # and the pass continues. Dropping the whole inventory because
                # one block of mathematics broke JSON escaping would lose four
                # documents' work to one call; the gap is reported instead.
                state["passes"][key] = {
                    "range": [frm, to],
                    "returned_units": [],
                    "returned": 0,
                    "located": 0,
                    "unlocated": 0,
                    "spans": [],
                    "unparsed": f"{type(exc).__name__}: {str(exc)[:160]}",
                }
                L.write_json(path, state)
                print(
                    f"    {doc:8s} block {i:3d} UNPARSED {type(exc).__name__}",
                    flush=True,
                )
                continue
            spans, unlocated = locate(
                [u for u in units if str(u).strip()], text, frm, to
            )
            state["passes"][key] = {
                "range": [frm, to],
                "returned_units": units,
                "returned": len(units),
                "located": len(spans),
                "unlocated": unlocated,
                "spans": spans,
            }
            L.write_json(path, state)
            print(
                f"    {doc:8s} block {i:3d} returned={len(units):4d} located={len(spans):4d} "
                f"unlocated={unlocated}",
                flush=True,
            )

        spans = [
            s
            for k in sorted(state["passes"], key=int)
            for s in state["passes"][k]["spans"]
        ]
        state["spans"] = spans
        state["units"] = [text[a:b].strip() for a, b in spans]
        state["unlocated_total"] = sum(p["unlocated"] for p in state["passes"].values())
        state["unparsed_blocks"] = [
            k for k, p in state["passes"].items() if p.get("unparsed")
        ]
        L.write_json(path, state)
        print(
            f"  {doc:8s} unitizer units={len(spans)} unlocated={state['unlocated_total']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
