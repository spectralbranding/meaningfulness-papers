#!/usr/bin/env python3
"""Build the publishable release tree for 2026bk.

Run:
    uv run --with pyyaml --with numpy --with scipy python code/redact_for_release.py --out release
    uv run --with pyyaml --with numpy --with scipy python code/redact_for_release.py --out release --verify

The specimens are third-party works and are not redistributed. Three classes of
run artifact carry their TEXT rather than referring to it:

  * extracted graphs -- every node carries a verbatim `span`, a 5-25 word
    quotation of the specimen; some 650 of them across the main run are a
    substantial extract of other people's documents.
  * rater judgments -- `author_declaration` quotes the sentence of the specimen
    the rater relied on, up to several hundred characters.
  * per-call logs -- the prompts embed the whole specimen, and the responses
    carry the graphs with their spans.

What ships instead is the same material reduced to what the analysis consumes.
Span matching uses located character OFFSETS (metrics_lib.span_offsets), so each
span is replaced by the offsets it resolved to in the original run, under the
same paragraph-first rule, plus its digest. Rater quotations become digests;
their verdicts, scores and the rest of the judgment stay. Logs keep the full
call metadata -- model version, parameters, token usage, latency, retries --
with the prompt and response bodies replaced by their digests.

Node `statement`s stay. They are the operators' one-sentence paraphrases, and
the lexical arm of the ladder is computed from them. Measured on the main run:
the longest verbatim run any statement shares with its specimen has median 25
characters and maximum 98, i.e. a phrase, not an extract.

--verify re-runs the analysis on the release records and compares every table
against the committed one; the redaction is only correct if they are identical.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PAPER_DIR / "data"
LOG_DIR = PAPER_DIR / "logs"
TABLE_DIR = PAPER_DIR / "output" / "tables"
SPEC_DIR = PAPER_DIR / "specimens"

sys.path.insert(0, str(PAPER_DIR / "code"))

# Keys whose value is specimen text by role, digested whole however short.
QUOTE_KEYS = ("span", "author_declaration", "quote", "text")
LOG_BODY_FIELDS = ("system_prompt", "user_prompt", "response")
# The release gate: no published string may share a verbatim run this long with
# any third-party specimen. Statements (max 98 measured) are the only text that
# legitimately approaches it, so the bound is set just above them.
MAX_VERBATIM_RUN = 100
OWN_WORKS = ("pilot_2026ao",)  # the author's own CC BY paper; not third-party


def digest(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()


def redacted(s: str) -> dict:
    return {"digest": digest(s), "n_chars": len(s), "redacted": True}


def sweep(obj, key=None):
    """Digest every value held under a quotation key, at any depth."""
    if isinstance(obj, str):
        return redacted(obj) if key in QUOTE_KEYS else obj
    if isinstance(obj, dict):
        return {k: sweep(v, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sweep(v, key) for v in obj]
    return obj


def doc_of(name: str) -> str | None:
    m = re.match(r"(?:spine|rating)_(.+?)__", name)
    return m.group(1) if m else None


def redact_graph(graph: dict, text: str | None) -> dict:
    """Replace each verbatim span with the offsets the analysis resolved it to."""
    import metrics_lib as M
    import spine_lib as L

    out = json.loads(json.dumps(graph))
    offsets = {}
    if text is not None:
        offsets = M.span_offsets(graph, text, L.paragraph_spans(text))
    kept = dropped = 0
    for n in out.get("nodes") or []:
        span = n.get("span")
        if isinstance(span, str) and span:
            n["span_digest"] = digest(span)
        loc = offsets.get(n.get("id"))
        if loc is not None:
            n["span_offsets"] = [int(loc[0]), int(loc[1])]
            kept += 1
        else:
            n["span_unlocatable"] = True
            dropped += 1
        n.pop("span", None)
    out["_redaction"] = {
        "spans_replaced_by_offsets": kept,
        "spans_unlocatable_in_source": dropped,
        "note": (
            "Verbatim spans removed; offsets are what the matcher consumes. "
            "The text is recoverable only from the specimen, which "
            "prepare_specimens.py fetches from its public source."
        ),
    }
    return out


def redact_log_line(rec: dict) -> dict:
    out = dict(rec)
    for f in LOG_BODY_FIELDS:
        v = out.get(f)
        if v is None:
            continue
        s = v if isinstance(v, str) else json.dumps(v, sort_keys=True)
        out[f] = redacted(s)
    # Providers echo the response inside response_metadata (content blocks,
    # reasoning blobs). Enumerating those fields does not survive the next
    # schema change, so every string over LOG_MAX_STR is digested wherever it is.
    return _sweep_long(out)


LOG_MAX_STR = 80  # a model identifier or a digest fits; a quoted passage does not


def _sweep_long(obj):
    if isinstance(obj, str):
        return redacted(obj) if len(obj) > LOG_MAX_STR else obj
    if isinstance(obj, dict):
        return {k: _sweep_long(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sweep_long(v) for v in obj]
    return obj


def build(out_root: Path) -> dict:
    import spine_lib as L

    if out_root.exists():
        shutil.rmtree(out_root)
    for sub in ("data", "tables", "logs"):
        (out_root / sub).mkdir(parents=True)
    texts: dict[str, str | None] = {}

    def text_for(doc: str) -> str | None:
        if doc not in texts:
            try:
                texts[doc] = L.specimen_text(doc)
            except FileNotFoundError:
                texts[doc] = None
        return texts[doc]

    counts = {"graphs": 0, "ratings": 0, "alignments": 0, "tables": 0, "logs": 0}
    for p in sorted(DATA_DIR.rglob("*.json")):
        rec = json.loads(p.read_text())
        rel = p.relative_to(DATA_DIR)
        if p.name.startswith("spine_"):
            red = sweep(redact_graph(rec, text_for(doc_of(p.name))))
            counts["graphs"] += 1
        elif p.name.startswith("rating_"):
            red = sweep(rec)
            counts["ratings"] += 1
        else:
            red = sweep(rec)
            counts["alignments"] += 1
        dst = out_root / "data" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(red, indent=1, ensure_ascii=False) + "\n")

    for p in sorted(TABLE_DIR.glob("*")):
        if not p.is_file():
            continue
        if p.suffix == ".json":
            red = sweep(json.loads(p.read_text()))
            (out_root / "tables" / p.name).write_text(
                json.dumps(red, indent=1, ensure_ascii=False) + "\n"
            )
        else:
            shutil.copy2(p, out_root / "tables" / p.name)
        counts["tables"] += 1

    for p in sorted(LOG_DIR.rglob("*.jsonl")):
        rel = p.relative_to(LOG_DIR)
        lines = [
            json.dumps(redact_log_line(json.loads(x)), ensure_ascii=False)
            for x in p.read_text().splitlines()
            if x.strip()
        ]
        dst = out_root / "logs" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text("\n".join(lines) + "\n")
        counts["logs"] += 1
    return counts


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)


def _longest_run(s: str, text: str, floor: int) -> int:
    """Longest substring of s found in text, searched only above `floor`."""
    best = 0
    lo, hi = floor, len(s)
    # binary search on run length: is there a window of length L in text?
    while lo <= hi:
        mid = (lo + hi) // 2
        if any(s[i : i + mid] in text for i in range(0, len(s) - mid + 1)):
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


def specimen_gate(out_root: Path) -> int:
    norm = lambda t: re.sub(r"\s+", " ", t)  # noqa: E731
    texts = {
        p.stem: norm(p.read_text(encoding="utf-8"))
        for p in SPEC_DIR.glob("*.txt")
        if p.stem not in OWN_WORKS
    }
    if not texts:
        print("specimen gate: no local specimens to check against -- REFUSED")
        return 1
    worst, checked, bad = 0, 0, []
    for p in sorted(out_root.rglob("*")):
        if not p.is_file() or p.suffix not in (".json", ".jsonl", ".md"):
            continue
        raw = p.read_text(encoding="utf-8")
        if p.suffix == ".jsonl":
            items = [json.loads(x) for x in raw.splitlines() if x.strip()]
        elif p.suffix == ".json":
            items = [json.loads(raw)]
        else:
            items = [raw]
        for it in items:
            for s in _strings(it):
                s = norm(s)
                if len(s) <= 40:
                    continue
                checked += 1
                for t in texts.values():
                    if not any(s[i : i + 41] in t for i in range(0, len(s) - 40)):
                        continue
                    run = _longest_run(s, t, 41)
                    worst = max(worst, run)
                    if run > MAX_VERBATIM_RUN:
                        bad.append((str(p.relative_to(out_root)), run, s[:60]))
    if bad:
        print(f"SPECIMEN GATE FAILED -- {len(bad)} string(s) exceed the bound:")
        for f, r, s in bad[:15]:
            print(f"   {f} run={r} {s!r}")
        return 1
    print(
        f"specimen gate: {checked} strings checked; longest verbatim run shared "
        f"with any third-party specimen = {worst} chars (bound {MAX_VERBATIM_RUN})."
    )
    return 0


ANALYSIS = [
    ["code/score_agreement.py", "--set", "pilot"],
    ["code/score_agreement.py", "--set", "main"],
    ["code/score_ladder.py"],
    ["code/score_targets.py"],
    ["code/emit_results_summary.py"],
]


def verify(out_root: Path) -> int:
    """Re-run the analysis on a copy whose data/ is the release records."""
    tmp = Path(tempfile.mkdtemp(prefix="2026bk_verify_"))
    try:
        work = tmp / "paper"
        shutil.copytree(
            PAPER_DIR,
            work,
            ignore=shutil.ignore_patterns("data", "logs", "output", "release*"),
        )
        shutil.copytree(out_root / "data", work / "data")
        (work / "output" / "tables").mkdir(parents=True)
        for cmd in ANALYSIS:
            r = subprocess.run(
                [sys.executable, *cmd], cwd=work, capture_output=True, text=True
            )
            if r.returncode != 0:
                print(f"VERIFY FAILED -- {' '.join(cmd)} exited {r.returncode}")
                print(r.stdout[-1500:], r.stderr[-1500:])
                return 1
        mismatches = []
        for p in sorted((out_root / "tables").glob("*")):
            fresh = work / "output" / "tables" / p.name
            if not fresh.exists():
                # Discarded pilot rounds are archived outputs; reproduce.sh never
                # regenerated them, before or after redaction.
                if not re.search(r"_round\d", p.name):
                    mismatches.append(f"{p.name}: not regenerated")
                continue
            a, b = p.read_text(), fresh.read_text()
            if p.suffix == ".json":
                a = json.dumps(json.loads(a), sort_keys=True)
                b = json.dumps(sweep(json.loads(b)), sort_keys=True)
            if a != b:
                mismatches.append(p.name)
        if mismatches:
            print("VERIFY FAILED -- tables differ:", ", ".join(mismatches))
            return 1
        print(
            "VERIFY OK -- every regenerated table is identical from the release "
            "records (archived pilot-round tables are not regenerated)."
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="release")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    out_root = (PAPER_DIR / a.out).resolve()
    print("staged:", json.dumps(build(out_root)))
    if specimen_gate(out_root):
        return 1
    if a.verify and verify(out_root):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
