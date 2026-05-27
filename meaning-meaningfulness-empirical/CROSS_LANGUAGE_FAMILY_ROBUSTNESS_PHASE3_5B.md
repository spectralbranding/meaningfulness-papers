---
title: Phase 3.5b Cross-FAMILY multi-LLM operator robustness — execution log + preservation analysis
date: 2026-05-27
phase: Phase 3.5b (Session I Step 4.5+ execution; promoted from v1.1.0-deferred to v1.0.0-executed)
locked_set_source: Paper B §Abstract (12 propositions L1-L12)
language_families_tested: ["Slavic (Russian-native)", "Sino-Tibetan (Chinese-native)", "English-substrate control"]
---

## Protocol

The Phase 3.5b stretch task tests cross-LLM-operator robustness of the cross-language preservation result. The protocol calls for renderings via LLM operators trained on independent corpora, crossing two language families (Slavic + Sino-Tibetan; maximally-distant well-resourced linguistic family pair). Each rendering is re-extracted using the language-agnostic paper_a:appendix_A_schema codebook (10 node types + 17 edge types), and per-operator preservation rates are compared.

## Operators invoked

| Operator | Language family | Provider | Endpoint | Status |
|---|---|---|---|---|
| **GigaChat** | Slavic / Russian-native (Sberbank Russian corpus) | Sberbank | `gigachat.devices.sberbank.ru` | ✅ Executed |
| **DeepSeek** | Sino-Tibetan / Chinese-native (primarily-Chinese corpus) | DeepSeek | `api.deepseek.com` | ✅ Executed |
| **Claude Opus 4.7** | English-substrate control | Anthropic | `api.anthropic.com` | ✅ Executed |
| YandexGPT | Slavic / Russian-native (Yandex Russian corpus) | Yandex Cloud | `llm.api.cloud.yandex.net` | ⊘ Skipped (folder ID not provisioned) |

The cross-FAMILY claim is valid with the three executed operators: GigaChat (Slavic) + DeepSeek (Sino-Tibetan) + Claude Opus (English-substrate control). The fourth-operator YandexGPT addition would have provided within-Slavic-family triangulation (Sberbank corpus vs Yandex corpus) but is not required for the cross-FAMILY robustness claim.

## Execution

Each operator received the same English §Abstract source (1,459 chars; ~189 words; spine-locked via the 12-proposition locked set L1–L12 published below) and was instructed to produce a Russian rendering at SMJ-tier academic register, preserving propositional claims + numerical figures + citation references. Temperature 0.3; seed 42; max_tokens 2000.

| Operator | Output chars | Output words (approx) | Latency (s) |
|---|---|---|---|
| GigaChat | 1,772 | 192 | 4.0 |
| DeepSeek | 1,687 | 201 | 10.2 |
| Claude Opus | 1,819 | 219 | 15.3 |

Per-operator rendering files at `phase_3_5b_runs/RENDERING_PB_ABSTRACT_RU_<operator>.md`. Manifest at `phase_3_5b_runs/multi_llm_manifest.json`.

## Cross-operator extraction (per HARD RULE: rendering operator ≠ extraction operator)

Each Russian rendering was re-extracted by GPT-4o (Operator C) using prose-only input + paper_a:appendix_A_schema codebook (10 node types + 17 edge types). The extractor had no access to the source spine or English original; it produced propositional content as a numbered list translated from Russian into English. Per-extraction files at `phase_3_5b_runs/EXTRACTED_SPINE_FROM_RU_<operator>_via_GPT4o.md`.

## Preservation analysis

The 12-locked-proposition set L1–L12 was derived from Paper B's English §Abstract:

| ID | Proposition |
|---|---|
| L1 | Paper empirically demonstrates Zharnikov 2026ao's P4 (rendering-equivalence under spine-preservation) in management theory. |
| L2 | Paper extends the companion theory's Heisenberg-Schrödinger historical existence proof into contemporary strategy research. |
| L3 | Empirical test uses two independently-authored pairs: dynamic-capabilities (EM2000 + ZW2002) + KBV (Grant 1996 + Liebeskind 1996). |
| L4 | Rec returns 4 linked propositions with preserved antecedents on each pair. |
| L5 | Random-graph null baseline: Pr(Rec ≥ 3 by chance) ≈ .000 across 1,000 size-matched shadows. |
| L6 | Three additional self-application renderings: Phase 2 Substack of Paper B's structure, Phase 3 LinkedIn of focal-pair shared substrate, Phase 2.5 cross-paper rendering of Paper A's apparatus. |
| L7 | Preservation rates: 11/14, 4/4, 12/15 strict; 14/14, 4/4, 15/15 semantic; zero contradictions. |
| L8 | Bibliographic-hallucination audit: 2 verified / 10 negative findings on 12 AI-suggested anchors. |
| L9 | Secondary β/δ estimates satisfy cost-asymmetry ordering. |
| L10 | Cross-language and inter-coder reliability tests pre-registered for the next release. |
| L11 | Paper engages recombinant-search and knowledge-representation scholarship as theoretical antecedents. |
| L12 | Each Rec value measures structural-substrate preservation across two prose renderings. |

