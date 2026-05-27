---
title: "What two famous dynamic-capabilities papers actually agree on — a structural read"
source_spine_pointer: "TWIN_PAIR_ISOMORPHISM_PB_FOCAL.md §2 alignment table (L1, L2, L3, L4 with their preserved antecedents)"
source_substrate_propositions:
  L1: "EM_P1/ZW_P1 — DCs are specific identifiable processes / routinized activities directed at developing operating routines (antecedent: Nelson-Winter 1982 routines; edge: refines)"
  L2: "EM_P7/ZW_P2 — Learning mechanisms guide DC evolution (antecedent: Levitt-March 1988 organizational learning; edge: refines)"
  L3: "EM_P3/ZW_P3 — Cross-firm commonalities at the best-practice / mechanism level despite firm-specific detail (antecedent: Teece-Pisano-Shuen 1997 dynamic-capabilities framework; edge: bridges)"
  L4: "EM_P5+EM_P6 / ZW_P4 — DC form is contingent on market / task features (antecedent: Eisenhardt-Tabrizi 1995 ASQ; edge: extends)"
rendering_target_audience: "LinkedIn professional network (strategy directors, organization-design consultants, dynamic-capabilities scholars, MBA program graduates working in industry); LinkedIn discoverability conventions (short lines; arrow bullets; one-tag-per-post)"
rendering_medium_spec: "LinkedIn long-post; ~1,000 words; declarative; arrow-bullet structure for the L1-L4 substrate; no equations; light citation in plain text not formal bibliography"
rendering_register_shift_from_source: "academic typed-DAG isomorphism table → LinkedIn declarative long-post"
expected_preservation_set:
  - "L1: DCs as identifiable processes refining operating routines (Nelson-Winter 1982 antecedent preserved)"
  - "L2: learning mechanisms drive DC evolution (Levitt-March 1988 antecedent preserved)"
  - "L3: cross-firm commonalities exist at the best-practice / mechanism level (Teece-Pisano-Shuen 1997 antecedent preserved)"
  - "L4: DC form is contingent on market or task features (Eisenhardt-Tabrizi 1995 antecedent preserved)"
  - "node typing preserved: each substrate item rendered as a proposition with explicit antecedent edge"
  - "edge types preserved (refines / refines / bridges / extends)"
date: 2026-05-27
session: Session H Phase 3 — Task β third rendering
status: research artifact NOT publication candidate; not posted to LinkedIn (per Session H init prompt)
---

# What two famous dynamic-capabilities papers actually agree on — a structural read

Two of the most-cited dynamic capabilities papers in strategy:

Eisenhardt and Martin (2000, Strategic Management Journal).
Zollo and Winter (2002, Organization Science).

Different vocabularies. Different journals. Different first authors. Different evidence bases. Different theoretical lineages.

If you ask scholars whether these two papers "agree," the usual answer is "more or less, yes." If you ask them to point to what specifically the two papers agree on, the answer gets fuzzier. We extracted the structural spine of each paper — the typed graph of claims and the dependencies among them — and looked at what overlaps.

The answer: four substrate propositions, each with an intact antecedent edge to a shared piece of prior literature. Same substrate underneath; different prose on top.

Here are the four.

→ **Dynamic capabilities are specific identifiable processes built on routines, not vague organizational mystique.** Eisenhardt and Martin frame this as "strategic and organizational processes — like product development, alliancing, and strategic decision-making" that "have significant commonalities across firms." Zollo and Winter frame it as "routinized activities directed at the development and adaptation of operating routines." Different vocabulary. Same underlying claim: DCs sit above operating routines and they are nameable. The shared antecedent is Nelson and Winter's 1982 evolutionary theory of routines — both papers carry that edge intact.

→ **Learning mechanisms drive how dynamic capabilities form and evolve.** Eisenhardt and Martin name "practice, codification of experience, mistakes, and pacing of experience" as the learning catalog. Zollo and Winter operationalize this into a three-mechanism partition: experience accumulation, knowledge articulation, knowledge codification. Different granularity. Same underlying claim: DCs do not emerge spontaneously; learning mechanisms produce them and shape their content. The shared antecedent is Levitt and March's 1988 organizational learning literature.

