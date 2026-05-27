---
title: "Twin-Pair Isomorphism Analysis — KBV Pair (Grant 1996 + Liebeskind 1996)"
author: Dmitry Zharnikov
version: v1.1.0
session: Session E continuation post-Path-A
date: 2026-05-27
schema: paper_a:appendix_A_schema (typed-DAG; 10 node types; 17 edge types)
spine_extractions:
  - VALIDATION_CASE_PB_KBV_GRANT_SPINE.yaml
  - VALIDATION_CASE_PB_KBV_LIEBESKIND_SPINE.yaml
---

# Twin-Pair Isomorphism Analysis — KBV Pair

## 1. Bikard-protocol independence check

The KBV pair (Grant 1996 + Liebeskind 1996) is a **same-special-issue parallel-submission twin**: both papers appeared in *Strategic Management Journal* Vol. 17 Winter Special Issue "Knowledge and the Firm" (1996). Same-special-issue parallel submission is one of the strongest forms of Bikard independence — both authors submitted to the same call for papers, both were finalized through similar editorial cycles, and cross-citation across same-issue papers at submission time is exceptionally rare (special-issue submissions are typically held confidential by the guest editors until the issue is finalized).

**Citation cross-check at draft time** (verified directly from each paper's reference list):

- **Grant 1996 reference list**: Does NOT cite Liebeskind (1996) — verified by scanning the OCR'd reference list. Grant cites Ghoshal-Moran 1996 (in-press at the time) and other contemporaries but not Liebeskind.
- **Liebeskind 1996 reference list**: Does NOT cite Grant (1996) — verified by scanning the available text extracts. Liebeskind cites Penrose, Spender, Barney, Lippman-Rumelt, Rumelt 1984 but not Grant.

**Verdict on Bikard independence**: STRONG. Same-special-issue parallel submission with confirmed mutual non-citation at draft time. Stronger than the focal pair's PARTIAL independence (where Eisenhardt-Martin 2000 cites Zollo-Winter 1999 WP). The KBV pair is the cleanest Bikard twin in Paper B's corpus to date.

## 2. Spine-to-spine alignment table

Mapping propositions from VALIDATION_CASE_PB_KBV_GRANT_SPINE.yaml (G_P1..G_P7) to VALIDATION_CASE_PB_KBV_LIEBESKIND_SPINE.yaml (L_P1..L_P7), preserving Paper A's typed-DAG edge types.

| Alignment id | Grant proposition | Liebeskind proposition | Edge type | Shared antecedent (preserved) | Linked? |
|---|---|---|---|---|---|
| K1 | G_P1 "Knowledge is the most strategically important resource of the firm; knowledge-based view as outgrowth of RBV" | L_P1+L_P2 "Firms have institutional capabilities to protect knowledge; these capabilities generate/protect resources central to strategic theory of the firm" | bridges (both anchor a strategic theory of the firm on knowledge as the central resource) | RBV-tradition (Penrose 1959; Barney 1991) | YES |
| K2 | G_P4 "Firm exists for knowledge integration because markets cannot coordinate due to tacit-knowledge immobility + explicit-knowledge expropriation risk" | L_P3+L_P4 "Where property rights in knowledge are weak, firms use organizational arrangements not available in markets to protect/integrate knowledge; firms differentially prevent expropriation + reduce observability" | refines (both posit firm-as-knowledge-protector with explicit reference to market-failure in knowledge transactions; Liebeskind operationalizes the 'expropriation risk' G_P4 invokes) | Coase 1937; Williamson 1975 markets-and-hierarchies | YES |
| K3 | G_P2 "Knowledge has characteristics including tacit/explicit distinction, transferability, aggregation" | L_P5 "Legal protections (patents/copyrights/trade secrets) exclude tacit knowledge; tacit-vs-explicit distinction structures the protection-gap argument" | bridges (both invoke the tacit/explicit knowledge distinction as central to their respective arguments; Grant for the integration mechanism; Liebeskind for the protection-gap) | Polanyi 1966 tacit knowledge | YES |
| K4 | G_P7 "Firm boundaries determined by efficient knowledge integration vs market alternatives" | L_F2 "Internalization (vs market contracting) is dominant where institutional knowledge-protection costs are lower than market-contracting protection costs" | refines (Grant's boundary claim is about integration-efficiency; Liebeskind's boundary claim is about protection-cost-efficiency; both reach the same firm-as-protector conclusion via different cost calculi) | Coase 1937; Williamson 1975 | YES |
| K5 | G_P5+G_P6 "Coordination within firm via integration mechanisms; hierarchy economizes on knowledge integration" | (no direct match in Liebeskind 1996; Liebeskind focuses on knowledge protection not coordination) | — | — | NO |
| K6 | G_P3 "Knowledge creation is individual; organizations apply existing knowledge" | (no direct match; Liebeskind treats knowledge creation as a given output of firm-internal processes) | — | — | NO |
| K7 | (no direct match) | L_P6+L_P7 "Firms differ in protective capabilities → profit heterogeneity + innovation-investment heterogeneity" | (no symmetric Grant proposition; resource-heterogeneity is Liebeskind-specific contribution) | — | NO |

**Linked-proposition count with preserved antecedents: 4 (K1, K2, K3, K4).**

## 3. Rec metric calculation

Per paper_a:recombination_operator: Rec(G_Grant, G_Liebeskind) = **4** on linked propositions with preserved antecedents.

**Threshold comparison**: Paper A's deterministic threshold for a recombination event is Rec ≥ 3. The KBV-pair Rec = 4 ≥ 3 → **the KBV twin pair satisfies paper_a:P2's existence-proof threshold at v1.1.0.**

## 4. β-conditional threshold check (paper_a:M Rec*(β))

At the grid-anchored β̂ = .7 calibrated in v1.0.0 §Results-cost-function-calibration, Rec*(β = .7) = ⌈3 · 2^.30⌉ = 4. The KBV-pair Rec = 4 satisfies the β-conditional threshold at the margin, identical to the focal pair (which also landed at Rec = 4 at β = .7).

**Cross-pair convergence observation:** both the focal pair (EM2000 + ZW2002, dynamic-capabilities sub-domain) AND the KBV pair (Grant 1996 + Liebeskind 1996, knowledge-based-view sub-domain) land at Rec = 4 with preserved antecedents. This is consistent with paper_a:P2 — twin pairs across distinct theoretical neighborhoods satisfy the recombination threshold at comparable levels, suggesting the threshold is not artifact of one sub-domain. v2.0.0+ will test whether the Rec = 4 modal value persists at larger N or whether the focal/KBV equivalence is a small-sample coincidence.

## 5. Honest limitations of the v1.1.0 isomorphism analysis

- **Single-coder extraction**: same as v1.0.0 (paper_a:axiom_A1 + PB_AA1); κ scheduled for v1.2.0.
- **OCR dependency for Grant 1996**: the Grant 1996 PDF in references/ is image-only; OCR via ocrmypdf was required. OCR introduces small text-fidelity errors (e.g., footnote-number misreads, dropped diacriticals); the spine extraction draws on OCR'd output and may differ at the margin from a perfectly-transcribed source. v1.2.0 would benefit from a hand-verified transcription pass; v1.1.0 reports the OCR-based extraction with this disclosure.
- **Strong Bikard independence not yet exploited**: the KBV pair is the cleanest Bikard twin in Paper B's corpus, but at N=2 the strength of independence cannot yet differentiate Rec values across independence levels. v2.0.0+ adds matched pairs at varying independence levels (partial, strong, full).
- **Liebeskind has 7 propositions; only 4 link to Grant.** The unlinked L_P6 (resource-heterogeneity from protection capabilities) and L_P7 (innovation-investment heterogeneity) are Liebeskind-specific contributions that Grant does not state. Similarly, Grant's G_P5 (coordination mechanisms) and G_P6 (hierarchy emergence) are Grant-specific. These divergences are genuine theoretical heterogeneity within the KBV neighborhood, not extraction artifacts.

## 6. Cross-link to paper_a:P4 (rendering-equivalence) at the cross-pair level

The KBV pair extends Paper B's evidence for paper_a:P4 from one within-discipline twin (focal pair; dynamic-capabilities sub-domain) to two within-discipline twins (focal + KBV; dynamic-capabilities + knowledge-based-view sub-domains). Both pairs satisfy Rec ≥ 3 deterministic threshold AND Rec*(β = .7) = 4 β-conditional threshold. P4 prediction at the cross-pair level: as the cohort grows from N=1 to N=2 to N=k, the modal Rec value should remain above the deterministic threshold; if it falls below at v2.0.0+ N=15-20 prospective cohort, the theory's existence-proof scope is overturned.

## 7. Summary verdict

- Bikard independence: **STRONG** (same SMJ Winter 1996 Special Issue 'Knowledge and the Firm'; confirmed mutual non-citation at draft time).
- Rec(G_Grant, G_Liebeskind): **4** linked propositions with preserved antecedents.
- Paper A P2 threshold (Rec ≥ 3): **SATISFIED**.
- β-conditional Rec*(β = .7) threshold: **SATISFIED** at the margin.
- Existence proof for P2 at v1.1.0 N=2 twin pairs (focal + KBV): **HOLDS** at both pairs.
- Cross-pair Rec convergence at Rec = 4: notable observation; suggests threshold is sub-domain-invariant at small N; v2.0.0+ tests at larger N.

**N = 2 status at v1.1.0**: Paper B v1.1.0 ships with TWO independently-extracted twin pairs in distinct theoretical sub-domains (dynamic capabilities + knowledge-based view) both satisfying the existence-proof threshold. This is a substantive strengthening over v1.0.0's N = 1 evidence base while remaining honest about the small-N existence-proof scope.