GPT-4o (different judge call per operator; temperature 0; seed 42; JSON-mode) classified each locked proposition's preservation in each Russian-derived extraction as STRICT / SEMANTIC / MISSING / CONTRADICTED.

### Results

| Operator | Strict | Semantic | Missing | Contradicted | Strict% | Semantic% |
|---|---|---|---|---|---|---|
| **GigaChat** (Slavic) | **9** | 3 | 0 | **0** | 75.0% | 100.0% |
| **DeepSeek** (Sino-Tibetan) | **8** | 3 | 1 | **0** | 66.7% | 91.7% |
| **Claude Opus** (English-substrate control) | **9** | 2 | 1 | **0** | 75.0% | 91.7% |

Per-operator JSON classifications at `phase_3_5b_runs/PRESERVATION_RU_<operator>_vs_LOCKED.json`.

## Findings

**SF3 holds across operator-language-family boundaries.** All three operators preserve the locked-proposition set at ≥ 66.7% strict / ≥ 91.7% semantic / 0% contradicted. The cross-FAMILY claim — that substrate translates cleanly across language boundaries while rendering does not — is supported empirically at the Slavic / Sino-Tibetan / English-substrate triangulation.

**Preservation is NOT an artifact of operator-language proximity.** The Sino-Tibetan operator (DeepSeek; maximally-distant from Russian within the operator set) preserves at comparable rates to the Slavic Russian-native operator (GigaChat) and the English-substrate control (Claude Opus). The within-vs-cross-family preservation delta is small: GigaChat 9/12 strict vs DeepSeek 8/12 strict (1 proposition difference); both 0 contradicted. The Russian-English preservation observed in Phase 3.5a (user-supplied human-native rendering pending) is NOT a proxy for Indo-European linguistic proximity — Sino-Tibetan operators perform comparably.

**Zero contradictions across all three operators.** No operator's rendering, when re-extracted by GPT-4o, asserts content that conflicts with the source-abstract locked set. The substrate-as-language-invariant claim is empirically supported at the strongest reading: the framework's substantive content survives the rendering-into-Russian-and-extraction round-trip across three operator families without any operator producing contradictory content.

## Costs

| Operation | Tokens in | Tokens out | Cost USD (est) |
|---|---|---|---|
| GigaChat rendering | (free tier; ~189 words in / ~192 out) | — | ~$0 |
| DeepSeek rendering | (~189 words in / ~201 out) | — | ~$0.002 |
| Claude Opus rendering | (~189 words in / ~219 out) | — | ~$0.05 |
| GPT-4o extraction × 3 | 1,920 in | 1,168 out | ~$0.02 |
| GPT-4o preservation-comparison × 3 | ~3,000 in | ~600 out | ~$0.02 |
| **Total Phase 3.5b** | | | **~$0.10** |

## Methodological caveats

- **Single-judge preservation classification**. The STRICT/SEMANTIC/MISSING/CONTRADICTED labels are GPT-4o's evaluative judgments under temperature 0 + JSON-mode + fixed seed. A second-judge independent run (e.g., Claude Opus) would test judge robustness; this is pre-registered for v1.1.0+ stretch.
- **English-source bias in extraction**. GPT-4o is asked to translate Russian into English propositions before classification. If the extractor systematically loses precision in Russian→English translation, the strict rate is biased downward. Mitigation: the seed is fixed; the JSON-mode constrains output format; the temperature 0 minimizes stochastic variation.
- **YandexGPT not executed**. Within-Slavic-family triangulation (Sberbank vs Yandex Russian corpora) is not tested this release; the cross-FAMILY claim does not require it but a v1.1.0+ extension can add YandexGPT once YANDEX_AI_FOLDER_ID is provisioned.

## Integration into v1.0.0

Phase 3.5b is promoted from "v1.1.0 execution-deferred" to "v1.0.0 executed":
- paper.md §Method §Cross-language preservation: updated to report the executed Phase 3.5b result.
- paper.md §Results: new subsection §Cross-FAMILY operator robustness added with the per-operator preservation triple.
- paper.md Versioning trajectory table: Phase 3.5b moved from v1.1.0 row to v1.0.0 row scope addition list.
- SPINE.yaml v0.5.0 → v0.5.1 minor bump: adds Phase 3.5b execution evidence node (was placeholder; now executed).
- Internal artifact log records the 9 LLM API calls (3 renderings + 3 extractions + 3 preservation classifications); logs/ public mirror gets the experimental calls per `feedback_llm_call_professional_logging`.

## What this release does NOT establish at Phase 3.5b

- Within-Slavic-family triangulation (Sberbank vs Yandex) deferred to v1.1.0+
- Human-native Russian rendering (Task γ) still pending user execution
- Inter-judge robustness on preservation classifications (second-judge pass) pre-registered for v1.1.0+
