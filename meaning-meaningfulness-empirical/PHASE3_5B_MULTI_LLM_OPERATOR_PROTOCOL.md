---
title: "Phase 3.5b multi-LLM cross-FAMILY robustness — Russian (Slavic) + Chinese (Sino-Tibetan) protocol + script + v1.1.0 execution-ready backlog"
date: 2026-05-27
session: Session H Phase 3.5b (NEW stretch per user mid-session addendum + Chinese expansion delta)
covers_stylized_fact: "SF3 cross-language preservation — robustness check on operator-choice variation AND cross-FAMILY robustness (Slavic + Sino-Tibetan; maximally distant well-resourced language families)"
purpose: "Reviewer-defense framing: preservation isn't an artifact of operator choice OR Russian-English linguistic proximity"
status: "Protocol documented + script execution-ready (research/meaningfulness_empirical_companion/code/multi_llm_rendering.py); BWS keys verified (YANDEX_AI_API_KEY + GIGACHAT_API_KEY + DEEPSEEK_API_KEY + ANTHROPIC_API_KEY + OPENAI_API_KEY); EXECUTION DEFERRED to v1.1.0 stretch per Session H init prompt stretch budget rule (better clean v1.0.0 + Zenodo ship Fri AM than partial 3.5b that slips Zenodo)"
academic_pattern: "LLM-as-evaluator robustness check (Chiang et al. 2023; Zheng et al. 2023) extended to rendering-operator level + cross-family linguistic-family robustness"
---

# Phase 3.5b multi-LLM Russian-operator robustness — protocol + skeleton + v1.1.0 backlog placement

## Why this Phase exists

Phase 3.5a tests SF3 with one human-native Russian rendering. A reviewer can plausibly object: "the result holds because of the operator's particular language-rendering choices; a different operator might produce a Russian rendering with different preservation rates." The academic-robustness pattern for this objection (from LLM-as-evaluator literature) is to run the same rendering task through multiple operator variants and compare preservation rates across operators.

The Phase 3.5b stretch test recruits 2-3 LLM operators (preferably 1-2 Russian-native LLMs to control for the English-substrate bias of US-trained LLMs, plus 1 English-substrate LLM for comparison) to produce Russian renderings of the same source text. Per-operator preservation rates and cross-operator agreement matrices supply robustness evidence.

## Operator selection (cross-FAMILY robustness — Slavic + Sino-Tibetan)

User-authorized expansion (Session H delta 2026-05-27): extend Phase 3.5b from Russian-only (Slavic family) to Russian + Chinese (Slavic + Sino-Tibetan). The cross-family pair (Russian + Chinese) is the maximally-distant well-resourced language-family pair, addressing the additional reviewer objection that within-Indo-European preservation may reflect linguistic proximity rather than substrate-as-language-invariant claim.

**Russian-native operators (Slavic family):**

- **YandexGPT** (Yandex; trained substantially on Russian-language web + RuWiki + RuNet); native fluency in Russian academic register. BWS key: `YANDEX_AI_API_KEY` ✓ verified provisioned.
- **GigaChat** (Sberbank; trained substantially on independent Russian corpus); native fluency; alternative training corpus to YandexGPT controls for Yandex-specific stylistic preferences. BWS key: `GIGACHAT_API_KEY` ✓ verified provisioned.

**Chinese-native operators (Sino-Tibetan family):**

- **DeepSeek** (DeepSeek-V3 or DeepSeek-R1; high-quality Chinese-native; OpenAI-compatible API). BWS key: `DEEPSEEK_API_KEY` ✓ verified provisioned.
- **Qwen** (通义千问 / Alibaba; Qwen-Plus or Qwen-Max; alternative Chinese corpus to DeepSeek). BWS key: ✗ NOT provisioned in BWS — operator drops out unless user adds key for v1.1.0 execution. Fallback options: Doubao (豆包 / ByteDance) or GLM (ZhipuAI 智谱); neither key currently in BWS.

**English-substrate operators (cross-substrate control):**

- **Claude Opus 4.7** (Anthropic; English-substrate primary; renders into BOTH Russian and Chinese for cross-substrate comparison). BWS key: `ANTHROPIC_API_KEY` ✓ verified provisioned.
- **GPT-4o** (OpenAI; English-substrate primary; alternative to Claude). BWS key: `OPENAI_API_KEY` ✓ verified provisioned.

**Verified-executable subset (v1.1.0)**: YandexGPT + GigaChat + DeepSeek + Claude Opus = 4 operators (2 Russian-native Slavic + 1 Chinese-native Sino-Tibetan + 1 English-substrate control rendering into both Russian and Chinese). This covers within-Slavic-family agreement, cross-Slavic-vs-Sino-Tibetan invariance, and within-English-substrate-vs-native operator-substrate comparison.

**Minimum-viable subset** (if time-or-budget short at v1.1.0 execution): YandexGPT + DeepSeek = 2 operators, 1 from each language family. The minimum cross-family preservation comparison; weaker on within-family agreement but preserves the cross-FAMILY robustness claim.

