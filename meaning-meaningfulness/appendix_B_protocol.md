# Online Appendix B — Spine-First Drafting Protocol (Operational Specification)

This appendix specifies the operational protocol that follows from the cost-asymmetry result in the main body. The protocol prescribes how an Operator should produce a knowledge artifact under conditions C1–C4. It is the cost-minimizing arrangement of Operator operations under the parameter regime β < 1 < δ. The protocol's enabling artifact (the substrate schema) is specified in Online Appendix A; its calibrated cost analysis is in Online Appendix C.

The protocol's full reference specification lives at `research/SPINE_FIRST_DRAFTING_PROTOCOL.md` in the project repository. This appendix reproduces the operational core for the paper's reader.

## B.1 The four operations

Every change to a spine S is one of four named operations. The operation is recorded as an append-only entry in the spine's changelog.

| Operation | When | What it does |
|-----------|------|--------------|
| **lock** | Phase 0.5 of the draft workflow | Initial substrate committed. Locked elements (propositions, antecedent edges, evidence anchors, boundary conditions) are marked. Drafting protocol activates: prose drafting cannot proceed without a locked spine. |
| **fork** | Prose surfaces a claim not yet in the spine | The new claim is added as a spine node with full provenance. Downstream reviewer verdicts re-validate; the spine version increments. |
| **rebase** | Prose contains a claim that does not align with the spine | The claim is dropped from prose. Alternatively, the claim is refactored to fit an existing spine entry. The operation records the disposition. |
| **merge** | Two propositions collapse into one | The spine entries combine. Body sections pointing at either entry are updated to point at the surviving entry. Provenance preserves both pre-merge lineages. |

Every operation appends a changelog entry. The spine is append-only at the file-history level (git tracks it) and at the changelog level (every operation recorded inline).

## B.2 The four-step drafting cycle

The Operator applies the following cycle each time prose is drafted or revised.

**Step 1 — Read the spine.** Before writing any prose, the Operator reads the artifact's spine (or creates one if none exists). Every prose claim the Operator intends to write must map to a spine entry. The mapping is checked node-by-node.

**Step 2 — Verify trace.** For each prose claim being written, the Operator verifies that a corresponding spine entry exists. If a claim has no spine support, the Operator performs either a fork (extend the spine first; then write the claim) or a rebase (drop the claim from prose). The Operator never silently introduces body content lacking spine support.

**Step 3 — Document fork or rebase.** Each fork or rebase operation appends a changelog entry recording the operation, the date, the agent (author, tool, or named AI invocation), and a note describing what changed and why.

**Step 4 — Surface separately to reviewers.** Reviewers receive both the spine and the prose. The reviewer's evaluation of substrate coherence and the reviewer's evaluation of prose craft are recorded separately. The Operator addresses substrate-coherence comments at the substrate layer (with further fork or rebase operations) and prose-craft comments at the rendering layer (with edits that preserve the locked subset).

## B.3 Operator's role in projection composition

The drafting cycle's two operation classes map to two projection composition modes.

*Structural-substrate operations during drafting* — surface a candidate proposition; check its DAG consistency against existing nodes; suggest the typed edges to existing nodes; pre-fill provenance metadata from the log-layer event; flag rivals already in the spine; flag robustness checks the new proposition affects. Under the post-AI projection composition, these operations execute under AI projection with the Operator reviewing. Under the pre-AI projection, the Operator performs them by hand.

*Judgment operations during drafting* — decide whether to fork or rebase a surfaced candidate; decide what the proposition's edges should be when the AI suggestion is wrong; decide whether the proposition's cohort-specific rendering serves the audience; decide whether the substrate operation reflects the Operator's intent. These operations execute under human projection across all current and near-future composition modes.

The protocol does not prescribe which projection composition mode an Operator should adopt. It prescribes the operation classes and the changelog discipline. The choice of projection composition is an Operator-level decision constrained by available capability, organizational policy, and the Operator's confidence in current AI projection quality on the artifact's domain.

## B.4 Reviewer separation

Reviewers under the protocol receive two artifacts: the spine and the rendering. The spine is evaluated against substrate-coherence criteria: are the locked propositions well-formed? Are antecedent edges supported by evidence anchors? Are rivals adequately surfaced? Are robustness checks present where central claims warrant them? Are limitations attached to the nodes they affect? The rendering is evaluated against prose-craft criteria independently: is the prose clear? Does it serve the target cohort? Does it respect the venue's length and structural conventions?

Decoupling the two evaluations addresses the cost asymmetry at the review layer. Under the pre-AI projection composition reviewers carried both evaluations simultaneously and the cost-asymmetry cascade compressed both surfaces into a single review verdict that mixed substrate and prose objections. Under the post-AI composition the two evaluations are separable because the spine is published as a first-class artifact; the review surface separates accordingly.

## B.5 Boundary conditions for protocol application

The protocol applies to artifacts under the framework's boundary conditions C1–C4 (Section *Boundary Conditions and Negative Scope* in the main body). The protocol does not apply to single-line copy edits, frontmatter changes, citation-format-only revisions, social-media posts, internal memos, or commentary that does not introduce new propositions. When in doubt: if the change requires reading paragraphs of prose to make, the spine must be consulted; if the change is local to a single field or token, the protocol does not apply.

## B.6 Self-application

The present paper is the first paper drafted under the protocol. The paper's substrate is published as a Zenodo companion artifact alongside the rendering. The companion paper (Zharnikov 2026ap) is itself drafted under the protocol, and each version of the companion paper is a worked self-application instance at the empirical-companion scale: each version is a rendering of a growing spine; the changelog-per-version is the log layer; the spine-per-version is the substrate; the paper.md per version is the rendering. The iterative-versioned working-paper format the companion paper adopts is itself a worked operational instance of P4 under cohort growth.

## B.7 Tooling

Reference tooling is available at `research/code/` in the project repository: `coverage_diagnostic.py` for single-paper spine-engagement checks; `verify_citations.py` for the five-stage cascade applied to spine evidence anchors; `extract_citation_contexts.py` for retroactive spine extraction from external paper.md or PDF sources. Tooling is not a precondition for the protocol; the protocol's discipline operates equally on hand-edited spine files. The tooling is a cost-amortization layer that exploits AI projection on structural-substrate operations to reduce the Operator's structural-substrate workload further.

## B.8 Audit discipline

The append-only changelog at the spine level is the bridge from the protocol to the log substrate. Every operation traces to a log-layer event (a git commit; a session log entry; an external record). The Operator's first-person substrate access — the operator's judgment about which substrate slice to query — is exempt from external audit, but every artifact-level operation that touches the spine is recorded. The audit discipline is what makes the protocol's substrate-coherence evaluation reproducible by external reviewers without requiring access to the Operator's first-person substrate.
