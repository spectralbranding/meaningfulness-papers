---
phase: "3.5d"
operator: qwen3.6:27b-ollama
role: extractor (cross-extractor robustness — applied to DeepSeek's Chinese rendering only)
language: input=Chinese (Simplified) prose; output=English structured spine (schema-invariant)
source_code_reference: "code/run_phases_3_5c_3_5d.py::EXTRACTION_CODEBOOK + CHINESE_EXTRACTION_USER (same as GPT-4o extractor)"
audit_trail: "Qwen3.6:27b serves as cross-extractor on DeepSeek's Chinese rendering ONLY. B!=C: Qwen (extractor here) is different from DeepSeek (renderer). Qwen self-extracts its own rendering is NOT done (Qwen-rendered → GPT-4o extractor only). This cross-extractor robustness test verifies that the Rec=12 finding for DeepSeek's rendering is extractor-invariant."
sha256_of_prompt_body: "see EXTRACT_FROM_ZH_via_GPT4o.md (codebook system prompt byte-identical; user prompt byte-identical)"
purity_status: CLEAN
cross_operator_compliance: "B != C verified — Qwen3.6:27b extractor applied ONLY to DeepSeek rendering (different from Qwen renderer which rendered its own Chinese text)"
ollama_discipline: "Serial-only per feedback_ollama_serial_only.md; executed AFTER Qwen rendering step (sequential)"
model_digest: "a50eda8ed977ab48a12431878896b27ffd5cef552c17af3317d9623b939a7f1e"
quantization: "Q4_K_M"
---

## System prompt

You are a structural-extraction operator applying the appendix-A schema from
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

(boundary_condition and stylized_fact are also first-class node types.)

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

## User prompt

Apply the appendix-A schema to the following prose (written in Simplified Chinese).
Extract central nodes, classify each by type (in English).
Translate all claims into English in your output.
Return a numbered list only:

{prose}
