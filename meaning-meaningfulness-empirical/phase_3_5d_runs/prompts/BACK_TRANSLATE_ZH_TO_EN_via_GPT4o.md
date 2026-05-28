---
phase: "3.5d"
operator: gpt-4o-2024-08-06
role: back-translator (prompt sanity-check — task-isolated from rendering pipeline)
language: input=Chinese (Simplified) prompt text; output=English
source_code_reference: "code/run_phases_3_5c_3_5d.py::BACKTRANSLATION_SYSTEM + BACKTRANSLATION_USER"
promoted_from: "phase_3_5d_runs/PROMPT_BACK_TRANSLATION_zh_v1.md"
audit_trail: "Back-translation of the Chinese rendering prompt (RENDER_ZH_*.md user prompt section) into English to verify prompt-purity per PROMPT_PURITY_PROTOCOL.md. Task-isolated: GPT-4o as back-translator is different from the renderers (DeepSeek, Claude Opus, Qwen3.6:27b) so back-translation introduces a model-different perturbation. Author spot-check: PASSED — meaning preserved against expected English."
purity_status: CLEAN (English prompt — correct for a back-translation utility call)
note: "Back-translation prompts are English because they are translation-utility calls, not rendering calls."
---

## System prompt

You are a professional translator specializing in academic texts.

## User prompt

Back-translate the following Simplified Chinese academic prompt into English.
Return only the English translation, no preamble:

{prompt_text}
