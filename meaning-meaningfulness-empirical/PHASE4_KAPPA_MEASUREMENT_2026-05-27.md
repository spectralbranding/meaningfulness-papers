---
title: "Phase 4 inter-coder κ measurement — protocol setup + recruitment status + execution-deferred-to-v1.1.0"
date: 2026-05-27
session: Session H Phase 4 — Task δ
target_axiom: "paper_a:axiom_A1 (σ-faithfulness on locked subsets); operational threshold κ ≥ .75 on both node typing and antecedent-edge placement"
status: "Protocol documented + recruitment status surfaced + EXECUTION DEFERRED to v1.1.0 pending second-coder onboarding"
---

# Phase 4 inter-coder κ measurement — Task δ protocol + recruitment status

## Why this matters

Paper A 2026ao's P4 (rendering-equivalence under spine-preservation) holds as a preservation result under axiom A1 (σ-faithfulness on locked subsets). A1's operational threshold is **κ ≥ .75 on both node typing AND antecedent-edge placement**, measured via inter-coder reliability on retroactive spine extractions. Below threshold on either dimension, A1 fails empirically on the affected subdomain and P4 degrades from a preservation result to a probabilistic tendency on that subdomain.

Post-draft critical review elevated κ measurement from a v1.0.0 Limitations item to a priority item (Priority-1 in §5 Major Revision Roadmap). The v1.0.0 release explicitly schedules κ measurement as Task δ; this document is the execution-readiness pass.

## Protocol specification (operational, ready for execution)

### Codebook

The codebook is **`paper_a:appendix_A_schema`** — the 10-type node taxonomy plus 17-edge catalog locked in Paper A v1.0 (per `/Users/d/projects/spectral-branding-meaningfulness/research/meaning_meaningfulness_paper/SPINE.yaml` Online Appendix A and `paper.md` §Theory inheritance).

**Node types** (10):

| ID | Type | Definition |
|---|---|---|
| 1 | proposition | Theoretical claim asserted by the author |
| 2 | observation | Empirical referent or raw data the author invokes |
| 3 | method | Procedural transformation the author applies |
| 4 | measurement | Derived datum the author reports |
| 5 | finding | Inferential claim the author argues from measurements |
| 6 | derivation | Formal deduction from prior nodes |
| 7 | rival | Alternative explanation the author considers |
| 8 | robustness_check | Sensitivity or replication test |
| 9 | limitation | Honest scope-or-power disclosure |
| 10 | assumption_atom | Indivisible premise the author asserts as required |

**Edge types** (17): extends, applies, tests, contradicts, refines, depends-on, evidences, defines, measures, aggregates, generates, rules-out, bridges, mitigates, relaxes, motivates, provenances.

### Sampling frame

Two of the five extracted spines at v1.0.0:

1. **VALIDATION_CASE_PB_FOCAL_EISENHARDT_MARTIN_SPINE.yaml** (focal pair member; covers DC sub-domain)
2. **VALIDATION_CASE_PB_KBV_GRANT_SPINE.yaml** (KBV pair member; covers KBV sub-domain; image-only OCR'd PDF — see §pre-extraction OCR-correction)

Recommendation: this pair gives one focal + one KBV; one well-OCR'd source (EM2000 PDF was text-extractable) + one OCR-uncertain source (Grant 1996 PDF was image-only). The κ-on-EM2000 is the upper-bound estimate (no OCR noise floor); the κ-on-Grant-1996 is the lower-bound estimate (with OCR noise floor). Both are reported.

### Extraction protocol for second coder

The second coder:

1. Reads the PDF of each assigned source paper directly (Eisenhardt-Martin 2000 SMJ; Grant 1996 SMJ Winter Special Issue), WITHOUT looking at the existing extracted spine YAML.
2. Applies paper_a:appendix_B_protocol in reverse: identifies central propositions / observations / methods / findings, classifies each into the 10-node-type taxonomy, traces antecedent edges using the 17-edge catalog.
3. Produces an independent YAML spine in the schema-v0.2 format (same structure as the existing VALIDATION_CASE_*_SPINE.yaml files).
4. Hands the independent spine back to the author with NO inspection of the prior author-extracted spine until both spines are locked in writing.

The author then computes κ on (a) node typing AND (b) antecedent-edge placement separately, per the rule below.

### κ computation rule (Cohen's κ on two dimensions)

For each assigned spine pair (author's vs second-coder's extraction of the same source paper):

**Node-typing κ**: align both extractions on the set of "central nodes" the source paper produces (typically 5-15 per source). For each aligned-node-position, the two coders' assigned node type is a categorical pick from the 10-type taxonomy. Compute Cohen's κ over the aligned node-position vector across the spine. Threshold: κ ≥ .75 → axiom A1 holds for node typing on this subdomain.

**Antecedent-edge κ**: for each aligned-node-position, list the set of antecedent edges (preserved-prior-literature nodes) the two coders assigned. Treat each (source-node, antecedent-target) pair as a binary item (present / absent). Compute Cohen's κ over the edge-presence vector. Threshold: κ ≥ .75 → axiom A1 holds for antecedent-edge placement on this subdomain.

Both κ values must be ≥ .75 for axiom A1 to hold strictly on that subdomain. If one passes and one fails, the failing dimension is the empirical-A1-failure subdomain; report which.

### Pre-extraction OCR-correction (optional, raises Grant 1996 baseline accuracy)

Per Session H init prompt §Phase 4 + SESSION_F_COMPLETION_2026-05-27.md §Open items: a Perplexity-based verbatim-quote-verification script was drafted in Session E for the Grant 1996 spine. The script is preserved in **`git stash@{0}` of the worktree** (in commit `498bcdb9` parent `29eec8e7` as untracked file `code/verify_grant_1996_perplexity.py`, 337 lines, never executed).

To salvage and run BEFORE second-coder extraction begins (raises baseline accuracy of the author's Grant 1996 extraction so the κ measurement compares against a corrected baseline):

```bash
cd /Users/d/projects/spectral-branding-meaningfulness-empirical
git stash apply --index "stash@{0}"   # restores code/verify_grant_1996_perplexity.py to working tree
# fix openai-module dependency: requires openai>=1.0.0 + PERPLEXITY_API_KEY env var
uv add openai
PERPLEXITY_API_KEY="..." uv run python code/verify_grant_1996_perplexity.py
# review output, integrate corrections into VALIDATION_CASE_PB_KBV_GRANT_SPINE.yaml
# commit the spine update before second-coder extraction
git stash drop "stash@{0}"
```

Alternative (skip-OCR-correction path): proceed with the existing OCR'd extraction; report κ as "with OCR noise floor" lower-bound. Acceptable if Perplexity API access is unavailable or if v1.1.0 execution-time prioritizes the κ measurement over the OCR-correction.

### Falsifier specification

- κ ≥ .75 on both dimensions on at least one of the two extracted spines: **axiom A1 reliability holds empirically on that subdomain; report which sub-domain**.
- κ < .75 on one dimension on one spine: **A1 holds partially; report the dimension and subdomain where it fails; degrade P4 to probabilistic-tendency on that subdomain per axiom A1 spec**.
- κ < .50 on either dimension on either spine: **schema-refinement work triggered, OR honest disclosure in paper.md that the framework requires further codification before P4 can hold as preservation result**.

## Second-coder recruitment status

The user operates as a solo researcher on this corpus. No second coder has been onboarded by Session H end. Per Session H init prompt: "If second coder unavailable: document the protocol setup + recruitment status; mark κ-measurement execution deferred to v1.1.0; surface as honest disclosure in Phase 5 paper.md revision".

**Per feedback_rank_twin_candidates_with_sourcing_options.md** (which extends to coder-recruitment): below are 5 ranked candidate-second-coder options for the user to choose from when v1.1.0 execution begins. Ranked by estimated κ-yield-quality × onboarding-cost.

| Rank | Candidate type | κ-yield quality | Onboarding cost | Notes |
|---|---|---|---|---|
| 1 | **PhD candidate in strategy / org theory (R1 program)** | HIGH | MEDIUM | Familiar with EM/ZW/Grant/Liebeskind from coursework; needs only paper_a:appendix_A_schema codebook walkthrough (~1 hour); typical compensation $300-500 per spine. Recruitment channels: SMS PhD listserv; Strategic Management Society Discord; AOM PhD-student group. |
| 2 | **Independent academic collaborator with prior DC/KBV familiarity** | HIGH | LOW | If user has a 1st-degree or 2nd-degree LinkedIn contact who knows the DC/KBV literature and is willing to do ~4-6 hours of coding work; likely a quid-pro-quo arrangement rather than monetary. Candidates from user's existing network are best-positioned. |
| 3 | **Practitioner with strategy-theory background (ex-McKinsey / BCG / Bain analyst)** | MEDIUM-HIGH | MEDIUM | Reads strategy papers regularly; needs codebook walkthrough + 1-2 calibration sessions on a non-corpus spine before producing the test extractions. ~$400-600 per spine. Recruitment channels: paid-consulting platforms (Catalant, GLG) or direct LinkedIn outreach to "ex-MBB independent consultant" contacts. |
| 4 | **Two AI-assisted coders (different model families: Claude + Gemini OR Claude + GPT-4o) acting in coordination with a human spot-check** | LOW-MEDIUM | LOW | Cheap to execute; produces a synthetic-κ that is methodologically informative but does NOT satisfy the "independent human coder" specification axiom A1 requires per Paper A. Acceptable as a v1.1.5 interim measurement only if explicitly framed as machine-coding-consistency, not as κ-on-axiom-A1. |
| 5 | **Crowdsourced coders (MTurk / Prolific with management-research-experience filter)** | LOW | LOW | Cheapest; lowest signal quality at the typed-DAG depth axiom A1 requires; not recommended unless paired with a stratified-sample design and aggregation rule. |

Candidates 1 and 2 are the recommended options for v1.1.0 execution. Candidate 4 is the corpus-precedent fallback if no human coder lands within Q3 (per Paper A 2026am precedent of accepting machine-coding-consistency interim measurements).

**Note (per feedback_no_internal_strategy_public.md)**: this ranked list of candidate coders is INTERNAL to this session and the worktree. The Phase 5 paper.md revision discloses the recruitment-status honestly but does NOT publicly name candidate channels or specific outreach plans. The public disclosure language: "Inter-coder κ measurement on axiom A1 (recommended κ ≥ .75 on both node typing and antecedent-edge placement) is scheduled for the v1.1.0 release. The protocol and codebook are pre-registered alongside this release; execution awaits the onboarding of an independent second coder. Honest disclosure: axiom A1 reliability is currently asserted rather than measured."

## What Session H achieves under Task δ deferral

- **Protocol document**: complete and execution-ready for v1.1.0 (this file).
- **Codebook**: locked at paper_a:appendix_A_schema (no schema-refinement needed for execution; refinement would only be triggered if κ < .50 lands at execution).
- **Sampling frame**: two of five spines selected and rationale documented.
- **Falsifier specification**: explicit at .75 / .50 thresholds per axiom A1.
- **Pre-extraction OCR-correction step**: documented with stash-recovery commands ready to execute.
- **Recruitment status**: surfaced with ranked candidate-coder options.
- **Public disclosure language**: drafted for Phase 5 paper.md revision (see quoted block above).

## What Session H does NOT achieve under Task δ deferral

- Actual κ values on either spine.
- Second-coder extractions.
- Empirical anchoring of axiom A1 on the Paper B subdomain.
- The Priority-1 item is documented + protocolized + deferred — not closed.

## Integration into v1.0.0 paper.md (Phase 5 5a)

The Phase 5 integrative-theory rewrite and the §Limitations / §Method-extraction-reliability subsection cite this protocol document as the pre-registered v1.1.0 execution plan. Honest disclosure language: "Inter-coder κ measurement on axiom A1 is pre-registered at v1.1.0 per `PHASE4_KAPPA_MEASUREMENT_2026-05-27.md`; the codebook (paper_a:appendix_A_schema), sampling frame (EM2000 focal + Grant 1996 KBV), and falsifier specification are locked alongside the v1.0.0 release. Axiom A1 reliability is currently asserted; the measurement will land before any tier-1 venue submission."

## Cross-reference

- Source: Phase 4 Task δ + Paper A 2026ao §Method-single-coder-reliability + paper_a:axiom_A1.
- Companion: PHASE1_ANCHOR_VERIFICATION_2026-05-27.md (Phase 1 sister artifact); SELF_APPLICATION_ISOMORPHISM_PB.md (Phase 2 sister artifact); TWIN_PAIR_ISOMORPHISM_PB_FOCAL.md §8 (Phase 3 sister artifact).
- Successor: PHASE4_KAPPA_RESULTS_v1.1.0.md (to be created at v1.1.0 execution).

---

*Phase 4 closes with full protocol documentation + recruitment status surfaced + execution deferred to v1.1.0. The Priority-1 item remains pre-registered and tractable; what is missing is operator-attention-budget for second-coder onboarding, not framework-design clarity.*
