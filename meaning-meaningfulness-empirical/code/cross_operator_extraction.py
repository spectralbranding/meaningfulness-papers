"""Cross-operator spine extraction — Phase 2-prime / 2.5-prime / 3-prime
retroactive re-extraction of Session H rendering artifacts using GPT-4 as
the extraction operator.

Per feedback_cross_operator_extraction_separation.md HARD RULE (2026-05-27):
when the same LLM both renders prose from a spine AND extracts spine from that
prose in the same session, "extraction" is partly memory reconstruction — not
pure prose→spine inference. The within-operator preservation result is
confounded by within-model context memory.

Correct three-operator pipeline:
- Operator A (orchestrator, Session H Claude): provides source spine; compares;
  reports.
- Operator B (rendering, Session H Claude in Phases 2/2.5/3): receives source
  spine; produces prose.
- Operator C (extraction, GPT-4 via this script): DIFFERENT model from B;
  receives ONLY the prose + the appendix-A codebook; NEVER receives the source
  spine; produces extracted spine.

Per feedback_llm_call_professional_logging.md: every extraction call JSONL-
logged at logs/<phase>_extraction_<extractor>_calls.jsonl.

Renderings re-extracted (Phase 2/2.5/3 — drafting work; the extraction is the
experiment that produces cited P4 evidence):
  - RENDERING_PB_SUBSTACK_PRACTITIONER.md   → Phase 2-prime
  - RENDERING_PA_PRACTITIONER.md             → Phase 2.5-prime
  - RENDERING_FOCAL_PAIR_THIRD_PROSE.md      → Phase 3-prime

Run (BWS-injected; OPENAI_API_KEY required):
    bws run -- uv run --with openai \\
        python [internal path removed]
"""

from __future__ import annotations

import json
import os
import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_call_logger import log_call  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
PAPER_DIR = REPO_ROOT / "research" / "meaningfulness_empirical_companion"
LOGS_DIR = PAPER_DIR / "logs"


# Appendix-A codebook (10 node types + 17 edge types) per paper_a:appendix_A_schema.
CODEBOOK = """
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
- Identify central propositions / observations / methods / findings the prose
  asserts.
- For each node, assign exactly one node-type from the 10-type taxonomy.
- For each node, identify antecedent edges (which prior literature, observation,
  method, or finding does this node depend on?) using the 17-edge-type catalog.
- Capture boundary conditions and stylized facts explicitly when the prose
  invokes them.
- Output STRICTLY VALID YAML matching the schema below; no Markdown, no
  commentary, no preamble. Just the YAML body.

YAML SCHEMA (top-level keys):

```yaml
spine_version: "0.2"
extracted_from: "<file path or rendering name>"
extracted_by: "gpt-4 (operator C; received prose only; no source spine)"
nodes:
  - id: <unique-id-prefix-by-source-paper-like-EM_P1-or-PA_R_P1>
    type: proposition | observation | method | measurement | finding | derivation | rival | robustness_check | limitation | assumption_atom | boundary_condition | stylized_fact
    statement: "<one-paragraph rendering of the node's content>"
    antecedent_edges:
      - target: "<prior literature reference, e.g., Nelson and Winter 1982>"
        edge_type: <extends | applies | tests | contradicts | refines | depends-on | evidences | defines | measures | aggregates | generates | rules-out | bridges | mitigates | relaxes | motivates | provenances>
boundary_conditions: [list of boundary_condition node IDs]
stylized_facts: [list of stylized_fact node IDs]
```

Return ONLY the YAML body. Do not wrap in code fences. Do not include any
explanatory text before or after the YAML.
"""


@dataclass
class RenderingTarget:
    phase: str  # "2", "2.5", "3"
    rendering_path: Path  # input prose-only rendering
    out_spine_path: Path  # output YAML
    description: str  # operation description for logs


