#!/usr/bin/env python3
"""Step 5 of the 2026bl run: the decomposition (Tables A1 and 2).

Reads only files already on disk; makes no call. Every layer is computed within
one document, under one condition, for one operator pair, and every
between-operator number is reported beside its within-operator counterpart on
the same statistic (M3).

Which pairs. Each operator ran k = 5 repetitions, so:
  * BETWEEN is every cross pair (A_i, B_j) -- 25 of them -- and its mean.
  * WITHIN (Layer B) is every same-operator pair (A_i, A_j) and (B_i, B_j) --
    10 per operator, 20 in all -- and its mean.
Reporting the mean of all pairs rather than one arbitrary pair is what makes the
two commensurable: both are averages over pairs of extractions drawn the same
way, differing only in whether the two came from one operator or two.

Layers 1, 2 and 4 need a shared inventory and are NOT DEFINED in U-free, which
has none (Table A1). They are reported as not applicable rather than as missing,
and are never compared by magnitude against the fixed-inventory conditions (C2).

Run:
    uv run --with pyyaml python code/score_layers.py
"""

from __future__ import annotations

import argparse
import re
import sys
from itertools import combinations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metrics_lib as M  # noqa: E402
import unit_lib as L  # noqa: E402

INVENTORY_FOR = {"u_det": "segmenter", "u_mod": "unitizer"}


# --- reading one extraction into comparable objects -------------------------


def fixed_view(result: dict) -> tuple[set[int], dict[int, str], set[tuple]]:
    """(selected units, unit -> type, typed triples) from a fixed-inventory answer."""
    selected, types = set(), {}
    for item in result.get("selected") or []:
        u = item.get("unit")
        if isinstance(u, int):
            selected.add(u)
            types[u] = item.get("type")
    triples = set()
    for e in result.get("edges") or []:
        f, t, ty = e.get("from"), e.get("to"), e.get("type")
        if isinstance(f, int) and isinstance(t, int):
            triples.add((f, t, ty))
    return selected, types, triples


def _locate(text: str, span: str) -> tuple[int, int] | None:
    if not span:
        return None
    idx = text.find(span)
    if idx < 0:  # whitespace in the quotation does not always match the source
        loose = re.escape(span.strip())
        loose = re.sub(r"\\\s+", r"\\s+", loose)
        m = re.search(loose, text)
        if not m:
            return None
        return m.start(), m.end()
    return idx, idx + len(span)


def free_view(
    result: dict, text: str
) -> tuple[dict[str, tuple[int, int]], dict[str, str], set[tuple]]:
    """(node id -> located span, node id -> type, typed triples) from a free answer.

    A node carries EITHER a verbatim `span`, which is located against the source
    text here, OR a precomputed `span_offsets` pair. The published records carry
    the offsets rather than the span, because a U-free span is a verbatim extract
    of a third-party document and is not redistributed (see redact_for_release.py).
    Matching downstream uses the offsets and nothing else, so the two forms are
    computationally identical -- which is verified cell by cell rather than
    asserted.
    """
    spans, types = {}, {}
    for n in result.get("nodes") or []:
        off = n.get("span_offsets")
        if (
            isinstance(off, (list, tuple))
            and len(off) == 2
            and all(isinstance(x, int) for x in off)
        ):
            loc = (off[0], off[1])
        else:
            loc = _locate(text, (n.get("span") or "").strip())
        if loc:
            spans[n.get("id")] = loc
        types[n.get("id")] = n.get("type")
    triples = {
        (e.get("from"), e.get("to"), e.get("type")) for e in result.get("edges") or []
    }
    return spans, types, triples


def match_free_nodes(a: dict, b: dict) -> dict[str, str]:
    """Match free-condition nodes by span overlap: the predecessor's problem, kept.

    Two nodes correspond when their located spans overlap by at least half the
    shorter span. This is exactly the alignment step the fixed inventory exists
    to remove, and it is used ONLY in U-free, where there is no shared index.
    """
    out = {}
    used = set()
    for ida, (sa, ea) in sorted(a.items(), key=lambda kv: kv[1][0]):
        best, best_ov = None, 0.0
        for idb, (sb, eb) in b.items():
            if idb in used:
                continue
            ov = max(0, min(ea, eb) - max(sa, sb))
            shorter = min(ea - sa, eb - sb) or 1
            frac = ov / shorter
            if frac > best_ov:
                best, best_ov = idb, frac
        if best is not None and best_ov >= 0.5:
            out[ida] = best
            used.add(best)
    return out


# --- one pair of extractions ------------------------------------------------


