# Prompt-Purity Protocol — Non-Native Language Contamination Discipline

**Companion to**: Zharnikov (2026ap) *Same Meaning, Different Prose* + Zharnikov (2026ao) *Spec-Based Research in the Post-AI Era*
**Status**: Active methodology for all multi-LLM rendering / extraction experiments in this research program
**First introduced**: 2026-05-28 (Paper B Phase 3.5c / 3.5d cross-language expansion)

---

## Why this protocol exists

The framework of Paper A (2026ao) treats Proposition P4 — rendering-equivalence under spine-preservation — as a structural preservation result. The empirical demonstration in Paper B (2026ap) tests whether two renderings of the same locked spine, produced by different operators, preserve the spine's typed-DAG structure at the level the recombination metric Rec detects.

If a prompt used to elicit a rendering is itself contaminated by content the renderer should be deriving from the spine, then the rendering is no longer a pure transformation of the locked spine into a target-language audience register — it is a transformation of the spine PLUS the prompt's leaked content. The preservation measurement that follows would therefore not test what the framework claims.

This protocol specifies the discipline that prevents that contamination at the prompt boundary.

---

## The hard rule

**Non-English prompts must be fully native, not mixed-language.**

This rule was established in the broader research program after an earlier mixed-language prompt incident, where mixed-language prompt templates (English structural framing inside what were nominally Russian-language prompts) produced renderings whose contamination signal was confounded with the perceptual signal the experiment was meant to measure.

The rule extends across every language used in this program: Russian, Chinese, and any future addition.

---

## What "clean from non-native language" means in practice

| Discipline | Russian example | Chinese example | English (as native baseline) |
|---|---|---|---|
| **No English structural framing in native-language prompt** | "Render the abstract" → "Создай аннотацию" | "Render the abstract" → "生成摘要" | n/a (native English prompt expected to be English) |
| **No English technical terms with native equivalents** | "spine" → "семантический остов"; "render" → "перевести в прозу"; "operator" → "оператор" (loanword permitted in Russian academic register) | "spine" → "结构骨架"; "render" → "渲染为散文"; "operator" → "操作者" | n/a |
| **No English register-marking words** | "academic register" → "академический регистр"; "audience" → "аудитория" | "academic register" → "学术语域"; "audience" → "读者群" | n/a |
| **No Latin-script tokens unless proper-noun convention** | OK to keep author names in Latin (Russian academic convention permits); replace inline "P4" with "P4 (Предложение 4)" or "четвёртое предложение" | OK to keep author names in Latin (per Chinese academic convention for non-Chinese authors); replace inline "P4" with "P4（命题4）" or "第四命题" | n/a |
| **No mixed-language section headers in the prompt** | "Format as: Abstract: …" → "Структура ответа: Аннотация: …" | "Format as: Abstract: …" → "回答结构：摘要：…" | n/a |
| **Native academic register conventions** | Formal "Вы"-form; preserve Russian academic abstract conventions | Simplified script default; 学术体 register; preserve Chinese academic abstract conventions | American academic English; sentence case in headings per AMA |

## What stays universal (and why English is correct there)

| Artifact | Why English is correct |
|---|---|
| The locked spine YAML (`SPINE.yaml`) | This is the SUBSTRATE being rendered. It stays identical across all phases (English node types: `observation`, `proposition`, `derivation`, …) so cross-phase Rec comparisons remain valid. Translating the spine itself would change the substrate identity. The locked spine is the experimental constant. |
| The extractor prompt (GPT-4o / Claude / Qwen-local) | The extractor receives target-language prose input and produces structured output in the spine's schema language (English node types). This is by-design schema invariance, not a translation step. |
| DOIs, ORCIDs, ISO codes, citation keys | Universally preserved in Latin per all academic conventions |
| Provenance metadata (timestamp, git_sha, model_version) | Machine-readable; English keyword convention preserved for tooling interoperability |

## What gets translated, by whom, and how

| Artifact | Translator | Quality check |
|---|---|---|
| Renderer prompt template (system + user prompts) | Hand-written in native target language by the experiment script (NOT auto-translated by an LLM at run-time — too risky for contamination) | Inspectable in the script source; reviewer can read the exact prompt byte-for-byte |
| The Chinese reference translation of the source English abstract (for the methods-section "translation sanity check" only — NOT input to renderers) | GPT-4o (one-shot translation) | Logged + included in the public mirror so reviewers can inspect |
| Any post-hoc clarification phrases | Hand-written in target language | Inspectable in script source |
| Back-translation verification (for languages where the author lacks native fluency, currently: Chinese) | A DIFFERENT model from both the renderer and the translator (e.g., Claude Opus or GPT-4o-mini back-translates Chinese → English; deliberate model-divergence so any back-translation introduces a model-different perturbation independent of the rendering pipeline) | Spot-checked by author against expected English meaning before any rendering call fires |

