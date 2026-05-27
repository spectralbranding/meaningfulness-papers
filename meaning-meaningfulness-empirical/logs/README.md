# LLM-call logs — Paper B 2026ap v1.3.0 reproducibility artifacts

This directory contains professionally-logged provenance for LLM/model API calls made during the **experimental research** for "Same Meaning, Different Prose: An Empirical Demonstration of Rendering-Equivalence Under Spine-Preservation in Organizational Knowledge Work" (Zharnikov 2026ap, Working Paper v1.3.0).

The logs are part of the paper's reproducibility artifact bundle, mirrored to the public GitHub mirror at Zenodo upload time. License: CC BY 4.0 (same as paper). DOI: shares the paper's Zenodo DOI; no separate DOI.

Source rules: `feedback_llm_call_professional_logging.md` (logging discipline HARD RULE) + `feedback_cross_operator_extraction_separation.md` (three-operator pipeline discipline HARD RULE).

## Scope: experiments vs drafting

Per user direction 2026-05-27, the public log includes ONLY calls that produce empirical evidence cited as a result in `paper.md`. Internal authoring-process calls (drafting assistance, internal peer-review cycles, AI-assisted literature exploration that does not produce a cited result) are NOT in the public log; those entries are kept locally at `logs/internal_only/` and excluded from public-mirror sync.

**Public scope (experimental evidence):**
- Phase 1 Crossref anchor verification (SF1 hallucination audit)
- Phase 2 / 2.5 / 3 rendering operator-B calls (P4 evidence renderers)
- Phase 2 / 2.5 / 3 within-operator extraction calls (within-operator baseline)
- Phase 2-prime / 2.5-prime / 3-prime cross-operator extraction calls (Operator-C cross-operator P4 evidence)
- Phase 3.5b v1.4.0 multi-LLM cross-family rendering + extraction (when executed)

