#!/usr/bin/env python3
"""Step 3 of the 2026bl run: predict the selection base rate, BEFORE any operator call.

M4b: "The expected selection base rate for each document is the predecessor's
recorded node count divided by this study's inventory size for that document.
Both quantities exist before any operator is called... any document whose
predicted index already breaches .85 is declared non-gating *in advance* rather
than after its coefficient has been seen."

Two operationalizations are forced here and both are recorded rather than
chosen quietly:

  * The predecessor recorded TWO node counts per document, one per operator.
    The point prediction is their mean, and both per-operator predictions are
    reported beside it, so a reader can see the range the mean stands for.
  * The prevalence index is Byrt's, which is computed from an observed 2x2
    table that does not exist before the run. Its pre-run analogue for a
    predicted base rate p is |2p - 1| -- the value Byrt's index takes when two
    raters agree at that base rate. That is what is predicted here, and the
    observed index is computed the ordinary way once the data exist.

No model is called. Run:
    uv run --with pyyaml python \\
        code/predict_base_rates.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402


def predicted_prevalence_index(base_rate: float) -> float:
    """Byrt's prevalence index under two raters agreeing at this base rate."""
    return abs(2.0 * base_rate - 1.0)


def main() -> int:
    proto = L.protocol()
    floor = float(proto["thresholds"]["prevalence_floor"])
    rows = []
    for doc, spec in proto["specimens"].items():
        inv = L.load_json(L.inventory_path(doc, "segmenter"))
        n_units = len(inv["units"])
        counts = spec["predecessor_nodes"]
        per_op = {op: n / n_units for op, n in counts.items()}
        mean_nodes = sum(counts.values()) / len(counts)
        base = mean_nodes / n_units
        pi = predicted_prevalence_index(base)
        rows.append(
            {
                "document": doc,
                "inventory_units": n_units,
                "math_merges": inv["math_merges"],
                "predecessor_nodes": counts,
                "predicted_base_rate_per_operator": per_op,
                "predicted_base_rate": base,
                "predicted_prevalence_index": pi,
                "gates": pi <= floor,
                "floor": floor,
            }
        )

    L.write_json(
        L.OUTPUT_DIR / "tables" / "predicted_base_rates.json",
        {
            "declared_before_any_operator_call": True,
            "prevalence_floor": floor,
            "rule": "predicted base rate = mean predecessor node count / inventory size; "
            "predicted prevalence index = |2p - 1|",
            "rows": rows,
        },
    )

    print(
        f"{'doc':8s} {'units':>6s} {'nodes(A/B)':>12s} {'base':>7s} {'PI':>7s}  gates?"
    )
    for r in rows:
        a, b = r["predecessor_nodes"].values()
        print(
            f"{r['document']:8s} {r['inventory_units']:6d} {f'{a}/{b}':>12s} "
            f"{r['predicted_base_rate']:7.3f} {r['predicted_prevalence_index']:7.3f}  "
            f"{'yes' if r['gates'] else 'NO -- declared uninterpretable in advance'}"
        )
    non_gating = [r["document"] for r in rows if not r["gates"]]
    print(
        f"\nDeclared non-gating in advance ({len(non_gating)}): "
        f"{', '.join(non_gating) if non_gating else 'none'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
