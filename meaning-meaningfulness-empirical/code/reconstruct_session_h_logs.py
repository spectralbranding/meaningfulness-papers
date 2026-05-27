"""Post-hoc reconstruction of LLM-call logs for Session H phases that
executed BEFORE feedback_llm_call_professional_logging.md HARD RULE arrived.

Per the rule's "How to apply (post-hoc for Claude Code harness work)" section,
reconstructed entries are marked `"human_in_loop": true` and
`"reconstructed_post_hoc": true` for honest disclosure.

Covers:
- Phase 1: Crossref bibliographic-verification calls (12 queries)
- Phase 2: Claude harness rendering — Paper B substrate → Substack practitioner article
- Phase 2.5: Claude harness rendering — Paper A substrate → Substack practitioner article
- Phase 3: Claude harness rendering — focal-pair shared substrate → LinkedIn long-post
- Phase 3.5a: Claude harness draft — Paper B abstract → Russian AI-draft starter

Phase 3.5b execution is deferred to v1.1.0 (BWS keys verified; protocol locked;
script execution-ready); real-time logging via llm_call_logger.py will run at
v1.1.0 execution.

Phase 6 Grok r2 fire happens AFTER this reconstruction lands; it logs in real-time
via llm_call_logger.py inside run_grok_review.py.
"""

from __future__ import annotations

from pathlib import Path

from llm_call_logger import log_call_post_hoc

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"


def reconstruct_phase_1() -> None:
    """12 Crossref queries from verify_2026ap_postdraft_r1_anchors.py."""
    anchors = [
        (
            "A01",
            "Kaplan, S., & Vakili, K. (2015). The double-edged sword of recombination in breakthrough innovation. SMJ.",
            "Kaplan Vakili",
            "10.1002/smj.2294",
        ),
        (
            "A02",
            "Felin, T., & Zenger, T. R. (2023). The theory of the firm and AI: Beyond black boxes. Strategy Science.",
            "Felin Zenger",
            None,
        ),
        (
            "A03",
            "Raisch, S., & Furr, N. (2024). The generative lens: AI as a catalyst for new theory. Academy of Management Review.",
            "Raisch Furr",
            None,
        ),
        (
            "A04",
            "Puranam, P., et al. (2024). Generative AI and the future of organizational theory. Organization Science.",
            "Puranam",
            None,
        ),
        (
            "A05",
            "Girotra, K., Meincke, L., Terwiesch, C., & Ulrich, K. T. (2023). Ideas are dimes a dozen: The value of ideation in innovation contests. Management Science.",
            "Girotra Meincke Terwiesch Ulrich",
            None,
        ),
        (
            "A06",
            "Lifshitz-Assaf, H., et al. (2024). AI and the transformation of R&D. Research Policy.",
            "Lifshitz-Assaf",
            None,
        ),
        (
            "A07",
            "Bingham, C. B., & Eisenhardt, K. M. (2024). The search for simplicity in strategy. SMJ.",
            "Bingham Eisenhardt",
            None,
        ),
        (
            "A08",
            "Teece, D. J. (2023). Dynamic capabilities in the age of AI. Industrial and Corporate Change.",
            "Teece",
            None,
        ),
        (
            "A09",
            "von Krogh, G., et al. (2024). Artificial intelligence in management: A review and research agenda. Journal of Management.",
            "von Krogh",
            None,
        ),
        (
            "A10",
            "Levinthal, D., & March, J. G. (1993). The myopia of learning.",
            "Levinthal March",
            "10.1002/smj.4250141009",
        ),
        (
            "A11",
            "Camuffo, A., et al. (2024). Scientific decision-making and the replication crisis in management. SMJ.",
            "Camuffo",
            None,
        ),
        (
            "A12",
            "Ethiraj, S. K., et al. (2024). The next frontier in strategy research: Computational approaches. SMJ.",
            "Ethiraj",
            None,
        ),
    ]
    for anchor_id, claim, author_query, resolved_doi in anchors:
        log_call_post_hoc(
            phase="1",
            operation="crossref_anchor_verification",
            operator="crossref",
            model_version="api.crossref.org REST API",
            system_prompt="(none; REST API)",
            user_prompt=(
                "GET https://api.crossref.org/works?"
                f"query.title=<title-of-{anchor_id}>&query.author={author_query}&rows=5"
            ),
            response=(
                f"Resolved to {resolved_doi}; VERIFIED"
                if resolved_doi
                else "No exact title+author+year match within rows=5; classified NF"
            ),
            parameters={"rows": 5, "user_agent": "Paper2026ap-anchor-verifier/0.1"},
            endpoint="https://api.crossref.org/works",
            sdk_version="urllib.request stdlib",
            cost_usd_est=0.0,  # Crossref is free
            human_in_loop=False,
            logs_dir=LOGS_DIR,
        )


