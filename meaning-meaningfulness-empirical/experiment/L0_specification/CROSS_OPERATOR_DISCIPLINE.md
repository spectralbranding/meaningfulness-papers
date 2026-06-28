# Cross-Operator Extraction Discipline

**HARD RULE — the cross-operator extraction separation rule**

**First introduced**: 2026-05-27 (Paper B v1.0.0)
**Formalized in L0 cascade**: v1.1.0 2026-05-28

---

## The Rule

The model that renders prose from a spine (Operator B) must be **different** from the model that extracts a spine from that prose (Operator C).

```
Operator B (renderer) != Operator C (extractor)
```

The extractor must **never** see the source spine. The extractor receives only the rendered prose as input.

## Why this rule exists

Within-model memory contamination: if the same model renders prose from a spine and then extracts a spine from that prose, the extraction output may reflect the model's own rendering decisions — not independent structural recovery of what the prose asserts. This would inflate preservation scores without providing evidence that the spine is recoverable by an independent observer.

Cross-operator separation (B != C) ensures the extraction is a genuine test of whether the prose, standing alone, preserves the spine's structural elements.

## Implementation in the experiment corpus

| Phase | Renderer (B) | Extractor (C) | B != C compliant |
|---|---|---|---|
| Phase 2 (self-application Substack) | Claude Opus (via harness) | Claude Opus | Within-operator (B = C); reported with explicit caveat; motivates cross-operator discipline |
| Phase 2-prime | Claude Opus | GPT-4o-2024-08-06 | YES |
| Phase 2.5 cross-paper | Claude Opus | GPT-4o-2024-08-06 | YES |
| Phase 3 (LinkedIn) | Claude Opus | Claude Opus | Within-operator (B = C); reported with caveat |
| Phase 3-prime | Claude Opus | GPT-4o-2024-08-06 | YES |
| Phase 3.5a (human-native RU) | Human | GPT-4o-2024-08-06 | YES (human != GPT-4o) |
| Phase 3.5b (multi-LLM RU) | GigaChat / YandexGPT / DeepSeek / Claude Opus | GPT-4o-2024-08-06 | YES for all four |
| Phase 3.5c (RU-native retry) | GigaChat / YandexGPT | GPT-4o-2024-08-06 | YES for both |
| Phase 3.5d (ZH rendering) | DeepSeek / Claude Opus / Qwen3.6:27b | GPT-4o-2024-08-06 | YES for all three |
| Phase 3.5d cross-extractor robustness | DeepSeek (renderer) | Qwen3.6:27b (extractor) | YES (DeepSeek != Qwen3.6:27b) |

## What the extractor never sees

In every cross-operator run, the extractor prompt contains:

> "Read ONLY the provided prose. You do NOT have access to any source spine."

This instruction is enforced at the call level: the extractor receives only the rendered prose in its user-turn context; no spine YAML, no locked-proposition list, no source abstract is included.

## Within-operator disclosure

Phase 2 and Phase 3 initial runs used same-operator re-extraction (Claude rendering then Claude extraction). These are disclosed explicitly in paper.md as **within-operator** results with a caveat that they constitute upper-bound estimates of strict preservation. The within-operator vs cross-operator comparison (disclosed in §Discussion §Reliability of the P4 Demonstration, Table 2) shows ~15 percentage-point strict / ~0 semantic gap, confirming that the B = C runs overcount STRICT labels relative to the B != C canonical runs.

## Three-operator pipeline

The canonical pipeline for all Phase 3.5c/3.5d runs is:

```
Operator A (orchestrator): experiment script + researcher judgment
Operator B (renderer): GigaChat | YandexGPT | DeepSeek | Claude Opus | Qwen3.6:27b-Ollama
Operator C (extractor): GPT-4o-2024-08-06 (canonical) | Qwen3.6:27b-Ollama (cross-extractor robustness only)
```

B and C are always different. A is always different from both B and C.

## Per-run compliance evidence

Each phase manifest (`*_manifest.json`) records a `cross_operator_discipline` block that names the renderer and extractor for each run and asserts B != C compliance. See:

- `phase_3_5c_runs/multi_llm_manifest.json::cross_operator_discipline`
- `phase_3_5d_runs/multi_llm_manifest.json::cross_operator_discipline`

---

*Source rule*: cross-operator extraction separation (2026-05-27)
*Companion document*: `PROMPT_PURITY_PROTOCOL.md` §Cross-references
