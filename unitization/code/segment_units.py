#!/usr/bin/env python3
"""Step 1 of the 2026bl run: build the deterministic unit inventory (M1b, M1c).

No model is called here. The segmenter is a released package pinned by version
in PROTOCOL.yaml, and the mathematical unit rule is applied to its output as a
declared post-step rather than by hand-editing any inventory.

The rule (M1c, declared before the run): a displayed expression attaches to the
sentence that introduces it and is not a unit of its own, and no unit boundary
falls inside symbolic material. Implemented as: a candidate segment carrying no
alphabetic word of two or more letters outside symbolic material is merged into
the segment before it; a leading such segment merges forward instead, since
there is nothing before it to attach to.

Run:
    uv run --with pysbd --with pyyaml python \\
        code/segment_units.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402

# A segment is "symbolic" when it states nothing OUTSIDE symbolic material --
# which is the declared rule, and means the content between math delimiters is
# removed before any word is counted, not merely the delimiters themselves. A
# displayed integral is symbolic even though `dx` is spelt with letters, because
# `dx` is inside the mathematics; a sentence of prose is not symbolic however
# much mathematics it also carries.
_MATH_SPAN = re.compile(r"\$\$.*?\$\$|\$[^$]*\$|\\\[.*?\\\]|\\\(.*?\\\)", re.S)
_TEX = re.compile(r"\\[A-Za-z]+|\\[\[\]()]|\$+|[{}^_&~]")
_WORD = re.compile(r"[A-Za-z]{2,}")


def is_symbolic(segment: str) -> bool:
    """True when the segment states nothing outside symbolic material."""
    stripped = _TEX.sub(" ", _MATH_SPAN.sub(" ", segment))
    return not _WORD.search(stripped)


def apply_math_rule(
    spans: list[tuple[int, int]], text: str
) -> tuple[list[tuple[int, int]], int]:
    """Merge displayed mathematics into the sentence that introduces it.

    Works on (start, end) character offsets rather than on strings, so that
    every unit keeps an exact position in the source. A merged unit spans from
    the introducing sentence's start to the mathematics' end, and its text is
    whatever lies between -- which is what makes a boundary comparable against
    an adjudicator's decision at the same offset.

    Returns the corrected spans and the number of merges performed, which is
    Table A2's displayed-mathematics column.
    """
    out: list[list[int]] = []
    merges = 0
    pending: list[int] | None = None
    for start, end in spans:
        if is_symbolic(text[start:end]):
            if out:
                out[-1][1] = end
                merges += 1
            elif pending:
                pending[1] = end
            else:
                pending = [start, end]
            continue
        if pending:
            start = pending[0]
            merges += 1
            pending = None
        out.append([start, end])
    if pending:  # a document of nothing but symbols; keep it rather than drop it
        out.append(pending)
    return [(a, b) for a, b in out if text[a:b].strip()], merges


def segment(text: str) -> tuple[list[tuple[int, int]], int, int]:
    import pysbd

    proto = L.protocol()["segmenter"]
    seg = pysbd.Segmenter(
        language=proto["language"],
        clean=proto["options"]["clean"],
        char_span=proto["options"]["char_span"],
    )
    raw = [(s.start, s.end) for s in seg.segment(text)]
    spans, merges = apply_math_rule(raw, text)
    return spans, len(raw), merges


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="*", help="restrict to these documents")
    args = ap.parse_args()

    proto = L.protocol()
    docs = list(proto["specimens"])
    if args.docs:
        docs = [d for d in docs if d in args.docs]

    import importlib.metadata as meta

    installed = meta.version("pysbd")
    pinned = str(proto["segmenter"]["version"])
    if installed != pinned:
        raise SystemExit(
            f"segmenter version {installed} != pinned {pinned}; the inventory a "
            "different release produces is a different instrument"
        )

    print(f"segmenter pysbd {installed} (pinned)")
    for doc in docs:
        text = L.specimen_text(doc)
        spans, raw_n, merges = segment(text)
        units = [text[a:b].strip() for a, b in spans]
        L.write_json(
            L.inventory_path(doc, "segmenter"),
            {
                "document": doc,
                "source": "segmenter",
                "package": f"pysbd=={installed}",
                "math_rule": proto["segmenter"]["math_rule"],
                "raw_segments": raw_n,
                "math_merges": merges,
                "spans": [[a, b] for a, b in spans],
                "units": units,
            },
        )
        print(
            f"  {doc:8s} raw={raw_n:5d}  math-merges={merges:4d}  units={len(units):5d}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