TARGETS = [
    RenderingTarget(
        phase="2_prime",
        rendering_path=PAPER_DIR / "RENDERING_PB_SUBSTACK_PRACTITIONER.md",
        out_spine_path=PAPER_DIR
        / "VALIDATION_CASE_PB_SELF_APPLICATION_GPT4_SPINE.yaml",
        description="extract_spine_from_substack_rendering_PB_via_GPT4",
    ),
    RenderingTarget(
        phase="2.5_prime",
        rendering_path=PAPER_DIR / "RENDERING_PA_PRACTITIONER.md",
        out_spine_path=PAPER_DIR / "VALIDATION_CASE_PA_PRACTITIONER_GPT4_SPINE.yaml",
        description="extract_spine_from_PA_practitioner_rendering_via_GPT4",
    ),
    RenderingTarget(
        phase="3_prime",
        rendering_path=PAPER_DIR / "RENDERING_FOCAL_PAIR_THIRD_PROSE.md",
        out_spine_path=PAPER_DIR / "VALIDATION_CASE_PB_FOCAL_THIRD_GPT4_SPINE.yaml",
        description="extract_spine_from_focal_pair_third_rendering_via_GPT4",
    ),
]


def strip_frontmatter(text: str) -> str:
    """Strip YAML frontmatter; pass only the body to the extractor."""
    return re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("ERROR: OPENAI_API_KEY not in environment (use `bws run --` wrapper)")
        sys.exit(1)

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    model = "gpt-4o-2024-08-06"

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    for target in TARGETS:
        if not target.rendering_path.exists():
            print(
                f"[{target.phase}] SKIP — rendering not found: {target.rendering_path}"
            )
            continue

        rendering_full = target.rendering_path.read_text()
        rendering_body = strip_frontmatter(rendering_full)
        print(f"\n=== {target.phase}: {target.rendering_path.name} ===")
        print(f"  prose chars (frontmatter-stripped): {len(rendering_body)}")

        with log_call(
            phase=target.phase,
            operation=target.description,
            operator="gpt-4o",
            endpoint="https://api.openai.com/v1/chat/completions",
            sdk_version="openai>=1.51",
            logs_dir=LOGS_DIR,
            human_in_loop=False,
        ) as logger:
            logger.set_system_prompt(CODEBOOK)
            logger.set_user_prompt(
                "Apply the appendix-A schema to the following prose. Extract "
                "central nodes, classify each by type, identify antecedent edges. "
                "Return YAML only (no Markdown fences, no preamble):\n\n"
                f"{rendering_body}"
            )
            logger.set_parameters(
                {
                    "model": model,
                    "temperature": 0.2,
                    "max_tokens": 4000,
                    "seed": 42,
                }
            )
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": CODEBOOK},
                    {
                        "role": "user",
                        "content": (
                            "Apply the appendix-A schema to the following prose. "
                            "Extract central nodes, classify each by type, identify "
                            "antecedent edges. Return YAML only (no Markdown fences, "
                            "no preamble):\n\n"
                            f"{rendering_body}"
                        ),
                    },
                ],
                temperature=0.2,
                max_tokens=4000,
                seed=42,
            )
            logger.capture_response(resp)
            extracted_yaml = resp.choices[0].message.content or ""
            # Strip accidental code fences
            extracted_yaml = re.sub(r"^```ya?ml\n", "", extracted_yaml)
            extracted_yaml = re.sub(r"\n```\s*$", "", extracted_yaml)
            cost_in = 0.0025 * (resp.usage.prompt_tokens / 1000)
            cost_out = 0.010 * (resp.usage.completion_tokens / 1000)
            logger.set_cost_estimate(cost_in + cost_out)

        target.out_spine_path.write_text(extracted_yaml)
        print(f"  wrote {target.out_spine_path.name}")
        print(
            f"  tokens: {resp.usage.prompt_tokens} in / "
            f"{resp.usage.completion_tokens} out; ~${cost_in + cost_out:.4f}"
        )

    print("\nAll cross-operator extractions complete.")


if __name__ == "__main__":
    main()
