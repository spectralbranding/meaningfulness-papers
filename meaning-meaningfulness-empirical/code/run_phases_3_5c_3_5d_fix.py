"""Phase 3.5d fix-pass: retry DeepSeek + Qwen3.6 (think=false) + cross-extractor.

Issues fixed:
1. DeepSeek call returned None response (transient API error). Add retry + safer
   response/usage handling.
2. Qwen3.6:27b is a thinking model — first run consumed all 2000 tokens on the
   `thinking` field with 0 chars in `response`. Set `"think": false` to disable
   reasoning and emit the answer directly.
3. Re-run all downstream steps that depended on DeepSeek/Qwen success:
   - DeepSeek extraction via GPT-4o
   - DeepSeek extraction via Qwen3.6 (cross-extractor robustness; SERIAL)
   - Qwen3.6 rendering extraction via GPT-4o (was OK structurally but extracted
     from empty prose; redo)
   - All preservation computations
4. Update Phase 3.5d manifest with corrected results.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))
from llm_call_logger import log_call  # noqa: E402
from run_phases_3_5c_3_5d import (  # noqa: E402
    SOURCE_ABSTRACT_EN,
    LOCKED_PROPOSITIONS,
    CHINESE_RENDER_PROMPT_SYSTEM,
    CHINESE_RENDER_PROMPT_USER,
    EXTRACTION_CODEBOOK,
    EXTRACTION_USER_PROMPT,
    extract_via_gpt4o,
    compute_preservation_via_gpt4o,
    rec_score,
    audit_prompt_purity,
    PHASE_3_5D_DIR,
    LOGS_DIR,
    SEED,
)

REPO_ROOT = CODE_DIR.parents[3]


def render_with_deepseek_zh_safe(
    source_text: str, openai_key_ds: str
) -> tuple[str | None, str | None]:
    """DeepSeek render with safer response handling + 2 retries."""
    from openai import OpenAI

    client = OpenAI(api_key=openai_key_ds, base_url="https://api.deepseek.com")
    user_prompt = CHINESE_RENDER_PROMPT_USER.format(source_text=source_text)

    last_err = None
    for attempt in range(3):
        with log_call(
            phase="3.5d",
            operation=f"render_PB_abstract_ZH_deepseek_retry_attempt_{attempt+1}",
            operator="deepseek",
            endpoint="https://api.deepseek.com/v1/chat/completions",
            sdk_version="openai>=1.51",
            logs_dir=LOGS_DIR,
        ) as logger:
            logger.set_system_prompt(CHINESE_RENDER_PROMPT_SYSTEM)
            logger.set_user_prompt(user_prompt)
            logger.set_parameters(
                {
                    "model": "deepseek-chat",
                    "temperature": 0.3,
                    "max_tokens": 2000,
                    "attempt": attempt + 1,
                }
            )
            try:
                resp = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": CHINESE_RENDER_PROMPT_SYSTEM},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.3,
                    max_tokens=2000,
                )
                # Safer extraction
                if resp is None or not getattr(resp, "choices", None):
                    raise RuntimeError(f"Empty response object on attempt {attempt+1}")
                content = resp.choices[0].message.content
                if not content:
                    raise RuntimeError(f"Empty content on attempt {attempt+1}")
                logger.capture_response(resp)
                if resp.usage is not None:
                    cost_in = 0.00014 * (resp.usage.prompt_tokens / 1000)
                    cost_out = 0.00028 * (resp.usage.completion_tokens / 1000)
                    logger.set_cost_estimate(cost_in + cost_out)
                logger.set_model_version(getattr(resp, "model", "deepseek-chat"))
                return content, None
            except Exception as e:
                last_err = str(e)
                logger.add_error(last_err)
                if attempt < 2:
                    time.sleep(2**attempt)
                    logger.increment_retry()

    return None, last_err


def render_with_qwen_zh_ollama_nothink(
    source_text: str,
) -> tuple[dict | None, str | None]:
    """Qwen3.6:27b render via Ollama with think=false (disable reasoning)."""
    import httpx

    user_prompt = CHINESE_RENDER_PROMPT_USER.format(source_text=source_text)
    full_prompt = f"{CHINESE_RENDER_PROMPT_SYSTEM}\n\n{user_prompt}"

    start_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    with log_call(
        phase="3.5d",
        operation="render_PB_abstract_ZH_qwen36_27b_ollama_nothink",
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
                "num_predict": 2000,
                "think": False,
            }
        )
        try:
            resp = httpx.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen3.6:27b",
                    "prompt": full_prompt,
                    "think": False,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 2000, "seed": SEED},
                },
                timeout=600.0,
            )
            resp.raise_for_status()
            result = resp.json()
            rendering = result.get("response", "")
            if not rendering:
                raise RuntimeError(
                    "Qwen3.6 returned empty response even with think=false"
                )
            logger.capture_response(result)
            logger.set_model_version("qwen3.6:27b")
            logger._tokens = {
                "input": result.get("prompt_eval_count", 0),
                "output": result.get("eval_count", 0),
            }
        except Exception as e:
            logger.add_error(str(e))
            end_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
            return None, str(e)

    end_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    return {"rendering": rendering, "start_ts": start_ts, "end_ts": end_ts}, None


def extract_via_qwen_ollama_nothink(
    prose: str, phase: str, operation_suffix: str
) -> tuple[dict | None, str | None]:
    """Qwen3.6:27b extraction via Ollama with think=false."""
    import httpx

    user_prompt = EXTRACTION_USER_PROMPT.format(prose=prose)
    full_prompt = f"{EXTRACTION_CODEBOOK}\n\n{user_prompt}"

    start_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    with log_call(
        phase=phase,
        operation=f"extract_spine_{operation_suffix}_via_qwen36_27b_nothink",
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
                "num_predict": 4000,
                "think": False,
            }
        )
        try:
            resp = httpx.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen3.6:27b",
                    "prompt": full_prompt,
                    "think": False,
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 4000, "seed": SEED},
                },
                timeout=600.0,
            )
            resp.raise_for_status()
            result = resp.json()
            extraction = result.get("response", "")
            if not extraction:
                raise RuntimeError("Qwen3.6 returned empty extraction")
            logger.capture_response(result)
            logger.set_model_version("qwen3.6:27b")
            logger._tokens = {
                "input": result.get("prompt_eval_count", 0),
                "output": result.get("eval_count", 0),
            }
        except Exception as e:
            logger.add_error(str(e))
            return None, str(e)

    end_ts = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    return {"extraction": extraction, "start_ts": start_ts, "end_ts": end_ts}, None


def main():
    openai_key = os.environ["OPENAI_API_KEY"].strip()
    deepseek_key = os.environ["DEEPSEEK_API_KEY"].strip()

    print("=" * 70)
    print("Phase 3.5d FIX-PASS — DeepSeek retry + Qwen3.6 think=false")
    print(f"Start: {dt.datetime.now(dt.timezone.utc).isoformat()}")
    print("=" * 70)

    wall_start = time.time()

    # ---- DeepSeek retry ----
    print("\n--- DeepSeek Chinese rendering (with retry) ---")
    t0 = time.time()
    deepseek_zh_rendering, deepseek_zh_error = render_with_deepseek_zh_safe(
        SOURCE_ABSTRACT_EN, deepseek_key
    )
    if deepseek_zh_rendering:
        print(
            f"  OK in {time.time()-t0:.1f}s. Length: {len(deepseek_zh_rendering)} chars"
        )
        ds_path = PHASE_3_5D_DIR / "RENDERING_PB_ABSTRACT_ZH_deepseek.md"
        ds_path.write_text(
            "## 摘要 (DeepSeek)\n\n" + deepseek_zh_rendering + "\n", encoding="utf-8"
        )
        print(f"  Wrote: {ds_path}")
    else:
        print(f"  STILL FAILED after retries: {deepseek_zh_error}")

    # ---- Qwen3.6 retry (SERIAL — single Ollama process at a time) ----
    print("\n--- Qwen3.6:27b (Ollama) Chinese rendering [SERIAL, think=false] ---")
    t0 = time.time()
    qwen_zh_result, qwen_zh_error = render_with_qwen_zh_ollama_nothink(
        SOURCE_ABSTRACT_EN
    )
    qwen_zh_rendering = None
    if qwen_zh_result:
        qwen_zh_rendering = qwen_zh_result["rendering"]
        print(f"  OK in {time.time()-t0:.1f}s. Length: {len(qwen_zh_rendering)} chars")
        qw_path = PHASE_3_5D_DIR / "RENDERING_PB_ABSTRACT_ZH_qwen36_27b_ollama.md"
        qw_path.write_text(
            "## 摘要 (Qwen3.6:27b Ollama)\n\n" + qwen_zh_rendering + "\n",
            encoding="utf-8",
        )
        print(f"  Wrote: {qw_path}")
    else:
        print(f"  FAILED: {qwen_zh_error}")

    # ---- Cross-extractor: Qwen extracts DeepSeek rendering (SERIAL — after Qwen render) ----
    qwen_ds_result = None
    qwen_ds_error = None
    if deepseek_zh_rendering:
        print(
            "\n--- Cross-extractor: Qwen3.6:27b (Ollama) extracts DeepSeek ZH rendering [SERIAL, think=false] ---"
        )
        t0 = time.time()
        qwen_ds_result, qwen_ds_error = extract_via_qwen_ollama_nothink(
            deepseek_zh_rendering, "3.5d", "ZH_deepseek_via_qwen36"
        )
        if qwen_ds_result:
            print(f"  OK in {time.time()-t0:.1f}s")
            ex_path = (
                PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_deepseek_via_qwen36_27b.md"
            )
            ex_path.write_text(qwen_ds_result["extraction"], encoding="utf-8")
            print(f"  Wrote: {ex_path}")
        else:
            print(f"  FAILED: {qwen_ds_error}")

    # ---- GPT-4o extractions for DeepSeek + Qwen renderings ----
    deepseek_zh_extraction = None
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

    qwen_zh_extraction = None
    if qwen_zh_rendering:
        print("\n--- Extracting Qwen3.6 ZH rendering (GPT-4o) [B!=C] ---")
        t0 = time.time()
        qwen_zh_extraction = extract_via_gpt4o(
            qwen_zh_rendering, openai_key, "3.5d", "ZH_qwen36_27b_ollama"
        )
        print(f"  Done in {time.time()-t0:.1f}s")
        ex_path = (
            PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_qwen36_27b_ollama_via_GPT4o.md"
        )
        ex_path.write_text(qwen_zh_extraction, encoding="utf-8")
        print(f"  Wrote: {ex_path}")

    # ---- Preservation ----
    deepseek_zh_preservation = None
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

    if qwen_ds_result and qwen_ds_result.get("extraction"):
        print(
            "\n--- Preservation: DeepSeek ZH (Qwen3.6 extractor — cross-extractor robustness) ---"
        )
        deepseek_zh_preservation_qwen = compute_preservation_via_gpt4o(
            qwen_ds_result["extraction"],
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

    # ---- Update manifest with corrected results ----
    manifest_path = PHASE_3_5D_DIR / "multi_llm_manifest.json"
    manifest = json.loads(manifest_path.read_text())

    # Update renderers
    if deepseek_zh_rendering:
        manifest["renderers"]["deepseek"]["status"] = "SUCCESS"
        manifest["renderers"]["deepseek"]["error"] = None
        manifest["renderers"]["deepseek"][
            "rendering_path"
        ] = "phase_3_5d_runs/RENDERING_PB_ABSTRACT_ZH_deepseek.md"
        manifest["renderers"]["deepseek"]["char_count"] = len(deepseek_zh_rendering)
        manifest["renderers"]["deepseek"][
            "retry_note"
        ] = "First attempt returned None response (transient API error); succeeded on retry."

    if qwen_zh_result:
        manifest["renderers"]["qwen36_27b_ollama"]["status"] = "SUCCESS"
        manifest["renderers"]["qwen36_27b_ollama"]["char_count"] = len(
            qwen_zh_rendering
        )
        manifest["renderers"]["qwen36_27b_ollama"]["ollama_start_ts"] = qwen_zh_result[
            "start_ts"
        ]
        manifest["renderers"]["qwen36_27b_ollama"]["ollama_end_ts"] = qwen_zh_result[
            "end_ts"
        ]
        manifest["renderers"]["qwen36_27b_ollama"]["think_disabled"] = True
        manifest["renderers"]["qwen36_27b_ollama"]["think_note"] = (
            "Qwen3.6:27b is a thinking model — first run consumed all 2000 tokens on internal "
            "reasoning, leaving empty response. Re-ran with Ollama 'think': false to disable "
            "reasoning and emit answer directly."
        )

    # Update Ollama serialization log
    manifest["ollama_serialization"]["qwen_rendering"] = {
        "start_ts": qwen_zh_result["start_ts"] if qwen_zh_result else "FAILED",
        "end_ts": qwen_zh_result["end_ts"] if qwen_zh_result else "FAILED",
        "model": "qwen3.6:27b",
        "digest_prefix": "a50eda8ed977ab48a124",
        "think_disabled": True,
    }
    if qwen_ds_result:
        manifest["ollama_serialization"]["qwen_extraction_deepseek"] = {
            "start_ts": qwen_ds_result["start_ts"],
            "end_ts": qwen_ds_result["end_ts"],
            "model": "qwen3.6:27b",
            "think_disabled": True,
            "note": "Executes AFTER Qwen rendering completes; strict serial order maintained",
        }

    # Update preservation
    manifest["preservation"]["deepseek_zh_gpt4o_extractor"] = deepseek_zh_preservation
    manifest["preservation"]["qwen36_zh_gpt4o_extractor"] = qwen_zh_preservation
    manifest["preservation"][
        "deepseek_zh_qwen36_extractor_robustness"
    ] = deepseek_zh_preservation_qwen

    # Add fix-pass note
    manifest["fix_pass_notes"] = {
        "timestamp_utc": dt.datetime.now(dt.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "issue_1": "DeepSeek first attempt returned None response (transient API). Retried successfully.",
        "issue_2": "Qwen3.6:27b first attempt consumed all tokens on internal thinking (thinking-model behavior). Re-ran with Ollama think=false flag.",
        "fix_script": "code/run_phases_3_5c_3_5d_fix.py",
    }
    manifest["timestamp_utc_fix"] = (
        dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    )

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n  Updated manifest: {manifest_path}")

    wall_elapsed = time.time() - wall_start
    print("\n" + "=" * 70)
    print(f"Fix-pass complete in {wall_elapsed/60:.1f} minutes")
    print("=" * 70)

    print("\nPhase 3.5d FINAL results:")
    print(f"  DeepSeek:    {'OK' if deepseek_zh_rendering else 'FAILED'}")
    if deepseek_zh_preservation:
        s = deepseek_zh_preservation["summary"]
        print(
            f"    Rec={rec_score(deepseek_zh_preservation)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )
    print(f"  Qwen3.6:27b: {'OK' if qwen_zh_result else 'FAILED'}")
    if qwen_zh_preservation:
        s = qwen_zh_preservation["summary"]
        print(
            f"    Rec={rec_score(qwen_zh_preservation)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )
    print(f"  Cross-extractor (DeepSeek via Qwen3.6):")
    if deepseek_zh_preservation_qwen:
        s = deepseek_zh_preservation_qwen["summary"]
        print(
            f"    Rec={rec_score(deepseek_zh_preservation_qwen)} | strict={s['strict']} semantic={s['semantic']} missing={s['missing']}"
        )


if __name__ == "__main__":
    main()
