---
title: "Twin-Pair Isomorphism Analysis — Focal Pair (Eisenhardt-Martin 2000 + Zollo-Winter 2002)"
author: Dmitry Zharnikov
version: v1.0.0
session: Session E Phase 2
date: 2026-05-27
schema: paper_a:appendix_A_schema (typed-DAG; 10 node types; 17 edge types)
spine_extractions:
  - VALIDATION_CASE_PB_FOCAL_EISENHARDT_MARTIN_SPINE.yaml
  - VALIDATION_CASE_PB_FOCAL_ZOLLO_WINTER_SPINE.yaml
---

# Twin-Pair Isomorphism Analysis — Focal Pair

## 1. Bikard-protocol independence check

Per paper_a:appendix_B_protocol applied in reverse, the focal pair must satisfy Bikard's idea-twin independence criterion: **mutual non-citation at draft time** of any prior preprint that supplies the partner paper's central thesis.

**Citation cross-check at draft time** (verified directly from each paper's reference list):

- **EM2000 cites ZW1999 working paper WP 99-07** ("From organizational routines to dynamic capabilities") in its References list. The citation is one of approximately 40+ references, located in the alphabetical-by-author closing positions of the reference list (without prominent in-text engagement in EM2000's central argument). EM2000's reference list also includes Zollo-Singh (1998) AOM Best Paper Proceedings on M&A codification — adjacent but distinct from the central ZW2002 thesis.
- **ZW2002 does not cite EM2000** (verified by absence in ZW2002's reference list as preserved in the working-paper version subsequently published 2002).

**Verdict on Bikard independence**: PARTIAL. EM2000's reference of the ZW1999 WP demonstrates EM2000's authors were *aware* of Zollo-Winter's parallel work; but the in-text engagement in EM2000 builds its central thesis (DCs-as-identifiable-processes; market-velocity boundary condition) on a different intellectual lineage (Brown-Eisenhardt 1997 simple rules; Cisco/Toyota/Disney best-practice cases) without inheriting ZW1999's central claim (three-mechanism learning co-evolution; task-feature contingencies). The two papers share antecedents (Teece-Pisano-Shuen 1997; Nelson-Winter 1982 routines) but neither is a derivative of the other.

This is a **partial-independence twin**: stronger than full mutual citation (which would disqualify as twin) but weaker than full mutual non-citation (which is Bikard's strict criterion). For Paper B v1.0.0 existence-proof scope, the partial-independence twin is *acceptable* if we report the independence finding honestly. The v1.1.0 release will tighten by adding a fully-independent pair to compare against.

## 2. Spine-to-spine alignment table

Mapping propositions from VALIDATION_CASE_PB_FOCAL_EISENHARDT_MARTIN_SPINE.yaml (EM_P1..EM_P7) to VALIDATION_CASE_PB_FOCAL_ZOLLO_WINTER_SPINE.yaml (ZW_P1..ZW_P6), preserving Paper A's typed-DAG edge types (extends, applies, tests, contradicts, refines, depends-on, evidences, defines, measures, aggregates, generates, rules-out, bridges, mitigates, relaxes, motivates, provenances).

| Alignment id | EM proposition | ZW proposition | Edge type | Shared antecedent (preserved) | Linked? |
|---|---|---|---|---|---|
| L1 | EM_P1 "DCs are specific identifiable processes" | ZW_P1 "DCs are routinized activities directed at developing operating routines" | refines (EM specifies process examples; ZW specifies routinized-substrate ontology) | Nelson-Winter 1982 routines | YES |
| L2 | EM_P7 "Learning mechanisms (practice, codification, articulation, error rate, pacing) guide DC evolution" | ZW_P2 "Three learning mechanisms (experience accumulation + articulation + codification) shape DC evolution" | refines (ZW operationalizes EM's catalog into a tri-partition with hypotheses) | Levitt-March 1988 organizational learning | YES |
| L3 | EM_P3 "DCs are idiosyncratic in detail but have significant commonalities across firms (best practices)" | ZW_P3 "Firms adopt a mix of learning behaviors (semi-automatic + deliberate articulation + codification)" | bridges (both posit cross-firm commonality at the mechanism/process level despite firm-specific detail) | Teece-Pisano-Shuen 1997 dynamic-capabilities framework | YES |
| L4 | EM_P5+EM_P6 "DC form is market-contingent (moderately dynamic ↔ high velocity)" | ZW_P4 "Mechanism effectiveness is task-contingent (frequency / homogeneity / causal ambiguity)" | extends (both posit DC contingencies on task/environment features) | Eisenhardt-Tabrizi 1995 ASQ; Burgelman 1991 OrgSci | YES |
| L5 | EM_P4 "DCs are more homogeneous, fungible, equifinal than RBV assumes" | ZW_P5 "Deliberate codification dominates at low-frequency / high-heterogeneity / high-causal-ambiguity tasks (counterintuitive)" | (no direct match; ZW_P5 is a contingency result that EM does not state) | — | NO (no direct twin) |
| L6 | EM_P2 "DCs are neither vague nor tautological" | (no direct match in ZW2002) | — | — | NO |
| L7 | (no direct match in EM2000) | ZW_P6 "DCs themselves require investment; don't emerge automatically from operating-routine variance" | — | — | NO |

**Linked-proposition count with preserved antecedents: 4 (L1, L2, L3, L4).**

## 3. Rec metric calculation

Per paper_a:recombination_operator: Rec(G_1, G_2) is the size of the maximum common subgraph that preserves both node typing and antecedent edges.

For the focal pair:
- Linked propositions (preserved antecedents): 4 (L1-L4 above).
- Each linked proposition has at least one preserved antecedent (Nelson-Winter 1982; Levitt-March 1988; Teece-Pisano-Shuen 1997; Eisenhardt-Tabrizi 1995).
- Node-type preservation: each link is proposition-to-proposition (same node type); edge-type for each link is from the typed-DAG catalog (refines / bridges / extends — all valid edge types in Paper A's 17-type catalog).

**Rec(G_EM, G_ZW) = 4** on linked propositions with preserved antecedents.

**Threshold comparison**: Paper A's threshold for a recombination event is **Rec ≥ 3 on linked propositions with preserved antecedents** (paper_a:recombination_operator). The focal-pair Rec = 4 ≥ 3 → **the focal twin pair satisfies paper_a:P2's existence-proof threshold at v1.0.0.**

Below the threshold would be a falsifier outcome; the observed value is comfortably above the threshold. This is an existence proof (one positive case at small N), not falsification (which requires sampling and statistical power Paper B v2.0.0+ will supply).

## 4. β-conditional threshold check (paper_a:M Rec*(β))

Per Paper B PREDRAFT_BUNDLE §M, the β-conditional minimum-threshold function is Rec*(β) = ⌈3 · 2^(1−β)⌉. At illustrative β values from the parameter grid Paper A Online Appendix C explores:
- β = .5: Rec*(.5) = ⌈3 · 2^.5⌉ = ⌈4.24⌉ = 5
- β = .7: Rec*(.7) = ⌈3 · 2^.3⌉ = ⌈3.69⌉ = 4
- β = .9: Rec*(.9) = ⌈3 · 2^.1⌉ = ⌈3.21⌉ = 4

Focal-pair observed Rec = 4 satisfies Rec*(β) at β = .7 or β = .9 but is just below the threshold at β = .5. The β estimate that will be calibrated empirically in §Results-cost-function-calibration determines which threshold the focal pair satisfies. Paper B reports the threshold-conditional reading without claiming statistical power.

## 5. Honest limitations of the v1.0.0 isomorphism analysis

- **Partial Bikard independence** (§1 above): EM2000 cites ZW1999 WP in its reference list, weakening but not eliminating independence. Acceptable for v1.0.0 existence proof; v1.1.0 adds fully-independent pair.
- **Single-coder extraction** (paper_a:axiom_A1 + PB_AA1): the spine-to-spine alignment table reflects one coder's typing decisions. Inter-coder κ measurement scheduled for v1.1.0; current alignments at v1.0.0 are author-reported.
- **No matched-non-twin baseline** (reviewer ask, deferred to v2.0.0+): the Rec = 4 value cannot be compared against a placebo non-twin baseline at v1.0.0. The threshold-comparison Rec ≥ 3 is anchored to Paper A's deterministic spec, not to a sampling distribution.
- **Edge-type judgment calls**: L3 (bridges) is the closest edge-type-decision call; "bridges" was chosen over "extends" because both EM_P3 and ZW_P3 posit cross-firm commonality without one being a strict extension of the other.
- **Linked propositions not exhaustive**: L5-L7 catalog unlinked propositions; the per-paper unique propositions (EM_P2, ZW_P5, ZW_P6) are not artifacts of incomplete spine extraction but real theoretical divergences between the twin members.

## 6. Cross-link to paper_a:P4 (rendering-equivalence)

Paper A's P4 predicts that two prose renderings of a locked spine arrive at the same conclusion set iff both preserve spine structure. The focal twin pair is a worked instance: two parallel prose renderings (EM2000 + ZW2002) of an implicitly shared dynamic-capabilities-as-routinized-mechanisms spine (substrate). The Rec = 4 linked-proposition count is the empirical measurement of spine-structure preservation across the two renderings. Per paper_a:axiom_A1, this is the σ-extracted typed-DAG restricted to the locked subset; below-threshold κ would weaken the preservation finding (deferred to v1.1.0 measurement).

Paper A's P4 was illustrated at appendix-D depth on the Heisenberg-Schrödinger 1925-26 pair (non-management domain; existence proof of cross-formalism convergence). Paper B's focal-pair Rec = 4 extends the P4 evidence to a same-discipline management-theory twin pair, sharpening from "the pattern holds in a non-management domain" to "the pattern also holds within management theory at a known idea-twin pair."

## 7. Summary verdict

- Bikard independence: PARTIAL (EM2000 cites ZW1999 WP in references; no derivative-of relationship; both share antecedents in Teece-Pisano-Shuen 1997 + Nelson-Winter 1982).
- Rec(G_EM, G_ZW): **4** linked propositions with preserved antecedents.
- Paper A P2 threshold (Rec ≥ 3): **SATISFIED**.
- β-conditional Rec*(β) threshold: satisfied at β ≥ .7; just-below at β = .5 (depends on empirical β calibration).
- Existence proof for P2 at v1.0.0 N=1 focal pair: **HOLDS**.
- Secondary-pair 20-year-gap sensitivity check on P4 robustness: **DEFERRED to v1.1.0** (Tushman-O'Reilly 1996 spine released standalone; partner extraction + isomorphism deferred).

## 8. Third-rendering preservation analysis (Session H Phase 3 Task β)

Task β per SESSION_F_COMPLETION_2026-05-27.md spec and Session H init prompt: render the focal-pair shared substrate (L1-L4 above) into a third independent prose form, re-extract the spine from the third rendering, and compute Rec(G_third, G_shared_spine). Success criterion: ≥ 4 substrate items preserved (i.e., the full L1-L4 substrate persists across the third rendering). Falsifier: < 3 preserved (substrate degrades on re-rendering; P4 weakens at the focal-pair-substrate boundary).

**Third rendering**: `RENDERING_FOCAL_PAIR_THIRD_PROSE.md` — 1,044-word LinkedIn long-post in practitioner register, arrow-bullet structure for the L1-L4 substrate, named antecedents in plain text, no equations. Medium selected by user from three options (textbook synthesis / LinkedIn / review abstract); LinkedIn chosen to cover a SECOND practitioner register distinct from the Phase 2 Substack rendering (LinkedIn = professional-network register; Substack = consumer-essay register).

**Re-extracted spine**: `VALIDATION_CASE_PB_FOCAL_THIRD_RENDERING_SPINE.yaml` — re-extracted from the LinkedIn rendering using paper_a:appendix_B_protocol applied in reverse; T_ node prefix.

**Per-substrate-item preservation check**:

| Source substrate (focal-pair shared) | Re-extracted node | Node typing | Antecedent edge | Verdict |
|---|---|---|---|---|
| L1 (DCs as identifiable processes / routinized activities; antecedent Nelson-Winter 1982; edge refines) | T_L1 | proposition (preserved) | Nelson-Winter 1982 named with edge "refines" | **PRESERVED** |
| L2 (learning mechanisms guide DC evolution; antecedent Levitt-March 1988; edge refines) | T_L2 | proposition (preserved) | Levitt-March 1988 explicitly named; edge "refines" preserved (EM catalog → ZW partition operationalization) | **PRESERVED** |
| L3 (cross-firm commonalities at best-practice / mechanism level; antecedent Teece-Pisano-Shuen 1997; edge bridges) | T_L3 | proposition (preserved) | Teece-Pisano-Shuen 1997 named with full author list; edge "bridges" preserved | **PRESERVED** |
| L4 (DC form contingent on market/task features; antecedent Eisenhardt-Tabrizi 1995 ASQ; edge extends) | T_L4 | proposition (preserved) | Eisenhardt-Tabrizi 1995 ASQ explicitly named; edge "extends" preserved | **PRESERVED** |

**Rec(G_third, G_shared_spine) = 4** with all four antecedent edges preserved.

**Verdict**: success criterion met. Third rendering preserves the entire focal-pair shared substrate at the node-typing + antecedent-edge level required by paper_a:P4. Plus, the LinkedIn rendering's accurate preservation of the L5-L6-L7 unlinked propositions (EM's homogeneity-fungibility-equifinality claim explicitly named as not-in-ZW; ZW's counterintuitive codification prediction explicitly named as not-in-EM) demonstrates the rendering preserved not only the shared substrate but also the substrate's negative space — the per-paper unique propositions remain accurately disjoint from the shared core.

**Bridging consistency with Phase 2 Task α**: the Phase 3 rendering and the Phase 2 RENDERING_PB_SUBSTACK_PRACTITIONER.md both name GitLab + Stripe as canonical handbook-discipline reference cases; both name the substrate-vs-rendering distinction as the central operational implication; both preserve the AI cost-asymmetry framing. Two practitioner-register renderings produced from overlapping substrates by the same operator on the same day; expected high consistency; observed zero contradictions across the two renderings.

**Honest limitation**: same-operator re-extraction risk applies here as it does for Task α — the coder who extracted the third-rendering spine wrote the third rendering and knows the source. Task δ (independent second-coder κ on 2 of 5 spines) is the appropriate test of the cross-coder reliability.

**Integration into paper.md**: cite as a second P4 evidence point at the focal-pair-shared-substrate boundary (complementing the original Rec=4 on the EM-vs-ZW pair). The Phase 2 Task α result is the P4 evidence point at the Paper-B-own-spine boundary; the Phase 3 Task β result is the P4 evidence point at the focal-pair-shared-substrate boundary. Both are below the v2.0.0+ prospective-cohort empirical scale reviewers ask for, but both meaningfully extend the v1.0.0 N=2-twin-pairs evidence base.
