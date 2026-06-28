---
phase: "3.5d"
operator: qwen3.6:27b-ollama
role: renderer
language: Chinese (Simplified) — Chinese-native open-weights renderer
source_code_reference: "code/run_phases_3_5c_3_5d.py::CHINESE_RENDER_PROMPT_SYSTEM + CHINESE_RENDER_PROMPT_USER + /no_think directive"
promoted_from: "phase_3_5d_runs/PROMPT_TEMPLATE_zh_v1.md"
reused_from: "phase_3_5d_runs/prompts/RENDER_ZH_deepseek.md (core prompt body byte-identical)"
audit_trail: "Qwen3.6:27b is the Chinese-native open-weights renderer. Same core prompt as DeepSeek/Claude. Note: Qwen3.6 is a thinking model; '/no_think' directive + 'think:false' option prepended to system prompt to disable reasoning tokens and route all tokens to the final response."
sha256_of_prompt_body: "see RENDER_ZH_deepseek.md (core body byte-identical; Ollama prepends /no_think to system)"
purity_status: CLEAN
latin_tokens_in_prompt_body: ["SMJ"]
english_structural_framing: []
native_register: "学术体 (academic register), Simplified Chinese"
back_translation_path: "phase_3_5d_runs/PROMPT_BACK_TRANSLATION_zh_v1.md"
ollama_discipline: "Serial-only per the Ollama serial-only rule; num_predict=8000; seed=42; think=false"
model_digest: "a50eda8ed977ab48a12431878896b27ffd5cef552c17af3317d9623b939a7f1e"
quantization: "Q4_K_M"
---

## System prompt

/no_think

您是一位专注于战略管理领域的学术编辑，具备在中文核心期刊发表论文的丰富经验。请以规范的中文学术语域撰写。

## User prompt

请将以下英文学术摘要改写为适合中文学术读者（以《战略管理杂志》SMJ水平为参照）的自然流畅的中文摘要。要求：保留所有命题陈述、数值结果和文献引用；不要逐字翻译，而是创作符合中文学术写作规范的摘要；仅返回中文文本，不附加任何前言或说明。

{source_text}
