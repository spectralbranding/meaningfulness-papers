#!/usr/bin/env python3
"""Step 2 of the 2026bl run: Layer S -- validate the segmenter BEFORE any operator call.

The order is the substantive part (M1a): measured afterwards, the segmenter's
error becomes available as an explanation for whatever the operators did.

Two adjudicators decide, independently and blind, which candidate positions are
unit boundaries; a third resolves only the positions they disagree on. Nothing
here tells any model what the division is for, that another model is doing the
same task, or what this study expects.

Candidate positions are fixed by a rule that does not consult the segmenter
(PROTOCOL.yaml `layer_s`), so all three parties decide over one shared index and
kappa is defined without an alignment step.

Run (keys injected, never printed):
    bws run -- uv run --with httpx --with pyyaml python \\
        code/adjudicate_segmentation.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402
from segment_units import is_symbolic  # noqa: E402

# Candidate boundary positions. Deliberately generous: a position no party
# would choose still costs nothing but a "no" from each of them, whereas a
# position missing from the index set is a disagreement that CANNOT BE SEEN --
# and an index that cannot represent a division's boundaries would flatter
# whichever party makes them.
#
# Three sources, all rules about the text and none of them consulting the
# segmenter: a sentence-terminating mark; a blank-line break; and the edges of a
# displayed-mathematics block, which is where a rule that splits on punctuation
# is most likely to cut and where M1c says it must not.
_CANDIDATE = re.compile(r"""[.?!]["'\)\]]*(?=\s)|\n[ \t]*\n""")


def _math_block_edges(text: str) -> set[int]:
    """Start and end offsets of every blank-line block that is purely symbolic."""
    edges: set[int] = set()
    pos = 0
    for block in re.split(r"(\n[ \t]*\n)", text):
        if block and not block.startswith("\n"):
            if is_symbolic(block):
                edges.add(pos)
                edges.add(pos + len(block.rstrip()))
        pos += len(block)
    return edges


def candidates(text: str) -> list[int]:
    """Character offsets at which a unit may end, by the declared rule."""
    found = {m.end() for m in _CANDIDATE.finditer(text)}
    found |= _math_block_edges(text)
    return sorted(p for p in found if 0 < p < len(text))


def marked(text: str, cands: list[int]) -> str:
    """The text with a numbered marker at every candidate position."""
    out, prev = [], 0
    for i, pos in enumerate(cands, start=1):
        out.append(text[prev:pos])
        out.append(f"<<{i}>>")
        prev = pos
    out.append(text[prev:])
    return "".join(out)


def boundaries_from_spans(
    spans: list[list[int]], cands: list[int]
) -> tuple[set[int], int]:
    """Which candidates a division treats as boundaries, from its exact spans.

    A unit end that is not itself a candidate is snapped to the nearest
    candidate within a few characters: trailing whitespace and the math merge
    move an end by a character or two, and charging that as a disagreement
    would measure the snapping rather than the segmenter. An end with no
    candidate within that window is counted as UNREPRESENTABLE and reported --
    an index that cannot express a boundary would silently flatter whoever drew
    it, which is the failure this whole design exists to avoid.
    """
    ends: set[int] = set()
    unrepresentable = 0
    cand_set = set(cands)
    for _, end in spans[:-1]:  # the final unit's end is the document end
        if end in cand_set:
            ends.add(end)
            continue
        near = [c for c in cands if abs(c - end) <= 3]
        if near:
            ends.add(min(near, key=lambda c: abs(c - end)))
        else:
            unrepresentable += 1
    return ends, unrepresentable


def cohen_kappa(a: set[int], b: set[int], universe: list[int]) -> dict:
    """Cohen's kappa for two binary labellings of the same index set."""
    n = len(universe)
    both = len(a & b)
    neither = n - len(a | b)
    only_a = len(a - b)
    only_b = len(b - a)
    po = (both + neither) / n if n else 0.0
    pa1, pb1 = len(a) / n if n else 0, len(b) / n if n else 0
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return {
        "n_candidates": n,
        "both_boundary": both,
        "neither": neither,
        "only_first": only_a,
        "only_second": only_b,
        "raw_agreement": po,
        "expected_agreement": pe,
        "kappa": kappa,
        "marginal_first": pa1,
        "marginal_second": pb1,
    }


