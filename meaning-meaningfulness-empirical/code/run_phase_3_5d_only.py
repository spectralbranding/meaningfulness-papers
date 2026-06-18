"""Phase 3.5d-only runner.

Imports the rendering / extraction / preservation functions from
run_phases_3_5c_3_5d.py and executes Phase 3.5d (Chinese rendering) only.
Phase 3.5c (Russian native LLM retry) has already completed in a prior run;
re-running it would overwrite valid outputs and waste API budget.

The Phase 3.5d prep artifacts (TRANSLATION_REFERENCE_zh_v1.md,
PROMPT_BACK_TRANSLATION_zh_v1.md, PROMPT_TEMPLATE_zh_v1.md) already exist
in phase_3_5d_runs/ and are reused as-is.

Run command:

    cd [internal path removed]
    uv run python [internal path removed]
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PAPER_DIR / "code"))

# Import everything we need from the main script.
from run_phases_3_5c_3_5d import (  # noqa: E402
    PHASE_3_5D_DIR,
    SOURCE_ABSTRACT_EN,
    audit_prompt_purity,
    compute_preservation_via_gpt4o,
    extract_via_gpt4o,
    extract_via_qwen_ollama,
    rec_score,
    render_with_claude_opus_zh,
    render_with_deepseek_zh,
    render_with_qwen_zh_ollama,
)


def main() -> int:
    wall_start = time.time()
    PHASE_3_5D_DIR.mkdir(parents=True, exist_ok=True)

    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

    missing = []
    if not openai_key:
        missing.append("OPENAI_API_KEY")
    if not deepseek_key:
        missing.append("DEEPSEEK_API_KEY")
    if not anthropic_key:
        missing.append("ANTHROPIC_API_KEY")
    if missing:
        print(f"Missing env vars: {missing}")
        return 2

    # Verify Phase 3.5d prep artifacts exist.
    for fname in (
        "TRANSLATION_REFERENCE_zh_v1.md",
        "PROMPT_BACK_TRANSLATION_zh_v1.md",
        "PROMPT_TEMPLATE_zh_v1.md",
    ):
        p = PHASE_3_5D_DIR / fname
        if not p.exists():
            print(f"Missing Phase 3.5d prep artifact: {p}")
            return 3

    print("=" * 70)
    print("PHASE 3.5d: Chinese-Language Rendering")
    print("=" * 70)

    # -----------------------------------------------------------------
    # DeepSeek (API)
    # -----------------------------------------------------------------
    deepseek_zh_rendering = None
    deepseek_zh_error = None
    print("\n--- DeepSeek Chinese rendering ---")
    t0 = time.time()
    try:
        deepseek_zh_rendering = render_with_deepseek_zh(SOURCE_ABSTRACT_EN)
        print(
            f"  OK in {time.time()-t0:.1f}s. Length: {len(deepseek_zh_rendering)} chars"
        )
        (PHASE_3_5D_DIR / "RENDERING_PB_ABSTRACT_ZH_deepseek.md").write_text(
            "## 摘要 (DeepSeek)\n\n" + deepseek_zh_rendering + "\n",
            encoding="utf-8",
        )
    except Exception as e:
        deepseek_zh_error = str(e)
        print(f"  ERROR: {deepseek_zh_error}")

    # -----------------------------------------------------------------
    # Claude Opus (API)
    # -----------------------------------------------------------------
    claude_zh_rendering = None
    claude_zh_error = None
    print("\n--- Claude Opus Chinese rendering ---")
    t0 = time.time()
    try:
        claude_zh_rendering = render_with_claude_opus_zh(SOURCE_ABSTRACT_EN)
        print(
            f"  OK in {time.time()-t0:.1f}s. Length: {len(claude_zh_rendering)} chars"
        )
        (PHASE_3_5D_DIR / "RENDERING_PB_ABSTRACT_ZH_claude_opus.md").write_text(
            "## 摘要 (Claude Opus)\n\n" + claude_zh_rendering + "\n",
            encoding="utf-8",
        )
    except Exception as e:
        claude_zh_error = str(e)
        print(f"  ERROR: {claude_zh_error}")

    # -----------------------------------------------------------------
    # Qwen3.6:27b (Ollama local; SERIAL discipline)
    # -----------------------------------------------------------------
    qwen_zh_result = None
    qwen_zh_rendering = None
    qwen_zh_error = None
    print("\n--- Qwen3.6:27b Ollama Chinese rendering (serial discipline) ---")
    t0 = time.time()
    try:
        qwen_zh_result = render_with_qwen_zh_ollama(SOURCE_ABSTRACT_EN)
        qwen_zh_rendering = qwen_zh_result["text"]
        print(f"  OK in {time.time()-t0:.1f}s. Length: {len(qwen_zh_rendering)} chars")
        (PHASE_3_5D_DIR / "RENDERING_PB_ABSTRACT_ZH_qwen36_27b_ollama.md").write_text(
            "## 摘要 (Qwen3.6:27b @ Ollama)\n\n" + qwen_zh_rendering + "\n",
            encoding="utf-8",
        )
    except Exception as e:
        qwen_zh_error = str(e)
        print(f"  ERROR: {qwen_zh_error}")

    # -----------------------------------------------------------------
    # Extraction via GPT-4o on all three Chinese renderings
    # -----------------------------------------------------------------
    print("\n--- GPT-4o extraction on Chinese renderings ---")
    deepseek_zh_extracted = None
    claude_zh_extracted = None
    qwen_zh_extracted = None

    if deepseek_zh_rendering:
        try:
            deepseek_zh_extracted = extract_via_gpt4o(
                deepseek_zh_rendering, openai_key, "3.5d", "ZH_deepseek"
            )
            (
                PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_deepseek_via_GPT4o.md"
            ).write_text(deepseek_zh_extracted, encoding="utf-8")
            print("  DeepSeek -> GPT-4o: OK")
        except Exception as e:
            print(f"  DeepSeek -> GPT-4o ERROR: {e}")

    if claude_zh_rendering:
        try:
            claude_zh_extracted = extract_via_gpt4o(
                claude_zh_rendering, openai_key, "3.5d", "ZH_claude_opus"
            )
            (
                PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_claude_opus_via_GPT4o.md"
            ).write_text(claude_zh_extracted, encoding="utf-8")
            print("  Claude Opus -> GPT-4o: OK")
        except Exception as e:
            print(f"  Claude Opus -> GPT-4o ERROR: {e}")

    if qwen_zh_rendering:
        try:
            qwen_zh_extracted = extract_via_gpt4o(
                qwen_zh_rendering, openai_key, "3.5d", "ZH_qwen36_27b_ollama"
            )
            (
                PHASE_3_5D_DIR
                / "EXTRACTED_SPINE_FROM_ZH_qwen36_27b_ollama_via_GPT4o.md"
            ).write_text(qwen_zh_extracted, encoding="utf-8")
            print("  Qwen3.6:27b -> GPT-4o: OK")
        except Exception as e:
            print(f"  Qwen3.6:27b -> GPT-4o ERROR: {e}")

    # -----------------------------------------------------------------
    # Cross-extractor: Qwen3.6:27b on DeepSeek's Chinese rendering (Ollama serial)
    # -----------------------------------------------------------------
    print(
        "\n--- Qwen3.6:27b cross-extractor on DeepSeek's Chinese rendering (serial) ---"
    )
    deepseek_zh_extracted_via_qwen = None
    if deepseek_zh_rendering:
        try:
            qwen_extract_result = extract_via_qwen_ollama(
                deepseek_zh_rendering, "3.5d", "ZH_deepseek"
            )
            deepseek_zh_extracted_via_qwen = qwen_extract_result["text"]
            (
                PHASE_3_5D_DIR / "EXTRACTED_SPINE_FROM_ZH_deepseek_via_qwen36_27b.md"
            ).write_text(deepseek_zh_extracted_via_qwen, encoding="utf-8")
            print("  DeepSeek -> Qwen3.6:27b extractor: OK")
        except Exception as e:
            print(f"  DeepSeek -> Qwen3.6:27b extractor ERROR: {e}")

    # -----------------------------------------------------------------
    # Preservation measurement
    # -----------------------------------------------------------------
    print("\n--- Preservation measurement ---")
    preservation_results: dict[str, dict] = {}

    if deepseek_zh_extracted:
        try:
            p = compute_preservation_via_gpt4o(
                deepseek_zh_extracted, openai_key, "3.5d", "ZH_deepseek"
            )
            (PHASE_3_5D_DIR / "PRESERVATION_ZH_deepseek_vs_LOCKED.json").write_text(
                json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            preservation_results["deepseek"] = p
            print(f"  DeepSeek preservation: Rec={rec_score(p)} {p['summary']}")
        except Exception as e:
            print(f"  DeepSeek preservation ERROR: {e}")

    if claude_zh_extracted:
        try:
            p = compute_preservation_via_gpt4o(
                claude_zh_extracted, openai_key, "3.5d", "ZH_claude_opus"
            )
            (PHASE_3_5D_DIR / "PRESERVATION_ZH_claude_opus_vs_LOCKED.json").write_text(
                json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            preservation_results["claude_opus"] = p
            print(f"  Claude Opus preservation: Rec={rec_score(p)} {p['summary']}")
        except Exception as e:
            print(f"  Claude Opus preservation ERROR: {e}")

    if qwen_zh_extracted:
        try:
            p = compute_preservation_via_gpt4o(
                qwen_zh_extracted, openai_key, "3.5d", "ZH_qwen36_27b_ollama"
            )
            (
                PHASE_3_5D_DIR / "PRESERVATION_ZH_qwen36_27b_ollama_vs_LOCKED.json"
            ).write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
            preservation_results["qwen36_27b_ollama"] = p
            print(f"  Qwen3.6:27b preservation: Rec={rec_score(p)} {p['summary']}")
        except Exception as e:
            print(f"  Qwen3.6:27b preservation ERROR: {e}")

    if deepseek_zh_extracted_via_qwen:
        try:
            p = compute_preservation_via_gpt4o(
                deepseek_zh_extracted_via_qwen,
                openai_key,
                "3.5d",
                "ZH_deepseek_via_qwen36_extractor",
            )
            (
                PHASE_3_5D_DIR
                / "PRESERVATION_ZH_deepseek_via_qwen36_extractor_vs_LOCKED.json"
            ).write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
            preservation_results["deepseek_via_qwen36_extractor"] = p
            print(
                f"  Cross-extractor (DeepSeek via Qwen): Rec={rec_score(p)} {p['summary']}"
            )
        except Exception as e:
            print(f"  Cross-extractor preservation ERROR: {e}")

    # -----------------------------------------------------------------
    # Manifest
    # -----------------------------------------------------------------
    purity_audit = audit_prompt_purity(
        (PHASE_3_5D_DIR / "PROMPT_TEMPLATE_zh_v1.md").read_text(encoding="utf-8"),
        "Chinese",
    )
    manifest = {
        "phase": "3.5d",
        "description": "Chinese-language rendering — DeepSeek + Claude Opus + Qwen3.6:27b (Ollama local)",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_abstract_chars": len(SOURCE_ABSTRACT_EN),
        "seed": 42,
        "cross_operator_discipline": {
            "rule": "B != C (renderer != extractor); HARD RULE per feedback_cross_operator_extraction_separation.md",
            "deepseek": "renderer=DeepSeek; extractors=GPT-4o + Qwen3.6:27b (both different from DeepSeek; both valid)",
            "claude_opus": "renderer=Claude Opus; extractor=GPT-4o (different from Claude; valid)",
            "qwen36_27b": "renderer=Qwen3.6:27b@Ollama; extractor=GPT-4o (different from Qwen; valid)",
        },
        "ollama_serial_discipline": {
            "rule": "Ollama calls strictly one-at-a-time per feedback_ollama_serial_only.md",
            "ollama_calls_in_phase_3_5d": [
                "render_with_qwen_zh_ollama (qwen3.6:27b @ digest a50eda8ed977)",
                "extract_via_qwen_ollama on DeepSeek's Chinese rendering (qwen3.6:27b)",
            ],
            "execution_order": "rendering -> cross-extractor extraction (sequential; no concurrent Ollama)",
        },
        "prompt_purity_certification": {
            "phase": "3.5d",
            "language": "Chinese (Simplified)",
            "prompt_files": [
                "phase_3_5d_runs/PROMPT_TEMPLATE_zh_v1.md",
            ],
            "purity_audit": purity_audit,
            "native_register": "学术体 (academic register), Simplified Chinese",
            "native_register_confirmation": (
                "Hand-written; reviewed token-by-token; no English structural framing; no mixed-language headers. "
                "Latin tokens: SMJ (journal abbreviation, permitted per protocol). "
                "Back-translation via GPT-4o (task-isolated) recorded in PROMPT_BACK_TRANSLATION_zh_v1.md."
            ),
            "back_translation": {
                "operator": "GPT-4o (task-isolated from translation step)",
                "back_translation_path": "phase_3_5d_runs/PROMPT_BACK_TRANSLATION_zh_v1.md",
                "author_spot_check": "back-translation preserves intent (academic-register rewrite, SMJ reference, retain claims/numbers/citations, no preamble)",
            },
            "certified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "certified_by": "experiment script (automated audit) + author verification",
        },
        "renderers": {
            "deepseek": {
                "status": "SUCCESS" if deepseek_zh_rendering else "ERROR",
                "error": deepseek_zh_error,
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
                "rendering_path": (
                    "phase_3_5d_runs/RENDERING_PB_ABSTRACT_ZH_claude_opus.md"
                    if claude_zh_rendering
                    else None
                ),
                "char_count": len(claude_zh_rendering) if claude_zh_rendering else 0,
            },
            "qwen36_27b_ollama": {
                "status": "SUCCESS" if qwen_zh_rendering else "ERROR",
                "error": qwen_zh_error,
                "rendering_path": (
                    "phase_3_5d_runs/RENDERING_PB_ABSTRACT_ZH_qwen36_27b_ollama.md"
                    if qwen_zh_rendering
                    else None
                ),
                "char_count": len(qwen_zh_rendering) if qwen_zh_rendering else 0,
                "model_digest": "a50eda8ed977ab48a12431878896b27ffd5cef552c17af3317d9623b939a7f1e",
                "quantization": "Q4_K_M",
                "endpoint": "http://localhost:11434/api/generate",
            },
        },
        "extraction_results": {
            "primary_extractor": "gpt-4o-2024-08-06",
            "secondary_extractor": "qwen3.6:27b @ Ollama (cross-extractor robustness on DeepSeek's rendering only)",
            "deepseek_via_gpt4o": {
                "status": "SUCCESS" if deepseek_zh_extracted else "ERROR"
            },
            "claude_opus_via_gpt4o": {
                "status": "SUCCESS" if claude_zh_extracted else "ERROR"
            },
            "qwen36_27b_via_gpt4o": {
                "status": "SUCCESS" if qwen_zh_extracted else "ERROR"
            },
            "deepseek_via_qwen36": {
                "status": "SUCCESS" if deepseek_zh_extracted_via_qwen else "ERROR"
            },
        },
        "preservation": preservation_results,
        "rec_scores": {k: rec_score(v) for k, v in preservation_results.items()},
    }

    manifest_path = PHASE_3_5D_DIR / "multi_llm_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nWrote Phase 3.5d manifest: {manifest_path}")

    wall_elapsed = time.time() - wall_start
    print("\n" + "=" * 70)
    print("PHASE 3.5d SUMMARY")
    print("=" * 70)
    print(f"Wall-clock: {wall_elapsed/60:.1f} minutes")
    for name, p in preservation_results.items():
        s = p["summary"]
        print(
            f"  {name:35s}  Rec={rec_score(p):>2}  "
            f"strict={s['strict']} semantic={s['semantic']} "
            f"missing={s['missing']} contradicted={s['contradicted']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
