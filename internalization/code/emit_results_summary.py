#!/usr/bin/env python3
"""Render every scored quantity into one Markdown summary.

The paper's Results section is written from this file rather than from numbers
copied out of JSON by hand, so a reported value and a computed value cannot
drift apart. Read-only; no API access.

Run:
    uv run --with pyyaml python \
        code/emit_results_summary.py
"""

from __future__ import annotations

import json
import sys

import spine_lib as L

TABLES = L.OUTPUT_DIR / "tables"


def load(name: str):
    path = TABLES / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def fmt(x, nd: int = 3) -> str:
    """Corpus number style: no leading zero below 1, em dash for missing."""
    if x is None:
        return "—"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, int):
        return str(x)
    if x != x:  # NaN
        return "—"
    s = f"{x:.{nd}f}"
    return s.replace("0.", ".", 1) if s.startswith("0.") else s


def agreement_section(rows, title: str) -> list[str]:
    if not rows:
        return [f"### {title}\n\n_not run_\n"]
    out = [
        f"### {title}",
        "",
        "| document | nodes A | nodes B | matched | Layer 1 α | Layer 2 F1 | untyped F1 | null p99 | beats null | Layer 3 ρ |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        a, b = list(r["nodes"])
        l1, l2, l3 = r["layer1"], r["layer2"], r["layer3"]
        out.append(
            f"| {r['document']} | {r['nodes'][a]} | {r['nodes'][b]} | {l1['matched_nodes']} | "
            f"{fmt(l1['alpha_nominal'])} | {fmt(l2['triple_f1'])} | "
            f"{fmt(l2.get('triple_f1_untyped_diagnostic'))} | {fmt(l2['null']['p99'])} | "
            f"{fmt(l2['beats_null_p99'])} | {fmt(l3['spearman_rho'])} |"
        )
    out += [
        "",
        "Thresholds: α ≥ .65 (Layer 1), F1 ≥ .60 and above the null's 99th "
        "percentile (Layer 2, the gate), ρ ≥ .50 (Layer 3, reported not gated).",
        "",
    ]
    for r in rows:
        out.append(
            f"- **{r['document']}** — Layer 1 {'passes' if r['layer1']['passes'] else 'FAILS'}; "
            f"Layer 2 {'passes' if r['layer2']['passes'] else 'FAILS'} "
            f"({r['layer2']['shared_triples']} shared of "
            f"{r['layer2']['triples'][list(r['layer2']['triples'])[0]]}/"
            f"{r['layer2']['triples'][list(r['layer2']['triples'])[1]]} triples); "
            f"boundary precision {fmt(r['layer1']['boundary_precision'])}, "
            f"recall {fmt(r['layer1']['boundary_recall'])}."
        )
    out.append("")
    return out


def ladder_section(ladder) -> list[str]:
    if not ladder:
        return ["## VC3 — the ladder\n\n_not run_\n"]
    out = ["## VC3 — the ladder", ""]
    for op, rungs in ladder["rungs"].items():
        out += [
            f"### Arm {op}",
            "",
            "| rung | prose mass | nodes | edges | mean support mass | derived | verified only | miracle |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for rung, p in rungs.items():
            sc = p["status_counts"]
            out.append(
                f"| {rung} | {p['prose_mass']['words_math_collapsed']} | {p['nodes']} | "
                f"{p['edges']} | {fmt(p['mean_support_mass'], 2)} | {sc['derived']} | "
                f"{sc['verified_only']} | {sc['miracle']} |"
            )
        o = ladder["ordering"][op]
        out += [
            "",
            f"Monotonic miracle ordering MC(R0) > MC(R1) > MC(R2): "
            f"**{'holds' if o['strictly_decreasing'] else 'FAILS'}**"
            + (
                f" — inversions at {', '.join(o['inversions'])}"
                if o["inversions"]
                else ""
            )
            + ".",
            "",
            "| pair | F1 (blind aligner) | null p99 | preserves | F1 (lexical) | preserves |",
            "|---|---|---|---|---|---|",
        ]
        for pair, v in ladder["preservation"][op].items():
            llm, lex = v["llm_alignment"], v["lexical_alignment"]
            out.append(
                f"| {pair} | {fmt(llm['triple_f1'])} | {fmt(llm['null']['p99'])} | "
                f"{fmt(llm['preserves'])} | {fmt(lex['triple_f1'])} | {fmt(lex['preserves'])} |"
            )
        out.append("")
    out += [
        f"**Ordering survives on both arms: "
        f"{fmt(ladder['ordering']['survives_on_both_arms'])}** — the pre-declared rule.",
        "",
    ]
    return out


def targets_section(targets) -> list[str]:
    if not targets:
        return ["## Recovery targets T1-T3\n\n_not run_\n"]
    out = [
        "## Recovery targets T1-T3",
        "",
        "| document | arm | T1 | T2 | T3 | T2 and T3 both |",
        "|---|---|---|---|---|---|",
    ]
    for doc, per_doc in targets["documents"].items():
        for op, entry in per_doc.items():
            t = entry["targets"]
            out.append(
                f"| {doc} | {op} | {t['T1']['final']} | {t['T2']['final']} | "
                f"{t['T3']['final']} | {fmt(t['success_rule_T2_and_T3'])} |"
            )
    rec = targets["third_rater_recourse"]
    share = rec["resolved"] / rec["targets"] if rec["targets"] else 0
    out += [
        "",
        f"Third-rater recourse: {rec['resolved']} of {rec['targets']} target judgments "
        f"({fmt(share)}).",
        "",
    ]
    return out


def main() -> int:
    lines = [
        "# Computed results — Internalization (2026bk)",
        "",
        "Generated by `code/emit_results_summary.py` from the committed scoring outputs.",
        "Every number in the paper's Results section comes from this file.",
        "",
        "## RC1 — extraction agreement",
        "",
    ]
    lines += agreement_section(load("agreement_main.json"), "Specimens")
    lines += agreement_section(
        load("agreement_pilot.json"), "Pilot (non-specimen material)"
    )
    lines += ladder_section(load("ladder.json"))
    lines += targets_section(load("targets.json"))

    out = L.OUTPUT_DIR / "tables" / "RESULTS_SUMMARY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwritten -> {out.relative_to(L.REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