→ **There are cross-firm commonalities in dynamic capabilities at the best-practice or mechanism level, even where firm-specific detail diverges.** Eisenhardt and Martin call this "best practices that lead to common-form configurations of dynamic capabilities." Zollo and Winter call it "a mix of learning behaviors firms use across contexts." Different framings. Same underlying claim: DCs are not pure firm idiosyncrasy. Some structural patterns generalize, and finding them is a research-program goal. The shared antecedent is Teece, Pisano, and Shuen's 1997 SMJ dynamic-capabilities framework.

→ **Dynamic-capability form is contingent on market or task features.** Eisenhardt and Martin distinguish "moderately dynamic markets" from "high-velocity markets" and predict different DC forms in each. Zollo and Winter distinguish task frequency, task homogeneity, and causal ambiguity, and predict different mechanism-effectiveness across these task features. Different contingency variables. Same underlying claim: DC form is not market-or-task-invariant. Boundary conditions matter, and the same DC machinery does not run equivalently in every environment. The shared antecedent is Eisenhardt and Tabrizi's 1995 ASQ work on adaptive processes.

Four substrate propositions. Four preserved antecedents. Same underlying structure across two prose renderings that look, on the page, like substantially different papers.

There are claims each paper makes that the other does not. Eisenhardt and Martin's argument that DCs are more "homogeneous, fungible, and equifinal" than RBV assumes does not appear in Zollo and Winter; Zollo and Winter's counterintuitive prediction that deliberate codification dominates specifically at low-frequency / high-heterogeneity / high-causal-ambiguity tasks does not appear in Eisenhardt and Martin. Those are real theoretical divergences, not artifacts of incomplete spine extraction. The two papers genuinely differ — at the periphery. They agree — at the center.

Why does this matter outside academic theory?

Two reasons.

First, for anyone doing strategy work that touches dynamic capabilities — and that is most strategy work in firms operating in environments that change faster than incumbents' routines can keep up — the agreement-at-center pattern means you can act on a stable shared substrate without having to pick a side between two formulations. The four substrate propositions above are what to act on. The framings either paper layers on top of them are vocabulary, and you can pick the vocabulary that fits your audience.

Second, this is a worked example of a more general pattern. Two independently-produced prose renderings of the same underlying substrate converge on conclusions when the substrate is preserved. The dynamic-capabilities pair is one example. The knowledge-based-view pair (Grant 1996, Liebeskind 1996, same Strategic Management Journal special issue) is another, with the same structural-overlap pattern. Whatever knowledge artifact your team produces — board memo, audit report, vendor evaluation, internal handbook — has the same substrate-vs-rendering layering underneath it, and the same convergence-when-substrate-preserved property is empirically testable on your own artifacts.

The operational implication is the one that keeps coming up in organizational discussions of generative AI: if you make the substrate of your knowledge work explicit and version-controlled — separate from any one rendering — you get two things at once. You get the AI cost advantage (AI is cheap on structure; humans remain expensive on rendering verification). And you get the convergence-across-renderings guarantee (the same substrate, rendered three different ways for three different audiences, produces the same bottom-line conclusion across audiences).

Strategy groups inside large firms that already maintain explicit decision logs and structured handbooks — GitLab and Stripe being the canonical reference cases — are getting both advantages right now. Most teams that ship rendered communications without an underlying substrate document are paying full human verification cost on every rendering and getting drift across renderings that no one is monitoring.

The dynamic-capabilities literature converged on a stable substrate in part because the field organized itself around that substrate over a couple of decades and disciplined its renderings against it. Your team can do the same in months, on its own knowledge artifacts, if it takes the substrate seriously as a separate first-class object.

The four propositions above are a working summary you can carry into any DC conversation. The four-shared-propositions pattern, applied to your own organization's renderings, is a working diagnostic.

This is part of a working paper on rendering-equivalence under spine-preservation in organizational knowledge work; the full version, with the typed-DAG extractions and the per-paper alignment tables, is available at the project's Zenodo page when it lands.

— *@Strategic Management Society* | *#dynamiccapabilities* | *#strategy* | *#knowledgework* | *#organizationaldesign*

---

*This is a research-artifact rendering, not a publication. Posted to LinkedIn only as part of a controlled re-rendering experiment in Paper B 2026ap v1.0.0 Task β. Per Session H init prompt, this file is not pushed to live LinkedIn.*
