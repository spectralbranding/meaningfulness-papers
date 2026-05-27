---
title: "When two strategy papers say the same thing in different words — and what that tells you about AI in your organization"
source_spine_pointer: "research/meaningfulness_empirical_companion/SPINE.yaml v0.3.1"
rendering_target_audience: "senior practitioners (CMOs, strategy directors, organization-design leaders, knowledge-management heads, partner-track consultants)"
rendering_medium_spec: "Substack standalone article; ~1,500 words; practitioner register; plain English; minimal jargon; named-case examples; explicit Monday-morning moves; first-person plural where natural"
rendering_register_shift_from_source: "academic-paper.md (third-person, hedged, mathematical notation, citation-dense, AMA structure) → Substack practitioner article (declarative, named-case anecdotes, no equations, light citation, three first moves)"
expected_preservation_set:
  - "central claim: two prose versions of the same idea reach the same conclusions if they preserve the same structural elements (P4)"
  - "the structural element of a paper / memo / artifact is a typed graph of claims and their dependencies, not the prose"
  - "we measured how much structure is shared between two famously-similar pairs of strategy papers; the answer is four linked elements in both pairs"
  - "the focal pair is Eisenhardt-Martin 2000 + Zollo-Winter 2002 on dynamic capabilities"
  - "the second pair is Grant 1996 + Liebeskind 1996 on the knowledge-based view of the firm"
  - "the same idea can be rendered into different prose, different language, different audience register, different medium — and still reach the same conclusions, IF the underlying structure is preserved"
  - "AI is cheap on the structure; humans remain expensive on the prose verification — the cost asymmetry"
  - "concrete operational implication for organizations: separate the structural artifact from the rendered artifact; AI handles structure, humans judge prose"
  - "boundary conditions where this applies (version-controlled artifacts, propositional content, audience divergence, volume exceeding human review capacity)"
  - "self-application: the Substack article you are reading is itself a worked instance of the framework — same idea, different rendering, conclusions preserved"
date: 2026-05-27
session: Session H Phase 2 (Task α self-application — P4 evidence at the Paper-B-own-spine boundary)
status: research artifact NOT publication candidate; do not post to spectralbranding.substack.com (per Session H init prompt restriction)
---

# When two strategy papers say the same thing in different words — and what that tells you about AI in your organization

Most strategy people who have read both Eisenhardt and Martin's 2000 paper on dynamic capabilities and Zollo and Winter's 2002 paper on the same topic will tell you the two papers agree on most of the important points. They use different vocabularies — Eisenhardt and Martin call them "best practices that converge to common forms," Zollo and Winter call them "deliberate learning mechanisms" — but they reach similar conclusions about what dynamic capabilities are, how they form, and why they matter for firm performance.

The same is true of Grant 1996 and Liebeskind 1996. Both were published in the same Strategic Management Journal special issue on the knowledge-based view of the firm. Grant frames the argument around how firms integrate dispersed knowledge. Liebeskind frames it around how firms protect knowledge from imitation. Different vocabularies; similar conclusions about why firms exist and what they are good for.

This is not a coincidence, and it is not just a feature of academic publishing. It points at something practical for anyone running an organization that produces knowledge artifacts at scale — memos, decks, audit reports, briefing notes, vendor evaluations, board materials — under generative AI.

## The substrate vs the rendering

Every knowledge artifact has two layers. There is the **structural substrate** — the typed graph of claims, observations, methods, findings, and the dependencies among them. And there is the **rendering** — the actual prose, in a specific language, for a specific audience, at a specific length, in a specific medium.

You can write the same substrate as a tier-1 academic paper, a board memo, a Substack article, a LinkedIn long-post, an internal Slack thread, or an investor one-pager. The renderings look completely different. The substrate underneath them is the same.

The interesting empirical question is: when two people independently produce two prose renderings of the same underlying substrate, do their conclusions actually converge? Or does the rendering medium itself distort what gets concluded?

In a recent working paper, we tested this on two of the most-cited pairs in modern strategy theory. We retroactively reconstructed the structural substrate of each paper — extracting the claims, observations, methods, findings, and the dependency edges among them — then asked how much of that substrate is shared between the two members of each pair.

The answer is four linked elements in both pairs. Four central claims with their full dependency structure intact, present in both Eisenhardt and Martin and Zollo and Winter; present again in Grant and Liebeskind. Across two different theoretical sub-domains, the same pattern: substantial structural overlap underneath very different prose.

## Why this matters for AI in your organization

Here is the cost asymmetry generative AI introduces. AI is good — and getting better quickly — at operating on structure. It can extract the substrate of a memo, audit whether each claim has a supporting observation, check whether the dependency chain has any gaps, and recombine pieces of one substrate with pieces of another. The cost of these operations scales roughly with the size of the structural graph, and it scales sub-linearly: doubling the graph does not double the cost.

AI is much less good — and is improving more slowly — at verifying the rendered prose against the substrate. Reading a 30-page board memo end-to-end and judging whether the rendered argument actually follows from the underlying substrate, in your specific organizational context, with your specific cohort of readers, is still a human job. The cost scales super-linearly with the length of the prose: doubling the prose more than doubles the human verification cost.

