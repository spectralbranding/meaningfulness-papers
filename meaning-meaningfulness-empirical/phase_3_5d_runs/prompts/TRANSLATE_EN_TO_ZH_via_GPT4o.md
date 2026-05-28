---
phase: "3.5d"
operator: gpt-4o-2024-08-06
role: translator (reference only — NOT input to renderers)
language: input=English; output=Chinese (Simplified)
source_code_reference: "code/run_phases_3_5c_3_5d.py::TRANSLATION_SYSTEM + TRANSLATION_USER"
promoted_from: "phase_3_5d_runs/TRANSLATION_REFERENCE_zh_v1.md"
audit_trail: "This translation is a sanity-check / methods-transparency artifact only. It is NOT used as input to any Chinese renderer. Per PROMPT_PURITY_PROTOCOL.md: renderers receive the original English source text directly (not via a pre-translated version). The translation is produced for reviewer inspection."
sha256_of_prompt_body: "computed from (system_prompt + newline + --- + newline + user_prompt_template).encode('utf-8')"
purity_status: CLEAN (English prompt — correct for a translation utility call)
note: "English prompts are appropriate here because this is a translation utility, not a rendering call. The prompt-purity rule applies to rendering prompts, not to translation-reference calls."
---

## System prompt

You are a professional translator specializing in management science.

## User prompt

Translate the following English academic abstract into Simplified Chinese.
Preserve all technical terms, citations, and numerical values.
Return only the Chinese translation, no preamble:

{source_text}