## Execution-ready script

Script: `research/meaningfulness_empirical_companion/code/multi_llm_rendering.py` (per user direction: single shared script under the paper's own code/ directory). Run pattern (BWS-injected per fleet convention; reference: `audit/scripts/dr_v1_empirical_cases.py`):

```bash
cd /Users/d/projects/spectral-branding-meaningfulness-empirical
bws run -- uv run --with anthropic --with openai --with httpx \
  python research/meaningfulness_empirical_companion/code/multi_llm_rendering.py \
  --source-text research/meaningfulness_empirical_companion/paper.md \
  --source-extract abstract \
  --target-languages ru zh \
  --operators yandexgpt gigachat deepseek claude_opus \
  --output-dir research/meaningfulness_empirical_companion/multi_llm_cross_family/ \
  --seed 42
```

### Required secrets (BWS-injected via `bws run --`) — ALL VERIFIED PROVISIONED

- `YANDEX_AI_API_KEY` ✓ — Yandex Cloud API key (folder ID embedded in key or via separate `YANDEX_AI_FOLDER_ID`; verify at execution time)
- `GIGACHAT_API_KEY` ✓ — Sberbank GigaChat credential (OAuth2 token-exchange flow inside script)
- `DEEPSEEK_API_KEY` ✓ — DeepSeek (OpenAI-compatible endpoint at https://api.deepseek.com/v1)
- `ANTHROPIC_API_KEY` ✓ — for Claude Opus
- `OPENAI_API_KEY` ✓ — for GPT-4o (if added)
- `QWEN_API_KEY` ✗ NOT PROVISIONED — operator drops out unless user adds for v1.1.0

### Expected outputs

Naming convention per user spec: `RENDERING_PB_<RU|ZH>_<ABSTRACT|SECTION_THEORY>_<LLM_NAME>.md`

- `multi_llm_cross_family/RENDERING_PB_RU_ABSTRACT_YANDEXGPT.md` (~250-300 Russian words)
- `multi_llm_cross_family/RENDERING_PB_RU_ABSTRACT_GIGACHAT.md` (~250-300 Russian words)
- `multi_llm_cross_family/RENDERING_PB_RU_ABSTRACT_CLAUDE_OPUS.md` (~250-300 Russian words; English-substrate control)
- `multi_llm_cross_family/RENDERING_PB_ZH_ABSTRACT_DEEPSEEK.md` (~350-450 Chinese characters)
- `multi_llm_cross_family/RENDERING_PB_ZH_ABSTRACT_CLAUDE_OPUS.md` (~350-450 Chinese characters; English-substrate control rendering into Chinese)
- `multi_llm_cross_family/multi_llm_manifest.json` (per-operator metadata)

### Per-operator spine re-extraction (Claude as extractor, per user authorization)

Per user direction (Session H delta): "QUALITY CONTROL FOR CHINESE: you are the spine extractor for Chinese renderings. You're Claude, fluent in Chinese reading + structured extraction. The Paper A codebook is language-agnostic (conceptual node types, not lexical). Extract directly from Chinese prose; do not back-translate."

Per-operator re-extraction follows the same protocol as the English / Russian extractions:

- Read the per-operator rendering directly (no back-translation; preserves the rendering-layer signal without confounding by translation-layer noise)
- Apply paper_a:appendix_A_schema (10 node types + 17 edge types) — language-agnostic conceptual taxonomy
- Output per-operator: `VALIDATION_CASE_PB_<RU|ZH>_<LLM_NAME>_SPINE.yaml`

### Cross-operator + cross-FAMILY analysis

Output: `CROSS_LANGUAGE_MULTI_OPERATOR_ROBUSTNESS.md`. Contents per user spec:

- **Per-operator preservation rate table**: operator × source spine; preservation count + % + node-type-match accuracy + antecedent-edge-match accuracy
- **Within-family agreement**: do Russian operators (human + YandexGPT + GigaChat + Claude-rendering-into-Russian) preserve the SAME locked-proposition set? Same question for Chinese operators (DeepSeek + Claude-rendering-into-Chinese). Within-family agreement matrix.
- **Cross-FAMILY agreement**: does the proposition set preserved in Russian renderings match the set preserved in Chinese renderings? (Strongest SF3 evidence — cross-family preservation invariance regardless of operator)
- **Honest disclosure**: name any operator falling below ≥ 90% threshold + which propositions dropped + hypothesize translation-layer vs spine-extraction-layer cause
- **Methodological observation**: if Chinese topic-prominent syntax makes antecedent-edge extraction systematically harder than Russian, document as schema-refinement candidate (per user note: "If Session H notices systematic drift... that's a methodological finding worth documenting in the robustness analysis — not a falsifier of P4 but a refinement of the schema.")

## NEW spine node if Phase 3.5b executes

**PB_F8 cross-language multi-operator robustness** (cross-family preservation invariance evidence):
- Per-operator preservation rate across Russian + Chinese rendering operators
- Within-family agreement rate (intra-Slavic + intra-Sino-Tibetan)
- Cross-family preservation invariance rate (Slavic ∩ Sino-Tibetan preserved-proposition set / total locked propositions)
- Falsifier: cross-family agreement < 70% on locked propositions = SF3 cross-family robustness fails

Added to SPINE.yaml v0.4.1 if 3.5b lands at v1.1.0.

## Reviewer-defense framing (cross-family expansion)

Two reviewer objections 3.5b addresses:

1. **Operator-choice artifact**: "Your Russian-rendering preservation result may be an artifact of the particular rendering operator chosen. Show that the result holds across operators."
2. **Linguistic-proximity confound**: "Russian and English are both Indo-European; preservation may reflect linguistic proximity rather than the substrate-as-language-invariant claim. Show the result holds across maximally distant language families."

The defense (per user spec):

> "Cross-language preservation tested under N operators across 2 language families (Slavic: 1 human + K LLM operators rendering English→Russian; Sino-Tibetan: M LLM operators rendering English→Chinese). Within-family preservation rates: Russian mean X% (SD), Chinese mean Y% (SD). Cross-family preservation invariance: Z% of locked propositions preserved in BOTH Russian and Chinese renderings (regardless of operator). The cross-family result addresses the linguistic-proximity confound — preservation holds across maximally distant language families among well-resourced languages, not only within Indo-European."

This is the LLM-as-evaluator robustness pattern formalized in Chiang et al. (2023) "Can Large Language Models Be an Alternative to Human Evaluations?" and Zheng et al. (2023) "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" — applied here at the rendering-operator level rather than the evaluation-judge level, AND extended across language-family boundaries (Slavic + Sino-Tibetan) for cross-family-invariance evidence.

## v1.1.0 backlog placement (Session H stretch budget rule)

Per Session H init prompt:

> Stretch budget rule: execute ONLY if Phase 3.5a finishes with >2h remaining in Thu PM window; otherwise record as v1.1.0 backlog. Better clean v1.0.0 with human-rendering SF3 than partial v1.0.0 that slips Zenodo.

Phase 3.5a closed at the AI-draft + user-QC-handoff state (not human-native-rendering executed in Session H). The Session H budget cannot afford partial execution of 3.5b on top. **Phase 3.5b is marked v1.1.0 backlog**.

What Session H delivers under 3.5b:

- Protocol documented (this file).
- Operator subset selected and rationalized (YandexGPT + GigaChat + Claude Opus).
- Execution-ready script skeleton (audit/scripts/dr_phase3_5b_multi_llm_russian_robustness.py): per-operator render functions stubbed; BWS-injection pattern compatible with fleet convention; OAuth2 flow for GigaChat included; per-operator manifest written.
- BWS secret-name requirements documented (YANDEXGPT_API_KEY + YANDEXGPT_FOLDER_ID + GIGACHAT_AUTH + ANTHROPIC_API_KEY + OPENAI_API_KEY).
- Re-extraction + cross-operator preservation analysis sub-pipeline outlined.

What Session H does NOT deliver under 3.5b:

- Actual per-operator Russian renderings (API calls not fired; budget rule).
- Per-operator re-extracted spines.
- Cross-operator preservation matrix.
- Integration of cross-operator robustness evidence into paper.md.

## Cost estimate for v1.1.0 execution

- YandexGPT: ~$0.0005 per 1k chars × ~5k chars per rendering × 1 rendering = ~$0.0025 per pass
- GigaChat: free-tier OK for single-rendering size; or ~$0.0001 per token if billed
- Claude Opus: ~$15/M input + ~$75/M output × ~5k input + ~3k output = ~$0.30 per pass
- Total per execution pass: ~$0.31 (Claude dominates; one-shot)

Cost is not the constraint. Operator-attention budget for v1.1.0 user-QC of the human-native rendering (Phase 3.5a) + cross-operator analysis (3.5b) is the constraint.

## Integration into v1.0.0 paper.md

Phase 3.5b status disclosed in paper.md v1.0.0 §Discussion §Cross-language preservation (NEW subsection; co-located with Phase 3.5a disclosure) as: "Cross-operator robustness check via multi-LLM Russian rendering is documented in the v1.1.0 protocol (PHASE3_5B_MULTI_LLM_OPERATOR_PROTOCOL.md). The Russian rendering preservation result therefore awaits both (a) the v1.1.0 human-native Russian rendering pass and (b) the v1.1.0 multi-operator robustness check before being integrated into the published paper."

---

*Phase 3.5b closes with documented protocol + execution-ready script skeleton + v1.1.0 backlog placement. Session H prioritizes clean v1.0.0 ship over partial 3.5b execution; the multi-LLM cross-operator robustness evidence lands at v1.1.0 alongside the human-native Russian pass.*
