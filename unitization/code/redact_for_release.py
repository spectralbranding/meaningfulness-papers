#!/usr/bin/env python3
"""Build the publishable release tree for 2026bl.

Run:
    uv run python code/redact_for_release.py --out release
    uv run python code/redact_for_release.py --out release --verify

The five specimens are third-party works. Three classes of run artifact carry
their TEXT rather than referring to it, and none of the three may be published:

  * U-free extraction records  -- each node carries a verbatim `span` (up to 272
    characters here) plus a `statement`; fifty such records are a substantial
    extract of somebody else's document.
  * segmenter / unitizer inventories -- these ARE the documents, cut into units
    (longest single unit here: 687 characters).
  * raw per-call logs -- the prompts embed the passages the operators were shown
    (longest string: 59,512 characters, i.e. a whole specimen).

What ships instead is the same material reduced to what the analysis actually
consumes. The U-free matcher uses located character OFFSETS and never the span
text itself (score_layers.free_view), so publishing offsets preserves every
coefficient exactly while carrying no source text. Inventories become offsets
plus a digest per unit. Logs keep the full professional-logging metadata --
model version, epoch, parameters, token usage, latency, retries -- with the
prompt and response bodies replaced by their digests.

Published verbatim, because they carry no source text at all: the 100
fixed-condition extraction records (an answer under a supplied inventory is a
set of unit indices and typed edges; longest string 31 characters), the
adjudicator and resolution inventories (longest string 18), and the derived
tables.

--verify re-scores every cell from the redacted records and compares against the
committed tables. The redaction is only correct if that comparison is exact; it
is checked rather than asserted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PAPER_DIR / "data"
LOG_DIR = PAPER_DIR / "output" / "logs"
TABLE_DIR = PAPER_DIR / "output" / "tables"

sys.path.insert(0, str(PAPER_DIR / "code"))

# Any string longer than this is replaced by its digest, ANYWHERE in a published
# record. Enumerating the fields that carry text does not work -- the first pass
# of this script missed two (`passes` in the unitizer inventories, and the
# encoded reasoning blobs inside `response_metadata`), and the next schema change
# would add a third. A depth-first sweep makes the guarantee structural: no
# published string exceeds the limit, whatever the provider decides to put in a
# field tomorrow. 80 is the tightest bound that clears every legitimate value: a unit
# digest is 71 characters and a model identifier under 30.
MAX_STR = 80

# Fields whose value is free text from, or derived verbatim from, a specimen.
TEXT_FIELDS_NODE = ("span", "statement", "text", "quote")
LOG_BODY_FIELDS = ("system_prompt", "user_prompt", "response")


def digest(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()


# Fields that hold specimen text BY ROLE, and are therefore digested whole
# regardless of how short any individual value is. The length sweep alone is not
# sufficient and the reason is worth recording: `passes[].returned_units` is a
# list of the units the unitizer emitted, i.e. the document cut into sentences.
# Sweeping by length published every unit under the threshold verbatim -- which
# is most of them, since sentences are short -- and a few hundred short sentences
# concatenate back into the document. Length cannot distinguish a short piece of
# metadata from a short piece of somebody else's paper. Role can.
TEXT_BEARING_KEYS = ("returned_units", "units", "text", "unit", "span", "statement")

# Blocks this script writes itself, exempt from the sweep so its own notes stay
# readable rather than being replaced by digests of themselves.
SELF_AUTHORED_KEYS = ("_redaction",)


def sweep(obj, _stats=None, _key=None):
    """Depth-first redaction.

    Two rules, and the first is the one that matters. A value under a
    text-bearing KEY is digested whole, however short it is. Everything else is
    digested only if it exceeds MAX_STR, which is the backstop for fields no one
    anticipated -- the encoded reasoning blobs providers attach, for instance.
    """
    if _stats is None:
        _stats = {"n": 0}
    if _key in SELF_AUTHORED_KEYS:
        return obj
    if isinstance(obj, str):
        if _key in TEXT_BEARING_KEYS or len(obj) > MAX_STR:
            _stats["n"] += 1
            return {"digest": digest(obj), "n_chars": len(obj), "redacted": True}
        return obj
    if isinstance(obj, dict):
        return {k: sweep(v, _stats, k) for k, v in obj.items()}
    if isinstance(obj, list):
        # A list inherits its parent's key: the elements of `returned_units` are
        # units, and each one is text even though the list itself is not.
        return [sweep(v, _stats, _key) for v in obj]
    return obj


def locate_all(result: dict, text: str) -> dict:
    """Replace every node's verbatim span with its located character offsets."""
    import score_layers as S

    out = json.loads(json.dumps(result))
    kept, dropped = 0, 0
    for n in out.get("nodes") or []:
        span = (n.get("span") or "").strip()
        loc = S._locate(text, span) if span else None
        if loc:
            n["span_offsets"] = [loc[0], loc[1]]
            kept += 1
        else:
            # Unlocatable span: the node contributed nothing to matching in the
            # original run either (free_view drops it), so it contributes
            # nothing here. Recorded so the count is auditable.
            n["span_unlocatable"] = True
            dropped += 1
        for f in TEXT_FIELDS_NODE:
            n.pop(f, None)
    out["_redaction"] = {
        "spans_replaced_by_offsets": kept,
        "spans_unlocatable_in_source": dropped,
        "note": (
            "Verbatim spans removed; offsets are what the matcher consumes. "
            "Reconstructing the text requires the specimen, which is not "
            "redistributed."
        ),
    }
    return out


