# Pre-Declared Decision Rule — Internalization (2026bk)

**Status: PRE-DECLARED 2026-08-06, before any run, before any prose.** Nothing in this document
may be revised in the light of a result. If a threshold here turns out to be wrong, the paper
reports that it was wrong and reports the number it actually got; it does not move the line. Any
change made before data collection begins is a FORK with a changelog row and a stated reason that
does not refer to an observed outcome.

The standard this document is written against is simple: *pre-declaring a rule that the run might
fail is the whole point.*
Without it the result is unfalsifiable by construction, because any outcome can be narrated as a
partial success after the fact.

---

## 0. What changed before the rule could be written

Writing the rule surfaced a defect in the spine, and the defect had to be fixed first.

RC1 as locked specifies extraction agreement as "a graph edit distance supplied as the distance
function to an agreement coefficient that admits custom distances" — Krippendorff's alpha
parameterized by graph edit distance. The Phase-2 query found **no prior art for that
construction**. Alpha requires an expected-disagreement term; computing it over the combinatorial
space of random typed graphs is not a detail to be handled at implementation time, and without a
defended approximation the coefficient has no interpretation.

So the spine as locked would have required the paper to **invent and defend a new agreement
instrument** — an unplanned methodological contribution, decisive under L0, sitting on the one
robustness check the paper cannot afford to lose. It is exactly the class of error the pre-draft
gate exists to catch, and it is caught here at the cost of a rebase rather than at the cost of a
referee report.

**RC1 is rebased onto instruments that already exist and that reviewers already accept.** The rule
below uses them.

---

## 1. Extraction agreement (RC1, rebased) — the layered rule

Agreement is **not** reported as a single number over the whole graph. It is layered, because the
failure modes are different at each layer and because a single graph-level statistic hides which
one fired. Layer separation is also what a competent methodology referee will require.

### Layer 1 — Node recovery

Two independent operators extract the artifact. The unit is the typed spine node (proposition,
method, evidence, assumption, boundary condition).

- **Statistic**: Krippendorff's alpha, nominal, over node type assignments on unitized spans,
  reported alongside raw node-boundary precision and recall.
- **Pre-declared threshold**: **α ≥ .65**.
- **Justification**: this is *below* the flat-label conventions on purpose. The .70/.80
  conventions originate in categorical diagnostic agreement (Landis & Koch 1977) and their
  transfer to structured annotation is specifically criticised (Artstein & Poesio 2008). The
  scientific-argument-mining literature is the right reference class, and it sits lower than the
  essay-scoring literature does.

### Layer 2 — Edge recovery given agreed nodes

Computed only over nodes both operators recovered. This is the layer the whole paper rests on: an
edge is a dependency, and a dependency graph is what P1 and P2 are about.

- **Statistic**: triple-overlap F1 in the Smatch sense (Cai & Knight 2013) — the maximum F1 over
  matched `(node, edge-type, node)` triples — reported **against a random-graph null**, not as a
  bare number. The null is the expected triple overlap of two operators assigning the same
  marginal edge-type distribution at random over the agreed node set. The corpus already has
  precedent for a random-graph null in this exact role.
- **Pre-declared threshold**: **F1 ≥ .60, and the null must be exceeded at the 99th percentile.**
- **Justification for .60 rather than the .83 expert ceiling reported for AMR**: that ceiling is
  for a fixed annotation scheme with a trained annotator pool on sentence-scale semantics. This
  task is document-scale dependency extraction with a schema not designed for it, on a specimen
  from a domain that omits dependencies by convention (L1). Declaring .83 here would be declaring
  a number the task cannot produce, which is a way of guaranteeing a null result rather than
  risking one.
- **The chance-correction objection is conceded in advance, not answered after the fact.** Smatch
  F1 is not chance-corrected. That is precisely why the random-graph null is part of the rule
  rather than an appendix: the null does the work chance-correction would do, and it is reported
  whether or not it flatters the result.

### Layer 3 — Load-ranking agreement

- **Statistic**: rank correlation between the two operators' M3 load rankings, over the agreed
  node set, under the pre-committed centrality definition.
- **Pre-declared threshold**: **ρ ≥ .50**, reported with the RC2 sensitivity across the alternative
  centrality definition.
- **Note**: this threshold is deliberately weak. It is a report-and-inspect layer, not a gate. A
  low value is informative — it would say the divergence claim in P2 is unstable under operator
  variation — and the paper says so rather than suppressing the layer.

### The pilot, and what it may and may not change

A **pilot on a small number of documents runs first**, on material that is *not* either specimen,
and its distributions are reported. Its purpose is to check that the extraction protocol is
executable at all and to estimate variance.