**Internal scope (drafting/research, not published):**
- AI-draft Russian rendering starter (drafting helper for user's v1.4.0 human-native pass)
- Grok review fire cycles (internal peer review of paper draft)
- Any LLM-assisted paper drafting or editing

## Per-phase JSONL files (v1.3.0 release; public scope)

| File | Calls | Operator | What it covers |
|---|---|---|---|
| `phase_1_crossref_anchor_verification_calls.jsonl` | 12 | crossref | Each of the 12 Grok-suggested anchor verifications against the Crossref REST API; resolves DOIs for 2 (A01, A10) and classifies 10 as NF |
| `phase_2_render_PB_spine_to_substack_practitioner_calls.jsonl` | 1 | claude-via-harness (Operator B) | Substack practitioner-register rendering of Paper B's own substrate (1,615w; for Task α self-application) |
| `phase_2_extract_spine_from_substack_rendering_calls.jsonl` | 1 | claude-via-harness (Operator B; within-operator baseline) | Within-operator re-extraction of spine from Substack rendering |
| `phase_2_prime_extract_spine_from_substack_rendering_PB_via_GPT4_calls.jsonl` | 1 | gpt-4o (Operator C; cross-operator) | Cross-operator re-extraction of spine from Substack rendering (prose-only input; no source spine context) |
| `phase_2.5_render_PA_spine_to_substack_practitioner_calls.jsonl` | 1 | claude-via-harness (Operator B) | Substack practitioner-register rendering of Paper A's full theoretical apparatus (2,102w; cross-paper P4 test + Article 1 raw material) |
| `phase_2.5_extract_spine_from_PA_practitioner_rendering_calls.jsonl` | 1 | claude-via-harness (Operator B; within-operator baseline) | Within-operator re-extraction of spine from Paper A practitioner rendering |
| `phase_2.5_prime_extract_spine_from_PA_practitioner_rendering_via_GPT4_calls.jsonl` | 1 | gpt-4o (Operator C; cross-operator) | Cross-operator re-extraction of spine from Paper A practitioner rendering |
| `phase_3_render_focal_pair_shared_substrate_to_linkedin_calls.jsonl` | 1 | claude-via-harness (Operator B) | LinkedIn long-post rendering of focal-pair shared substrate L1-L4 (1,044w; for Task β third rendering) |
| `phase_3_prime_extract_spine_from_focal_pair_third_rendering_via_GPT4_calls.jsonl` | 1 | gpt-4o (Operator C; cross-operator) | Cross-operator re-extraction of spine from LinkedIn rendering |

## Schema (per-call JSONL row)

```json
{
  "log_format_version": "1.0",
  "phase": "<phase identifier; e.g., 1, 2, 2.5, 3, 3.5a, 3.5b, 6>",
  "operation": "<purpose; e.g., crossref_anchor_verification>",
  "operator": "<crossref | claude-via-harness | deepseek | yandexgpt | gigachat | grok | perplexity | ...>",
  "model_version": "<exact model identifier returned by API; e.g., claude-opus-4-7, deepseek-v3-0324, api.crossref.org REST API>",
  "timestamp_utc": "<ISO 8601 UTC>",
  "system_prompt": "<full text; redacted if API-key values accidentally embedded>",
  "user_prompt": "<full text>",
  "parameters": {"temperature": ..., "max_tokens": ..., "seed": ..., "...": "..."},
  "request_id": "<API request ID if returned; null otherwise>",
  "endpoint": "<API endpoint URL>",
  "sdk_version": "<SDK name + version>",
  "response": "<full response text>",
  "response_metadata": {"finish_reason": "stop", "...": "..."},
  "tokens": {"input": <int>, "output": <int>},
  "latency_seconds": <float>,
  "cost_usd_est": <float>,
  "errors": [...],
  "retries": <int>,
  "git_sha_caller": "<git SHA at call time>",
  "python_env_hash": "<uv.lock SHA prefix>",
  "human_in_loop": <bool>,
  "reconstructed_post_hoc": <bool>
}
```

## Reconstructed-post-hoc entries

Logs marked `"reconstructed_post_hoc": true` were assembled from the Claude Code session transcript after the LLM-call professional logging HARD RULE arrived mid-session (Phase 5 of Session H). They reflect honest disclosure of the gap between when the work executed and when structured logging was added. Reconstructed entries lack tokens / latency / cost values for the harness-internal Claude rendering operations (claude-via-harness operator); the Crossref calls in Phase 1 have full reconstruction fidelity because the calling script `audit/scripts/verify_2026ap_postdraft_r1_anchors.py` recorded the requests it made.

Reconstruction script: `research/meaningfulness_empirical_companion/code/reconstruct_session_h_logs.py`. Future research-pass calls use real-time logging via `research/meaningfulness_empirical_companion/code/llm_call_logger.py`.

## Reproduction guide

1. Clone the public mirror at `sbt-papers/meaningfulness-empirical/` (URL filled at Zenodo upload).
2. For each phase, the JSONL log + the artifacts in the paper's main directory (`RENDERING_*.md`, `VALIDATION_CASE_*.yaml`, `*_ISOMORPHISM*.md`) together let an independent reader reproduce the result chain.
3. For Phase 1 anchor verification: rerun `audit/scripts/verify_2026ap_postdraft_r1_anchors.py` against the live Crossref API to confirm the 2 VERIFIED / 10 NF classification (results may drift if Crossref metadata updates; the log preserves point-in-time provenance).
4. For Phases 2, 2.5, 3 Claude renderings: the log captures the system prompt + user prompt + the response summary. Full rendered articles are at `research/meaningfulness_empirical_companion/RENDERING_*.md`. An independent reader can re-render with any AI operator using the same prompts to compare against this paper's renderings.
5. For Phase 3.5b multi-LLM cross-family renderings (v1.4.0 execution): the script `research/meaningfulness_empirical_companion/code/multi_llm_rendering.py` uses `llm_call_logger.py` with real-time logging from invocation; results land in `phase_3.5b_*.jsonl` files at v1.4.0 release.
6. For Phase 6 Grok r2 fire: `audit/scripts/run_grok_review.py` invocation captures raw output to `audit/grok_outputs/2026ap_grok_postdraft_r2.md`; structured JSONL logging lands at `phase_6_grok_r2_calls.jsonl` via the same `llm_call_logger.py` integration.

## Redaction audit

The logger applies redaction patterns at write time:
- API key fragments (sk-..., sk-ant-..., sk-proj-..., AQVN...) → `[REDACTED:api_key]`
- Bearer tokens → `Bearer [REDACTED:token]`
- Authorization header values → `Authorization: [REDACTED]`

Verification grep after each phase:
```bash
grep -iE "(sk-ant-|sk-proj-|AQVN|Bearer [A-Za-z0-9])" logs/*.jsonl   # must return empty
grep -iE "PENDING_UPDATES|SESSION_[A-Z]_(COMPLETION|HANDOFF)|TRIAGE_MEMO|AUDIT_INTERNAL" logs/*.jsonl   # must return empty
```

Post-redaction warnings (if any patterns matched internal-doc references) are written to `REDACTION_WARNINGS.log` in this directory; check there for items flagged for manual review before public-mirror push.

## Cost summary across all logged phases (v1.3.0; public scope)

| Phase | Operator | Calls | Cost USD (est) |
|---|---|---|---|
| 1 | crossref | 12 | 0.00 (Crossref REST API is free for non-commercial query) |
| 2 / 2.5 / 3 | claude-via-harness Operator B + within-operator extraction | 6 | 0.00 (harness-internal; not separately metered) |
| 2-prime / 2.5-prime / 3-prime | gpt-4o Operator C cross-operator extraction | 3 | ~0.04 (tokens: 8,239 in / 2,160 out at gpt-4o pricing) |
| **Total v1.3.0 public scope** | | **21** | **~0.04** |

Internal-only logs (not published): Phase 3.5a AI-draft Russian (drafting helper) + Phase 6 Grok r2 review (internal review). Internal cost: ~$0.15 (Grok r2 only; AI-draft Russian was harness-internal).

## Deferred to v1.4.0 (logged at execution time)

- Phase 3.5b multi-LLM cross-family rendering: ~5 calls × ~$0.06 avg = ~$0.30 + per-operator spine extractions by claude-via-harness (~5 entries, internal)
- Phase 4 inter-coder κ measurement: depends on independent second coder's tool stack; not LLM-operator-mediated; logging not required
- Phase 3.5a human-native Russian rendering: NOT LLM-call (user-produced); no log entry; the AI-draft starter already logged in v1.3.0 phase_3.5a entries

## Related artifacts

- `code/llm_call_logger.py` — logger utility (single-source schema + writer + redaction)
- `code/reconstruct_session_h_logs.py` — post-hoc reconstruction for v1.3.0 release
- `code/multi_llm_rendering.py` — v1.4.0 Phase 3.5b execution-ready script (uses logger from day one)
- `code/null_baseline.py` + `rec_metric.py` + `cost_function_calibration.py` — Paper B's computation scripts (no LLM calls; deterministic Python; logged separately per PAPER_QUALITY_STANDARDS items 37a-37e)