def redact_inventory(inv: dict) -> dict:
    """Units become offsets + digest. No unit text survives."""
    out = json.loads(json.dumps(inv))
    units = out.get("units") or []
    red = []
    for i, u in enumerate(units):
        if isinstance(u, dict):
            t = u.get("text") or u.get("unit") or ""
            entry = {k: v for k, v in u.items() if k not in ("text", "unit")}
        else:
            t = str(u)
            entry = {}
        entry["index"] = i
        entry["n_chars"] = len(t)
        entry["digest"] = digest(t)
        red.append(entry)
    out["units"] = red
    out["passes"] = sweep(out.get("passes"))
    # `spans` are (start, end) offsets already -- they carry no text and stay.
    out["_redaction"] = {
        "unit_text_removed": True,
        "n_units": len(red),
        "note": (
            "Unit boundaries and digests only. The inventory IS the specimen "
            "when its text is included, so the text is not published."
        ),
    }
    return out


def redact_log_line(rec: dict) -> dict:
    out = dict(rec)
    for f in LOG_BODY_FIELDS:
        v = out.get(f)
        if isinstance(v, str):
            out[f] = {"digest": digest(v), "n_chars": len(v), "redacted": True}
        elif v is not None:
            s = json.dumps(v, sort_keys=True)
            out[f] = {"digest": digest(s), "n_chars": len(s), "redacted": True}
    return out


def build(out_root: Path) -> dict:
    import unit_lib as L

    if out_root.exists():
        shutil.rmtree(out_root)
    for sub in ("records", "inventories", "tables", "logs"):
        (out_root / sub).mkdir(parents=True)

    counts = {
        "records_verbatim": 0,
        "records_offsets": 0,
        "inventories_verbatim": 0,
        "inventories_redacted": 0,
        "logs": 0,
        "tables": 0,
    }
    texts: dict[str, str] = {}

    for p in sorted(DATA_DIR.glob("extract_*.json")):
        doc = p.name.split("__")[0][len("extract_") :]
        rec = json.loads(p.read_text())
        if "__u_free__" in p.name:
            if doc not in texts:
                texts[doc] = L.specimen_text(doc)
            red = sweep(locate_all(rec, texts[doc]))
            counts["records_offsets"] += 1
        else:
            red = rec
            counts["records_verbatim"] += 1
        (out_root / "records" / p.name).write_text(json.dumps(red, indent=1))

    for p in sorted(DATA_DIR.glob("inventory_*.json")):
        inv = json.loads(p.read_text())
        if p.name.endswith(("__segmenter.json", "__unitizer.json")):
            red = sweep(redact_inventory(inv))
            counts["inventories_redacted"] += 1
        else:
            red = inv
            counts["inventories_verbatim"] += 1
        (out_root / "inventories" / p.name).write_text(json.dumps(red, indent=1))

    for p in sorted(TABLE_DIR.iterdir()):
        if p.is_file():
            shutil.copy2(p, out_root / "tables" / p.name)
            counts["tables"] += 1

    for p in sorted(LOG_DIR.glob("*.jsonl")):
        lines = []
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            lines.append(json.dumps(sweep(redact_log_line(json.loads(line)))))
        (out_root / "logs" / p.name).write_text("\n".join(lines) + "\n")
        counts["logs"] += 1

    return counts