**The pilot may not move the thresholds above.** They are declared now, in advance of it. The
pilot may only (a) refine the annotation guidelines, (b) inform the number of documents in the
main run, or (c) cause the study to be abandoned before the main run — in which case the paper
reports that too. Allowing a pilot to reset thresholds is the standard way a pre-declaration is
quietly converted into a post-hoc rationalisation, and it is forbidden here by name.

### What failing this layer means

If Layer 2 falls below .60 or fails to beat the null, **AA1 is refuted at the declared level and
the paper says so in the abstract.** It does not proceed to report downstream miracle counts and
acceptance-test results as though the input were sound — L0 already commits the paper to making no
downstream claim at an agreement level it has not demonstrated. The honest paper in that world is
a negative result about the extraction frontier, which is publishable and is the fallback that
keeps the work truthful.

---

## 2. Validation recovery targets (VC1) — what counts as recovery

Three targets, each scored separately so that a partial recovery implicates a specific pipeline
step. Each is scored by **two raters blind to the pipeline's provenance**, against the exposition's
own statements.

| # | Target | Counts as recovered when |
|---|---|---|
| T1 | The generative object | The extracted graph contains a single node from which the extracted derivation edges to the separable goals originate, and it corresponds to the object the exposition presents as generative. Partial credit is not available: it is one node or it is not. |
| T2 | The stated decomposition | The extracted graph contains the author's separable goals as distinct nodes, with the decomposition represented as edges from the rebased statement, and no goal is merged with or split from the author's own division. |
| T3 | The marked residuals | Every step the author explicitly marks as unexplained is classified `miracle`, and no step the author derives is classified `miracle`. Scored as two error counts (missed residuals, false residuals), both of which must be zero. |

**The pre-declared success rule: T2 and T3 must both be recovered.** T1 is reported and is not
part of the rule.

**Scope note added 2026-08-06 (operator decision on the ladder).** T1–T3 are scored on renderings
whose authors state a decomposition and mark residuals. That is the expert rung (VC1 / R2) and
VC2. **They are not scored on R0 or R1**, which mark no residuals — T3 is vacuous there, and
scoring T1–T3 on a rendering that does not label itself would be scoring the analyst's
reconstruction rather than the author's declaration. The ladder's own criteria are in §2a.

## 2a. The ladder (VC3) — pairwise preservation and monotonic ordering

Three renderings of one fixed result: R0 raw automated output, R1 the human-edited exposition of
that output, R2 the independent expert digestion. **Each rung is extracted independently; no rung
is ever generated from another.** The pipeline is not asked to reproduce an insight, which is what
would make this a test of discovery rather than of extraction.

**Pre-declared, before any extraction:**

1. **Pairwise spine preservation** across R0–R1, R1–R2, R0–R2, each at the Layer-2 threshold of
   §1. Each check gates only the comparison it spans.
2. **Monotonic miracle ordering** under one declared reader model:
   $\mathrm{MC}(R_0) > \mathrm{MC}(R_1) > \mathrm{MC}(R_2)$. Strict. **Any inversion
   disconfirms.** This is deliberately a stronger commitment than a single directional difference
   — an ordering over three points is much harder to obtain by chance, and correspondingly easier
   to fail.
3. **Prose-mass divergence**: prose mass across the rungs against structural load across the
   rungs. If structural load is approximately constant while prose mass varies by a factor of
   several, that is P2 measured rather than argued.

**A count that falls over an unpreserved spine is never reported as a lowered count.** If R0–R1
preserves and R1–R2 does not, the first differential is reported and the second is not.

**Pre-declared branch — the expert rung fails preservation.** This is a finding, not a null. It
would mean expert internalization sometimes *replaces* structure rather than preserving it,
bounding P5 and the inherited rendering-equivalence result — which hold only under spine
preservation and would not apply to that rung — and saying that the operation specified here is
narrower than what a human expert does. Declared now precisely so it cannot be narrated as a
success later.

The reasoning, recorded so it is not reconstructed later. T2 is the structural claim — if
extraction cannot recover a decomposition the author *states in the text*, step 1 does not do what
step 1 claims, and the easiest possible case has failed. T3 is contribution 2 — the miracle count
is the paper's measurement contribution, and a count that misclassifies the author's own declared
residuals is not measuring explanatory status. T1 is excluded from the rule deliberately: it is
the target most exposed to the discovery/extraction confusion that already forced one rebase, and
a rule that depends on it would be a rule about mathematical insight rather than about extraction.

**T3 is the strictest clause in this document and it is meant to be.** Requiring both error counts
at zero on a specimen with exactly two marked residuals is a genuine risk of failure. A looser
rule — "most residuals recovered" — would be unfalsifiable at N = 1.

