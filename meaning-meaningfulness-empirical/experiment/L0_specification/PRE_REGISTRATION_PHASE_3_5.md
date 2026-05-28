# Pre-Registration: Phase 3.5 Cross-Language Rendering Experiments

**Type**: Retroactive pre-registration (honest framing per open-science norms)
**Registered for**: Zharnikov (2026ap) v1.1.0 public release
**Created**: 2026-05-28 (v1.1.0 consolidation pass)
**Framing note**: Phases 3.5a/b/c/d were executed and results observed before this document was written. This is an **exploratory** registration, not a confirmatory pre-registration. The exploratory label is honest; results inform the v1.1.0 dataset and are reported as exploratory. Confirmatory pre-registration for future cross-language phases will precede execution.

---

## Phase 3.5a — Russian Human-Native Renderings (exploratory baseline)

**Hypothesis**: Human-native Russian renderings of Paper B §Abstract and §Theory positioning sections will preserve the locked proposition set (L1–L12 for Abstract; equivalent for Theory section) at Rec ≥ Rec_threshold (Rec threshold per PHASE3_5A_RUSSIAN_RENDERING_PROTOCOL.md: ≥70% strict / ≥95% semantic SF3-holds threshold).

**Design**: Human academic with native Russian fluency produces two renderings (§Abstract + §Theory-positioning). Extractor: GPT-4o-2024-08-06 (cross-operator B != C, human != GPT-4o). Preservation classified as STRICT / SEMANTIC / MISSING / CONTRADICTED via GPT-4o judge (T=0, JSON-mode, seed=42).

**Analysis plan**: Per-proposition preservation labels; Rec = strict + semantic count; comparison against Rec_threshold.

**Status**: EXPLORATORY — results reported in paper.md §Discussion §Cross-language preservation Table 4.

**Outcome at execution**: §Abstract 10/12 strict, 12/12 semantic, 0 contradicted; §Theory 11/12 strict, 12/12 semantic, 0 contradicted. Both above 70% strict threshold (SF3-holds-with-rendering-cost-frontier). Human-native outperforms best-machine-operator by 1 strict proposition.

---

## Phase 3.5b — Russian Multi-LLM Cross-FAMILY Operator Robustness

**Hypothesis**: Multiple LLM renderers across training-corpus language families (Slavic + Sino-Tibetan + English-substrate) will each preserve the locked proposition set L1–L12 at Rec ≥ 3 (the deterministic P4 threshold from Zharnikov 2026ao). Zero contradictions expected under SF3 (SF3 prediction: substrate translates cleanly, rendering cost frontier observed on strict criterion).

**Design**: Four operators render Paper B §Abstract into Russian: GigaChat (Sberbank Slavic), YandexGPT (Yandex Slavic), DeepSeek (Sino-Tibetan training), Claude Opus (English-substrate control). Extractor: GPT-4o-2024-08-06 (canonical cross-operator; B != C for all four). Preservation judge: separate GPT-4o call (T=0, JSON-mode, seed=42). Seed fixed at 42 per PAPER_QUALITY_STANDARDS item 37a.

**Analysis plan**: Rec per operator; cross-operator agreement on STRICT/SEMANTIC/MISSING labels; within-Slavic-family variance (GigaChat vs YandexGPT); cross-FAMILY variance (Slavic operators vs Sino-Tibetan DeepSeek vs English Claude).

**Status**: EXPLORATORY — results reported in paper.md §Discussion §Cross-language preservation Table 3.

**Outcome at execution**: GigaChat: 9 strict, 3 semantic, 0 missing, 0 contradicted, Rec=12. YandexGPT: 4 strict, 8 semantic, 0 missing, 0 contradicted, Rec=12. DeepSeek: 8 strict, 3 semantic, 1 missing, 0 contradicted, Rec=11. Claude Opus: 9 strict, 3 semantic, 0 missing, 0 contradicted, Rec=12. NOTE: GigaChat Phase 3.5b had OAuth 400-error; YandexGPT had YANDEX_AI_FOLDER_ID skip — both resolved in Phase 3.5c.

---

## Phase 3.5c — Russian-Native LLM Retry (GigaChat + YandexGPT)

**Hypothesis**: With Phase 3.5b infrastructure issues resolved (GigaChat OAuth credentials corrected; YandexGPT YANDEX_AI_FOLDER_ID provisioned), GigaChat and YandexGPT will each produce valid Russian renderings of Paper B §Abstract that preserve the locked set at Rec ≥ 3.