def _walk_strings(obj, skip_self_authored: bool = True):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            if skip_self_authored and k in SELF_AUTHORED_KEYS:
                continue  # notes this script wrote, not material from a specimen
            yield from _walk_strings(v, skip_self_authored)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_strings(v, skip_self_authored)


def scan(out_root: Path, limit: int = MAX_STR) -> list[tuple[str, int, str]]:
    """The release gate: no published string exceeds the limit.

    Lengths are measured on DECODED strings, the same way `sweep` measures them.
    An earlier version regex-matched the raw file and so counted JSON escape
    sequences -- `\\ufb01` is six characters on disk and one in the string --
    which flagged files that were already within the limit. The gate and the
    redactor must measure the same thing or one of them is lying.
    """
    bad = []
    for p in sorted(out_root.rglob("*")):
        if not p.is_file() or p.suffix not in (".json", ".jsonl"):
            continue
        # `tables/` is exempt, and the exemption is narrow rather than
        # convenient: those files are derived statistics plus notes this study
        # wrote itself, they contain no material drawn from a specimen, and they
        # are already published verbatim in the paper's public repository. Their
        # long strings are sentences like "predicted base rate = mean
        # predecessor node count / inventory size". The gate exists for the three
        # classes built FROM the documents, and those are the ones it scans.
        if p.parent.name == "tables":
            continue
        longest, where = 0, ""
        if p.suffix == ".jsonl":
            docs = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        else:
            docs = [json.loads(p.read_text())]
        for d in docs:
            for s in _walk_strings(d):
                if len(s) > longest:
                    longest, where = len(s), s[:60]
        if longest > limit:
            bad.append((str(p.relative_to(out_root)), longest, where))
    return bad


def emit_jsonl(out_root: Path, hf_root: Path) -> dict:
    """Consolidate the redacted tree into the corpus's HF layout.

    The per-file tree is the right shape for verification -- one file per cell,
    named as the harness names it -- and the wrong shape for a dataset viewer,
    which needs a split whose rows share a schema. Every other dataset in this
    corpus ships `records/*.jsonl` with one record per line and a `configs:`
    block naming each split; this does the same. The four splits are separated by
    SCHEMA, not by convenience: fixed-condition answers are (selected, edges),
    free-condition answers are (nodes, edges), inventories are per-document
    boundary records, and calls are the log rows.
    """
    if hf_root.exists():
        shutil.rmtree(hf_root)
    (hf_root / "records").mkdir(parents=True)
    (hf_root / "tables").mkdir(parents=True)
    counts = {}

    def write(name: str, rows: list[dict]) -> None:
        path = hf_root / "records" / name
        path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
        counts[name] = len(rows)

    fixed, free = [], []
    for p in sorted((out_root / "records").glob("extract_*.json")):
        stem = p.stem[len("extract_") :]
        doc, cond, op, rep = stem.split("__")
        rec = json.loads(p.read_text())
        base = {
            "document": doc,
            "condition": cond,
            "operator": op,
            "repetition": int(rep.lstrip("r")),
        }
        if cond == "u_free":
            free.append({**base, "nodes": rec.get("nodes"), "edges": rec.get("edges")})
        else:
            fixed.append(
                {**base, "selected": rec.get("selected"), "edges": rec.get("edges")}
            )
    write("extractions_fixed.jsonl", fixed)
    write("extractions_free.jsonl", free)

    invs = []
    for p in sorted((out_root / "inventories").glob("inventory_*.json")):
        doc, source = p.stem[len("inventory_") :].split("__")
        inv = json.loads(p.read_text())
        invs.append(
            {
                "document": doc,
                "source": source,
                "n_units": len(inv.get("units") or []),
                "n_boundaries": len(inv.get("boundaries") or []),
                "record": inv,
            }
        )
    write("inventories.jsonl", invs)

    calls = []
    for p in sorted((out_root / "logs").glob("*.jsonl")):
        for line in p.read_text().splitlines():
            if line.strip():
                calls.append({"log_file": p.name, **json.loads(line)})
    write("calls.jsonl", calls)

    for p in sorted((out_root / "tables").iterdir()):
        if p.is_file():
            shutil.copy2(p, hf_root / "tables" / p.name)
    counts["tables"] = len(list((hf_root / "tables").iterdir()))
    return counts


