#!/usr/bin/env python3
"""The declared re-analysis (M5, P3): the predecessor's node layer, joint-scored.

The predecessor scored its node layer over the nodes the two operators happened
to match, which charges nothing for the boundary disagreement that produced the
matching. This recomputes the same layer under a joint unitizing coefficient,
which charges it.

The direction is declared in advance: the recomputed column is expected to be
WORSE than the reported one (P3). It is reported whichever way it comes out.

This is a re-analysis performed by this paper, not a correction to the
predecessor's record: its guidelines stay frozen and its published numbers stand
as published. Nothing here writes into the predecessor's record.

Run:
    uv run --python 3.12 --with pygamma-agreement --with pyannote.core \\
        --with pyyaml python code/reanalyse_predecessor.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import score_layers as S  # noqa: E402
import unit_lib as L  # noqa: E402

PRED = L.PAPER_DIR.parent / "internalization"
PRECISION = 0.05


def main() -> int:
    from pygamma_agreement import CombinedCategoricalDissimilarity, Continuum
    from pyannote.core import Segment

    reported = {
        r["document"]: r
        for r in L.load_json(PRED / "output" / "tables" / "agreement_main.json")
    }
    diss = CombinedCategoricalDissimilarity(alpha=1, beta=1)

    rows = []
    for doc in L.protocol()["specimens"]:
        text = (PRED / "specimens" / f"{doc}.txt").read_text(encoding="utf-8")
        cont = Continuum()
        located = {}
        for op in ("OP_A", "OP_B"):
            path = PRED / "data" / f"spine_{doc}__{op}.json"
            if not path.exists():
                break
            graph = L.load_json(path)
            spans, types, _ = S.free_view(graph, text)
            located[op] = {
                "nodes": len(graph.get("nodes") or []),
                "located": len(spans),
            }
            for nid, (start, end) in spans.items():
                if end > start:
                    cont.add(op, Segment(float(start), float(end)), str(types.get(nid)))
        if len(located) < 2:
            continue
        res = cont.compute_gamma(diss, precision_level=PRECISION)
        as_reported = reported[doc]["layer1"]["alpha_nominal"]
        rows.append(
            {
                "document": doc,
                "as_reported_matched_nodes_only": as_reported,
                "as_reported_statistic": "Krippendorff alpha over matched nodes (the predecessor's layer 1)",
                "recomputed_joint_gamma": float(res.gamma),
                "recomputed_gamma_cat": float(res.gamma_cat),
                "difference": float(res.gamma) - as_reported,
                "nodes": located,
                "predecessor_matched_nodes": reported[doc]["layer1"]["matched_nodes"],
            }
        )
        print(
            f"  {doc:8s} reported={as_reported:.3f} joint_gamma={res.gamma:.3f} "
            f"diff={res.gamma - as_reported:+.3f}",
            flush=True,
        )

    worse = [r for r in rows if r["difference"] < 0]
    L.write_json(
        L.OUTPUT_DIR / "tables" / "reanalysis.json",
        {
            "declared_direction": "recomputed worse than reported (P3)",
            "documents_in_declared_direction": len(worse),
            "documents": len(rows),
            "precision_level": PRECISION,
            "rows": rows,
        },
    )
    print(
        f"\nDeclared direction (recomputed worse) holds on {len(worse)}/{len(rows)} documents"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
