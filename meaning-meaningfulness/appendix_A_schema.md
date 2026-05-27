# Online Appendix A — Substrate Schema and Preservation Theorem (Full Specification)

This appendix provides the full specification of the substrate schema referenced in the main body, the formal statement and proof of the P4 preservation theorem under axiom A1, and the inter-coder reliability threshold that operationalizes the empirical testability of A1.

## A.1 Spine as typed directed acyclic graph

The spine S of a knowledge artifact is a typed directed acyclic graph $G = (V, E, \tau)$ where V is a finite set of node-typed vertices, E ⊆ V × V is a set of typed directed edges, and τ : V → T is a typing function over the schema's 10-element node-type taxonomy T. The DAG constraint is structural: the substrate represents the logical-dependency order of claims, observations, and findings; cycles in the dependency graph indicate either circular reasoning or a missing intermediate node.

## A.2 Node-type taxonomy (10 first-class types)

| Type | Symbol | Definition |
|------|--------|------------|
| Observation | O | Raw log-layer event lifted into the spine: a captured instrument reading, AI-tool output, archival entry, or attributed edit. Immutable; does not assert anything beyond "this happened." |
| Method | M | Procedural transformation operating on observations or measurements to produce derived data, findings, or other methods. Type field distinguishes statistical analysis, simulation, formal derivation, qualitative coding, archival search, verification cascade, AI invocation, survey instrument, computation. |
| Measurement | m | Derived data produced by applying a method to one or more observations. Carries a value, an uncertainty estimate, and the units. |
| Finding | F | Inferential aggregation of one or more measurements via one or more methods; a "what is the case" claim distinct from a proposition. |
| Proposition | P | Explanatory theoretical claim; a "why is it the case" statement. Type subfield distinguishes ontological, organizational-outcome, rendering-equivalence, and empirical-finding propositions. |
| Derivation | D | Reasoning bridge between antecedent propositions and a conclusion proposition. Type subfield distinguishes deductive, cost-minimization, analogical, inductive, abductive, and formal-proof derivations. |
| Alternative explanation | A | Rival theoretical claim that the spine's propositions exclude; carries a status (candidate, rejected, partially ruled out, open) and an explicit ruling-out trace. |
| Robustness check | RC | Sensitivity analysis specifying a parameter varied, the range explored, the result-stability verdict, and the nodes the check affects. |
| Limitation | L | Honest scope assertion attached to specific nodes via an `affects` field; carries severity and mitigation pointers. |
| Negative finding | NF | Discovery of absence: expected observation explicitly not found; the negative result motivates downstream stylized facts or propositions. |
| Assumption atom | AA | Assumed-without-test premise; carries a relaxability flag and the consequence-of-relaxation trace. |

Two additional first-class types operate at the framework boundary rather than at the per-claim layer: **boundary conditions** (C-prefixed) and **stylized facts** (SF-prefixed). Boundary conditions cannot be relaxed by definition (the theory does not apply outside them); assumption atoms can. Stylized facts aggregate findings into framework-level empirical patterns.

## A.3 Edge-type catalog (17 typed relations)

| Edge | Source type | Target type | Meaning |
|------|-------------|-------------|---------|
| extends | P | P | Source extends the target proposition |
| applies | P | P | Source applies the target proposition to a new domain |
| tests | F, RC | P, AA | Source tests the target |
| contradicts | F, P | P | Source contradicts the target |
| refines | P | P | Source refines the target's statement |
| depends-on | P | P | Source's truth requires the target's truth |
| evidences | F, O | P | Source supplies evidence for the target |
| defines | P, M | construct | Source defines a construct used elsewhere |
| measures | M | O | Method extracts measurement from observation |
| aggregates | F | m | Finding is the inferential aggregation of measurements |
| generates | M | F, m | Method produces the named output |
| rules-out | F, O | A | Source rules out the alternative explanation |
| bridges | D | P | Derivation bridges antecedent propositions to conclusion |
| mitigates | RC | L | Robustness check mitigates the named limitation |
| relaxes | analysis | AA | Analysis explores relaxation of the assumption |
| motivates | NF | P, SF | Negative finding motivates downstream claim by surfacing literature gap |
| provenances | provenance | log_event | Node's provenance points to its log-layer source |