def reconstruct_phase_2() -> None:
    """Claude harness rendering — Paper B substrate → Substack practitioner article."""
    log_call_post_hoc(
        phase="2",
        operation="render_PB_spine_to_substack_practitioner",
        operator="claude-via-harness",
        model_version="claude-opus-4-7",
        system_prompt=(
            "Session H Phase 2 Task α: render Paper B v1.0.0's SPINE.yaml v0.3.0 into a "
            "1,500-word Substack practitioner-register article. Different audience (CMO/strategy-"
            "director tier; not tier-1 academic); different prose conventions (named-case "
            "anecdotes; no mathematical notation); different length (one-quarter the academic "
            "word count); different tone (declarative rather than hedged)."
        ),
        user_prompt=(
            "Re-render Paper B's central P4-demonstration claim + Rec=4 evidence + "
            "boundary conditions + self-application + AI cost asymmetry into Substack "
            "practitioner register. Output: RENDERING_PB_SUBSTACK_PRACTITIONER.md."
        ),
        response=(
            "Output saved to research/meaningfulness_empirical_companion/"
            "RENDERING_PB_SUBSTACK_PRACTITIONER.md (1,615 words; frontmatter with source-spine "
            "pointer + expected-preservation-set; ~80 paragraphs; named-case examples GitLab + "
            "Stripe + audit-memo; three first-moves section)."
        ),
        parameters={
            "medium": "Substack standalone article",
            "target_length_words": 1500,
            "audience": "senior practitioners",
        },
        tokens={"input": 0, "output": 0},  # harness-internal; not separately metered
        cost_usd_est=0.0,
        human_in_loop=True,
        logs_dir=LOGS_DIR,
    )
    # Spine re-extraction by Claude (separate harness-internal operation)
    log_call_post_hoc(
        phase="2",
        operation="extract_spine_from_substack_rendering",
        operator="claude-via-harness",
        model_version="claude-opus-4-7",
        system_prompt=(
            "Apply paper_a:appendix_B_protocol in reverse: read Substack rendering as "
            "fresh source; identify central propositions / observations / methods / findings; "
            "classify each into the 10-node-type taxonomy; trace antecedent edges using 17-edge "
            "catalog. Produce YAML spine with RPB_ node prefix."
        ),
        user_prompt="Re-extract spine from RENDERING_PB_SUBSTACK_PRACTITIONER.md",
        response=(
            "Output: VALIDATION_CASE_PB_SELF_APPLICATION_SPINE.yaml (RPB_O1..O3 + RPB_M1-M2 + "
            "RPB_F1-F4 + RPB_BC_VC/PROP/AUD/VOL/SUB + propositions block + recommended_actions "
            "+ limitations + rendering_choices). Per-node maps_to_source_spine + map_quality "
            "annotations. Compared to SPINE.yaml v0.3.1: 11/14 strict, 14/14 semantic, 0 contradicted."
        ),
        parameters={
            "codebook": "paper_a:appendix_A_schema (10 node types; 17 edge types)"
        },
        cost_usd_est=0.0,
        human_in_loop=True,
        logs_dir=LOGS_DIR,
    )


def reconstruct_phase_2_5() -> None:
    log_call_post_hoc(
        phase="2.5",
        operation="render_PA_spine_to_substack_practitioner",
        operator="claude-via-harness",
        model_version="claude-opus-4-7",
        system_prompt=(
            "Session H Phase 2.5 cross-paper P4: render Paper A 2026ao's SPINE.yaml v0.7.3 into "
            "a Substack practitioner-register article ~2,000-2,500 words. Dual-purpose: research "
            "artifact + Article 1 raw material for forthcoming Substack series."
        ),
        user_prompt=(
            "Render Paper A's full theoretical apparatus (Operator role + three-layer L→S→R + "
            "P1-P4 propositions + SF1-SF4 stylized facts + C1-C4 boundary conditions + spine-"
            "first protocol + Heisenberg-Schrödinger appendix + three Design Propositions) into "
            "practitioner Substack register. Output: RENDERING_PA_PRACTITIONER.md."
        ),
        response=(
            "Output saved to RENDERING_PA_PRACTITIONER.md (2,102 words). Five-part structure: "
            "three-layer decomposition + Operator role + cost asymmetry + four stylized facts + "
            "boundary conditions + three first moves. Greek symbols selectively retained where "
            "they ARE the explanation (σ-direction SF1 failure mode); dropped elsewhere; math "
            "notation dropped; self-referential audit incidents dropped per "
            "feedback_audit_record_discipline."
        ),
        parameters={
            "medium": "Substack standalone article",
            "target_length_words": 2300,
            "dual_purpose": "research artifact + Article 1 raw material",
        },
        cost_usd_est=0.0,
        human_in_loop=True,
        logs_dir=LOGS_DIR,
    )
    log_call_post_hoc(
        phase="2.5",
        operation="extract_spine_from_PA_practitioner_rendering",
        operator="claude-via-harness",
        model_version="claude-opus-4-7",
        system_prompt=(
            "Apply paper_a:appendix_B_protocol in reverse to PA practitioner rendering. "
            "Compare against Paper A SPINE.yaml v0.7.3 locked-set of 15 elements."
        ),
        user_prompt="Re-extract spine from RENDERING_PA_PRACTITIONER.md and compare to Paper A locked set",
        response=(
            "Output: VALIDATION_CASE_PA_PRACTITIONER_SPINE.yaml + CROSS_PAPER_P4_ISOMORPHISM.md. "
            "Preservation: 12/15 strict, 15/15 semantic, 0 contradicted. Three partial "
            "preservations (PA3 P2 organizational-outcome; PA4 cost-function functional forms; "
            "PA15 Design Propositions formal structure) match same rendering-cost frontier as "
            "Phase 2 (L12 versioning trajectory; L13 three-layer L; L14 cost-function forms)."
        ),
        parameters={"codebook": "paper_a:appendix_A_schema", "locked_set_size": 15},
        cost_usd_est=0.0,
        human_in_loop=True,
        logs_dir=LOGS_DIR,
    )