def score_pair_fixed(ra: dict, rb: dict, n_units: int) -> dict:
    sel_a, ty_a, tri_a = fixed_view(ra)
    sel_b, ty_b, tri_b = fixed_view(rb)
    universe = set(range(1, n_units + 1))

    layer1 = M.cohen_kappa_binary(sel_a, sel_b, universe)
    joint = sorted(sel_a & sel_b)
    layer2 = M.cohen_kappa_nominal(
        [(ty_a.get(u), ty_b.get(u)) for u in joint], L.NODE_TYPES
    )
    agreed = set(joint)
    layer3 = M.triple_f1(
        {t for t in tri_a if t[0] in agreed and t[1] in agreed},
        {t for t in tri_b if t[0] in agreed and t[1] in agreed},
    )
    layer4 = M.triple_f1(tri_a, tri_b)
    return {"layer1": layer1, "layer2": layer2, "layer3": layer3, "layer4": layer4}


def score_pair_free(ra: dict, rb: dict, text: str) -> dict:
    sa, _, tri_a = free_view(ra, text)
    sb, _, tri_b = free_view(rb, text)
    mapping = match_free_nodes(sa, sb)
    agreed_a = set(mapping)
    tri_a_m = {(f, t, ty) for f, t, ty in tri_a if f in agreed_a and t in agreed_a}
    tri_b_m = {
        (f, t, ty)
        for f, t, ty in tri_b
        if f in set(mapping.values()) and t in set(mapping.values())
    }
    projected = {(mapping[f], mapping[t], ty) for f, t, ty in tri_a_m}
    return {
        "layer1": {"note": "not defined in U-free (no shared inventory)"},
        "layer2": {"note": "not defined in U-free (no shared inventory)"},
        "layer3": M.triple_f1(projected, tri_b_m),
        "layer4": {"note": "not defined in U-free (no fixed inventory to charge)"},
        "matched_nodes": len(mapping),
        "nodes_a": len(sa),
        "nodes_b": len(sb),
    }


def _val(cell: dict, key: str):
    return cell.get(key) if isinstance(cell, dict) else None


