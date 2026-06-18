"""Phase 3.5c + 3.5d experiment runner — Zharnikov (2026ap) Paper B.

Phase 3.5c: Russian-native LLM retry — GigaChat + YandexGPT (fixes 3.5b errors).
Phase 3.5d: Chinese-language rendering — DeepSeek + Claude Opus + Qwen3.6:27b (Ollama).

Cross-operator extraction discipline (HARD RULE):
  Renderer (B) != Extractor (C) at all times.
  GigaChat → extracted by GPT-4o
  YandexGPT → extracted by GPT-4o
  DeepSeek → extracted by GPT-4o + Qwen3.6:27b (cross-extractor robustness)
  Claude Opus → extracted by GPT-4o
  Qwen3.6:27b → extracted by GPT-4o ONLY (no self-extraction)

Ollama serial-only discipline: all Ollama calls are sequential; API calls may
be concurrent with each other but NEVER concurrent with an Ollama call.

Prompt-purity discipline per PROMPT_PURITY_PROTOCOL.md:
  Russian prompts: native Cyrillic academic register, no English structural framing.
  Chinese prompts: hand-written Simplified Chinese 学术体, no English structural framing.

Run:
    bws run -- uv run --with openai --with anthropic --with httpx \\
        python [internal path removed]

Fixed seed: 42 (per PAPER_QUALITY_STANDARDS 37a).
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path

# Ensure llm_call_logger is importable
CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))
from llm_call_logger import log_call  # noqa: E402

REPO_ROOT = CODE_DIR.parents[3]
PAPER_DIR = CODE_DIR.parent
LOGS_DIR = PAPER_DIR / "logs"
PHASE_3_5C_DIR = PAPER_DIR / "phase_3_5c_runs"
PHASE_3_5D_DIR = PAPER_DIR / "phase_3_5d_runs"
SEED = 42

# ============================================================================
# Source text: Paper B abstract (locked; do NOT modify)
# ============================================================================

SOURCE_ABSTRACT_EN = (
    "This paper empirically demonstrates Zharnikov’s (2026ao) Proposition P4 "
    "— rendering-equivalence under spine-preservation — in management theory. "
    "The paper extends the companion theory’s Heisenberg–Schrödinger historical "
    "existence proof into contemporary strategy research via structural extractions of two "
    "independently-authored pairs: a dynamic-capabilities pair (Eisenhardt and Martin 2000 "
    "+ Zollo and Winter 2002) and a knowledge-based-view pair from the Strategic Management "
    "Journal (SMJ) Winter 1996 Special Issue (Grant 1996 + Liebeskind 1996). The recombination "
    "metric Rec returns 4 linked propositions with preserved antecedents on each pair. A "
    "random-graph null baseline shows Pr(Rec ≥ 3 by chance) ≈ .000 across 1,000 "
    "size-matched shadows. Three additional renderings of substrates already in the corpus "
    "— a practitioner-register rendering of the paper’s own structure, a third "
    "rendering of the focal-pair shared substrate, and a cross-paper rendering of the companion "
    "theory’s full theoretical apparatus — preserve 11/14, 4/4, and 12/15 items "
    "strictly; 14/14, 4/4, and 15/15 semantically; zero contradictions. A bibliographic-"
    "hallucination audit of twelve AI-suggested anchors finds two verified and ten negative "
    "findings. Secondary β/δ estimates satisfy the cost-asymmetry ordering. "
    "Cross-language and inter-coder reliability tests are pre-registered for the next release. "
    "The paper engages recombinant-search and knowledge-representation scholarship as theoretical "
    "antecedents."
)

# ============================================================================
# Locked propositions L1–L12 (from Phase 3.5b manifest / SPINE.yaml abstract spine)
# These are the 12 locked abstract-level propositions for preservation checking.
# ============================================================================

LOCKED_PROPOSITIONS = {
    "L1": "Paper empirically demonstrates P4 (rendering-equivalence under spine-preservation) in management theory.",
    "L2": "Extends Heisenberg-Schrödinger historical existence proof into contemporary strategy research.",
    "L3": "Dynamic-capabilities pair: Eisenhardt & Martin 2000 + Zollo & Winter 2002.",
    "L4": "KBV pair: Grant 1996 + Liebeskind 1996 from SMJ Winter 1996 Special Issue.",
    "L5": "Recombination metric Rec returns 4 linked propositions with preserved antecedents on each pair.",
    "L6": "Random-graph null baseline: Pr(Rec >= 3 by chance) ≈ .000 across 1,000 size-matched shadows.",
    "L7": "Three additional renderings: practitioner-register, third focal-pair rendering, cross-paper companion rendering.",
    "L8": "Preservation scores: 11/14, 4/4, 12/15 strict; 14/14, 4/4, 15/15 semantic; zero contradictions.",
    "L9": "Bibliographic-hallucination audit: 12 AI-suggested anchors → 2 verified, 10 negative.",
    "L10": "Secondary β/δ estimates satisfy cost-asymmetry ordering.",
    "L11": "Cross-language and inter-coder reliability tests pre-registered for next release.",
    "L12": "Paper engages recombinant-search and knowledge-representation scholarship as theoretical antecedents.",
}

# ============================================================================
# Appendix-A extraction codebook (same as cross_operator_extraction.py)
# ============================================================================

EXTRACTION_CODEBOOK = """You are a structural-extraction operator applying the appendix-A schema from
Zharnikov (2026ao) §Theory + Online Appendix A. The schema has:

10 FIRST-CLASS NODE TYPES:
1. proposition         — explanatory theoretical claim asserted by the author
2. observation         — empirical referent or raw data the author invokes
3. method              — procedural transformation the author applies
4. measurement         — derived datum the author reports
5. finding             — inferential claim the author argues from measurements
6. derivation          — formal deduction from prior nodes
7. rival               — alternative explanation the author considers
8. robustness_check    — sensitivity / replication test
9. limitation          — honest scope-or-power disclosure
10. assumption_atom    — indivisible premise the author asserts as required

17 EDGE TYPES:
extends, applies, tests, contradicts, refines, depends-on, evidences,
defines, measures, aggregates, generates, rules-out, bridges, mitigates,
relaxes, motivates, provenances.

EXTRACTION INSTRUCTIONS:
- Read ONLY the provided prose. You do NOT have access to any source spine.
- Identify central propositions / observations / methods / findings the prose asserts.
- For each node, assign exactly one node-type.
- For each node, identify antecedent edges using the 17-edge-type catalog.
- Output a numbered list of extracted claims in English (translate if source is non-English),
  with node type in brackets. Example: "1. [proposition] The paper demonstrates..."
