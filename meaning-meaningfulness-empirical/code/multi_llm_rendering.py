"""Phase 3.5b — Multi-LLM Russian operator robustness for cross-language P4 evidence.

User direction (Session H addendum): test whether P4 cross-language preservation
holds across rendering OPERATOR types (academic-robustness pattern from LLM-as-
evaluator literature; e.g., Chiang et al. 2023). Each LLM operator gets the
same English source text → renders into Russian → spine re-extracted → per-
operator preservation rate computed → cross-operator agreement on locked-
proposition set reported.

Reviewer-defense framing: "preservation isn't an artifact of operator choice."

Operators (target: 2-3 of these depending on API access):
  - YandexGPT (Russian-native; YANDEXGPT_API_KEY + YANDEXGPT_FOLDER_ID env)
  - GigaChat by Sberbank (Russian-native, independent corpus; GIGACHAT_AUTH env)
  - Claude (English-substrate; ANTHROPIC_API_KEY env)
  - GPT-4o (English-substrate; OPENAI_API_KEY env)

Per Session H init prompt §Phase 3.5b stretch budget rule: execute ONLY when
Phase 3.5a finishes with >2h remaining; otherwise mark as v1.4.0 backlog.
This script is the EXECUTION-READY SKELETON for that v1.4.0 sub-task; it is
NOT fired in Session H.

Run pattern (BWS-injected per fleet convention):
    bws run -- uv run --with openai --with anthropic --with httpx \\
        python audit/scripts/dr_phase3_5b_multi_llm_russian_robustness.py \\
        --source-text research/meaningfulness_empirical_companion/paper.md \\
        --source-extract abstract \\
        --operators yandexgpt gigachat claude_opus \\
        --output-dir research/meaningfulness_empirical_companion/multi_llm_russian/ \\
        --seed 42

The `bws run` wrapper injects API keys from Bitwarden Secrets Manager into
the environment before exec. See audit/scripts/dr_v1_empirical_cases.py for
the reference pattern.

Random seed fixed at 42 per PAPER_QUALITY_STANDARDS 37a. Outputs include
per-operator rendering files + per-operator re-extracted spine YAMLs +
cross-operator preservation matrix.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path
from typing import Callable

SEED = 42


def get_source_extract(paper_md_path: Path, extract: str) -> str:
    """Pull the requested extract from paper.md.

    extract ∈ {abstract, theory_positioning, full_substrate_summary}.
    """
    text = paper_md_path.read_text()
    if extract == "abstract":
        # naive regex; adjust if paper structure changes
        import re

        m = re.search(r"## Abstract\n\n(.*?)\n\n\*\*Keywords", text, flags=re.DOTALL)
        if m:
            return m.group(1).strip()
        raise RuntimeError("Abstract block not found in paper.md")
    raise NotImplementedError(f"extract={extract} not yet supported")


# ============================================================================
# Per-operator render functions. Each takes (source_english_text, seed) and
# returns the operator's Russian rendering. Stubs for v1.4.0 execution.
# ============================================================================


def render_with_yandexgpt(source_text: str, seed: int) -> str:
    """Render English source into Russian via YandexGPT.

    Requires YANDEXGPT_API_KEY and YANDEXGPT_FOLDER_ID in environment.
    Endpoint: https://llm.api.cloud.yandex.net/foundationModels/v1/completion
    Reference: https://yandex.cloud/en/docs/foundation-models/operations/yandexgpt/create-prompt
    """
    import httpx

    api_key = os.environ.get("YANDEXGPT_API_KEY", "").strip()
    folder_id = os.environ.get("YANDEXGPT_FOLDER_ID", "").strip()
    if not api_key or not folder_id:
        raise RuntimeError("YANDEXGPT_API_KEY and YANDEXGPT_FOLDER_ID required")
    prompt = (
        "Render the following English academic abstract into native Russian "
        "appropriate for an SMJ-tier Russian academic readership. Preserve all "
        "propositional claims, numerical figures, and citation references. Use "
        "formal academic Russian register. Do not translate verbatim; render "
        "naturally:\n\n"
        f"{source_text}"
    )
    resp = httpx.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers={
            "Authorization": f"Api-Key {api_key}",
            "x-folder-id": folder_id,
        },
        json={
            "modelUri": f"gpt://{folder_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": 2000,
            },
            "messages": [{"role": "user", "text": prompt}],
        },
        timeout=120.0,
    )
    resp.raise_for_status()
    return resp.json()["result"]["alternatives"][0]["message"]["text"]


def render_with_gigachat(source_text: str, seed: int) -> str:
    """Render via GigaChat (Sberbank).

    Requires GIGACHAT_AUTH (basic-auth credential) OR GIGACHAT_API_KEY (same
    value; base64 of client_id:client_secret) in environment.
    Endpoint: https://gigachat.devices.sberbank.ru/api/v1/chat/completions
    OAuth2 flow: POST to /api/v2/oauth with client credentials, get token,
    then call /api/v1/chat/completions.
    Reference: https://developers.sber.ru/docs/ru/gigachat/api/overview
    """
    import httpx

    auth = os.environ.get("GIGACHAT_AUTH", "").strip() or os.environ.get("GIGACHAT_API_KEY", "").strip()
    if not auth:
        raise RuntimeError("GIGACHAT_AUTH or GIGACHAT_API_KEY required (basic-auth credential)")
    # OAuth2 token flow (RqUID must be a valid UUID v4)
    import uuid
    token_resp = httpx.post(
        "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        headers={
            "Authorization": f"Basic {auth}",
            "RqUID": str(uuid.uuid4()),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data={"scope": "GIGACHAT_API_PERS"},
        verify=False,
        timeout=60.0,
    )
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]
    prompt = (
        "Переведи следующий академический английский абстракт на естественный "
        "русский академический язык, подходящий для русскоязычной аудитории "
        "уровня SMJ. Сохрани все пропозициональные утверждения, числовые "
        "величины и цитирования. Не переводи дословно; делай естественный "
        "академический рендеринг:\n\n"
        f"{source_text}"
    )
    resp = httpx.post(
        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={
            "model": "GigaChat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 2000,
        },
        verify=False,
        timeout=120.0,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def render_with_claude_opus(source_text: str, seed: int) -> str:
    """Render via Claude (English-substrate operator; for cross-operator comparison)."""
    from anthropic import Anthropic

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = (
        "Render the following English academic abstract into native Russian "
        "appropriate for an SMJ-tier Russian academic readership. Preserve all "
        "propositional claims, numerical figures, and citation references. Use "
        "formal academic Russian register. Do not translate verbatim; render "
        "naturally. Return only the Russian text, no preamble:\n\n"
        f"{source_text}"
    )
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def render_with_gpt4o(source_text: str, seed: int) -> str:
    """Render via GPT-4o (English-substrate operator; for cross-operator comparison)."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "Render the following English academic abstract into native Russian "
        "appropriate for an SMJ-tier Russian academic readership. Preserve all "
        "propositional claims, numerical figures, and citation references. Use "
        "formal academic Russian register. Do not translate verbatim; render "
        "naturally. Return only the Russian text, no preamble:\n\n"
        f"{source_text}"
    )
    resp = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000,
        seed=seed,
    )
    return resp.choices[0].message.content