def score_cell(doc: str, condition: str, ops: list[dict], k: int) -> dict:
    text = L.specimen_text(doc)
    n_units = None
    if condition != "u_free":
        n_units = len(
            L.load_json(L.inventory_path(doc, INVENTORY_FOR[condition]))["units"]
        )

    runs: dict[str, dict[int, dict]] = {}
    missing = []
    for op in ops:
        runs[op["id"]] = {}
        for rep in range(1, k + 1):
            p = L.extraction_path(doc, condition, op["id"], rep)
            if p.exists():
                runs[op["id"]][rep] = L.load_json(p)
            else:
                missing.append(f"{op['id']}/r{rep}")

    a_id, b_id = ops[0]["id"], ops[1]["id"]

    def pair(x, y):
        return (
            score_pair_free(x, y, text)
            if condition == "u_free"
            else score_pair_fixed(x, y, n_units)
        )

    between = [
        pair(runs[a_id][i], runs[b_id][j])
        for i, j in product(sorted(runs[a_id]), sorted(runs[b_id]))
    ]
    # The DECLARED within-operator baseline pools both operators' same-operator
    # pairs and takes the mean, exactly as M3 specifies. That pooled figure is
    # what `within_mean` reports below and it is NOT changed here.
    #
    # It is also kept PER OPERATOR, additively, because pooling hides something
    # the run made visible. The two operators are not sampled the same way, and
    # they cannot be: this provider pair offers no common setting. OP_B is
    # called at temperature 0 with a fixed seed, so most of its cells return
    # byte-identical answers across all k repetitions -- its within-operator
    # agreement is then 1.000 BY CONSTRUCTION rather than by measurement. OP_A's
    # family rejects sampling parameters outright, so it cannot be pinned the
    # same way and its repetitions genuinely vary. A pooled baseline therefore
    # averages a measured quantity with a constant, which flatters the noise
    # floor and makes P2's separation easier to obtain. Reporting both keeps the
    # declared statistic intact and lets a reader see what it is made of.
    within = []
    within_by_op: dict[str, list[dict]] = {}
    for op_id in (a_id, b_id):
        pairs = [
            pair(runs[op_id][i], runs[op_id][j])
            for i, j in combinations(sorted(runs[op_id]), 2)
        ]
        within_by_op[op_id] = pairs
        within += pairs

    out = {
        "document": doc,
        "condition": condition,
        "n_units": n_units,
        "missing_runs": missing,
        "n_between_pairs": len(between),
        "n_within_pairs": len(within),
    }
    for layer, key in (
        ("layer1", "kappa"),
        ("layer2", "kappa"),
        ("layer3", "f1"),
        ("layer4", "f1"),
    ):
        b_vals = [_val(p[layer], key) for p in between]
        w_vals = [_val(p[layer], key) for p in within]
        out[layer] = {
            "between_mean": M.mean(b_vals),
            "within_mean": M.mean(w_vals),
            "between_values": b_vals,
            "within_values": w_vals,
            "detail_first_pair": between[0][layer] if between else None,
            "separation": M.separation_test(
                b_vals, w_vals, seed=L.stream_seed(doc, condition, layer)
            ),
            # Additive to the declared pooled figure above; see the note at the
            # within-pair construction. `zero_variance` is the diagnostic that
            # matters: an operator whose k repetitions are identical contributes
            # a constant 1.000 to the pooled baseline.
            "within_by_operator": {
                op_id: {
                    "mean": M.mean([_val(p[layer], key) for p in pairs]),
                    "values": [_val(p[layer], key) for p in pairs],
                    "zero_variance": len(
                        {
                            v
                            for v in (_val(p[layer], key) for p in pairs)
                            if v is not None
                        }
                    )
                    == 1,
                }
                for op_id, pairs in within_by_op.items()
            },
        }
    if between:
        l3, l4 = out["layer3"]["between_mean"], out["layer4"]["between_mean"]
        # Layer 4 is NOT DEFINED in U-free, which has no fixed inventory to
        # charge, so its between-mean is None there and the ratio is too. The
        # ratio gate is the only Layer 4 criterion (M4a), so "not applicable"
        # is the correct value rather than a number computed from a missing
        # one -- and reporting it as absent is what C2 requires anyway.
        out["layer4"]["ratio_to_layer3"] = (
            (l4 / l3) if (l3 and l4 is not None) else None
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="*")
    ap.add_argument("--conditions", nargs="*")
    args = ap.parse_args()

    proto = L.protocol()
    k = int(proto["repetitions_k"])
    ops = proto["extraction_operators"]
    th = proto["thresholds"]
    floor = float(th["prevalence_floor"])
    predicted = {
        r["document"]: r
        for r in L.load_json(L.OUTPUT_DIR / "tables" / "predicted_base_rates.json")[
            "rows"
        ]
    }

    rows = []
    for condition in proto["condition_order"]:
        if args.conditions and condition not in args.conditions:
            continue
        for doc in proto["specimens"]:
            if args.docs and doc not in args.docs:
                continue
            if not any(
                L.extraction_path(doc, condition, o["id"], 1).exists() for o in ops
            ):
                continue
            cell = score_cell(doc, condition, ops, k)
            cell["gates"] = predicted[doc]["gates"]
            cell["predicted_prevalence_index"] = predicted[doc][
                "predicted_prevalence_index"
            ]
            cell["verdicts"] = {
                "layer1": (
                    None
                    if not cell["gates"] or cell["layer1"]["between_mean"] is None
                    else cell["layer1"]["between_mean"]
                    >= float(th["layer_1_selection_kappa"])
                ),
                "layer2": (
                    None
                    if cell["layer2"]["between_mean"] is None
                    else cell["layer2"]["between_mean"]
                    >= float(th["layer_2_typing_kappa"])
                ),
                "layer3_absolute": (
                    None
                    if cell["layer3"]["between_mean"] is None
                    else cell["layer3"]["between_mean"]
                    >= float(th["layer_3_edges_absolute"])
                ),
                "layer3_relative_not_separated_below_floor": (
                    None
                    if not cell["layer3"]["separation"].get("separated") is not None
                    else not cell["layer3"]["separation"].get("separated")
                ),
                "layer4_ratio": (
                    None
                    if cell["layer4"].get("ratio_to_layer3") is None
                    else cell["layer4"]["ratio_to_layer3"]
                    > float(th["layer_4_ratio_to_layer_3"])
                ),
            }
            rows.append(cell)
            print(
                f"  {doc:8s} {condition:7s} "
                f"L1={_fmt(cell['layer1']['between_mean'])}/{_fmt(cell['layer1']['within_mean'])} "
                f"L2={_fmt(cell['layer2']['between_mean'])}/{_fmt(cell['layer2']['within_mean'])} "
                f"L3={_fmt(cell['layer3']['between_mean'])}/{_fmt(cell['layer3']['within_mean'])} "
                f"L4={_fmt(cell['layer4']['between_mean'])}/{_fmt(cell['layer4']['within_mean'])} "
                f"{'' if cell['gates'] else '(non-gating, PI floor)'}"
            )

    L.write_json(
        L.OUTPUT_DIR / "tables" / "decomposition.json",
        {"thresholds": dict(th), "prevalence_floor": floor, "rows": rows},
    )
    return 0


def _fmt(x) -> str:
    return " n/a " if x is None else f"{x:.3f}"


if __name__ == "__main__":
    sys.exit(main())