---

## Enforcement procedure (must be applied per phase, per language)

For each new non-English language introduced into the experimental pipeline, the following checklist is completed BEFORE any rendering call is invoked:

1. **Render prompt audit**: read the rendering prompt template token-by-token; verify no English structural framing, no Latin-script technical terms with native equivalents, no mixed-language section headers.
2. **Native register check**: verify formal-register conventions of the target language are observed (e.g., Russian formal "Вы"-form; Chinese 学术体).
3. **Latin-script-token audit**: enumerate every Latin-script token in the prompt; for each, confirm it is in the "stays universal" list (author names, DOIs, citation keys) or transliterate it to native script.
4. **Back-translation verification (for languages without on-team native fluency)**: a different model back-translates the prompt to English; the author spot-checks against expected English meaning.
5. **Certification snippet**: a brief one-paragraph certification is added to the phase manifest stating: language, Latin-script-token count and breakdown, English-technical-term count, native register confirmation, back-translation verification (if applicable). This becomes part of the experimental record.

If any audit step fails, the prompt is rewritten and re-audited before any rendering call is invoked.

---

## Per-language certification template (recorded in the phase manifest)

```yaml
prompt_purity_certification:
  phase: "3.5d"  # or "3.5c", etc.
  language: "Chinese (Simplified)"
  prompt_files:
    - "code/multi_llm_rendering.py::render_prompt_zh_v1"
  latin_script_tokens:
    total_count: 0  # excluding author-name proper nouns + DOIs
    breakdown:
      proper_nouns: ["Eisenhardt", "Martin", "Zollo", "Winter", "Grant", "Liebeskind"]
      DOIs: []  # not included in renderer prompt
      citation_keys: []  # not included in renderer prompt
      english_technical_terms: []  # MUST be empty
      english_structural_framing: []  # MUST be empty
  native_register: "学术体 (academic register), Simplified Chinese"
  native_register_confirmation: "Reviewed against academic Chinese abstract conventions; passes."
  back_translation:
    operator: "Claude Opus (different from renderer)"
    back_translation_text_path: "phase_3_5d_runs/PROMPT_BACK_TRANSLATION_zh_v1.md"
    author_spot_check: "PASSED on 2026-MM-DD; meaning preserved against expected English"
  certified_at: "2026-MM-DDThh:mm:ssZ"
  certified_by: "experiment author"
```

---

## Prompt publication discipline (HARD RULE 2026-05-28)

**Every prompt text used in any rendering, translation, back-translation, or extraction step of the experimental pipeline is published in the public repository of the paper as a standalone, inspectable file.**

The prompt text is the experimental treatment for P4 evidence. Reviewers and replicators inspect the prompt byte-for-byte to verify:
- That the prompt is native-clean per this protocol
- That the prompt does not leak source-spine content to the renderer
- That the extractor prompt does not leak source-spine content to the extractor
- That the back-translation prompt is task-isolated from the translation step

### File layout in the public mirror

For each phase, prompts are published in a `prompts/` subdirectory:

```
meaningfulness-papers/meaning-meaningfulness-empirical/
├── phase_3_5b_runs/
│   └── prompts/
│       ├── RENDER_RU_gigachat.md
│       ├── RENDER_RU_yandexgpt.md
│       ├── RENDER_RU_claude_opus.md
│       ├── RENDER_RU_deepseek.md
│       └── EXTRACT_FROM_RU_via_GPT4o.md
├── phase_3_5c_runs/
│   └── prompts/
│       ├── RENDER_RU_gigachat.md
│       ├── RENDER_RU_yandexgpt.md
│       └── EXTRACT_FROM_RU_via_GPT4o.md
└── phase_3_5d_runs/
    └── prompts/
        ├── RENDER_ZH_deepseek.md
        ├── RENDER_ZH_claude_opus.md
        ├── RENDER_ZH_qwen36_27b_ollama.md
        ├── EXTRACT_FROM_ZH_via_GPT4o.md
        ├── EXTRACT_FROM_ZH_via_qwen36_27b_ollama.md
        ├── TRANSLATE_EN_TO_ZH_via_GPT4o.md
        └── BACK_TRANSLATE_ZH_TO_EN_via_GPT4o.md
```