Edges are not stored as separate objects; they live in the `antecedents`, `inputs`, `outputs`, `ruled_out_by`, `aggregates_findings`, and analogous fields of node entries. The catalog above defines the semantic of each field.

## A.4 Provenance requirements

Every node carries a provenance block recording:

- `created_by`: one of `author` (human-authored), `tool:<tool-name>` (deterministic tool), or `ai:<model>+seed:<seed>+prompt_anchor:<file>` (AI invocation with reproducible prompt anchor).
- `created_at`: ISO-8601 timestamp.
- `source_log_event`: pointer to the log-layer event (git commit hash plus file:line, session log entry, or external record).
- `under_conditions`: contextual metadata (model version, environment, dataset version).
- `modified_by`: optional append-only audit trail of subsequent modifying agents.

Provenance is the bridge from the spine (S layer) to the log substrate (L layer). Without it, the S layer is detached from the artifact's actual authoring history and the framework's σ operator cannot be empirically grounded.

## A.5 Faithful extraction axiom and preservation theorem

The framework's P4 (rendering-equivalence under spine-preservation) is provable as a graph-theoretic preservation theorem under one explicit axiom of σ-faithfulness on locked subsets.

**Definition (locked subset).** For a spine S, the *locked subset* $S_{\text{locked}} \subseteq S$ is the set of nodes and edges explicitly marked by the operator's lock operation: the propositions, antecedent edges among propositions, evidence anchors attached to propositions, and the boundary conditions. The lock operation is the first changelog entry recording the spine's transition from drafting to drafted state.

**Definition (conclusion set).** For a rendering $R = \rho(S, c, \ell, m)$, the *conclusion set* of R is $K(R) := \sigma(R) \cap S_{\text{locked}}$, the σ-extracted typed-DAG restricted to the locked subset.

**Axiom A1 (σ-faithfulness on locked subsets).** For any rendering R such that ρ preserves the locked elements of S, $\sigma(R) \supseteq S_{\text{locked}}$. Operationally: when the rendering keeps the locked propositions, antecedent edges, evidence anchors, and boundary conditions visible, the σ extraction operator recovers them exactly.

A1 is an assumption about σ's extraction quality, not a derived property. It is empirically testable via inter-coder reliability on retroactive spine extractions (Section A.7 below). The threshold for empirical support is Cohen's κ ≥ .75 on both node typing and edge placement.

**Theorem (P4 — preservation under faithful extraction).** Let $S = (V, E, \tau)$ be a locked spine and let $\rho_1, \rho_2$ be two renderings of S. Then $K(\rho_1(S)) = K(\rho_2(S))$ iff both $\rho_i$ preserve the locked elements of S.

*Proof.*

(→) Suppose both $\rho_i$ preserve the locked elements of S. By A1, $\sigma(\rho_i(S)) \supseteq S_{\text{locked}}$ for $i = 1, 2$. Hence $K(\rho_i(S)) = \sigma(\rho_i(S)) \cap S_{\text{locked}} = S_{\text{locked}}$ for both i (the intersection is the full locked subset). Therefore $K(\rho_1(S)) = K(\rho_2(S)) = S_{\text{locked}}$.

(←) Suppose $K(\rho_1(S)) = K(\rho_2(S)) = K \subseteq S_{\text{locked}}$. By definition, $K = \sigma(\rho_i(S)) \cap S_{\text{locked}}$, so both σ-extractions agree on the same subset of the locked elements. Suppose for contradiction that one rendering, say $\rho_1$, failed to preserve some locked element $e \in S_{\text{locked}}$. The contrapositive of A1 implies $\sigma(\rho_1(S))$ omits e (if A1's hypothesis fails for e, A1's conclusion need not contain e). Hence $K(\rho_1(S))$ omits e. By assumption $K(\rho_1(S)) = K(\rho_2(S))$, so $K(\rho_2(S))$ also omits e. But A1 applied to $\rho_2$ (which preserves e by symmetric assumption-elimination) gives e ∈ K(\rho_2(S))$, contradiction. Hence the supposition fails: both renderings preserve every locked element.  $\square$

