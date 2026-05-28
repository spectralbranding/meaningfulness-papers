# Ollama Serial-Only Discipline

**HARD RULE — feedback_ollama_serial_only.md**

**First introduced**: Phase 3.5d 2026-05-28 (Qwen3.6:27b first use)
**Formalized in L0 cascade**: v1.1.0 2026-05-28

---

## The Rule

All Ollama calls (local-model inference via `http://localhost:11434/api/generate`) must be invoked **strictly sequentially** — never in parallel.

API-based calls (OpenAI, Anthropic, DeepSeek, GigaChat, YandexGPT) may run concurrently with each other, but they must **not** run concurrently with any Ollama call.

## Why this rule exists

The local machine (fmini Apple M4 Pro 64GB unified memory) runs a single quantized 27B model (Qwen3.6:27b Q4_K_M) that saturates available GPU compute and memory bandwidth. Concurrent Ollama calls would either fail (out-of-memory if a second model is loaded) or contend for the same compute resources (thrashing), producing unreliable results. Serializing at the experiment-script level is the cleaner discipline regardless of whether GPU saturation actually occurs on any given run.

## Hardware context

- Machine: fmini (Apple M4 Pro 64GB unified memory)
- Model: qwen3.6:27b, quantization Q4_K_M
- Digest: `a50eda8ed977ab48a12431878896b27ffd5cef552c17af3317d9623b939a7f1e`
- Endpoint: `http://localhost:11434/api/generate`

## Implementation in Phase 3.5d

Phase 3.5d Ollama calls in execution order:

1. `render_with_qwen_zh_ollama` — Qwen3.6:27b renders Paper B abstract into Chinese
2. `extract_via_qwen_ollama` — Qwen3.6:27b extracts spine from DeepSeek's Chinese rendering (cross-extractor robustness)

Step 2 fires only after Step 1 completes. No concurrent Ollama invocations.

API-based calls (DeepSeek, Claude Opus, GPT-4o) run before the Ollama sequence and do not overlap with any Ollama call.

## Per-call timestamp record

The `phase_3_5d_runs/multi_llm_manifest.json::ollama_serial_discipline` block records:

```json
{
  "ollama_calls_in_phase_3_5d": [
    "render_with_qwen_zh_ollama (qwen3.6:27b @ digest a50eda8ed977)",
    "extract_via_qwen_ollama on DeepSeek's Chinese rendering (qwen3.6:27b)"
  ],
  "execution_order": "rendering -> cross-extractor extraction (sequential; no concurrent Ollama)"
}
```

JSONL logs at `logs/phase_3.5d_render_PB_abstract_ZH_qwen36_27b_ollama_calls.jsonl` and `logs/phase_3.5d_extract_spine_ZH_deepseek_via_qwen36_27b_calls.jsonl` record per-call timestamps confirming serialization.

## Scope

This rule applies to all current and future Ollama-served models in this research program. The constraint is methodological hygiene; it does not affect the validity of any preservation measurement, only elapsed wall-clock time.

---

*Source rule*: `feedback_ollama_serial_only.md` (HARD RULE; Phase 3.5d 2026-05-28)
*Companion document*: `PROMPT_PURITY_PROTOCOL.md` §Local-model serialization constraint