What this means operationally: in any organization that produces propositional knowledge artifacts at volume, you have a measurable advantage available if you separate the two layers and route AI to the substrate while keeping human judgment on the rendering. The strategy groups that already do this — the ones that maintain explicit handbooks, structured decision logs, machine-readable knowledge graphs — are already getting the cost advantage. The ones that do not, are paying full human verification cost on every rendered artifact.

## Named patterns you can recognize

You have probably seen at least one of these patterns in your own organization:

**The same insight, three audiences, three documents.** Strategy team produces an executive memo, a board deck, and an investor one-pager — all of the same underlying analysis, all written by different people on different schedules, all eventually inconsistent on the details because no one is maintaining the underlying substrate. The renderings have drifted; the substrate is not the source of truth.

**The handbook nobody updates.** GitLab and Stripe famously maintain structured, public, version-controlled handbooks. When a policy changes, the handbook changes first; the rendered communications (Slack announcements, all-hands talks, hiring deck) come from the handbook. Most organizations work the other way around — communications first, handbook drift second.

**The audit memo that reads beautifully but does not survive recombination.** Consulting partners know this one: a deliverable lands well, the client signs off, then six months later a different team tries to reuse the same analysis for an adjacent question and discovers that the underlying logic does not actually generalize. The rendering was strong; the substrate was thin.

In each case, the operational fix is the same: lift the substrate out as an explicit artifact, version-controlled, separate from any one rendering. Then any rendering can be checked against the substrate, and any future rendering can preserve the substrate or, knowingly, change it.

## Boundary conditions — where this does not apply

This is not universal. The framework applies under four conditions: authoring is version-controlled (so you can see the substrate changing over time); claims are propositional (so the substrate has typed nodes and edges, not just narrative arcs); the audience for different renderings is genuinely divergent (so the renderings have to look different); and the artifact volume exceeds what unaided human reviewers can verify (so AI assistance on the structural layer actually saves time).

If your organization produces a small number of long narrative documents read by one homogeneous audience — say, a single annual report for a single regulator — the gain is small. If you produce a large volume of structured propositional artifacts for divergent audiences — strategy groups, consulting firms, large in-house counsel, research organizations — the gain is substantial.

## A test you can run on the article you are reading

This article is itself a worked example of the framework. The underlying substrate is the same structural graph that the working paper, the academic article, and the Substack post all share. The rendering you are reading is different from the academic one — shorter, plainer, no equations, named examples instead of citations — but if the framework holds, the conclusions you reach reading this should be the same conclusions a reader of the working paper reaches.

If the framework fails, you would expect: a reader of the academic paper would walk away with a different bottom-line claim than a reader of this Substack article. That is the falsification test, and we would like to know if you experience it. Tell us in the comments.

## Three first moves for Monday morning

If you want to test this in your own organization without committing to a full transformation, three concrete moves work as starting points.

**One.** Pick any single recurring knowledge artifact your team produces — a weekly review, a quarterly board update, a vendor evaluation form. Lift the substrate out as a structured document: the claims being made, the observations they rest on, the methods used, the dependencies among them. Maintain that substrate document separately from any rendered version.

**Two.** Run two renderings of the same substrate at the same time — one for an internal technical audience, one for an external non-technical audience. Have a colleague read both and ask whether they reach the same bottom-line conclusion. If yes, the substrate is doing its job and the cost asymmetry is available to you. If no, the substrate is too thin or the renderings are not actually rendering from it.

**Three.** Instrument the cost. Track how long it takes AI to operate on the structural layer (extracting claims, checking dependency completeness, generating a draft rendering from a locked substrate) versus how long it takes a human to verify the resulting rendering. The ratio is your AI-leverage point. If the ratio is small, the substrate is not yet structured enough to give AI a clean operating surface; if the ratio is large, you have evidence of the cost asymmetry at your specific organizational scale.

The point of the working-paper research is not that any specific number — Rec equals four; β below one; δ above one — generalizes to your organization. The point is that the **separation between substrate and rendering** generalizes, and that the **direction of the cost asymmetry under generative AI** generalizes. The specific numbers, you measure for yourself.

The full working paper (with the math, the typed-graph extractions, the boundary conditions, and the iterative self-application protocol) is available at the project's Zenodo page; the public code companion is at the project's GitHub mirror. Whichever rendering you reach, if the framework is doing its work, the conclusions you land on should be the same.

— *This is a Substack rendering of the working paper "Same Meaning, Different Prose: An Empirical Demonstration of Rendering-Equivalence Under Spine-Preservation in Organizational Knowledge Work" (Zharnikov 2026ap, v1.3.0). The academic version is the source of truth on the formal definitions, the typed-DAG schema, and the per-paper extraction details. This rendering is itself a research artifact: when re-extracted, its spine should preserve the same locked propositions as the academic version's spine. Whether it does — and where it does not — is the strongest piece of evidence the framework can produce about itself.*
