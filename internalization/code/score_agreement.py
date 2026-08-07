#!/usr/bin/env python3
"""Stage 2 of the 2026bk run: RC1 extraction agreement, in three layers.

Reads the committed extractions and the pre-declared thresholds; writes one
JSON per document plus a summary table. No API access, no keys: given the
extractions in data/, this reproduces every agreement number exactly.

Layer 1  nominal Krippendorff alpha over node types on matched spans, with
         node-boundary precision and recall alongside.
Layer 2  triple-overlap F1 over the agreed node set, against a random-graph
         null at the 99th percentile. This is the gate.
Layer 3  Spearman rank correlation of support mass over the agreed node set,
         reported and inspected rather than gated, plus the RC2 sensitivity.

Run:
    uv run --with numpy --with pyyaml python \
        code/score_agreement.py --set main
"""

from __future__ import annotations

import argparse
import json
import sys

import metrics_lib as M
import spine_lib as L

# Thresholds as pre-declared in DECISION_RULE.md. Restated here as constants so
# the scorer is self-contained; they are read-only and are never recomputed.
L1_ALPHA = 0.65
L2_F1 = 0.60
L3_RHO = 0.50


def score_document(doc: str, ops: list[dict], seed: int, draws: int) -> dict:
    text = L.specimen_text(doc)
    ga, gb = (L.load_graph(doc, op["id"]) for op in ops)
    paras = L.paragraph_spans(text)
    off_a, off_b = M.span_offsets(ga, text, paras), M.span_offsets(gb, text, paras)
    pairs = M.match_by_span(off_a, off_b)

    type_a = {n["id"]: n.get("type") for n in ga["nodes"]}
    type_b = {n["id"]: n.get("type") for n in gb["nodes"]}
    labels = [(type_a[a], type_b[b]) for a, b, _ in pairs]
    alpha = M.krippendorff_alpha_nominal(labels)

    alias_a = {a: f"m{k}" for k, (a, _b, _j) in enumerate(pairs)}
    alias_b = {b: f"m{k}" for k, (_a, b, _j) in enumerate(pairs)}
    ta, tb = M.triples(ga, alias_a), M.triples(gb, alias_b)
    f1 = M.triple_f1(ta, tb)
    null = M.random_graph_null(ta, tb, list(alias_a.values()), draws=draws, seed=seed)
    # Diagnostic only: the same overlap with the edge type erased, which
    # separates disagreement about whether an edge exists from disagreement
    # about what to call it. Never substituted for the gate.
    ua = {(u, "*", v) for u, _t, v in ta}
    ub = {(u, "*", v) for u, _t, v in tb}
    f1_untyped = M.triple_f1(ua, ub)

    sm_a, sm_b = M.support_mass(ga), M.support_mass(gb)
    rho, n_rank = M.spearman(
        [sm_a[a] for a, _b, _j in pairs], [sm_b[b] for _a, b, _j in pairs]
    )

    rc2 = {}
    for op, g, sm in ((ops[0], ga, sm_a), (ops[1], gb, sm_b)):
        pr = M.reverse_pagerank(g)
        ids = list(sm)
        r, n = M.spearman([sm[i] for i in ids], [pr[i] for i in ids])
        rc2[op["id"]] = {"rho_support_mass_vs_reverse_pagerank": r, "n": n}

    return {
        "document": doc,
        "operators": {op["id"]: op["model"] for op in ops},
        "nodes": {ops[0]["id"]: len(ga["nodes"]), ops[1]["id"]: len(gb["nodes"])},
        "edges": {
            ops[0]["id"]: len(ga.get("edges", [])),
            ops[1]["id"]: len(gb.get("edges", [])),
        },
        "spans_located": {ops[0]["id"]: len(off_a), ops[1]["id"]: len(off_b)},
        "layer1": {
            "alpha_nominal": alpha,
            "matched_nodes": len(pairs),
            "boundary_precision": len(pairs) / len(ga["nodes"]) if ga["nodes"] else 0.0,
            "boundary_recall": len(pairs) / len(gb["nodes"]) if gb["nodes"] else 0.0,
            "threshold": L1_ALPHA,
            "passes": bool(alpha == alpha and alpha >= L1_ALPHA),
        },
        "layer2": {
            "triple_f1": f1,
            "triples": {ops[0]["id"]: len(ta), ops[1]["id"]: len(tb)},
            "shared_triples": len(ta & tb),
            "null": null,
            "threshold": L2_F1,
            "beats_null_p99": bool(f1 > null["p99"]),
            "passes": bool(f1 >= L2_F1 and f1 > null["p99"]),
            "triple_f1_untyped_diagnostic": f1_untyped,
            # How much of each operator's edge set survives the restriction to
            # the agreed node set. A low value says the Layer-2 statistic is
            # being computed on a small slice of what either operator drew,
            # which bounds how much it can be read as edge disagreement.
            "edge_retention": {
                ops[0]["id"]: (
                    len(ta) / len(ga.get("edges", [])) if ga.get("edges") else 0.0
                ),
                ops[1]["id"]: (
                    len(tb) / len(gb.get("edges", [])) if gb.get("edges") else 0.0
                ),
            },
        },
        "layer3": {
            "spearman_rho": rho,
            "n": n_rank,
            "threshold": L3_RHO,
            "meets_threshold": bool(rho == rho and rho >= L3_RHO),
            "gated": False,
        },
        "rc2_centrality_sensitivity": rc2,
        "status_counts": {
            ops[0]["id"]: M.status_counts(ga),
            ops[1]["id"]: M.status_counts(gb),
        },
        "miracle_count": {
            ops[0]["id"]: M.miracle_count(ga),
            ops[1]["id"]: M.miracle_count(gb),
        },
        "prose_mass": M.prose_mass(text),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", choices=["pilot", "main"], required=True)
    ap.add_argument("--draws", type=int, default=10000)
    args = ap.parse_args()

    proto = L.protocol()
    docs = list(proto["pilot_documents"] if args.set == "pilot" else proto["specimens"])
    ops = proto["extraction_operators"]
    seed = int(proto["seed"])

    out_dir = L.OUTPUT_DIR / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for doc in docs:
        try:
            results.append(score_document(doc, ops, seed, args.draws))
        except FileNotFoundError as exc:
            print(f"  {doc:16s} SKIPPED (missing extraction: {exc})")
    path = out_dir / f"agreement_{args.set}.json"
    path.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")

    print(f"\nRC1 agreement -- {args.set}")
    head = f"{'document':16s} {'nA':>4s} {'nB':>4s} {'match':>6s} {'alpha':>7s} {'F1':>6s} {'null99':>7s} {'rho':>7s}"
    print(head)
    print("-" * len(head))
    for r in results:
        a, b = list(r["nodes"])
        print(
            f"{r['document']:16s} {r['nodes'][a]:>4d} {r['nodes'][b]:>4d} "
            f"{r['layer1']['matched_nodes']:>6d} {r['layer1']['alpha_nominal']:>7.3f} "
            f"{r['layer2']['triple_f1']:>6.3f} {r['layer2']['null']['p99']:>7.3f} "
            f"{r['layer3']['spearman_rho']:>7.3f}"
        )
    print(f"\nwritten -> {path.relative_to(L.PAPER_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