def check_against_specimens(out_root: Path, min_len: int = 25) -> int:
    """The decisive gate: no published string may occur inside any specimen.

    The length gate and the role gate are both rules about how the redactor
    BELIEVES the records are shaped. This one checks the actual question -- is
    any of somebody else's document in here -- against the documents themselves,
    and it does not care how the string got there.
    """
    import unit_lib as L

    texts = {
        d: L.specimen_text(d) for d in ("vc1", "vc2", "vc3_r0", "vc3_r1", "vc3_r2")
    }
    hits, checked = [], 0
    for p in sorted(out_root.rglob("*")):
        if p.suffix not in (".json", ".jsonl") or not p.is_file():
            continue
        if p.parent.name == "tables":
            continue
        if p.suffix == ".jsonl":
            items = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        else:
            items = [json.loads(p.read_text())]
        for d in items:
            for s in _walk_strings(d):
                if len(s) < min_len:
                    continue
                checked += 1
                for name, t in texts.items():
                    if s in t:
                        hits.append((str(p.relative_to(out_root)), name, s[:60]))
    if hits:
        print(
            f"SPECIMEN GATE FAILED — {len(hits)} published string(s) appear in a specimen:"
        )
        for f, n, s in hits[:15]:
            print(f"   {f} [{n}] {s!r}")
        return 1
    print(
        f"specimen gate: {checked} published strings of {min_len}+ characters "
        "checked; none occurs in any specimen."
    )
    return 0


def verify(out_root: Path) -> int:
    """Re-score every cell from the redacted records; require an exact match."""
    import unit_lib as L
    import score_layers as S

    committed = json.loads((TABLE_DIR / "decomposition.json").read_text())

    # The scorer reads records and inventories from one directory, so give it a
    # flat view of both published subtrees -- and nothing else. Anything the
    # scorer needs that is NOT in this view is, by construction, something the
    # release does not carry, which is exactly what the verification is for.
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="2026bl_verify_"))
    for sub in ("records", "inventories"):
        for f in (out_root / sub).glob("*.json"):
            shutil.copy2(f, tmp / f.name)

    orig_data = L.DATA_DIR
    L.DATA_DIR = tmp
    S.L.DATA_DIR = tmp
    try:
        proto = L.protocol()
        ops = proto["extraction_operators"]
        k = int(proto["repetitions_k"])
        mismatches = []
        for row in committed["rows"]:
            doc, cond = row["document"], row["condition"]
            fresh = S.score_cell(doc, cond, ops, k)
            for layer in ("layer1", "layer2", "layer3", "layer4"):
                a = S._val(row[layer], "between_mean")
                b = S._val(fresh[layer], "between_mean")
                c = S._val(row[layer], "within_mean")
                d = S._val(fresh[layer], "within_mean")
                for name, x, y in (("between", a, b), ("within", c, d)):
                    if x is None and y is None:
                        continue
                    if x is None or y is None or abs(x - y) > 1e-12:
                        mismatches.append(f"{doc}/{cond}/{layer}/{name}: {x} != {y}")
        if mismatches:
            print("VERIFY FAILED — redacted records do not reproduce the tables:")
            for m in mismatches[:25]:
                print("   ", m)
            return 1
        print(
            f"VERIFY OK — all {len(committed['rows'])} cells reproduce exactly "
            "from the redacted records (between and within, every layer)."
        )
        return 0
    finally:
        L.DATA_DIR = orig_data
        S.L.DATA_DIR = orig_data
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="release")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--hf-out", default=None, help="also emit the HF JSONL layout")
    a = ap.parse_args()
    out_root = (PAPER_DIR / a.out).resolve()

    counts = build(out_root)
    print("staged:", json.dumps(counts))

    bad = scan(out_root)
    if bad:
        print(f"\nRELEASE GATE FAILED — {len(bad)} file(s) carry long strings:")
        for f, n, w in bad[:20]:
            print(f"   {f}: {n} chars — {w!r}")
        return 1
    print(f"release gate: no published string exceeds {MAX_STR} characters.")

    if check_against_specimens(out_root):
        return 1

    if a.verify and verify(out_root):
        return 1

    if a.hf_out:
        hf_root = (PAPER_DIR / a.hf_out).resolve()
        print("hf layout:", json.dumps(emit_jsonl(out_root, hf_root)))
        # The gates run again on what is ACTUALLY uploaded, not only on the tree
        # it was derived from -- a consolidation step is one more place to leak.
        bad = scan(hf_root)
        if bad:
            print(f"HF GATE FAILED — {len(bad)} file(s) carry long strings:")
            for f, n, w in bad[:10]:
                print(f"   {f}: {n} chars — {w!r}")
            return 1
        if check_against_specimens(hf_root):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