def reconstruct_phase_3() -> None:
    log_call_post_hoc(
        phase="3",
        operation="render_focal_pair_shared_substrate_to_linkedin",
        operator="claude-via-harness",
        model_version="claude-opus-4-7",
        system_prompt=(
            "Session H Phase 3 Task β: render focal-pair shared substrate (L1-L4 from "
            "TWIN_PAIR_ISOMORPHISM_PB_FOCAL.md §2) into a 1,000-word LinkedIn long-post. "
            "Practitioner register; arrow-bullet structure for L1-L4; named antecedents in plain "
            "prose; no equations; light citation."
        ),
        user_prompt=(
            "Render L1-L4 (DCs as identifiable processes / learning mechanisms drive evolution / "
            "cross-firm commonalities at best-practice level / market-task contingency) into "
            "LinkedIn long-post. Output: RENDERING_FOCAL_PAIR_THIRD_PROSE.md."
        ),
        response=(
            "Output: RENDERING_FOCAL_PAIR_THIRD_PROSE.md (1,044 words; arrow bullets; named "
            "antecedents Nelson-Winter 1982 + Levitt-March 1988 + Teece-Pisano-Shuen 1997 + "
            "Eisenhardt-Tabrizi 1995 explicit; SMS @-tag + 5 hashtags per LinkedIn outperformance "
            "pattern). Re-extraction yields Rec(G_third, G_shared_spine) = 4 with all four "
            "antecedent edges preserved + L5-L7 unlinked propositions accurately rendered as "
            "not-in-the-other-paper."
        ),
        parameters={"medium": "LinkedIn long-post", "target_length_words": 1000},
        cost_usd_est=0.0,
        human_in_loop=True,
        logs_dir=LOGS_DIR,
    )


def reconstruct_phase_3_5a() -> None:
    log_call_post_hoc(
        phase="3.5a",
        operation="ai_draft_russian_rendering_for_user_qc",
        operator="claude-via-harness",
        model_version="claude-opus-4-7",
        system_prompt=(
            "Session H Phase 3.5a: produce an AI-draft Russian rendering of paper.md v1.0.0 "
            "§Abstract as a starter for the user (native Russian speaker) to edit, replace, or "
            "approve for use as research artifact. This is NOT a final human-native rendering."
        ),
        user_prompt=(
            "Render English Paper B abstract (198 words) into native Russian academic register "
            "appropriate for SMJ-tier Russian-language audience. Preserve all propositional claims, "
            "numerical figures, citation references."
        ),
        response=(
            "Russian rendering (~270 Russian words) saved inside PHASE3_5A_RUSSIAN_RENDERING_"
            "PROTOCOL.md §AI-draft Russian rendering. Known limitations flagged for user QC: "
            "term choices (Положение/Утверждение/Постулат); hedging-density adjustment; "
            "корпус connotation; calque alerts; number formatting (Russian decimal-comma vs AMA "
            "leading-zero-suppression)."
        ),
        parameters={
            "target_language": "ru",
            "target_register": "academic_smj_tier",
            "source": "PB v1.0.0 abstract",
        },
        cost_usd_est=0.0,
        human_in_loop=True,
        logs_dir=LOGS_DIR,
    )


def main() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    reconstruct_phase_1()
    reconstruct_phase_2()
    reconstruct_phase_2_5()
    reconstruct_phase_3()
    reconstruct_phase_3_5a()
    print("Reconstructed Session H phase 1 / 2 / 2.5 / 3 / 3.5a logs at:")
    for f in sorted(LOGS_DIR.glob("*.jsonl")):
        n_lines = sum(1 for _ in f.open())
        print(f"  {f.name}: {n_lines} entries")


if __name__ == "__main__":
    main()
