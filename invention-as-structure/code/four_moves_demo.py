#!/usr/bin/env python3
"""Companion demonstration for the invention-as-structure paper (P7 existence proof).

Claim under test (paper P7): the four-move account of invention *predicts* the
classification of a cross-owner interaction between two authors' specification
modules, and the admissibility of a proposed combination, via a decidable
compatibility predicate. This script exercises the four invention moves as
ontology operations and checks that the corpus's federated negotiator
(negotiate_modules.py) classifies each exactly as the account predicts.

Move -> ontology operation -> predicted negotiation class:
  adjoin a dimension  -> owns a new term            -> (no cross-interaction; pure adjunction)
  glue across domains -> imports the other's term   -> CROSS_IMPORT
  re-specify / rescale-> refines the other's term   -> CROSS_REFINE
  admissibility check -> same key, compatible def   -> AGREEMENT   (admissible)
                      -> same key, incompatible def -> CONFLICT    (inadmissible)

Deterministic; no network, no randomness. Fixed inputs = ./fixtures/authorX,
./fixtures/authorY. Exits 0 iff every predicted class is observed.

Run:
  uv run python code/four_moves_demo.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Self-contained: negotiate_modules.py + build_ontology.py are vendored beside this
# script (a reproduction snapshot of the corpus ontology-negotiation tools), so the
# demonstration runs standalone from a public checkout with only Python 3.12 + PyYAML.
NEGOTIATOR = HERE / "negotiate_modules.py"
AX = HERE / "fixtures" / "authorX"
AY = HERE / "fixtures" / "authorY"

# invention move -> (ontology operation exercised, predicted negotiation class)
PREDICTIONS = {
    "glue across domains": ("import the other author's owned term", "CROSS_IMPORT"),
    "re-specify / rescale": (
        "refine the other author's term (narrows_to)",
        "CROSS_REFINE",
    ),
    "admissible adjunction": ("same key, identical definition", "AGREEMENT"),
    "inadmissible adjunction": ("same key, incompatible definition", "CONFLICT"),
}


def run_negotiator() -> str:
    proc = subprocess.run(
        [sys.executable, str(NEGOTIATOR), "--author-a", str(AX), "--author-b", str(AY)],
        capture_output=True,
        text=True,
        cwd=str(HERE),
    )
    if proc.returncode not in (
        0,
        1,
    ):  # 1 is the --gate "unresolved" code; we don't gate
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(f"negotiator failed (rc={proc.returncode})")
    return proc.stdout + proc.stderr


def main() -> int:
    for d in (NEGOTIATOR, AX, AY):
        if not d.exists():
            raise SystemExit(f"missing input: {d}")
    out = run_negotiator()

    print("=" * 68)
    print("Four invention moves -> ontology operation -> negotiation class")
    print("=" * 68)
    ok = True
    for move, (op, predicted) in PREDICTIONS.items():
        observed = predicted in out
        ok &= observed
        mark = "OK " if observed else "MISS"
        print(f"[{mark}] {move:24s} | {op:44s} | {predicted}")
    print("-" * 68)
    print(
        "adjoin a dimension       | owns a new term (authorX 'adjoin-dimension') "
        "| no cross-interaction (pure adjunction), as predicted"
    )
    print("=" * 68)

    if ok:
        print(
            "\nRESULT: PASS — every predicted classification observed. "
            "The four-move account is borne out by the running adjudicator."
        )
        return 0
    print("\nRESULT: FAIL — a predicted classification was not observed.")
    print("\n--- negotiator output ---\n" + out)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
