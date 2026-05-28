# Cross-Phase Summary: Phase 3.5 Preservation Results

**Paper**: Zharnikov (2026ap) *Same Meaning, Different Prose*
**Version**: v1.1.0 (2026-05-28)
**Locked proposition set**: L1–L12 (Paper B §Abstract spine; 12 propositions)

---

## Hypothesis verdict table

| Phase | Renderer | Renderer Family | Extractor | Lang | Strict | Semantic | Missing | Contradicted | Rec | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 3.5a | Human (native) | Human | GPT-4o | RU | 10 | 2 | 0 | 0 | 12 | H: SF3 holds (rendering-cost frontier observed) |
| 3.5a | Human (theory) | Human | GPT-4o | RU | 11 | 1 | 0 | 0 | 12 | H: SF3 holds strongly |
| 3.5b | GigaChat | Slavic | GPT-4o | RU | 9 | 3 | 0 | 0 | 12 | H: P4 demonstrated |
| 3.5b | YandexGPT | Slavic | GPT-4o | RU | 4 | 8 | 0 | 0 | 12 | H: P4 demonstrated (strict-criterion operator-sensitive) |
| 3.5b | DeepSeek | Sino-Tibetan | GPT-4o | RU | 8 | 3 | 1 | 0 | 11 | H: P4 demonstrated |
| 3.5b | Claude Opus | Western | GPT-4o | RU | 9 | 3 | 0 | 0 | 12 | H: P4 demonstrated |
| 3.5c | GigaChat | Slavic | GPT-4o | RU | 8 | 4 | 0 | 0 | 12 | H: P4 demonstrated; resolves 3.5b OAuth error |
| 3.5c | YandexGPT | Slavic | GPT-4o | RU | 8 | 3 | 1 | 0 | 11 | H: P4 demonstrated; resolves 3.5b folder-id skip |
| 3.5d | DeepSeek | Sino-Tibetan | GPT-4o | ZH | 9 | 3 | 0 | 0 | 12 | H1+H2: P4 demonstrated in Chinese (proprietary API) |
| 3.5d | Claude Opus | Western | GPT-4o | ZH | 8 | 3 | 1 | 0 | 11 | H1: P4 demonstrated in Chinese (English-substrate control) |
| 3.5d | Qwen3.6:27b-Ollama | Sino-Tibetan | GPT-4o | ZH | 8 | 4 | 0 | 0 | 12 | H2: P4 demonstrated — open-weights local = proprietary API |
| 3.5d | DeepSeek (cross-extractor) | Sino-Tibetan | Qwen3.6:27b | ZH | 7 | 5 | 0 | 0 | 12 | H3: extractor-invariant — Rec=12 unchanged when extractor changes |

---

## Summary

- **All 12 cross-language renderings (3.5a/b/c/d combined) return Rec ≥ 11.**
- **Zero contradictions across all 12 renderings.**
- P4 is demonstrated across English (baseline), Russian (3.5a/b/c), and Chinese (3.5d) output languages.
- P4 is demonstrated across 6 renderer families: human native, Slavic LLM (GigaChat, YandexGPT), Sino-Tibetan (DeepSeek), Western English-substrate (Claude Opus), Chinese open-weights local (Qwen3.6:27b).
- P4 is demonstrated across 2 deployment tiers: proprietary API (DeepSeek, Claude Opus, GigaChat, YandexGPT) and open-weights local (Qwen3.6:27b Q4_K_M via Ollama on Apple M4 Pro).
- P4 is extractor-invariant: DeepSeek's Chinese rendering returns Rec=12 whether extracted by GPT-4o or Qwen3.6:27b.

## Null baseline

Random-graph null (Phase 1, v1.0.0): Pr(Rec ≥ 3 by chance) ≈ .000 across 1,000 size-matched shadows. All cross-language Rec values (Rec ≥ 11 on L1-L12) are far above the Rec ≥ 3 null threshold.

## Cross-operator B != C compliance

All Phase 3.5b/c/d runs comply with the cross-operator extraction discipline (CROSS_OPERATOR_DISCIPLINE.md). See per-phase manifests for per-run evidence.

---

*Source manifests*: `phase_3_5a_runs/task_gamma_human_rendering_manifest.json`, `phase_3_5b_runs/multi_llm_manifest.json`, `phase_3_5c_runs/multi_llm_manifest.json`, `phase_3_5d_runs/multi_llm_manifest.json`