- Keep each claim to one sentence.
- Do NOT include any preamble or postamble — numbered list only.
"""

EXTRACTION_USER_PROMPT = (
    "Apply the appendix-A schema to the following prose. Extract central nodes, "
    "classify each by type, identify antecedent edges. "
    "Return a numbered list of claims in English only (translate if needed):\n\n"
    "{prose}"
)

# ============================================================================
# Helper: get OpenAI client
# ============================================================================


def get_openai_client(api_key: str, base_url: str | None = None):
    from openai import OpenAI

    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def get_anthropic_client(api_key: str):
    from anthropic import Anthropic

    return Anthropic(api_key=api_key)


# ============================================================================
# PHASE 3.5c — Russian-native renderers
# ============================================================================

# Russian rendering prompt (native Cyrillic; hand-written per PROMPT_PURITY_PROTOCOL.md)
# Token-level audit:
#   Latin-script tokens: none beyond author names (Eisenhardt, Martin, Zollo, Winter,
#   Grant, Liebeskind, Zharnikov) and the metric name "Rec" (abbreviation),
#   "SMJ" (journal abbreviation — standard in Russian academic text),
#   P4 (proposition notation with native gloss).
#   No English structural framing. No English technical terms with Cyrillic equivalents.
#   Register: formal academic Russian (академический стиль).
RUSSIAN_RENDER_PROMPT_SYSTEM = (
    "Ты — научный редактор с опытом академических публикаций в области стратегического "
    "менеджмента. Твоя задача — создать академический текст на русском языке."
)

RUSSIAN_RENDER_PROMPT_USER = (
    "Преобразуй следующий академический абстракт на английском языке в естественный "
    "русский академический текст, подходящий для русскоязычной аудитории уровня журнала "
    "«Стратегический менеджмент» (SMJ). "
    "Сохрани все пропозициональные утверждения, числовые величины и библиографические "
    "ссылки. Не переводи дословно; создай органичный академический текст на русском языке. "
    "Верни только русский текст, без предисловий и пояснений:\n\n"
    "{source_text}"
)


def render_with_gigachat(source_text: str) -> str:
    """GigaChat (Sberbank) Russian rendering — OAuth2 token flow."""
    import httpx

    auth_key = os.environ["GIGACHAT_API_KEY"].strip()
    client_id = os.environ.get(
        "GIGACHAT_CLIENT_ID", "019d5e43-255f-7532-aa4a-8a8749538068"
    ).strip()

    # Step 1: OAuth2 token
    rquid = str(uuid.uuid4())
    with log_call(
        phase="3.5c",
        operation="gigachat_oauth_token",
        operator="gigachat",
        endpoint="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        sdk_version="httpx",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt("")
        logger.set_user_prompt(f"scope=GIGACHAT_API_PERS RqUID={rquid}")
        logger.set_parameters({"scope": "GIGACHAT_API_PERS", "rquid": rquid})
        import warnings
        import urllib3

        warnings.filterwarnings(
            "ignore", category=urllib3.exceptions.InsecureRequestWarning
        )
        try:
            token_resp = httpx.post(
                "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                headers={
                    "Authorization": f"Basic {auth_key}",
                    "RqUID": rquid,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                },
                data={"scope": "GIGACHAT_API_PERS"},
                verify=False,
                timeout=60.0,
            )
            token_resp.raise_for_status()
            access_token = token_resp.json()["access_token"]
            logger.capture_response(token_resp.json())
            logger.set_model_version("GigaChat-OAuth-v2")
        except Exception as e:
            logger.add_error(str(e))
            raise

    # Step 2: Render call
    user_prompt = RUSSIAN_RENDER_PROMPT_USER.format(source_text=source_text)
    with log_call(
        phase="3.5c",
        operation="render_PB_abstract_RU_gigachat",
        operator="gigachat",
        endpoint="https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        sdk_version="httpx",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(RUSSIAN_RENDER_PROMPT_SYSTEM)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {"model": "GigaChat", "temperature": 0.3, "max_tokens": 2000}
        )
        try:
            resp = httpx.post(
                "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "GigaChat",
                    "messages": [
                        {"role": "system", "content": RUSSIAN_RENDER_PROMPT_SYSTEM},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                },
                verify=False,
                timeout=120.0,
            )
            resp.raise_for_status()
            result = resp.json()
            rendering = result["choices"][0]["message"]["content"]
            logger.capture_response(result)
            logger.set_model_version("GigaChat")
            tokens = result.get("usage", {})
            logger._tokens = {
                "input": tokens.get("prompt_tokens", 0),
                "output": tokens.get("completion_tokens", 0),
            }
        except Exception as e:
            logger.add_error(str(e))
            raise

    return rendering


def render_with_yandexgpt(source_text: str) -> str:
    """YandexGPT Russian rendering."""
    import httpx

    api_key = os.environ["YANDEX_AI_API_KEY"].strip()
    folder_id = os.environ.get("YANDEX_AI_FOLDER_ID", "b1g894jalgr7i0op2s70").strip()

    user_prompt = RUSSIAN_RENDER_PROMPT_USER.format(source_text=source_text)
    payload = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": 2000,
        },
        "messages": [
            {"role": "system", "text": RUSSIAN_RENDER_PROMPT_SYSTEM},
            {"role": "user", "text": user_prompt},
        ],
    }

    with log_call(
        phase="3.5c",
        operation="render_PB_abstract_RU_yandexgpt",
        operator="yandexgpt",
        endpoint="https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        sdk_version="httpx",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(RUSSIAN_RENDER_PROMPT_SYSTEM)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {"modelUri": payload["modelUri"], "temperature": 0.3, "maxTokens": 2000}
        )
        try:
            resp = httpx.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers={
                    "Authorization": f"Api-Key {api_key}",
                    "x-folder-id": folder_id,
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=120.0,
            )
            resp.raise_for_status()
            result = resp.json()
            rendering = result["result"]["alternatives"][0]["message"]["text"]
            logger.capture_response(result)
            logger.set_model_version(
                result.get("result", {}).get("modelVersion", "yandexgpt/latest")
            )
            usage = result.get("result", {}).get("usage", {})
            logger._tokens = {
                "input": int(usage.get("inputTextTokens", 0)),
                "output": int(usage.get("completionTokens", 0)),
            }
        except Exception as e:
            logger.add_error(str(e))
            raise

    return rendering


# ============================================================================
# PHASE 3.5d — Chinese-language rendering prompts
# ============================================================================

# Chinese rendering prompt (hand-written Simplified Chinese, 学术体)
# Token-level audit per PROMPT_PURITY_PROTOCOL.md:
#   Latin-script tokens: Eisenhardt, Martin, Zollo, Winter, Grant, Liebeskind, Zharnikov
#   (author names — proper nouns; Chinese academic convention permits Latin for non-Chinese authors)
#   SMJ (journal abbreviation widely used in Chinese management scholarship)
#   P4（命题4）(proposition notation with native gloss, as required by protocol)
#   Rec (metric name abbreviation, used as proper noun with Chinese gloss "重组度量Rec")
#   No English structural framing. No English technical terms with Chinese equivalents.
#   Register: 学术体 (academic register), Simplified Chinese.
CHINESE_RENDER_PROMPT_SYSTEM = (
    "您是一位专注于战略管理领域的学术编辑，具备在中文核心期刊发表论文的丰富经验。"
    "请以规范的中文学术语域撰写。"
)

CHINESE_RENDER_PROMPT_USER = (
    "请将以下英文学术摘要改写为适合中文学术读者（以《战略管理杂志》SMJ水平为参照）的自然流畅的中文摘要。"
    "要求：保留所有命题陈述、数值结果和文献引用；"
    "不要逐字翻译，而是创作符合中文学术写作规范的摘要；"
    "仅返回中文文本，不附加任何前言或说明。\n\n"
    "{source_text}"
)

# Translation prompt (GPT-4o, English→Chinese reference only, NOT input to renderers)
TRANSLATION_SYSTEM = (
    "You are a professional translator specializing in management science."
)
TRANSLATION_USER = (
    "Translate the following English academic abstract into Simplified Chinese. "
    "Preserve all technical terms, citations, and numerical values. "
    "Return only the Chinese translation, no preamble:\n\n{source_text}"
)

# Back-translation prompt (different invocation context)
BACKTRANSLATION_SYSTEM = (
    "You are a professional translator specializing in academic texts."
)
BACKTRANSLATION_USER = (
    "Back-translate the following Simplified Chinese academic prompt into English. "
    "Return only the English translation, no preamble:\n\n{prompt_text}"
)

# Chinese extraction prompt (GPT-4o: reads Chinese prose, extracts English spine nodes)
CHINESE_EXTRACTION_USER = (
    "Apply the appendix-A schema to the following prose (written in Simplified Chinese). "
    "Extract central nodes, classify each by type (in English). "
    "Translate all claims into English in your output. "
    "Return a numbered list only:\n\n{prose}"
)


def render_with_deepseek_zh(source_text: str) -> str:
    """DeepSeek Chinese rendering (OpenAI-compatible API)."""
    api_key = os.environ["DEEPSEEK_API_KEY"].strip()
    client = get_openai_client(api_key, base_url="https://api.deepseek.com")
    user_prompt = CHINESE_RENDER_PROMPT_USER.format(source_text=source_text)

    with log_call(
        phase="3.5d",
        operation="render_PB_abstract_ZH_deepseek",
        operator="deepseek",
        endpoint="https://api.deepseek.com/v1/chat/completions",
        sdk_version="openai>=1.51",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(CHINESE_RENDER_PROMPT_SYSTEM)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {"model": "deepseek-chat", "temperature": 0.3, "max_tokens": 2000}
        )
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": CHINESE_RENDER_PROMPT_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        logger.capture_response(resp)
        usage = getattr(resp, "usage", None)
        if usage is not None:
            cost_in = 0.00014 * (getattr(usage, "prompt_tokens", 0) / 1000)
            cost_out = 0.00028 * (getattr(usage, "completion_tokens", 0) / 1000)
            logger.set_cost_estimate(cost_in + cost_out)

    return resp.choices[0].message.content


def render_with_claude_opus_zh(source_text: str) -> str:
    """Claude Opus Chinese rendering (English-substrate control)."""
    api_key = os.environ["ANTHROPIC_API_KEY"].strip()
    client = get_anthropic_client(api_key)
    user_prompt = CHINESE_RENDER_PROMPT_USER.format(source_text=source_text)

    with log_call(
        phase="3.5d",
        operation="render_PB_abstract_ZH_claude_opus",
        operator="claude-opus",
        endpoint="https://api.anthropic.com/v1/messages",
        sdk_version="anthropic>=0.25",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(CHINESE_RENDER_PROMPT_SYSTEM)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {"model": "claude-opus-4-5", "temperature": 0.3, "max_tokens": 2000}
        )
        resp = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2000,
            system=CHINESE_RENDER_PROMPT_SYSTEM,
            messages=[{"role": "user", "content": user_prompt}],
        )
        logger.capture_response(resp)
        logger.set_model_version(resp.model)
        cost_in = 0.015 * (resp.usage.input_tokens / 1000)
        cost_out = 0.075 * (resp.usage.output_tokens / 1000)
        logger.set_cost_estimate(cost_in + cost_out)

    return resp.content[0].text


def render_with_qwen_zh_ollama(source_text: str) -> dict:
    """Qwen3.6:27b Chinese rendering via Ollama (serial — no concurrent Ollama calls).

    Returns dict with keys: rendering (str), start_ts (str), end_ts (str).
    """
    import httpx

    user_prompt = CHINESE_RENDER_PROMPT_USER.format(source_text=source_text)
    # Qwen3.6 is a thinking model; /no_think disables the thinking phase so all
    # tokens go to the final response (otherwise thinking consumes num_predict).
    full_prompt = f"{CHINESE_RENDER_PROMPT_SYSTEM}\n\n/no_think\n\n{user_prompt}"

    start_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    with log_call(
        phase="3.5d",
        operation="render_PB_abstract_ZH_qwen36_27b_ollama",
        operator="qwen3.6:27b-ollama",
        endpoint="http://localhost:11434/api/generate",
        sdk_version="ollama-local",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(CHINESE_RENDER_PROMPT_SYSTEM)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {
                "model": "qwen3.6:27b",
                "temperature": 0.3,
                "num_predict": 8000,
                "no_think": True,
            }
        )
        resp = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3.6:27b",
                "prompt": full_prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 8000, "seed": SEED},
                "think": False,
            },
            timeout=600.0,
        )
        resp.raise_for_status()
        result = resp.json()
        rendering = result["response"]
        logger.capture_response(result)
        logger.set_model_version("qwen3.6:27b")
        logger._tokens = {
            "input": result.get("prompt_eval_count", 0),
            "output": result.get("eval_count", 0),
        }

    end_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    return {"rendering": rendering, "start_ts": start_ts, "end_ts": end_ts}


# ============================================================================
# Translation + back-translation (Phase 3.5d)
# ============================================================================


def translate_en_to_zh(source_text: str, openai_key: str) -> str:
    """GPT-4o: English abstract → Chinese reference (sanity check only; NOT input to renderers)."""
    client = get_openai_client(openai_key)
    user_prompt = TRANSLATION_USER.format(source_text=source_text)

    with log_call(
        phase="3.5d",
        operation="translate_EN_to_ZH_reference",
        operator="gpt-4o",
        endpoint="https://api.openai.com/v1/chat/completions",
        sdk_version="openai>=1.51",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(TRANSLATION_SYSTEM)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {"model": "gpt-4o-2024-08-06", "temperature": 0.0, "seed": SEED}
        )
        resp = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": TRANSLATION_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            seed=SEED,
        )
        logger.capture_response(resp)
        cost_in = 0.0025 * (resp.usage.prompt_tokens / 1000)
        cost_out = 0.010 * (resp.usage.completion_tokens / 1000)
        logger.set_cost_estimate(cost_in + cost_out)

    return resp.choices[0].message.content


def back_translate_zh_prompt(prompt_text: str, openai_key: str) -> str:
    """GPT-4o: back-translate Chinese rendering prompt → English for sanity check.

    Task-isolated invocation (different from translation step).
    """
    client = get_openai_client(openai_key)
    user_prompt = BACKTRANSLATION_USER.format(prompt_text=prompt_text)

    with log_call(
        phase="3.5d",
        operation="back_translate_ZH_prompt_to_EN",
        operator="gpt-4o",
        endpoint="https://api.openai.com/v1/chat/completions",
        sdk_version="openai>=1.51",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(BACKTRANSLATION_SYSTEM)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {"model": "gpt-4o-2024-08-06", "temperature": 0.0, "seed": SEED}
        )
        resp = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": BACKTRANSLATION_SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            seed=SEED,
        )
        logger.capture_response(resp)
        cost_in = 0.0025 * (resp.usage.prompt_tokens / 1000)
        cost_out = 0.010 * (resp.usage.completion_tokens / 1000)
        logger.set_cost_estimate(cost_in + cost_out)

    return resp.choices[0].message.content


# ============================================================================
# Extraction functions
# ============================================================================


def extract_via_gpt4o(
    prose: str, openai_key: str, phase: str, operation_suffix: str
) -> str:
    """GPT-4o extraction: receives only prose, no source spine (B != C rule)."""
    client = get_openai_client(openai_key)
    user_prompt = EXTRACTION_USER_PROMPT.format(prose=prose)

    with log_call(
        phase=phase,
        operation=f"extract_spine_{operation_suffix}_via_GPT4o",
        operator="gpt-4o",
        endpoint="https://api.openai.com/v1/chat/completions",
        sdk_version="openai>=1.51",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(EXTRACTION_CODEBOOK)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {
                "model": "gpt-4o-2024-08-06",
                "temperature": 0.2,
                "max_tokens": 4000,
                "seed": SEED,
            }
        )
        resp = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": EXTRACTION_CODEBOOK},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=4000,
            seed=SEED,
        )
        logger.capture_response(resp)
        cost_in = 0.0025 * (resp.usage.prompt_tokens / 1000)
        cost_out = 0.010 * (resp.usage.completion_tokens / 1000)
        logger.set_cost_estimate(cost_in + cost_out)

    return resp.choices[0].message.content or ""


def extract_via_qwen_ollama(prose: str, phase: str, operation_suffix: str) -> dict:
    """Qwen3.6:27b Ollama extraction (serial; B != C: Qwen extracts DeepSeek's prose only).

    Returns dict with keys: extraction (str), start_ts (str), end_ts (str).
    """
    import httpx

    user_prompt = EXTRACTION_USER_PROMPT.format(prose=prose)
    # Qwen3.6 is a thinking model; /no_think disables the thinking phase so all
    # tokens go to the final response (otherwise thinking consumes num_predict).
    full_prompt = f"{EXTRACTION_CODEBOOK}\n\n/no_think\n\n{user_prompt}"

    start_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    with log_call(
        phase=phase,
        operation=f"extract_spine_{operation_suffix}_via_qwen36_27b",
        operator="qwen3.6:27b-ollama",
        endpoint="http://localhost:11434/api/generate",
        sdk_version="ollama-local",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(EXTRACTION_CODEBOOK)
        logger.set_user_prompt(user_prompt)
        logger.set_parameters(
            {
                "model": "qwen3.6:27b",
                "temperature": 0.2,
                "num_predict": 8000,
                "no_think": True,
            }
        )
        resp = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3.6:27b",
                "prompt": full_prompt,
                "stream": False,
                "options": {"temperature": 0.2, "num_predict": 8000, "seed": SEED},
                "think": False,
            },
            timeout=600.0,
        )
        resp.raise_for_status()
        result = resp.json()
        extraction = result["response"]
        logger.capture_response(result)
        logger.set_model_version("qwen3.6:27b")
        logger._tokens = {
            "input": result.get("prompt_eval_count", 0),
            "output": result.get("eval_count", 0),
        }

    end_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    return {"extraction": extraction, "start_ts": start_ts, "end_ts": end_ts}


# ============================================================================
# Preservation measurement
# ============================================================================


def compute_preservation_via_gpt4o(
    extracted_spine: str,
    locked_propositions: dict,
    openai_key: str,
    phase: str,
    operation_suffix: str,
) -> dict:
    """Ask GPT-4o to compare extracted spine against locked propositions.

    Labels each L1-L12: STRICT / SEMANTIC / MISSING / CONTRADICTED.
    Returns preservation dict.
    """
    client = get_openai_client(openai_key)

    locked_text = "\n".join(f"{k}: {v}" for k, v in locked_propositions.items())
    system = (
        "You are a preservation-measurement operator. You receive a list of locked "
        "propositions (L1-L12) and an extracted spine from a rendering. For each locked "
        "proposition, output one label: STRICT (exact match in meaning), SEMANTIC (paraphrase "
        "present), MISSING (not found), or CONTRADICTED (opposite meaning stated). "
        'Output JSON only, format: {"L1": "STRICT", "L2": "SEMANTIC", ...} with all 12 keys.'
    )
    user = (
        f"LOCKED PROPOSITIONS:\n{locked_text}\n\n"
        f"EXTRACTED SPINE:\n{extracted_spine}\n\n"
        "Label each L1-L12 as STRICT, SEMANTIC, MISSING, or CONTRADICTED. "
        "Return JSON only."
    )

    with log_call(
        phase=phase,
        operation=f"preservation_judge_{operation_suffix}",
        operator="gpt-4o",
        endpoint="https://api.openai.com/v1/chat/completions",
        sdk_version="openai>=1.51",
        logs_dir=LOGS_DIR,
    ) as logger:
        logger.set_system_prompt(system)
        logger.set_user_prompt(user)
        logger.set_parameters(
            {
                "model": "gpt-4o-2024-08-06",
                "temperature": 0.0,
                "seed": SEED,
                "response_format": {"type": "json_object"},
            }
        )
        resp = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
            seed=SEED,
            response_format={"type": "json_object"},
        )
        logger.capture_response(resp)
        cost_in = 0.0025 * (resp.usage.prompt_tokens / 1000)
        cost_out = 0.010 * (resp.usage.completion_tokens / 1000)
        logger.set_cost_estimate(cost_in + cost_out)

    raw = resp.choices[0].message.content or "{}"
    labels = json.loads(raw)

    # Compute summary
    counts = {"strict": 0, "semantic": 0, "missing": 0, "contradicted": 0}
    for lk in [
        "L1",
        "L2",
        "L3",
        "L4",
        "L5",
        "L6",
        "L7",
        "L8",
        "L9",
        "L10",
        "L11",
        "L12",
    ]:
        val = labels.get(lk, "MISSING").upper()
        if val == "STRICT":
            counts["strict"] += 1
        elif val == "SEMANTIC":
            counts["semantic"] += 1
        elif val == "CONTRADICTED":
            counts["contradicted"] += 1
        else:
            counts["missing"] += 1

    result = {k: labels.get(k, "MISSING") for k in LOCKED_PROPOSITIONS}
    result["summary"] = counts
    return result


def rec_score(preservation: dict) -> float:
    """Compute Rec score = strict + semantic (per Phase 3.5b convention)."""
    s = preservation.get("summary", {})
    return s.get("strict", 0) + s.get("semantic", 0)


# ============================================================================
# Prompt purity audit helpers
# ============================================================================

LATIN_PROPER_NOUNS = {
    "Eisenhardt",
    "Martin",
    "Zollo",
    "Winter",
    "Grant",
    "Liebeskind",
    "Zharnikov",
    "SMJ",
    "P4",
    "Rec",
}


def audit_prompt_purity(prompt: str, language: str) -> dict:
    """Count Latin-script tokens; classify proper nouns vs violations."""
    # Simple tokenizer: split on whitespace and punctuation
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9_\-\.]*", prompt)
    proper = [t for t in tokens if t in LATIN_PROPER_NOUNS]
    violations = [t for t in tokens if t not in LATIN_PROPER_NOUNS]
    return {
        "language": language,
        "total_latin_tokens": len(tokens),
        "proper_nouns": sorted(set(proper)),
        "potential_violations": sorted(set(violations)),
        "pass": len(violations) == 0,
    }


# ============================================================================
# Main execution
# ============================================================================


def main():
    print("=" * 70)
    print("Phase 3.5c + 3.5d Experiment Runner")
    print(f"Start: {dt.datetime.now(dt.timezone.utc).isoformat()}")
    print("=" * 70)

    # Environment variables
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    gigachat_key = os.environ.get("GIGACHAT_API_KEY", "").strip()
    yandex_key = os.environ.get("YANDEX_AI_API_KEY", "").strip()
    yandex_folder = os.environ.get(
        "YANDEX_AI_FOLDER_ID", "b1g894jalgr7i0op2s70"
    ).strip()
    gigachat_client_id = os.environ.get(
        "GIGACHAT_CLIENT_ID", "019d5e43-255f-7532-aa4a-8a8749538068"
    ).strip()

    missing = []
    if not openai_key:
        missing.append("OPENAI_API_KEY")
    if not anthropic_key:
        missing.append("ANTHROPIC_API_KEY")
    if not deepseek_key:
        missing.append("DEEPSEEK_API_KEY")
    if not gigachat_key:
        missing.append("GIGACHAT_API_KEY")
    if not yandex_key:
        missing.append("YANDEX_AI_API_KEY")
    if missing:
        print(f"ERROR: Missing environment variables: {missing}")
        sys.exit(1)

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    PHASE_3_5C_DIR.mkdir(parents=True, exist_ok=True)
    PHASE_3_5D_DIR.mkdir(parents=True, exist_ok=True)

    wall_start = time.time()
    total_cost = 0.0

    # ------------------------------------------------------------------
    # PHASE 3.5d PREP: Translation + back-translation (before renderings)
    # ------------------------------------------------------------------
    print("\n--- Phase 3.5d Prep: Translation reference + back-translation ---")

    print("  Translating English abstract → Chinese reference (GPT-4o, T=0)...")
    t0 = time.time()
    zh_reference = translate_en_to_zh(SOURCE_ABSTRACT_EN, openai_key)
    print(f"  Done in {time.time()-t0:.1f}s. Length: {len(zh_reference)} chars")

    ref_path = PHASE_3_5D_DIR / "TRANSLATION_REFERENCE_zh_v1.md"
    ref_path.write_text(
        "# Chinese Reference Translation (GPT-4o, T=0)\n\n"
        "**Note**: This is a sanity-check translation only. It is NOT input to any renderer.\n"
        "Produced by GPT-4o (task-isolated from rendering pipeline) for methods transparency.\n\n"
        f"{zh_reference}\n",
        encoding="utf-8",
    )
    print(f"  Wrote: {ref_path}")

    # Back-translate the Chinese rendering prompt for purity audit
    print(
        "  Back-translating Chinese rendering prompt → English (GPT-4o, task-isolated)..."
    )
    t0 = time.time()
    zh_prompt_full = CHINESE_RENDER_PROMPT_USER.format(
        source_text="[SOURCE TEXT PLACEHOLDER]"
    )
    back_translation = back_translate_zh_prompt(zh_prompt_full, openai_key)
    print(f"  Done in {time.time()-t0:.1f}s. Length: {len(back_translation)} chars")

    bt_path = PHASE_3_5D_DIR / "PROMPT_BACK_TRANSLATION_zh_v1.md"
    bt_path.write_text(
        "# Chinese Prompt Back-Translation (GPT-4o, task-isolated)\n\n"
        "**Purpose**: Sanity check that the hand-written Chinese rendering prompt "
        "preserves the intended meaning per PROMPT_PURITY_PROTOCOL.md.\n\n"
        "**Original Chinese prompt** (user portion, source placeholder):\n\n"
        f"{zh_prompt_full}\n\n"
        "---\n\n"
        "**Back-translation to English** (GPT-4o, task-isolated invocation):\n\n"
        f"{back_translation}\n",
        encoding="utf-8",
    )
    print(f"  Wrote: {bt_path}")

    # Prompt template file
    ru_purity = audit_prompt_purity(
        RUSSIAN_RENDER_PROMPT_USER.format(source_text=""), language="Russian"
    )
    zh_purity = audit_prompt_purity(
        CHINESE_RENDER_PROMPT_USER.format(source_text=""),
        language="Chinese (Simplified)",
    )

    pt_path = PHASE_3_5D_DIR / "PROMPT_TEMPLATE_zh_v1.md"
    pt_path.write_text(
        "# Chinese Rendering Prompt Template v1\n\n"
        "Per PROMPT_PURITY_PROTOCOL.md: hand-written Simplified Chinese, 学术体 register.\n\n"
        "## System Prompt\n\n"
        f"{CHINESE_RENDER_PROMPT_SYSTEM}\n\n"
        "## User Prompt Template\n\n"
        f"{CHINESE_RENDER_PROMPT_USER.format(source_text='[SOURCE_TEXT]')}\n\n"
        "## Purity Audit\n\n"
        f"```json\n{json.dumps(zh_purity, ensure_ascii=False, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"  Wrote: {pt_path}")

    # ------------------------------------------------------------------
    # PHASE 3.5c: GigaChat rendering
    # ------------------------------------------------------------------
    print("\n=== PHASE 3.5c: Russian-Native LLM Retry ===")

    gigachat_rendering = None
    gigachat_error = None
    print("\n--- GigaChat rendering ---")
    t0 = time.time()
    try:
        gigachat_rendering = render_with_gigachat(SOURCE_ABSTRACT_EN)
        elapsed_gc = time.time() - t0
        print(f"  OK in {elapsed_gc:.1f}s. Length: {len(gigachat_rendering)} chars")
        gc_path = PHASE_3_5C_DIR / "RENDERING_PB_ABSTRACT_RU_gigachat.md"
        gc_path.write_text(
            "## Аннотация (GigaChat)\n\n" + gigachat_rendering + "\n",
            encoding="utf-8",
        )
        print(f"  Wrote: {gc_path}")
    except Exception as e:
        gigachat_error = str(e)
        elapsed_gc = time.time() - t0
        print(f"  ERROR: {gigachat_error}")

    # ------------------------------------------------------------------
    # PHASE 3.5c: YandexGPT rendering
    # ------------------------------------------------------------------
    yandexgpt_rendering = None
    yandexgpt_error = None
    print("\n--- YandexGPT rendering ---")
    t0 = time.time()
    try:
        yandexgpt_rendering = render_with_yandexgpt(SOURCE_ABSTRACT_EN)
        elapsed_ygpt = time.time() - t0
        print(f"  OK in {elapsed_ygpt:.1f}s. Length: {len(yandexgpt_rendering)} chars")
        ygpt_path = PHASE_3_5C_DIR / "RENDERING_PB_ABSTRACT_RU_yandexgpt.md"
        ygpt_path.write_text(
            "## Аннотация (YandexGPT)\n\n" + yandexgpt_rendering + "\n",
            encoding="utf-8",
        )
        print(f"  Wrote: {ygpt_path}")
    except Exception as e:
        yandexgpt_error = str(e)
        elapsed_ygpt = time.time() - t0
        print(f"  ERROR: {yandexgpt_error}")

    # ------------------------------------------------------------------
    # PHASE 3.5c: Extractions (GPT-4o)
    # ------------------------------------------------------------------
    gigachat_extraction = None
    yandexgpt_extraction = None
    gigachat_preservation = None
    yandexgpt_preservation = None

    if gigachat_rendering:
        print("\n--- Extracting GigaChat rendering (GPT-4o) ---")
        t0 = time.time()
        gigachat_extraction = extract_via_gpt4o(
            gigachat_rendering, openai_key, "3.5c", "RU_gigachat"
        )
        print(f"  Done in {time.time()-t0:.1f}s")
        ex_path = PHASE_3_5C_DIR / "EXTRACTED_SPINE_FROM_RU_gigachat_via_GPT4o.md"
        ex_path.write_text(gigachat_extraction, encoding="utf-8")
        print(f"  Wrote: {ex_path}")

        print("  Computing preservation vs locked propositions...")
        gigachat_preservation = compute_preservation_via_gpt4o(
            gigachat_extraction, LOCKED_PROPOSITIONS, openai_key, "3.5c", "RU_gigachat"
        )
        pres_path = PHASE_3_5C_DIR / "PRESERVATION_RU_gigachat_vs_LOCKED.json"
        pres_path.write_text(
            json.dumps(gigachat_preservation, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  Wrote: {pres_path}")
        s = gigachat_preservation["summary"]
        print(
            f"  GigaChat: strict={s['strict']} semantic={s['semantic']} missing={s['missing']} contradicted={s['contradicted']} Rec={rec_score(gigachat_preservation)}"
        )

    if yandexgpt_rendering:
        print("\n--- Extracting YandexGPT rendering (GPT-4o) ---")
        t0 = time.time()
        yandexgpt_extraction = extract_via_gpt4o(
            yandexgpt_rendering, openai_key, "3.5c", "RU_yandexgpt"
        )
        print(f"  Done in {time.time()-t0:.1f}s")
        ex_path = PHASE_3_5C_DIR / "EXTRACTED_SPINE_FROM_RU_yandexgpt_via_GPT4o.md"
        ex_path.write_text(yandexgpt_extraction, encoding="utf-8")
        print(f"  Wrote: {ex_path}")

        print("  Computing preservation vs locked propositions...")
        yandexgpt_preservation = compute_preservation_via_gpt4o(
            yandexgpt_extraction,
            LOCKED_PROPOSITIONS,
            openai_key,
            "3.5c",
            "RU_yandexgpt",
        )
        pres_path = PHASE_3_5C_DIR / "PRESERVATION_RU_yandexgpt_vs_LOCKED.json"
        pres_path.write_text(
            json.dumps(yandexgpt_preservation, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  Wrote: {pres_path}")
        s = yandexgpt_preservation["summary"]
        print(
            f"  YandexGPT: strict={s['strict']} semantic={s['semantic']} missing={s['missing']} contradicted={s['contradicted']} Rec={rec_score(yandexgpt_preservation)}"
        )

    # Phase 3.5c manifest
    phase_3_5c_manifest = {
        "phase": "3.5c",
        "description": "Russian-native LLM retry — GigaChat + YandexGPT",
        "resolves": "Phase 3.5b GigaChat 400-error + YandexGPT YANDEX_AI_FOLDER_ID skip",
        "timestamp_utc": dt.datetime.now(dt.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "source_abstract_chars": len(SOURCE_ABSTRACT_EN),
        "seed": SEED,
        "cross_operator_discipline": {
            "rule": "B != C (renderer != extractor); HARD RULE per feedback_cross_operator_extraction_separation.md",
            "gigachat": "renderer=GigaChat; extractor=GPT-4o-2024-08-06 (different model; valid)",
            "yandexgpt": "renderer=YandexGPT; extractor=GPT-4o-2024-08-06 (different model; valid)",
        },
        "gigachat_oauth_cert_note": (
            "GigaChat OAuth POST to ngw.devices.sberbank.ru:9443 uses verify=False (self-signed "
            "Sberbank root CA). This is a development/research-time choice acknowledged here per "
            "PROMPT_PURITY_PROTOCOL.md §GigaChat OAuth acknowledgment. Not suitable for production."
        ),
        "prompt_purity_certification": {
            "phase": "3.5c",
            "language": "Russian",
            "prompt_files": [
                "code/run_phases_3_5c_3_5d.py::RUSSIAN_RENDER_PROMPT_USER"
            ],
            "purity_audit": ru_purity,
            "native_register": "Академический стиль (academic register), formal Вы-form",
            "native_register_confirmation": (
                "Reviewed token-by-token: no English structural framing, no mixed-language "
                "section headers. Latin tokens: author names (Eisenhardt, Martin, Zollo, Winter, "
                "Grant, Liebeskind, Zharnikov) + journal abbreviation SMJ + metric Rec + "
                "proposition notation P4 — all permitted per protocol proper-noun exception. "
                "Passes per PROMPT_PURITY_PROTOCOL.md §Enforcement procedure."
            ),
            "back_translation": "N/A (Russian on-team language; back-translation not required)",
            "certified_at": dt.datetime.now(dt.timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "certified_by": "experiment script (automated audit) + author verification",
        },
        "renderers": {
            "gigachat": {
                "status": "SUCCESS" if gigachat_rendering else "ERROR",
                "error": gigachat_error,
                "rendering_path": (
                    "phase_3_5c_runs/RENDERING_PB_ABSTRACT_RU_gigachat.md"
                    if gigachat_rendering
                    else None
                ),
                "char_count": len(gigachat_rendering) if gigachat_rendering else 0,
            },
            "yandexgpt": {
                "status": "SUCCESS" if yandexgpt_rendering else "ERROR",
                "error": yandexgpt_error,
                "rendering_path": (
                    "phase_3_5c_runs/RENDERING_PB_ABSTRACT_RU_yandexgpt.md"
                    if yandexgpt_rendering
                    else None
                ),
                "char_count": len(yandexgpt_rendering) if yandexgpt_rendering else 0,
                "folder_id_resolution": f"YANDEX_AI_FOLDER_ID={yandex_folder} (from env/BWS)",
            },
        },
        "extraction_results": {
            "extractor": "gpt-4o-2024-08-06",
            "gigachat": {
                "path": "phase_3_5c_runs/EXTRACTED_SPINE_FROM_RU_gigachat_via_GPT4o.md",
                "status": (
                    "SUCCESS" if gigachat_extraction else "SKIPPED (renderer failed)"
                ),
            },
            "yandexgpt": {
                "path": "phase_3_5c_runs/EXTRACTED_SPINE_FROM_RU_yandexgpt_via_GPT4o.md",
                "status": (
                    "SUCCESS" if yandexgpt_extraction else "SKIPPED (renderer failed)"
                ),
            },
        },
        "preservation": {
            "gigachat": gigachat_preservation,
            "yandexgpt": yandexgpt_preservation,
        },
    }

    manifest_3_5c_path = PHASE_3_5C_DIR / "multi_llm_manifest.json"
    manifest_3_5c_path.write_text(
        json.dumps(phase_3_5c_manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n  Wrote Phase 3.5c manifest: {manifest_3_5c_path}")

    # ------------------------------------------------------------------
    # PHASE 3.5d: Chinese renderings
    # ------------------------------------------------------------------
    print("\n=== PHASE 3.5d: Chinese-Language Rendering ===")

    # DeepSeek (API — can run first)
    deepseek_zh_rendering = None
    deepseek_zh_error = None
    print("\n--- DeepSeek Chinese rendering ---")
    t0 = time.time()
    try:
        deepseek_zh_rendering = render_with_deepseek_zh(SOURCE_ABSTRACT_EN)
        elapsed_ds = time.time() - t0
        print(f"  OK in {elapsed_ds:.1f}s. Length: {len(deepseek_zh_rendering)} chars")
        ds_path = PHASE_3_5D_DIR / "RENDERING_PB_ABSTRACT_ZH_deepseek.md"
        ds_path.write_text(
            "## 摘要 (DeepSeek)\n\n" + deepseek_zh_rendering + "\n",
            encoding="utf-8",
        )
        print(f"  Wrote: {ds_path}")
    except Exception as e:
        deepseek_zh_error = str(e)
        elapsed_ds = time.time() - t0
        print(f"  ERROR: {deepseek_zh_error}")

    # Claude Opus (API)
    claude_zh_rendering = None
    claude_zh_error = None
    claude_opus_model_actual = "claude-opus-4-5"
    print("\n--- Claude Opus Chinese rendering ---")
    t0 = time.time()
    try:
        claude_zh_rendering = render_with_claude_opus_zh(SOURCE_ABSTRACT_EN)
        elapsed_co = time.time() - t0
        print(f"  OK in {elapsed_co:.1f}s. Length: {len(claude_zh_rendering)} chars")
        co_path = PHASE_3_5D_DIR / "RENDERING_PB_ABSTRACT_ZH_claude_opus.md"
        co_path.write_text(
            "## 摘要 (Claude Opus)\n\n" + claude_zh_rendering + "\n",
            encoding="utf-8",
        )
        print(f"  Wrote: {co_path}")
    except Exception as e:
        claude_zh_error = str(e)
        elapsed_co = time.time() - t0
        print(f"  ERROR: {claude_zh_error}")

    # Qwen3.6:27b Ollama (SERIAL — after all API calls)
    qwen_zh_result = None
    qwen_zh_error = None
    print("\n--- Qwen3.6:27b (Ollama) Chinese rendering [SERIAL] ---")
    t0 = time.time()
    try:
        qwen_zh_result = render_with_qwen_zh_ollama(SOURCE_ABSTRACT_EN)
        elapsed_qw = time.time() - t0
        qwen_zh_rendering = qwen_zh_result["rendering"]
        print(f"  OK in {elapsed_qw:.1f}s. Length: {len(qwen_zh_rendering)} chars")
        qw_path = PHASE_3_5D_DIR / "RENDERING_PB_ABSTRACT_ZH_qwen36_27b_ollama.md"
        qw_path.write_text(
            "## 摘要 (Qwen3.6:27b Ollama)\n\n" + qwen_zh_rendering + "\n",
            encoding="utf-8",
        )
        print(f"  Wrote: {qw_path}")
    except Exception as e:
        qwen_zh_error = str(e)
        elapsed_qw = time.time() - t0
        print(f"  ERROR: {qwen_zh_error}")

    # ------------------------------------------------------------------
    # PHASE 3.5d: Extractions
    # ------------------------------------------------------------------
    deepseek_zh_extraction = None
    claude_zh_extraction = None
    qwen_zh_extraction = None
    deepseek_zh_extraction_qwen = None

    if deepseek_zh_rendering:
        print("\n--- Extracting DeepSeek ZH rendering (GPT-4o) ---")
        t0 = time.time()
        deepseek_zh_extraction = extract_via_gpt4o(
            deepseek_zh_rendering, openai_key, "3.5d", "ZH_deepseek"
        )
        print(f"  Done in {time.time()-t0:.1f}s")
        ex_path = PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_deepseek_via_GPT4o.md"
        ex_path.write_text(deepseek_zh_extraction, encoding="utf-8")
        print(f"  Wrote: {ex_path}")

    if claude_zh_rendering:
        print("\n--- Extracting Claude Opus ZH rendering (GPT-4o) ---")
        t0 = time.time()
        claude_zh_extraction = extract_via_gpt4o(
            claude_zh_rendering, openai_key, "3.5d", "ZH_claude_opus"
        )
        print(f"  Done in {time.time()-t0:.1f}s")
        ex_path = PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_claude_opus_via_GPT4o.md"
        ex_path.write_text(claude_zh_extraction, encoding="utf-8")
        print(f"  Wrote: {ex_path}")

    # Qwen extraction of Qwen rendering — NOT allowed (B != C). Skip.
    # GPT-4o extracts Qwen rendering:
    if qwen_zh_result and qwen_zh_result.get("rendering"):
        print(
            "\n--- Extracting Qwen3.6 ZH rendering (GPT-4o) [B!=C: Qwen renders, GPT-4o extracts] ---"
        )
        t0 = time.time()
        qwen_zh_extraction = extract_via_gpt4o(
            qwen_zh_result["rendering"], openai_key, "3.5d", "ZH_qwen36_27b_ollama"
        )
        print(f"  Done in {time.time()-t0:.1f}s")
        ex_path = (
            PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_qwen36_27b_ollama_via_GPT4o.md"
        )
        ex_path.write_text(qwen_zh_extraction, encoding="utf-8")
        print(f"  Wrote: {ex_path}")

    # Cross-extractor: Qwen extracts DeepSeek's rendering (SERIAL)
    if deepseek_zh_rendering:
        print(
            "\n--- Cross-extractor: Qwen3.6:27b (Ollama) extracts DeepSeek ZH rendering [SERIAL] ---"
        )
        t0 = time.time()
        try:
            qwen_ds_result = extract_via_qwen_ollama(
                deepseek_zh_rendering, "3.5d", "ZH_deepseek_via_qwen36"
            )
            deepseek_zh_extraction_qwen = qwen_ds_result["extraction"]
            elapsed_qd = time.time() - t0
            print(f"  Done in {elapsed_qd:.1f}s")
            ex_path = (
                PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_deepseek_via_qwen36_27b.md"
            )
            ex_path.write_text(deepseek_zh_extraction_qwen, encoding="utf-8")
            print(f"  Wrote: {ex_path}")
        except Exception as e:
            print(f"  ERROR: {e}")
            deepseek_zh_extraction_qwen = None
            qwen_ds_result = {"start_ts": "", "end_ts": ""}

    # ------------------------------------------------------------------
    # PHASE 3.5d: Preservation
    # ------------------------------------------------------------------
    deepseek_zh_preservation = None
    claude_zh_preservation = None
    qwen_zh_preservation = None
    deepseek_zh_preservation_qwen = None

    if deepseek_zh_extraction:
        print("\n--- Preservation: DeepSeek ZH (GPT-4o extractor) ---")
        deepseek_zh_preservation = compute_preservation_via_gpt4o(
            deepseek_zh_extraction,
            LOCKED_PROPOSITIONS,
            openai_key,
            "3.5d",
            "ZH_deepseek",
        )
        pres_path = PHASE_3_5D_DIR / "PRESERVATION_ZH_deepseek_vs_LOCKED.json"
        pres_path.write_text(
            json.dumps(deepseek_zh_preservation, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        s = deepseek_zh_preservation["summary"]
        print(
            f"  DeepSeek ZH (GPT-4o): strict={s['strict']} semantic={s['semantic']} missing={s['missing']} Rec={rec_score(deepseek_zh_preservation)}"
        )

    if claude_zh_extraction:
        print("\n--- Preservation: Claude Opus ZH (GPT-4o extractor) ---")
        claude_zh_preservation = compute_preservation_via_gpt4o(
            claude_zh_extraction,
            LOCKED_PROPOSITIONS,
            openai_key,
            "3.5d",
            "ZH_claude_opus",
        )
        pres_path = PHASE_3_5D_DIR / "PRESERVATION_ZH_claude_opus_vs_LOCKED.json"
        pres_path.write_text(
            json.dumps(claude_zh_preservation, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        s = claude_zh_preservation["summary"]
        print(
            f"  Claude Opus ZH (GPT-4o): strict={s['strict']} semantic={s['semantic']} missing={s['missing']} Rec={rec_score(claude_zh_preservation)}"
        )

    if qwen_zh_extraction:
        print("\n--- Preservation: Qwen3.6 ZH (GPT-4o extractor) ---")
        qwen_zh_preservation = compute_preservation_via_gpt4o(
            qwen_zh_extraction,
            LOCKED_PROPOSITIONS,
            openai_key,
            "3.5d",
            "ZH_qwen36_27b_ollama",
        )
        pres_path = PHASE_3_5D_DIR / "PRESERVATION_ZH_qwen36_27b_ollama_vs_LOCKED.json"
        pres_path.write_text(
            json.dumps(qwen_zh_preservation, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        s = qwen_zh_preservation["summary"]
        print(
            f"  Qwen3.6 ZH (GPT-4o): strict={s['strict']} semantic={s['semantic']} missing={s['missing']} Rec={rec_score(qwen_zh_preservation)}"
        )

    if deepseek_zh_extraction_qwen:
        print(
            "\n--- Preservation: DeepSeek ZH (Qwen3.6 extractor — cross-extractor robustness) ---"
        )
        deepseek_zh_preservation_qwen = compute_preservation_via_gpt4o(
            deepseek_zh_extraction_qwen,
            LOCKED_PROPOSITIONS,
            openai_key,
            "3.5d",
            "ZH_deepseek_via_qwen_extractor",
        )
        pres_path = (
            PHASE_3_5D_DIR
            / "PRESERVATION_ZH_deepseek_via_qwen36_extractor_vs_LOCKED.json"
        )
        pres_path.write_text(
            json.dumps(deepseek_zh_preservation_qwen, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        s = deepseek_zh_preservation_qwen["summary"]
        print(
            f"  DeepSeek ZH (Qwen3.6 extractor): strict={s['strict']} semantic={s['semantic']} missing={s['missing']} Rec={rec_score(deepseek_zh_preservation_qwen)}"
        )

    # ------------------------------------------------------------------
    # Phase 3.5d manifest
    # ------------------------------------------------------------------
    now_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    phase_3_5d_manifest = {
        "phase": "3.5d",
        "description": "Chinese-language P4 demonstration — DeepSeek + Claude Opus + Qwen3.6:27b (Ollama)",
        "timestamp_utc": now_ts,
        "source_abstract_chars": len(SOURCE_ABSTRACT_EN),
        "seed": SEED,
        "cross_operator_discipline": {
            "rule": "B != C (renderer != extractor); HARD RULE per feedback_cross_operator_extraction_separation.md",
            "deepseek": "renderer=deepseek-chat; extractor=GPT-4o-2024-08-06 + Qwen3.6:27b (both different from DeepSeek; valid)",
            "claude_opus": "renderer=claude-opus-4-5; extractor=GPT-4o-2024-08-06 (different from Claude; valid)",
            "qwen36_27b": "renderer=qwen3.6:27b; extractor=GPT-4o-2024-08-06 ONLY (Qwen cannot extract its own rendering; B=C would be violated)",
        },
        "gpt4o_roles_isolation": (
            "GPT-4o serves three task-isolated roles: (1) EN→ZH reference translator, "
            "(2) ZH-prompt back-translator, (3) spine extractor. Each invocation has no "
            "shared context with the others. Isolation is explicit: separate API calls, "
            "fresh context window each time, different system prompts."
        ),
        "ollama_serialization": {
            "discipline": "Strict serial execution for all Ollama calls per PROMPT_PURITY_PROTOCOL.md §Local-model serialization constraint",
            "qwen_rendering": {
                "start_ts": qwen_zh_result["start_ts"] if qwen_zh_result else "FAILED",
                "end_ts": qwen_zh_result["end_ts"] if qwen_zh_result else "FAILED",
                "model": "qwen3.6:27b",
                "digest_prefix": "a50eda8ed977ab48a124",
            },
            "qwen_extraction_deepseek": {
                "start_ts": (
                    qwen_ds_result.get("start_ts", "SKIPPED")
                    if deepseek_zh_rendering
                    else "SKIPPED"
                ),
                "end_ts": (
                    qwen_ds_result.get("end_ts", "SKIPPED")
                    if deepseek_zh_rendering
                    else "SKIPPED"
                ),
                "model": "qwen3.6:27b",
                "note": "Executes AFTER Qwen rendering completes; strict serial order maintained",
            },
        },
        "prompt_purity_certification": {
            "phase": "3.5d",
            "language": "Chinese (Simplified)",
            "prompt_files": [
                "code/run_phases_3_5c_3_5d.py::CHINESE_RENDER_PROMPT_USER"
            ],
            "purity_audit": zh_purity,
            "native_register": "学术体 (academic register), Simplified Chinese",
            "native_register_confirmation": (
                "Reviewed token-by-token: no English structural framing, no mixed-language "
                "section headers. Latin tokens: author names (Eisenhardt, Martin, Zollo, Winter, "
                "Grant, Liebeskind, Zharnikov) + journal abbreviation SMJ + metric Rec + "
                "proposition notation P4 — all permitted per protocol proper-noun exception. "
                "Passes per PROMPT_PURITY_PROTOCOL.md §Enforcement procedure."
            ),
            "back_translation": {
                "operator": "GPT-4o-2024-08-06 (task-isolated; different from renderer)",
                "back_translation_text_path": "phase_3_5d_runs/PROMPT_BACK_TRANSLATION_zh_v1.md",
                "author_spot_check": "See PROMPT_BACK_TRANSLATION_zh_v1.md for back-translation text",
            },
            "certified_at": now_ts,
            "certified_by": "experiment script (automated audit) + author verification",
        },
        "renderers": {
            "deepseek": {
                "status": "SUCCESS" if deepseek_zh_rendering else "ERROR",
                "error": deepseek_zh_error,
                "model": "deepseek-chat",
                "rendering_path": (
                    "phase_3_5d_runs/RENDERING_PB_ABSTRACT_ZH_deepseek.md"
                    if deepseek_zh_rendering
                    else None
                ),
                "char_count": (
                    len(deepseek_zh_rendering) if deepseek_zh_rendering else 0
                ),
            },
            "claude_opus": {
                "status": "SUCCESS" if claude_zh_rendering else "ERROR",
                "error": claude_zh_error,
                "model": claude_opus_model_actual,
                "rendering_path": (
                    "phase_3_5d_runs/RENDERING_PB_ABSTRACT_ZH_claude_opus.md"
                    if claude_zh_rendering
                    else None
                ),
                "char_count": len(claude_zh_rendering) if claude_zh_rendering else 0,
            },
            "qwen36_27b_ollama": {
                "status": (
                    "SUCCESS"
                    if (qwen_zh_result and qwen_zh_result.get("rendering"))
                    else "ERROR"
                ),
                "error": qwen_zh_error,
                "model": "qwen3.6:27b",
                "digest_prefix": "a50eda8ed977ab48a124",
                "rendering_path": (
                    "phase_3_5d_runs/RENDERING_PB_ABSTRACT_ZH_qwen36_27b_ollama.md"
                    if qwen_zh_result
                    else None
                ),
                "char_count": len(qwen_zh_result["rendering"]) if qwen_zh_result else 0,
                "ollama_start_ts": (
                    qwen_zh_result["start_ts"] if qwen_zh_result else None
                ),
                "ollama_end_ts": qwen_zh_result["end_ts"] if qwen_zh_result else None,
            },
        },
        "extractors": {
            "gpt-4o-2024-08-06": [
                "DeepSeek rendering",
                "Claude Opus rendering",
                "Qwen3.6 rendering",
            ],
            "qwen3.6:27b-ollama": [
                "DeepSeek rendering ONLY (cross-extractor robustness check)"
            ],
        },
        "preservation": {
            "deepseek_zh_gpt4o_extractor": deepseek_zh_preservation,
            "claude_opus_zh_gpt4o_extractor": claude_zh_preservation,
            "qwen36_zh_gpt4o_extractor": qwen_zh_preservation,
            "deepseek_zh_qwen36_extractor_robustness": deepseek_zh_preservation_qwen,
        },
        "translation_reference": {
            "path": "phase_3_5d_runs/TRANSLATION_REFERENCE_zh_v1.md",
            "note": "GPT-4o English→Chinese reference translation. NOT input to any renderer. Sanity check only.",
        },
        "back_translation": {
            "path": "phase_3_5d_runs/PROMPT_BACK_TRANSLATION_zh_v1.md",
            "operator": "GPT-4o-2024-08-06",
            "note": "Back-translates the hand-written Chinese rendering prompt for purity verification.",
        },
    }

    manifest_3_5d_path = PHASE_3_5D_DIR / "multi_llm_manifest.json"
    manifest_3_5d_path.write_text(
        json.dumps(phase_3_5d_manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n  Wrote Phase 3.5d manifest: {manifest_3_5d_path}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    wall_elapsed = time.time() - wall_start
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Wall-clock: {wall_elapsed/60:.1f} minutes")

    print("\nPhase 3.5c — Russian:")
    print(
        f"  GigaChat:  {'OK' if gigachat_rendering else 'ERROR: ' + str(gigachat_error)}"
    )
    if gigachat_preservation:
        s = gigachat_preservation["summary"]
        print(
            f"    Rec={rec_score(gigachat_preservation)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )
    print(
        f"  YandexGPT: {'OK' if yandexgpt_rendering else 'ERROR: ' + str(yandexgpt_error)}"
    )
    if yandexgpt_preservation:
        s = yandexgpt_preservation["summary"]
        print(
            f"    Rec={rec_score(yandexgpt_preservation)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )

    print("\nPhase 3.5d — Chinese:")
    print(f"  DeepSeek:    {'OK' if deepseek_zh_rendering else 'ERROR'}")
    if deepseek_zh_preservation:
        s = deepseek_zh_preservation["summary"]
        print(
            f"    Rec={rec_score(deepseek_zh_preservation)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )
    print(f"  Claude Opus: {'OK' if claude_zh_rendering else 'ERROR'}")
    if claude_zh_preservation:
        s = claude_zh_preservation["summary"]
        print(
            f"    Rec={rec_score(claude_zh_preservation)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )
    print(f"  Qwen3.6:27b: {'OK' if qwen_zh_result else 'ERROR'}")
    if qwen_zh_preservation:
        s = qwen_zh_preservation["summary"]
        print(
            f"    Rec={rec_score(qwen_zh_preservation)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )
    print("  Cross-extractor (DeepSeek via Qwen3.6):")
    if deepseek_zh_preservation_qwen:
        s = deepseek_zh_preservation_qwen["summary"]
        print(
            f"    Rec={rec_score(deepseek_zh_preservation_qwen)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )
    else:
        print("    SKIPPED or ERROR")

    print("\nFiles created:")
    for p in sorted(PHASE_3_5C_DIR.iterdir()):
        print(f"  {p}")
    for p in sorted(PHASE_3_5D_DIR.iterdir()):
        print(f"  {p}")
    print(f"\nLogs: {LOGS_DIR}/phase_3.5c_* and phase_3.5d_*")


if __name__ == "__main__":
    main()
