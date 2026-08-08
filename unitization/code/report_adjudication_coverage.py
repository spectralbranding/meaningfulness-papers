#!/usr/bin/env python3
"""How much of Layer S was decided by two adjudicators, and how much by one.

The adjudication is elicited in chunks of candidate positions (AMENDMENTS A2),
and a chunk whose answer will not parse is recorded UNANSWERED rather than
failing the document (A3). An unanswered chunk contributes no boundary, so for
the positions inside it the design's "two independent adjudicators" reduces to
one adjudicator plus the resolver -- the resolver still decides them, because a
position one adjudicator marked and the other did not is by definition
disputed, and disputed positions are exactly what the resolver receives.

That is a bounded degradation rather than a hole, but it is a degradation, and
its size is a number rather than a reassurance. This script reports it so the
results version can state it per document instead of describing it.

Reads only files on disk; makes no call.

Run:
    uv run --with pyyaml --with pysbd python \\
        code/report_adjudication_coverage.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402
from adjudicate_segmentation import CHUNK, candidates  # noqa: E402


def main() -> int:
    proto = L.protocol()
    adjs = [a["id"] for a in proto["segmentation_adjudicators"]]
    rows = []
    for doc in proto["specimens"]:
        cands = candidates(L.specimen_text(doc))
        n = len(cands)
        singly = set()
        per_adj = {}
        for aid in adjs:
            path = L.inventory_path(doc, aid)
            state = L.load_json(path) if path.exists() else {}
            unanswered = state.get("unanswered") or []
            per_adj[aid] = len(unanswered)
            for idx in unanswered:
                singly.update(range(idx * CHUNK, min((idx + 1) * CHUNK, n)))
        rows.append(
            {
                "document": doc,
                "n_candidates": n,
                "n_chunks": -(-n // CHUNK),
                "unanswered_chunks": per_adj,
                "positions_decided_by_one_adjudicator": len(singly),
                "share": (len(singly) / n) if n else 0.0,
            }
        )

    print(
        f"{'document':9s} {'cands':>6s} {'chunks':>6s} "
        + " ".join(f"{a+' unans':>12s}" for a in adjs)
        + f" {'1-adj posns':>12s} {'share':>7s}"
    )
    for r in rows:
        share = f"{r['share']:.3f}".replace("0.", ".", 1)
        print(
            f"{r['document']:9s} {r['n_candidates']:6d} {r['n_chunks']:6d} "
            + " ".join(f"{r['unanswered_chunks'][a]:12d}" for a in adjs)
            + f" {r['positions_decided_by_one_adjudicator']:12d} {share:>7s}"
        )

    total = sum(r["positions_decided_by_one_adjudicator"] for r in rows)
    allc = sum(r["n_candidates"] for r in rows)
    print(
        f"\nAcross all five documents: {total} of {allc} candidate positions "
        f"({total / allc:.3%}) were decided by one adjudicator plus the "
        f"resolver rather than by two."
    )
    L.write_json(
        L.OUTPUT_DIR / "tables" / "adjudication_coverage.json",
        {"chunk_size": CHUNK, "adjudicators": adjs, "rows": rows},
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
