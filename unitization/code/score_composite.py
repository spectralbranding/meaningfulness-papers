#!/usr/bin/env python3
"""The published joint coefficient, computed rather than argued against (M5a).

Two instruments from the same family are computed in-study beside the
decomposition: the unified coefficient that scores unitizing and categorisation
jointly, and its companion that isolates categorisation while setting positional
discrepancy aside. Both come from one maintained implementation, pinned.

The companion is the near-neighbour of this design's conditional typing
statistic. The distinction the paper offers is that the companion sets position
aside as a nuisance whereas this design removes position by construction and
then measures selection as a quantity in its own right. If that distinction does
not survive contact with the companion's definition, the paper says so and the
decomposition's novelty narrows to the selection stage -- which is why the two
are printed side by side here rather than one being reported and the other
described.

Cost. The alignment is combinatorial, so the composite is computed on the FIRST
repetition of each operator rather than on all 25 cross pairs. That is declared
here rather than chosen once the numbers were visible: the layered form uses
every pair, the composite uses one, and the two are not averages over the same
thing.

Run:
    uv run --python 3.12 --with pygamma-agreement --with pyannote.core \\
        --with pyyaml python code/score_composite.py
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import score_layers as S  # noqa: E402
import unit_lib as L  # noqa: E402

PRECISION = 0.05


def continuum_for(doc: str, condition: str, ops: list[dict], rep: int = 1):
    from pyannote.core import Segment
    from pygamma_agreement import Continuum

    text = L.specimen_text(doc)
    cont = Continuum()
    counts = {}
    for op in ops:
        path = L.extraction_path(doc, condition, op["id"], rep)
        if not path.exists():
            return None, {}
        result = L.load_json(path)
        if condition == "u_free":
            spans, types, _ = S.free_view(result, text)
            items = [(spans[i][0], spans[i][1], types.get(i)) for i in spans]
        else:
            inv = L.load_json(L.inventory_path(doc, S.INVENTORY_FOR[condition]))
            unit_spans = inv["spans"]
            sel, types, _ = S.fixed_view(result)
            items = [
                (unit_spans[u - 1][0], unit_spans[u - 1][1], types.get(u))
                for u in sorted(sel)
                if 1 <= u <= len(unit_spans)
            ]
        counts[op["id"]] = len(items)
        for start, end, cat in items:
            if end > start:
                cont.add(op["id"], Segment(float(start), float(end)), str(cat))
    return cont, counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="*")
    ap.add_argument("--conditions", nargs="*")
    args = ap.parse_args()

    from pygamma_agreement import CombinedCategoricalDissimilarity

    proto = L.protocol()
    ops = proto["extraction_operators"]
    diss = CombinedCategoricalDissimilarity(alpha=1, beta=1)

    rows = []
    for condition in proto["condition_order"]:
        if args.conditions and condition not in args.conditions:
            continue
        for doc in proto["specimens"]:
            if args.docs and doc not in args.docs:
                continue
            cont, counts = continuum_for(doc, condition, ops)
            if cont is None or not counts or min(counts.values()) == 0:
                continue
            # The coefficient's expected disorder is estimated by sampling
            # random continua, and that sampler is NOT seeded by the library.
            # Unseeded, the same input returned .589, .593, .594 and .597 on
            # four runs of the same cell -- a spread of ~.008 that is invisible
            # in a single report and fatal to a reproduction attempt.
            #
            # PROTOCOL `separation_test.stream_seeding` already fixes the rule
            # for this study: every permutation and bootstrap stream is seeded
            # from a stable digest of (seed, document, condition, layer, ...),
            # never from a process hash, so a re-run reproduces. That rule was
            # applied to the separation test and missed here. Seeding the
            # composite APPLIES the pre-registration rather than amending it,
            # and it cannot move a verdict: M4 declares the composite
            # non-gating, so no conclusion rests on it.
            stream = L.stream_seed(doc, condition, "composite", "OP_A|OP_B")
            np.random.seed(stream % (2**32))
            random.seed(stream)
            res = cont.compute_gamma(diss, precision_level=PRECISION)
            row = {
                "document": doc,
                "condition": condition,
                "repetition": 1,
                "annotations": counts,
                "gamma": float(res.gamma),
                "gamma_cat": float(res.gamma_cat),
                "precision_level": PRECISION,
            }
            rows.append(row)
            print(
                f"  {doc:8s} {condition:7s} gamma={row['gamma']:.3f} "
                f"gamma_cat={row['gamma_cat']:.3f} units={counts}",
                flush=True,
            )

    L.write_json(
        L.OUTPUT_DIR / "tables" / "composite.json",
        {
            "implementation": "pygamma-agreement",
            "solver": "GLPK_MI via cvxpy (CBC absent); exact MILP, proven 0.0% gap",
            "sampler_seeded": True,
            "computed_on": "repetition 1 of each operator",
            "rows": rows,
        },
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
