#!/usr/bin/env python3
"""Render the run's tables into the paper's reporting format (Tables A1-A3, Table 2).

Reads output/tables/*.json and writes output/tables/RESULTS_SUMMARY.md. Makes no
call and computes no new quantity: everything here is a rendering of what the
scorers already wrote, so the paper and the record cannot drift.

Run:
    uv run --with pyyaml python code/emit_results_summary.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402

TABLES = L.OUTPUT_DIR / "tables"
COND = {"u_free": "U-free", "u_det": "U-det", "u_mod": "U-mod"}
DOC = {
    "vc1": "VC1",
    "vc2": "VC2",
    "vc3_r0": "VC3 R0",
    "vc3_r1": "VC3 R1",
    "vc3_r2": "VC3 R2",
}


def f3(x) -> str:
    """Three decimals, no leading zero -- the corpus reporting rule."""
    if x is None:
        return "--"
    s = f"{x:.3f}"
    return s.replace("0.", ".", 1) if s.startswith("0.") else s.replace("-0.", "-.", 1)


def load(name: str):
    p = TABLES / name
    return L.load_json(p) if p.exists() else None


def main() -> int:
    out: list[str] = ["# 2026bl run -- results as computed", ""]
    proto = L.protocol()
    out += [
        f"Protocol `{proto['protocol_version']}`, prompts `{proto['prompt_version']}`, "
        f"seed {proto['seed']}, k = {proto['repetitions_k']}.",
        "",
        "Every number here is rendered from `output/tables/*.json`. Nothing is computed twice.",
        "",
    ]

    ls = load("layer_s.json")
    if ls:
        out += [
            "## Table A2 -- segmenter fidelity, established before any operator call",
            "",
            "| Document | Units (segmenter) | Units (adjudicated) | Boundary agreement (kappa) | "
            "Adjudicators' own kappa | Displayed-mathematics merges | Gates? |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
        for r in ls["rows"]:
            out.append(
                f"| {DOC.get(r['document'], r['document'])} | {r['units_segmenter']} | "
                f"{r['units_adjudicated']} | {f3(r['layer_s_kappa']['kappa'])} | "
                f"{f3(r['adjudicator_kappa']['kappa'])} | {r['math_merges']} | "
                f"{'PASS' if r['passes'] else 'FAIL'} |"
            )
        out += ["", f"*Gate*: kappa >= {f3(ls['gate'])}.", ""]

    pbr = load("predicted_base_rates.json")
    if pbr:
        out += [
            "## Predicted base rates, declared before any operator call",
            "",
            "| Document | Inventory units | Predecessor nodes (A/B) | Predicted base rate | "
            "Predicted prevalence index | Gates? |",
            "|---|---:|---:|---:|---:|---|",
        ]
        for r in pbr["rows"]:
            a, b = r["predecessor_nodes"].values()
            out.append(
                f"| {DOC.get(r['document'], r['document'])} | {r['inventory_units']} | {a}/{b} | "
                f"{f3(r['predicted_base_rate'])} | {f3(r['predicted_prevalence_index'])} | "
                f"{'yes' if r['gates'] else 'NO (declared uninterpretable in advance)'} |"
            )
        out += [
            "",
            f"*Floor*: prevalence index > {f3(pbr['prevalence_floor'])} is non-gating.",
            "",
        ]

    dec = load("decomposition.json")
    if dec:
        out += [
            "## Table A1 -- decomposition by document, condition and layer",
            "",
            "Each cell is *between-operator* / *within-operator*, computed on the same statistic.",
            "",
            "| Document | Condition | Layer 1 (select) | Layer 2 (type given selected) | "
            "Layer 3 (edges given agreed) | Layer 4 (edges over inventory) | L4/L3 |",
            "|---|---|---|---|---|---|---:|",
        ]
        for r in dec["rows"]:
            cells = []
            for layer in ("layer1", "layer2", "layer3", "layer4"):
                cells.append(
                    f"{f3(r[layer]['between_mean'])} / {f3(r[layer]['within_mean'])}"
                )
            out.append(
                f"| {DOC.get(r['document'], r['document'])} | {COND.get(r['condition'], r['condition'])} | "
                + " | ".join(cells)
                + f" | {f3(r['layer4'].get('ratio_to_layer3'))} |"
            )
        out += [
            "",
            "Layers 1, 2 and 4 are not defined in U-free, which has no shared inventory.",
            "",
        ]

        out += [
            "## The within-operator baseline, per operator (A4)",
            "",
            "The pooled figure in Table A1 is the DECLARED statistic (M3). It is shown here "
            "split by operator, because the two are not sampled the same way and cannot be: "
            "one is called at temperature 0 with a fixed seed, the other belongs to a family "
            "that rejects sampling parameters. An operator whose $k$ repetitions are identical "
            "contributes a constant $1.000$ rather than a measurement, which inflates the "
            "pooled baseline and makes P2's separation easier to obtain.",
            "",
            "| Document | Condition | Layer | Pooled | OP_A | OP_B | Constant contributor? |",
            "|---|---|---|---:|---:|---:|---|",
        ]
        for r in dec["rows"]:
            for layer, label in (
                ("layer1", "1"),
                ("layer2", "2"),
                ("layer3", "3"),
                ("layer4", "4"),
            ):
                by = r[layer].get("within_by_operator") or {}
                if not by or r[layer]["within_mean"] is None:
                    continue
                flat = [
                    op
                    for op, v in by.items()
                    if v["zero_variance"] and v["mean"] is not None
                ]
                out.append(
                    f"| {DOC.get(r['document'], r['document'])} | "
                    f"{COND.get(r['condition'], r['condition'])} | {label} | "
                    f"{f3(r[layer]['within_mean'])} | "
                    f"{f3((by.get('OP_A') or {}).get('mean'))} | "
                    f"{f3((by.get('OP_B') or {}).get('mean'))} | "
                    f"{', '.join(flat) if flat else 'no'} |"
                )
        out.append("")

        out += [
            "## Layer 3, both criteria",
            "",
            "| Document | Condition | Between | Within (noise floor) | Difference | p | 95% CI | "
            "Absolute (>= .71)? | Separated below the floor? |",
            "|---|---|---:|---:|---:|---:|---|---|---|",
        ]
        for r in dec["rows"]:
            sep = r["layer3"]["separation"]
            if "difference" not in sep:
                continue
            out.append(
                f"| {DOC.get(r['document'], r['document'])} | {COND.get(r['condition'], r['condition'])} | "
                f"{f3(sep['mean_between'])} | {f3(sep['mean_within'])} | {f3(sep['difference'])} | "
                f"{f3(sep['p_value'])} | [{f3(sep['ci_low'])}, {f3(sep['ci_high'])}] | "
                f"{'yes' if r['verdicts']['layer3_absolute'] else 'no'} | "
                f"{'yes' if sep['separated'] else 'no'} |"
            )
        out.append("")

    comp = load("composite.json")
    if comp and comp["rows"]:
        out += [
            "## The published joint coefficients, computed in-study (M5a)",
            "",
            "| Document | Condition | gamma | gamma-cat |",
            "|---|---|---:|---:|",
        ]
        for r in comp["rows"]:
            out.append(
                f"| {DOC.get(r['document'], r['document'])} | {COND.get(r['condition'], r['condition'])} | "
                f"{f3(r['gamma'])} | {f3(r['gamma_cat'])} |"
            )
        out += ["", f"Computed on {comp['computed_on']}.", ""]

    rean = load("reanalysis.json")
    if rean:
        out += [
            "## Table A3 -- the predecessor's node layer, as reported and as recomputed",
            "",
            "| Document | As reported (matched nodes only) | Recomputed (charging boundary "
            "disagreement) | Difference |",
            "|---|---:|---:|---:|",
        ]
        for r in rean["rows"]:
            rep = r["as_reported_matched_nodes_only"]
            rep_s = "--" if rep != rep else f3(rep)  # NaN in the predecessor's record
            diff = r["difference"]
            diff_s = "--" if diff != diff else f3(diff)
            out.append(
                f"| {DOC.get(r['document'], r['document'])} | {rep_s} | "
                f"{f3(r['recomputed_joint_gamma'])} | {diff_s} |"
            )
        out += [
            "",
            f"Declared direction (recomputed worse) holds on "
            f"{rean['documents_in_declared_direction']} of {rean['documents']} documents.",
            "",
        ]

    path = TABLES / "RESULTS_SUMMARY.md"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