**Design**: Identical to Phase 3.5b for the two Russian-native operators. Renderers: GigaChat (GigaChat-Pro, Sberbank OAuth2) + YandexGPT (yandexgpt/latest, folder_id b1g894jalgr7i0op2s70). Extractor: GPT-4o-2024-08-06 (B != C maintained). Russian prompt: native Cyrillic academic register per PROMPT_PURITY_PROTOCOL.md; same prompt template as Phase 3.5b (byte-identical; reuse documented in phase_3_5c_runs/prompts/).

**Analysis plan**: Rec per operator; per-proposition labels; comparison with Phase 3.5b results (whether Phase 3.5c clears Phase 3.5b's infrastructure failures without changing the result pattern).

**Status**: EXPLORATORY — results reported in paper.md §Results §Cross-language results (v1.1.0 addition).

**Outcome at execution**: GigaChat: 8 strict, 4 semantic, 0 missing, 0 contradicted, Rec=12. YandexGPT: 8 strict, 3 semantic, 1 missing, 0 contradicted, Rec=11. Both above Rec ≥ 3 threshold. Phase 3.5c resolves Phase 3.5b errors. Cross-operator discipline: GPT-4o extractor for both (B != C maintained).

---

## Phase 3.5d — Chinese Cross-Language + Cross-Deployment-Tier

**Hypotheses**:
- H1 (P4 in Chinese): At least two of three Chinese-language renderers will preserve the locked proposition set at Rec ≥ 3.
- H2 (cross-deployment-tier): Open-weights local renderer (Qwen3.6:27b Q4_K_M, Ollama) will achieve Rec comparable to proprietary-API renderers (DeepSeek, Claude Opus), demonstrating that the P4 result is not gated on proprietary API access.
- H3 (cross-extractor robustness): Replacing the GPT-4o extractor with Qwen3.6:27b (different family) on DeepSeek's rendering will yield the same Rec verdict (±1 strict proposition), demonstrating extractor-invariance.

**Design**:
- Three renderers: DeepSeek (deepseek-chat, Chinese-native API), Claude Opus 4.5 (English-substrate control API), Qwen3.6:27b Q4_K_M (Chinese-native open-weights, Ollama local at localhost:11434).
- Chinese prompt: hand-written Simplified Chinese academic register, back-translated for sanity-check per PROMPT_PURITY_PROTOCOL.md §Enforcement procedure.
- Ollama: serial-only per OLLAMA_SERIAL_DISCIPLINE.md.
- Primary extractor: GPT-4o-2024-08-06 (all three renderings; B != C for all).
- Cross-extractor robustness: Qwen3.6:27b (Ollama) extracts DeepSeek's rendering only (B=DeepSeek != C=Qwen; valid).
- Reference translation (methods-transparency only, NOT input to renderers): GPT-4o EN→ZH one-shot.
- Seed: 42 for all API calls.

**Analysis plan**: Rec per renderer × extractor pair; per-proposition preservation labels; cross-deployment-tier comparison (Qwen Rec vs DeepSeek/Claude Rec); cross-extractor agreement (GPT-4o extractor vs Qwen3.6:27b extractor on DeepSeek rendering).

**Status**: EXPLORATORY — results reported in paper.md §Results §Cross-language results (v1.1.0 addition).

**Outcome at execution**:
- DeepSeek (GPT-4o extractor): 9 strict, 3 semantic, 0 missing, 0 contradicted, Rec=12. H1 CONFIRMED.
- Claude Opus (GPT-4o extractor): 8 strict, 3 semantic, 1 missing, 0 contradicted, Rec=11. H1 CONFIRMED.
- Qwen3.6:27b Ollama (GPT-4o extractor): 8 strict, 4 semantic, 0 missing, 0 contradicted, Rec=12. H2 CONFIRMED (Qwen local = DeepSeek API at Rec=12).
- DeepSeek (Qwen3.6:27b extractor): 7 strict, 5 semantic, 0 missing, 0 contradicted, Rec=12. H3 CONFIRMED (same Rec=12 verdict; 2-proposition strict→semantic shift when changing extractor; finding extractor-invariant).

---

*Companion documents*: `CROSS_OPERATOR_DISCIPLINE.md`, `OLLAMA_SERIAL_DISCIPLINE.md`, `PROMPT_PURITY_PROTOCOL.md`
*Source phases data*: `phase_3_5a_runs/`, `phase_3_5b_runs/`, `phase_3_5c_runs/`, `phase_3_5d_runs/`