def render_with_deepseek(source_text: str, seed: int) -> str:
    """Render via DeepSeek (Chinese-native operator; primarily-Chinese training corpus).

    Requires DEEPSEEK_API_KEY in environment.
    Endpoint: https://api.deepseek.com/chat/completions (OpenAI-compatible).
    Reference: https://api-docs.deepseek.com/
    """
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    prompt = (
        "Render the following English academic abstract into native Russian "
        "appropriate for an SMJ-tier Russian academic readership. Preserve all "
        "propositional claims, numerical figures, and citation references. Use "
        "formal academic Russian register. Do not translate verbatim; render "
        "naturally. Return only the Russian text, no preamble:\n\n"
        f"{source_text}"
    )
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000,
    )
    return resp.choices[0].message.content


OPERATORS: dict[str, Callable[[str, int], str]] = {
    "yandexgpt": render_with_yandexgpt,
    "gigachat": render_with_gigachat,
    "deepseek": render_with_deepseek,
    "claude_opus": render_with_claude_opus,
    "gpt4o": render_with_gpt4o,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phase 3.5b multi-LLM Russian operator robustness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(__doc__ or ""),
    )
    parser.add_argument(
        "--source-text",
        type=Path,
        required=True,
        help="Path to paper.md (or other source)",
    )
    parser.add_argument(
        "--source-extract",
        choices=["abstract", "theory_positioning"],
        default="abstract",
    )
    parser.add_argument(
        "--operators",
        nargs="+",
        choices=list(OPERATORS.keys()),
        default=["yandexgpt", "gigachat", "claude_opus"],
        help="Operator subset to invoke; default: yandexgpt + gigachat + claude_opus",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where per-operator rendering files are written",
    )
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    source_text = get_source_extract(args.source_text, args.source_extract)
    print(f"Source extract: {args.source_extract} ({len(source_text)} chars)")
    print(f"Operators: {args.operators}")
    print(f"Seed: {args.seed}")
    print()

    results: dict[str, dict] = {}
    for op_name in args.operators:
        op_func = OPERATORS[op_name]
        print(f"--- {op_name} ---")
        try:
            rendering = op_func(source_text, args.seed)
        except Exception as e:
            print(f"  ERROR: {e}")
            results[op_name] = {"error": str(e)}
            continue
        out_path = args.output_dir / f"RENDERING_PB_ABSTRACT_RU_{op_name}.md"
        out_path.write_text(rendering)
        results[op_name] = {
            "rendering_path": str(out_path),
            "char_count": len(rendering),
            "word_count_approx": len(rendering.split()),
        }
        print(
            f"  wrote {out_path} ({len(rendering)} chars; ~{len(rendering.split())} words)"
        )
        print()

    manifest_path = args.output_dir / "multi_llm_manifest.json"
    manifest = {
        "session": "Phase 3.5b multi-LLM Russian operator robustness",
        "source_extract": args.source_extract,
        "source_char_count": len(source_text),
        "seed": args.seed,
        "operators_invoked": args.operators,
        "results": results,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Manifest: {manifest_path}")
    print()
    print("Next step: each per-operator rendering is re-extracted by the")
    print("standard spine-extraction pipeline; per-operator preservation rates")
    print("compared in CROSS_OPERATOR_PRESERVATION_PB_RU.md.")


if __name__ == "__main__":
    main()