Per-file structure: a short YAML front-matter (phase, operator, role, language, source code reference, audit-trail comment), followed by the exact prompt text under a `## System prompt` and `## User prompt` heading. The prompt content is byte-identical to what the experiment script uses; the script reads from the same string constant or loads the same template file.

### Citation from paper.md

Paper B `paper.md` §Method §Cross-language extension cites the `prompts/` directory of each phase by the full GitHub URL of the public mirror. The URL is in the form:

```
https://github.com/spectralbranding/meaningfulness-papers/tree/main/meaning-meaningfulness-empirical/phase_3_5d_runs/prompts
```

This satisfies `the transparency-docs-must-be-public rule` HARD RULE: every academically-required transparency artifact cited by name in paper.md is reachable from the public mirror via a working GitHub URL.

### Symmetry across phases

If a Phase 3.5b prompt was reused without modification in Phase 3.5c (e.g., the GigaChat Russian rendering prompt), the Phase 3.5c file SAYS so explicitly in its YAML front-matter (`reused_from: phase_3_5b_runs/prompts/RENDER_RU_gigachat.md`) and contains the byte-identical prompt text. This is intentional duplication, not silent reuse. The duplication keeps each phase's `prompts/` directory self-contained for reviewer inspection.

### What this rule does NOT require publishing

- API key values, OAuth client IDs, folder IDs, or any other credential: REDACTED before publication. The `llm_call_logger.py` redaction discipline applies at publish time as well as at log-write time.
- Provider-side internal request IDs (if confidential by provider TOS): may be omitted from public files; retained in internal JSONL logs.
- Internal debugging notes added during development: NOT published (the published prompt text matches the prompt used in the final reported run).

### Enforcement

Each phase's `multi_llm_manifest.json` includes a `prompts_publication` field that lists every published prompt file with SHA-256 of the prompt-text bytes, the operator that used it, and the role. A pre-commit hook verifies the SHA against the published file when the public mirror is updated.

---

## How this protocol is published

Per `the transparency-docs-must-be-public rule` HARD RULE, this document is included in the public mirror of Paper B (`meaningfulness-papers/meaning-meaningfulness-empirical/PROMPT_PURITY_PROTOCOL.md`) and cited from `paper.md` Methods (§Cross-language extension) by full GitHub URL. Reviewers and replicators can inspect the prompt-purity discipline as part of the experimental record.

Each phase's certification snippet (template above) is recorded in the phase's `*_manifest.json` and is therefore inspectable alongside the rendering and extraction outputs.

---

## Local-model serialization constraint (Ollama)

When local models are invoked via Ollama on shared single-GPU hardware (e.g., fmini Apple M4 Pro), all Ollama calls must be invoked strictly sequentially — never in parallel.

Reason: a single quantized 27B-30B model loaded in unified memory saturates the available GPU compute and memory bandwidth; concurrent Ollama invocations would either fail (out-of-memory if loading a second model) or contend for the same compute resources (thrashing). Even when only one model is in use, parallel inference requests still serialize at the GPU level, so true parallelism is not achievable; serializing at the experiment-script level is the cleaner discipline.

Concretely:

- All steps that use an Ollama-served model run one-at-a-time, in sequence, in the experiment script. The script must enforce this with a per-Ollama-call lock or with serial top-level loops over Ollama steps.
- API-based calls (Anthropic, OpenAI, DeepSeek, GigaChat, YandexGPT) may still run concurrently with each other where the script supports it, but they may NOT run concurrently with an Ollama call (the local machine's resources are needed for Ollama).
- The Ollama call sequence is recorded in the phase manifest with per-call start/end timestamps to make the serialization explicit in the experimental record.

This constraint is methodological hygiene, not a methodology claim — it does not affect the validity of any preservation measurement, only the elapsed wall-clock time of the experiment.

---

## Cross-references

- Source rule: native-language prompt discipline (HARD RULE; established after an earlier mixed-language prompt incident)
- Cross-operator extraction discipline: `the cross-operator extraction separation rule` (HARD RULE; the B ≠ C rule for renderer vs extractor)
- LLM-call professional logging: `the LLM-call professional-logging discipline` (HARD RULE; the JSONL schema all calls land in)
- Transparency-doc publication: `the transparency-docs-must-be-public rule` (HARD RULE; this document is included per that rule)
- Paper B Methods §Cross-language extension (cites this document by GitHub URL)
