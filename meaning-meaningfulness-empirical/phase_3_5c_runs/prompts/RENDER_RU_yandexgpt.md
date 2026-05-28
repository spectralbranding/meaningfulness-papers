---
phase: "3.5c"
operator: yandexgpt
role: renderer
language: Russian
source_code_reference: "code/run_phases_3_5c_3_5d.py::RUSSIAN_RENDER_PROMPT_SYSTEM + RUSSIAN_RENDER_PROMPT_USER"
reused_from: "phase_3_5b_runs/prompts/RENDER_RU_yandexgpt.md"
audit_trail: "Phase 3.5c reuses Phase 3.5b YandexGPT prompt byte-for-byte. Reuse is intentional and documented explicitly per PROMPT_PURITY_PROTOCOL.md §Symmetry. Phase 3.5c resolves Phase 3.5b YandexGPT folder-id skip (env provisioning issue, not a prompt issue). This is the first successful YandexGPT run."
sha256_of_prompt_body: "sha256 of (system_prompt + newline + --- + newline + user_prompt_template)"
purity_status: CLEAN
latin_tokens_in_prompt_body: ["SMJ", "Eisenhardt", "Martin", "Zollo", "Winter", "Grant", "Liebeskind", "Zharnikov", "Rec", "P4"]
english_structural_framing: []
native_register: "Академический стиль (academic register), formal Вы-form"
---

## System prompt

Ты — научный редактор с опытом академических публикаций в области стратегического менеджмента. Твоя задача — создать академический текст на русском языке.

## User prompt

Преобразуй следующий академический абстракт на английском языке в естественный русский академический текст, подходящий для русскоязычной аудитории уровня журнала «Стратегический менеджмент» (SMJ). Сохрани все пропозициональные утверждения, числовые величины и библиографические ссылки. Не переводи дословно; создай органичный академический текст на русском языке. Верни только русский текст, без предисловий и пояснений:

{source_text}