# A whole document in one call does not survive contact with the providers: on
# the first attempt one adjudicator spent its entire 32,000-token budget
# reasoning and returned empty content, and another answered a 614-candidate
# document with 64 boundaries. So the decision is put in CHUNKS of candidates,
# each with its own text and its own small answer. Chunking changes nothing
# about what is decided -- every candidate is still decided exactly once, under
# the same rule, by the same model -- and every chunk is cached, so an
# interrupted pass resumes instead of re-asking.
CHUNK = 25


def _chunk_ranges(cands: list[int], text: str) -> list[tuple[int, list[int]]]:
    """(chunk index, candidate offsets) for each chunk, in document order."""
    return [(i // CHUNK, cands[i : i + CHUNK]) for i in range(0, len(cands), CHUNK)]


def ask_adjudicator(doc: str, adj: dict, text: str, cands: list[int]) -> set[int]:
    path = L.inventory_path(doc, adj["id"])
    state = (
        L.load_json(path)
        if path.exists()
        else {
            "document": doc,
            "source": adj["id"],
            "model": adj["model"],
            "family": adj["family"],
            "prompt_version": L.PROMPT_VERSION,
            "n_candidates": len(cands),
            "chunk_size": CHUNK,
            "chunks": {},
        }
    )
    system = L.SEGMENT_SYSTEM + """

You are given a passage with numbered markers <<1>>, <<2>>, ... at every position
where a unit could end. Decide, for EACH marker in turn, whether a unit ends
there. Most markers in ordinary prose do end a unit; a marker after an
abbreviation, an initial, a decimal or a symbol does not, and neither does one
inside a displayed expression.

OUTPUT. A single JSON object: {"boundaries": [1, 4, 5, ...]}, listing exactly
the marker numbers at which a unit ends. Answer with the JSON object only: no
reasoning, no prose, no markdown fence."""

    for idx, chunk in _chunk_ranges(cands, text):
        key = str(idx)
        if key in state["chunks"]:
            continue
        lo = cands[idx * CHUNK - 1] if idx > 0 else 0
        hi = chunk[-1] + 240
        local = [c for c in chunk]
        passage = text[lo:hi]
        out, prev = [], lo
        for i, pos in enumerate(local, start=1):
            out.append(text[prev:pos])
            out.append(f"<<{i}>>")
            prev = pos
        out.append(text[prev:hi])
        try:
            raw = L.call_model(
                adj["model"],
                adj["family"],
                system,
                f"PASSAGE WITH MARKERS ({len(local)} markers).\n\n{''.join(out)}\n",
                role="segmentation_adjudicator",
                operation=f"adjudicate|{adj['id']}|{doc}|c{idx}",
                phase="unitization_layer_s",
                max_out=16000,
                reasoning="low",
            )
            picked = L.parse_json_block(raw).get("boundaries") or []
        except Exception as exc:  # noqa: BLE001
            # One chunk that will not parse must not cost the document. The
            # chunk is recorded as UNANSWERED and the pass continues; an
            # unanswered chunk contributes no boundary, which is visible in the
            # count rather than silently indistinguishable from "no boundaries
            # here", because the key is written to `unanswered`.
            state.setdefault("unanswered", []).append(idx)
            state["chunks"][key] = []
            L.write_json(path, state)
            print(
                f"    {doc:8s} {adj['id']:6s} chunk {idx:3d} UNANSWERED {type(exc).__name__}",
                flush=True,
            )
            continue
        state["chunks"][key] = sorted(
            {
                local[i - 1]
                for i in picked
                if isinstance(i, int) and 1 <= i <= len(local)
            }
        )
        L.write_json(path, state)
        print(
            f"    {doc:8s} {adj['id']:6s} chunk {idx:3d} {len(state['chunks'][key]):3d}/{len(local)}",
            flush=True,
        )
        _ = passage  # the slice is what the markers were placed into

    keep = sorted({c for v in state["chunks"].values() for c in v})
    state["boundaries"] = keep
    L.write_json(path, state)
    print(f"  {doc:8s} {adj['id']:6s} boundaries={len(keep)}/{len(cands)}")
    return set(keep)


def resolve(
    doc: str, res: dict, text: str, cands: list[int], disputed: list[int]
) -> set[int]:
    """Put only the disputed positions to the resolver, without attribution."""
    path = L.inventory_path(doc, "resolution")
    if path.exists():
        return set(L.load_json(path)["boundaries"])
    if not disputed:
        L.write_json(
            path,
            {"document": doc, "source": res["id"], "disputed": [], "boundaries": []},
        )
        return set()
    idx = {c: i + 1 for i, c in enumerate(cands)}
    items = []
    for pos in disputed:
        before = text[max(0, pos - 220) : pos].replace("\n", " ")
        after = text[pos : pos + 220].replace("\n", " ")
        items.append(f"marker {idx[pos]}: ...{before}  <<HERE>>  {after}...")
    system = L.RESOLVE_SYSTEM + """

You are given the positions two independent divisions disagreed about, each
shown with the text before and after it. You are not told which division chose
what. Decide, for each, whether a unit ends at that position.

OUTPUT. A single JSON object: {"boundaries": [<marker numbers where a unit
ends>]}, drawn only from the markers you were given. No prose, no fence."""
    raw = L.call_model(
        res["model"],
        res["family"],
        system,
        "DISPUTED POSITIONS.\n\n" + "\n\n".join(items) + "\n",
        role="adjudication_resolver",
        operation=f"resolve|{res['id']}|{doc}",
        phase="unitization_layer_s",
        max_out=16000,
        reasoning="low",
    )
    picked = L.parse_json_block(raw).get("boundaries") or []
    rev = {i + 1: c for i, c in enumerate(cands)}
    keep = sorted(
        {
            rev[i]
            for i in picked
            if isinstance(i, int) and i in rev and rev[i] in set(disputed)
        }
    )
    L.write_json(
        path,
        {
            "document": doc,
            "source": res["id"],
            "model": res["model"],
            "family": res["family"],
            "disputed": disputed,
            "boundaries": keep,
        },
    )
    print(
        f"  {doc:8s} {res['id']:6s} resolved {len(keep)}/{len(disputed)} disputed as boundaries"
    )
    return set(keep)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="*")
    ap.add_argument(
        "--score-only",
        action="store_true",
        help="recompute Layer S from cached adjudications; makes no call",
    )
    args = ap.parse_args()

    proto = L.protocol()
    docs = [d for d in proto["specimens"] if not args.docs or d in args.docs]
    adjs = proto["segmentation_adjudicators"]
    res = proto["adjudication_resolver"]
    gate = float(proto["thresholds"]["layer_S_segmenter_kappa"])

    rows = []
    for doc in docs:
        text = L.specimen_text(doc)
        cands = candidates(text)
        inv = L.load_json(L.inventory_path(doc, "segmenter"))
        seg_bounds, unrepresentable = boundaries_from_spans(inv["spans"], cands)

        if args.score_only:
            a1 = set(
                L.load_json(L.inventory_path(doc, adjs[0]["id"])).get("boundaries")
                or []
            )
            a2 = set(
                L.load_json(L.inventory_path(doc, adjs[1]["id"])).get("boundaries")
                or []
            )
        else:
            a1 = ask_adjudicator(doc, adjs[0], text, cands)
            a2 = ask_adjudicator(doc, adjs[1], text, cands)
        disputed = sorted(a1 ^ a2)
        rpath = L.inventory_path(doc, "resolution")
        if args.score_only:
            resolved = (
                set(L.load_json(rpath).get("boundaries") or [])
                if rpath.exists()
                else set()
            )
        else:
            resolved = resolve(doc, res, text, cands, disputed)
        adjudicated = (a1 & a2) | resolved

        inter = cohen_kappa(a1, a2, cands)
        layer_s = cohen_kappa(seg_bounds, adjudicated, cands)
        rows.append(
            {
                "document": doc,
                "n_candidates": len(cands),
                "units_segmenter": len(inv["units"]),
                "units_adjudicated": len(adjudicated) + 1,
                "math_merges": inv["math_merges"],
                "segmenter_boundaries_unrepresentable": unrepresentable,
                "adjudicator_kappa": inter,
                "layer_s_kappa": layer_s,
                "gate": gate,
                "passes": layer_s["kappa"] >= gate,
            }
        )
        print(
            f"  {doc:8s} LAYER S kappa={layer_s['kappa']:.3f} "
            f"(adjudicators agree at {inter['kappa']:.3f}) "
            f"{'PASS' if layer_s['kappa'] >= gate else 'FAIL'} at {gate}"
        )

    L.write_json(
        L.OUTPUT_DIR / "tables" / "layer_s.json",
        {"gate": gate, "measured_before_any_operator_call": True, "rows": rows},
    )
    failed = [r["document"] for r in rows if not r["passes"]]
    print(
        f"\nLayer S: {len(rows) - len(failed)}/{len(rows)} pass; failing: {failed or 'none'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
