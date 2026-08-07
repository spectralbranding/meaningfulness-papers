#!/usr/bin/env python3
"""Stage 4 of the 2026bk run: the T1-T3 recovery targets.

Each extracted graph is scored against the text it came from by two raters,
blind to which operator produced it and drawn from families that did not
produce it. Disagreement on a target goes to a third rater, and the rate of
third-rater recourse is reported, as the decision rule requires.

The success rule is pre-declared and is not evaluated here as an average: T2
AND T3 must both be recovered. T1 is reported and is not part of the rule.

Run:
    bws run -- uv run --with httpx --with pyyaml python \
        code/score_targets.py
"""

from __future__ import annotations

import json
import sys

import spine_lib as L

TARGETS = ["T1", "T2", "T3"]


def blind_graph(graph: dict) -> str:
    """The graph as the rater sees it: no operator, no model, no provenance."""
    clean = {
        "nodes": [
            {
                k: v
                for k, v in n.items()
                if k
                in (
                    "id",
                    "type",
                    "statement",
                    "span",
                    "explanatory_status",
                    "status_reason",
                )
            }
            for n in graph.get("nodes", [])
        ],
        "edges": graph.get("edges", []),
    }
    return json.dumps(clean, indent=1, ensure_ascii=False)


def rate(doc: str, op_id: str, rater: dict) -> dict:
    cache = L.DATA_DIR / f"rating_{doc}__{op_id}__{rater['id']}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    graph = L.load_graph(doc, op_id)
    raw = L.call_model(
        rater["model"],
        rater["family"],
        L.RATING_SYSTEM,
        L.RATING_USER.format(text=L.specimen_text(doc), graph=blind_graph(graph)),
        role="target_rater",
        operation=f"rate|{rater['id']}|{doc}|{op_id}",
        phase="internalization_rating",
        max_out=16000,
    )
    parsed = L.parse_json_block(raw)
    parsed["_meta"] = {"document": doc, "graph_operator": op_id, "rater": rater["id"]}
    cache.write_text(
        json.dumps(parsed, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return parsed


def verdict(rating: dict, target: str) -> str:
    return (rating.get(target) or {}).get("verdict", "missing")


def main() -> int:
    proto = L.protocol()
    ops = proto["extraction_operators"]
    raters = proto["target_raters"]
    third = proto["third_rater"]
    docs = [d for d, cfg in proto["specimens"].items() if cfg.get("score_targets")]

    results: dict = {
        "documents": {},
        "third_rater_recourse": {"targets": 0, "resolved": 0},
    }
    for doc in docs:
        per_doc = {}
        for op in ops:
            ratings = {r["id"]: rate(doc, op["id"], r) for r in raters}
            entry: dict = {"raters": {r: ratings[r] for r in ratings}}
            per_target = {}
            for t in TARGETS:
                vs = [verdict(ratings[r["id"]], t) for r in raters]
                agreed = vs[0] == vs[1]
                results["third_rater_recourse"]["targets"] += 1
                final = vs[0]
                third_v = None
                if not agreed:
                    results["third_rater_recourse"]["resolved"] += 1
                    try:
                        r3 = rate(doc, op["id"], third)
                    except Exception as exc:  # noqa: BLE001
                        # A rater outage must not silently become a verdict.
                        # The disagreement is recorded as unresolved and the
                        # reason is kept with it.
                        entry.setdefault("third_rater", {})[t] = {
                            "unavailable": str(exc)[:200]
                        }
                        results["third_rater_recourse"].setdefault("unavailable", 0)
                        results["third_rater_recourse"]["unavailable"] += 1
                        per_target[t] = {
                            "rater_verdicts": dict(zip([r["id"] for r in raters], vs)),
                            "third_rater_verdict": None,
                            "agreed": False,
                            "final": "unresolved",
                        }
                        continue
                    third_v = verdict(r3, t)
                    entry.setdefault("third_rater", {})[t] = r3.get(t)
                    # Majority of the three; a three-way split stays unresolved.
                    counts = {
                        v: [vs[0], vs[1], third_v].count(v) for v in set(vs + [third_v])
                    }
                    top = max(counts.values())
                    final = next(
                        (v for v, c in counts.items() if c == top), "unresolved"
                    )
                    if top < 2:
                        final = "unresolved"
                per_target[t] = {
                    "rater_verdicts": dict(zip([r["id"] for r in raters], vs)),
                    "third_rater_verdict": third_v,
                    "agreed": agreed,
                    "final": final,
                }
            per_target["success_rule_T2_and_T3"] = bool(
                per_target["T2"]["final"] == "recovered"
                and per_target["T3"]["final"] == "recovered"
            )
            entry["targets"] = per_target
            per_doc[op["id"]] = entry
        results["documents"][doc] = per_doc

    out = L.OUTPUT_DIR / "tables" / "targets.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(results, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print("\nRecovery targets (success rule: T2 and T3 both)")
    header = f"{'document':10s} {'arm':6s} {'T1':>14s} {'T2':>14s} {'T3':>14s}  rule"
    print(header)
    print("-" * len(header))
    for doc, per_doc in results["documents"].items():
        for op_id, entry in per_doc.items():
            t = entry["targets"]
            print(
                f"{doc:10s} {op_id:6s} {t['T1']['final']:>14s} {t['T2']['final']:>14s} "
                f"{t['T3']['final']:>14s}  {t['success_rule_T2_and_T3']}"
            )
    rec = results["third_rater_recourse"]
    share = rec["resolved"] / rec["targets"] if rec["targets"] else 0
    print(f"\nthird-rater recourse: {rec['resolved']}/{rec['targets']} = {share:.3f}")
    print(f"written -> {out.relative_to(L.PAPER_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