## A.6 Reading note on the bare-content degradation

The theorem holds as stated under the strict K-as-typed-DAG definition of conclusions: the conclusion set includes antecedent edges and node types, not only propositional content. Under a weaker bare-propositional reading in which conclusions are an unordered set of propositional contents without antecedent DAG, the ← direction degrades to a high-probability empirical claim rather than a theorem. Two renderings could coincidentally agree on bare content while one of them breaks the spine in a way the other does not — for example, by omitting an antecedent edge whose absence does not surface in the bare-content read but does change the typed-DAG structure. The framework takes the strict definition as the central one and reports the bare-content degradation as a limitation rather than a failure of the theorem.

## A.7 Inter-coder reliability threshold (operationalizing A1)

A1 is empirical, not analytic. The operational test is two-coder agreement on retroactive spine extractions, measured by Cohen's κ on both node typing (10-type taxonomy) and edge placement (17-edge catalog) over a representative subsample.

**Threshold.** κ ≥ .75 on both dimensions. The threshold is informed by the established conventions in qualitative coding methodology, which treat κ in the range .60–.80 as substantial agreement and κ ≥ .80 as almost perfect; the framework adopts the .75 lower bound to allow for the genuine difficulty of retroactive spine extraction without slipping below substantial agreement.

**Interpretation at threshold.** κ ≥ .75 supports A1 on the locked subset; P4 holds as the theorem stated above.

**Interpretation below threshold.** κ < .75 on either dimension empirically fails A1 on the subdomain in question. P4 then holds only conditional on the failed A1; the theorem degrades to a probabilistic tendency on that subdomain. A negative scope condition for the failed subdomain is documented explicitly in the spine's `negative_scope_conditions` section.

The κ ≥ .75 threshold is the empirical falsifier the framework supplies for its central theorem. The companion empirical working paper (Zharnikov 2026ap) supplies the first measurement at N = 2 twin pairs in v1.0.0 and grows the measurement basis through subsequent versions.

## A.8 Worked dependency-chain example (SF1 in v0.2 schema)

The framework's SF1 (rendering-layer hallucination under R-only access) expands in the v0.2 schema to a fully traceable dependency chain rather than a single text-string assertion:

```
O1 (logged AI literature-review response)
  └─ M1 (5-stage verification cascade method) measures O1 → produces:
     ├─ m1 (citation 1: verification verdict)
     ├─ m2 (citation 2: verification verdict)
     ├─ ...
     └─ m_n (citation n: verification verdict)
  └─ M1 aggregates m1..m_n → produces:
     └─ F1 (corpus-internal aggregate fabrication rate)
        ├─ AA1 (Crossref-authoritative-for-period assumption underlying interpretive validity)
        ├─ L1 (single-session-corpus statistical-generalization limitation)
        ├─ A1 (alternative: outdated-training-data) → ruled_out_by F1's posterior-dated fabrications
        ├─ RC1 (planned cross-session replication) → mitigates L1
        └─ NF1 (no published per-DOI benchmark at scale ≥ 100 papers) → motivates SF1's framing
     └─ SF1 aggregates [F1, indirect-published-benchmarks] → stylized fact statement
        └─ P3 cites SF1 as motivating problem (evidence type: log-anchor; citation role: motivating-problem)
           └─ D1 bridges [P1, P2, P3] → spine-first-protocol intervention
```

A reviewer reading the substrate alone sees the chain structurally; a reviewer reading only the prose rendering sees the aggregated SF1 statement and the chain is hidden in inferential reading effort. The substrate-first publication of the spine alongside the rendering is the cost-asymmetry-result operationalized at the publication-format level.

## A.9 Schema version

Schema v0.2. The schema is a strict superset of v0.1; documents produced under v0.1 parse cleanly under v0.2 (extra fields are optional). Future schema versions follow the same superset discipline: additions, not breaking changes, except across major-version increments (v1.x → v2.x) where breaking changes are signalled by an explicit migration recipe in the schema reference document.