---

## 3. Acceptance-test clauses (M5) — what counts as passing

Administered per reader, under a declared reader model (C2). All three clauses are scored against
the extracted graph and the M3 ranking, both fixed before administration.

### Clause (a) — restate the spine unaided

- **Pass**: the reader's unaided restatement recovers the graph's nodes and dependency edges at
  **triple-overlap F1 ≥ .60 against the reference extraction**, using the same statistic and null
  as Layer 2 above.
- **Why the same number**: a reader is held to the standard two operators are held to, and not a
  higher one. Using a different threshold here would be arbitrary.
- **Corpus consequence**: this clause is the reader-side twin of 2026t P6, which asserts
  reconstruction at high agreement and is explicitly stated-but-untested with a falsifier at
  κ = .70. **This paper does not adopt P6's .70**, because P6 states it over a different unit;
  the paper must say so explicitly rather than appear to have retired P6 at its own declared
  level. What this paper can retire is P6's *untested* status, not its threshold.

### Clause (b) — name the step the rest depends on and what breaks without it

- **Pass**: the reader names a node in the **top decile** of the M3 load ranking, **and** states a
  consequence of its removal that a blind expert rater judges correct.
- **Both conjuncts are required.** Naming the right node with a wrong counterfactual is a fail;
  the clause tests whether the reader holds the dependency, not whether they can point at it.
- Rated by two blind raters; disagreements resolved by a third, with the rate of third-rater
  recourse reported.

### Clause (c) — execute one open fork

- **Pass**: the reader produces an output that satisfies an acceptance condition written **before
  administration** and checkable without reference to the reader's reasoning.
- **The transfer distance of the chosen fork is declared before administration** and reported with
  the result. This is not optional. A fork chosen too near proves nothing, and one chosen too far
  makes failure uninformative — the skeptical baseline in the transfer literature is that
  spontaneous far transfer is close to absent, so an undeclared distance lets any outcome be
  narrated favourably.

### The overall acceptance rule

**A comprehension claim requires all three clauses to pass.** Not two of three. The contract in
P4 is conjunctive by construction — clauses (a) and (b) are structure-recovery and clause (c) is
transfer, and the paper's own argument is that the third is what separates the contract from a
satisfaction rating. A disjunctive rule would let a reader pass on the two clauses the paper
already claims are easier.

Per-clause pass rates are reported separately regardless of the overall verdict, because a pattern
of passing (a) and (b) while failing (c) is itself the paper's most interesting possible finding:
it would say the pipeline delivers structure without delivering transfer.

---

## 4. Scope limits on this rule

Three things this document deliberately does not do.

1. **It sets no threshold for P2's prose-mass / structural-load correlation.** That measurement's
   corpus is still an open question in the spine — specifically whether a spine-first-drafted
   corpus is a biased sample — and a threshold declared before the sampling frame is settled would
   be theatre. It is pre-declared separately, before that run, or the run is not made.
2. **It sets no cross-reader or cross-specimen comparison rule.** L2 and C2 forbid comparing
   miracle counts across reader models, and nothing here creates an exception.
3. **It does not pre-declare a sample size for the acceptance test.** At v1.0.0 the paper is an
   existence proof (§3 of the thesis), the test is expensive per administration (L3), and a
   declared N would imply a power claim the design does not support. The paper reports the N it
   ran and claims no more than an existence proof supports.

## 5. Stopping rules

- **Extraction fails Layer 2** → the paper becomes a negative result about extraction fidelity;
  downstream stages are reported as not evaluable, not as unevaluated.
- **T2 or T3 fails on the mathematical specimen but passes on the non-mathematical one** → the
  domain-hostility reading is supported, L1's mitigation fires as written (the mathematical
  specimen is demoted from validation to illustration), and the scope narrows to non-mathematical
  argumentative artifacts.
- **T2 or T3 fails on both specimens** → the pipeline does not recover author-stated structure.
  The paper reports that. Contribution 3's closure is unsupported and the paper is rewritten as a
  protocol-plus-negative-result, which is the narrow fallback shape this design reserves for that case.
- **Acceptance test passes (a) and (b), fails (c) across readers** → reported as the primary
  finding, not as a limitation. See §3.
- **The ladder's ordering inverts at any rung** → P3's central operational claim is disconfirmed
  on the cleanest available case, and the paper says so in the abstract. It does not fall back to
  reporting the pairwise differences that happened to run the right way; that is the selection
  the pre-declaration exists to prevent.
- **The ladder's ordering holds but preservation fails throughout** → nothing about the miracle
  count is licensed, and the run is reported as a preservation failure. An ordering over
  unpreserved spines is not evidence for P3, because the counts are not comparable.
