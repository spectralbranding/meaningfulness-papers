# Internalization as an Operation: Recovering the Dependency Structure of a Result, and a Pre-Registered Failure to Do So

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.21828980](https://doi.org/10.5281/zenodo.21828980)

Working Paper v1.0.0 – August 2026

## Abstract

Machine systems now produce results faster than readers absorb them, and machine-generated summaries are widely observed to emphasize the wrong material. This paper argues the failure is structural, not one of model capability. Given only prose, a renderer can weight content by prose mass — the text an idea occupies — while the property it needs is structural load, defined over the dependency graph. The two diverge: a one-line lemma can carry an argument that pages of routine verification do not. The paper specifies a five-step internalization procedure, the inverse of structured drafting — prose to dependency graph to a second rendering — and supplies the measurement it requires: a miracle count, the number of steps verified but not derived from what a declared reader holds. Decision rules and agreement thresholds were fixed before any run. In the pre-registered validation, two machine operators from different model families extracted five documents; edge-level agreement fell below the declared threshold on every one, and the operators diverged on which nodes exist before how nodes connect. That extraction is well posed is refuted at that level, no downstream quantity is licensed, and the specification, the instrument, and the negative result are reported together.

**Keywords**: internalization, dependency structure, spine extraction, explanatory quality, argumentation mining, inter-annotator agreement, reader model, pre-registration.

---

A result that no one has absorbed is not yet knowledge. The gap between producing results and absorbing them has widened, and the response has largely been to produce more explanations — summaries, slide decks, generated overviews — whose recurring complaint is that they emphasize the wrong things. The complaint is not only anecdotal. Machine summaries of scientific work systematically overgeneralize what the work claims, broadening scope-limited findings into unqualified ones [@peters-chin-yee-2025-generalization-bias-summarization], and reading a result through a machine synthesis rather than the sources leaves the reader holding less of it afterwards [@melumad-yun-2025-depth-of-learning]. That second finding cuts against this paper as well as for it: if machine-mediated reading degrades depth generally, then some part of the deficit is not a missing-graph problem and would not be repaired by supplying a graph. The complaint is usually read as a quality problem to be solved by better models. This paper argues that at least part of it is a missing-input problem, and that the missing input can be named, recovered, and measured.

The argument rests on a distinction between two properties of an artifact. **Prose mass** is the quantity of text an idea occupies. **Structural load** is the extent to which a node carries the argument, and it is defined over the dependency graph — which claim stands on which — rather than over the text. A renderer given only prose can weight by the first. What it needs is the second. Nothing in the drafting process constrains the two to agree, and in technical writing they routinely do not: a single lemma may carry an entire result while pages of routine verification carry none. Any renderer denied the graph is therefore optimizing a proxy that is not reliably correlated with the quantity it needs, and no increase in capability repairs a missing input.

Zharnikov [-@zharnikov-2026ao-spec-based-research-post-ai] decomposes a knowledge artifact into a log substrate, a semantic substrate or spine extracted from it, and a cohort-conditional prose rendering produced from the spine, and states that verification cost on the structural layer scales sub-linearly with claim volume while cost on the rendered layer scales super-linearly. The present paper takes the reader's side of that asymmetry: the human-side exponent is the one that did not fall. It does not re-litigate the asymmetry; it inherits it.

The operation this paper specifies is the inverse of structured drafting. Drafting runs spine to prose. **Internalization** runs prose to spine to the reader's prose, in five steps — recover the dependency graph from the rendered artifact; negotiate that graph against the terms the reader already holds; compute which nodes are load-bearing over the graph rather than over the text; re-render for the reader's cohort; and submit the result to an acceptance test. Four of the five reuse machinery that already exists. The contribution is the closure, and the measurement that makes the closure checkable.

**Scope of the motivating claim.** The paper does not claim internalization is *the* bottleneck in contemporary research. Work on large scientific fields argues that as output scales the binding constraint is finite collective attention and reliance on prestige signals rather than structural illegibility: readers stop reading derivations at all [@chu-evans-2021-slowed-canonical-progress; @fortunato-2018-science-science]. That evidence competes with the motivating story, and the paper cites it rather than routing around it. The defensible claim is narrower and survives it: *for a reader who has decided to engage with a result, structural illegibility is a distinct and addressable constraint.*

**What this release does.** It specifies and instruments the operation, pre-registers its validation, and reports the result of running it — which is a failure at the first gate. The decision rules, agreement thresholds, and success criteria stated below were fixed before any data collection, and every one of them is reported against here, including the two that the run did not reach and the several it did not pass. That ordering is the point: a decision rule published after a run is not a decision rule, and a specification whose first empirical test fails is worth more in the open than in a drawer.

The remainder proceeds as follows. The Theory section states the inverse operation, the prose-mass/structural-load divergence, the miracle count, the acceptance contract, and the delta-rendering result, and positions each against the literature that already owns parts of it. The Method section specifies the five steps, the measurement stack, and the pre-declared decision rule. The Validation Design section states the two specimens and what would count as recovery. The Discussion section addresses the rival explanations and the boundary conditions. Limitations and Acknowledgments close.

## Theory

### *What the prior-art sweep took away.*

The paper concedes early, because conceding costs nothing and buys attention for what is new. The pipeline's components are individually owned elsewhere. Understanding a proof as the ability to modify, apply, and trace it is the standard philosophical account [@avigad-2008-understanding-proofs]. Internalization as the real social function of a proof, against mere formal checking, is a canonical position [@de-millo-1979-social-processes-proofs], and the argument that mathematical assimilation rests on intuition and tacit knowledge rather than on formal derivation is stated from inside mathematics [@thurston-1994-proof-progress-mathematics]. Comprehension as textbase extraction followed by integration with prior knowledge is a decades-old cognitive model whose two stages map onto steps 1 and 2 almost exactly [@kintsch-1988-role-knowledge-discourse]. Adapting instruction to held knowledge is the expertise-reversal literature [@kalyuga-2003-expertise-reversal-effect]. Graph centrality for summarization salience dates to 2004 [@erkan-radev-2004-lexrank-graph-based]. A proof skeleton that keeps logical dependencies and drops routine verification is a named object in formal methods [@wiedijk-2004-formal-proof-sketches]. Audience-relative, contrastive explanation is the settled position in explainable artificial intelligence [@miller-2019-explanation-artificial-intelligence]. Representing a paper as an extracted claim graph is industrialized [@groth-2010-anatomy-nanopublication].

So the framing *internalization is the inverse of drafting* is, on its own, incremental — the cognitive model mapped onto the proof-skeleton construct and justified by the social-processes argument. It is retained as the paper's organizing device and dropped as the paper's claim. What survives is stated below: the divergence of structural load from prose mass and its identification as the failure mechanism; the count of verified-but-unexplained steps as a measure nobody currently takes; and the closure of the loop from graph back out to a reader-addressed rendering with a test attached.

### *The inverse operation.*

**P1.** Internalization is the inverse of structured drafting: where drafting maps a dependency graph to prose, internalization maps prose to a dependency graph and then to a second prose rendering addressed to a specific reader. The inverse is a specifiable procedure over the artifact's structure, not a matter of authorial talent.

The forward protocol is already stated as a procedure with typed nodes and typed edges, so running it in reverse is defined on the same type system. That the reverse direction is at least performable is established rather than assumed: retroactive spine extraction from independently authored published papers has been executed and shipped as worked cases [@zharnikov-2026ap-same-meaning-different-prose].

P1 is falsifiable. If two competent operators running the stated procedure on the same artifact for the same declared reader produce dependency graphs whose agreement is at chance, the procedure does not specify an operation and P1 is false. The agreement level at which this is tested is declared in the Method section, before any run.

### *Why prose-only explanation misses.*

**P2.** A renderer given only rendered prose can weight content only by prose mass, while structural load is a property of the dependency graph. Because the two are not reliably correlated, the quality of a prose-only explanation is bounded by that correlation and does not improve with renderer capability alone. The failure is a missing input, not a missing ability.

The analytic case is immediate: structural load is defined over dependency edges, prose mass over token counts, and nothing in drafting constrains them to agree. The empirical case is stronger than the analytic one and comes from reading behaviour. Eye-tracking of expert and novice readers of mathematical proofs finds research-active mathematicians moving across structurally load-bearing logical dependencies while undergraduates fixate on surface manipulation and dense calculation [@inglis-alcock-2012-expert-novice-approaches]. That is the divergence measured in humans, in the domain the first specimen occupies.

A second line matters because it locates the mechanism precisely. Graph-based salience for summarization has, since its introduction, run over graphs whose nodes are *surface sentences* and whose edges are lexical similarity [@erkan-radev-2004-lexrank-graph-based], which keeps the ranking correlated with prose mass — pages of routine verification produce many well-connected nodes. Replacing surface nodes with discourse-structural ones changes the ranking [@xu-2020-discourse-aware-neural], and structural centrality tracks human importance judgments where surface frequency does not [@louis-2010-discourse-indicators-content]. The mechanism is therefore *node choice*, not graph machinery.

P2's falsifier is a correlation the paper must measure rather than assert: if prose mass and graph-derived structural load are strongly correlated across a corpus of argumentative artifacts, the diagnosis is empty and P2 is false.

**D1.** The five-step pipeline follows from P2 by a locate-the-missing-input argument. If the deficiency of prose-only explanation is the absence of the dependency graph, then supplying that graph, differencing it against the reader, weighting by it, and rendering from it is the minimal repair, and an acceptance test is what makes the repair checkable.

### *Measuring an explanation.*

**P3.** Under a declared reader model and a fixed result, explanatory quality is measurable as a **miracle count**: the number of nodes that are verified but not derived from anything the reader holds. Internalization is the operation that lowers this count. It does not drive it to zero; a successful internalization localizes and names its residual rather than concealing it.

The metric is adopted rather than invented, and the term is not the paper's coinage. A working mathematician, digesting a recent counterexample for his own understanding, states that he sought to write the explanation "in a manner that minimizes the amount of 'miracles' required" — then adds that a few places of remarkable phenomena remain, and marks one of them as something he can verify but cannot satisfactorily explain [@tao-2026-digestion-jacobian-counterexample]. That is the metric, its objective, and its residual class, stated by a practitioner without prompting. Formal-methods practice counts *unverified* steps; nobody counts verified-but-unexplained ones.

The distinction the count rests on is not hypothetical, and the clearest demonstration comes from the production side rather than the reader side. A recent collection presents ten long-open results in mathematics and theoretical computer science, each accompanied by a machine-checkable formal certificate [@openai-2026-ten-advances-mathematics]. Every result in it is fully verified; none is thereby explained. A certificate establishes that each step follows and supplies no account of why the construction works or which step carries the argument — it is the `verified_only` class in its purest available form, produced at scale. Verification and explanation are coming apart faster on the supply side than any reader-side remedy currently addresses, which is the condition this paper takes as its problem.

Operationally the metric adds one field to the spine schema: a per-node **explanatory status** taking one of three values relative to a declared reader model — `derived` (follows from nodes the reader holds), `verified_only` (checkable but not derived), or `miracle` (neither derived nor reducible, and named as such). The miracle count is the cardinality of the third class:

$$\mathrm{MC}(R \mid M) = \bigl| \{\, v \in V(\sigma(R)) : \mathrm{status}(v \mid M) = \texttt{miracle} \,\} \bigr|$$

where $R$ is a rendering, $M$ a declared reader model, and $\sigma$ the extraction operator.

**The fidelity precondition is part of the metric, not a caveat attached to it.** The count is scored only on renderings that preserve the source spine. Without that constraint it is trivially minimized by replacing load-bearing derivations with analogies the reader already holds, which lowers the score while destroying the argument — the metric would then measure familiarity rather than explanation. This is the objection the pragmatic, audience-relative account of explanation makes in general form [@miller-2019-explanation-artificial-intelligence; @van-fraassen-1980-scientific-image], and it is answered structurally rather than by assurance.

P3 is falsifiable: if, holding reader model and result fixed, independently scored miracle counts do not order a set of explanations consistently with expert judgments of explanatory quality on the same set, the count does not measure what it claims.

A scope note, and it is a real one. Contribution 2 sits in tension with the account locating explanatory power in objective properties of a proof such as symmetry and unity rather than in a reader-relative difference [@lange-2015-depth-explanation-mathematics]. The paper does not contest that account.[^lange] Its centre of gravity is the protocol and its measurement; the philosophical engagement is support, not spine.

[^lange]: The two address different questions. The objective account asks what makes a *proof* explanatory, as a property of the mathematics. The miracle count asks what makes an *exposition* explanatory *to a declared reader*. Both can hold. The count does not deny that some arguments are objectively deeper — it declines to measure that, and measures a reader-relative quantity instead, reported with its reader model and comparable only within a fixed model.

### *An acceptance contract for comprehension.*

**P4.** Comprehension admits an acceptance contract stated before the explanation is written and checked after it is read, with three clauses: restate the dependency structure unaided; name the load-bearing step and what fails without it; and execute one step the structure marks as open. The third clause has an objectively checkable outcome, which is what separates the contract from a satisfaction rating.

The move is inherited. Writing the acceptance condition as a runnable test *before* the process that is supposed to satisfy it is the design principle of experience-first specification [@zharnikov-2026-organizational-schema-theory-test-driven], and the waste criterion there — a node from which no path reaches an acceptance contract — is the structural analogue of a step that carries no load. What narrows here is the object under test: the deliverable whose acceptance is contracted is a reader's state rather than an artifact.

The closest existing corpus precedent is the proposition that a domain expert reading only machine-readable structure can reconstruct a paper's claim structure at high agreement against an expert reading the full paper [@zharnikov-2026t-paper-as-specification], which is explicitly stated but untested. Clause (a) is that proposition's reader-side twin. What this paper can retire is its untested status, not its threshold — the two state agreement over different units, and the paper says so rather than appearing to have satisfied a criterion it did not test.

P4's falsifier: if readers who pass all three clauses are indistinguishable, on an independent expert assessment of understanding, from readers who fail the third, the contract does not discriminate.

### *Define only the delta.*

**P5.** The rendering a reader needs is determined by the difference between the artifact's ontology and the reader's held ontology, not by the artifact alone. Because that difference is computable from a compatibility classification, the instruction to define only what the reader lacks is an operation rather than an aphorism.

Two prose renderings of the same locked structure converge on the same conclusions while differing on every surface dimension — language, register, ordering, tone, length, medium — provided both preserve the spine [@zharnikov-2026ao-spec-based-research-post-ai; @zharnikov-2026ap-same-meaning-different-prose]. Re-rendering for a reader is therefore a licensed operation rather than a lossy paraphrase.

The strongest form of the reader-side claim already on record is that a reader, or their tooling, can negotiate a paper *before* reading its prose [@zharnikov-2026-research-as-repository-git-native]. Step 2 is the case where one of the two negotiating parties is the audience.

P5's falsifier: if renderings built from the computed difference are not preferred, on comprehension outcomes, to renderings built from the artifact alone for the same readers, P5 is false.

### *Boundary conditions.*

The theory does not apply outside four conditions. **C1**: the artifact carries an argument with a recoverable dependency structure; data releases, catalogues, and purely narrative work are out of scope. **C2**: a reader model is declared before any measurement, and comparisons across reader models are not licensed. **C3**: the result is held fixed — the operation improves the explanation of a result, not the result. **C4**: the reader's held terms are themselves expressible as a module of owned and imported terms.

**C5 states the negative scope**, which the other four do not: the conditions under which the operation is expected to fail *even when step 1 recovered the dependency structure correctly*. Without this the operation is unfalsifiable below its first stage, because every downstream failure can be attributed to extraction. Three conditions are declared. **Without a declared reader model**, the negotiation step has nothing to difference against, the delta is undefined and the miracle count has no referent — the operation does not degrade gracefully here, it does not apply. **Without author-marked residuals in the source**, residual recovery cannot be scored, so the fidelity of the explanatory-status assignment is unaudited even where structure recovery succeeds. **Where a source's structure is supplied by genre template rather than by argument**, recovery may reflect section headings rather than dependency structure, and a pass carries little evidential weight.

Two of the three are instantiated by the specimen set rather than hypothesised: VC3 has no author-marked residuals, and the design-rationale document held in reserve is the template case.

Four assumptions were made without test when the design was fixed. The run has since changed the status of two, and each is stated below with the status it now carries. **AA1**: a rendered argumentative artifact has a dependency structure two competent extractors recover with better-than-chance agreement; if agreement is at chance, step 1 is not a measurement and the remaining steps inherit an unmeasured input. *Tested, and refuted at the declared level — this is the paper's principal result, reported below.* **AA2**: the reader's held knowledge can be elicited at a granularity comparable to the extracted graph's. *Untested; no reader was recruited.* **AA3**: an expert's own written account of how he decomposed a result is a usable label for that result's dependency structure. *Untested, and it is the assumption the recovery targets rest on.* **AA4**, which is not relaxable: a miracle count is scored only on a rendering that preserves the source spine. *Converted by the ladder from an assumption into a measurement at every rung; those measurements ran, and under the decision rule the counts they gate are not licensed.*

## Method

### *The five steps.*

**M1 — Spine extraction.** Recover the typed dependency graph — propositions, methods, evidence, assumptions, boundary conditions and their edges — from a rendered artifact, using the drafting schema run in reverse. Reuse: the forward schema's node and edge types; retroactive extraction has already been executed on independently authored published papers. New: the blinding and agreement protocol that makes extraction *measurable* rather than merely performed.

**M2 — Ontology negotiation.** Classify every interaction between the extracted graph's terms and the reader's held terms into the six cross-owner compatibility classes, then read the unresolved classes as reader-facing lists: an import neither side owns is a **prerequisite**; a shared term key held with a different definition hash is a **confusion** [@zharnikov-2026-research-as-repository-git-native]. The existing machinery negotiates between two authors; here one side is the audience, which is a change of interpretation rather than of mechanism.

**M3 — Load analysis.** Rank the extracted graph's nodes by structural load using centrality over the dependency edges. The paper pre-commits to one centrality definition and reports sensitivity across at least one alternative; without that pre-commitment the ranking is unfalsifiable.

**M4 — Re-rendering.** Produce prose that preserves the extracted spine and addresses the reader's held ontology, defining only the terms the negotiation step returned as prerequisites or confusions. Licensed by rendering-equivalence under spine preservation.

**M5 — Acceptance scoring.** Administer the three-clause contract and score it: spine restatement against the extracted graph, load identification against the M3 ranking with a stated counterfactual, and execution of one node the spine marks open.

### *The declared reader models.*

C2 requires a reader model to be fixed before any measurement, and the count has no referent without one. Three are declared, one per specimen chain, each stated as a module of held terms, held results, and an explicit **not-held** list — the form C4 requires, and the only form against which a per-node explanatory status is decidable. For the mathematical exposition the model is the reader its author says he wrote for: one who holds polynomial algebra over the complex numbers, Jacobian determinants and elementary complex analysis, and who does not hold the machinery of algebraic geometry. For the ladder a single model is used at all three rungs — holding number fields, ramification and the unit-distance problem as a statement, and not holding pro-$p$ groups, the Golod–Shafarevich inequality or the tower construction the result rests on, so that the held/not-held boundary falls exactly where the construction lives. For the philosophical argument the reader holds ordinary educated vocabulary and no computability theory.

Two conventions travel with the models. A term is held at the granularity of a named definition or theorem, and partial familiarity counts as **not** held — a convention that can only raise a miracle count, never lower it, and therefore cannot flatter a result. And no quantity is compared across models, which is C2 and L2 restated at the point of use. The models are not claims about any real reader; they fix a referent, in the sense in which an item-difficulty statistic is reported with the population it was estimated on.

### *The cost gradient runs the other way.*

It is tempting to assume step 1 is the machine-cheap layer and step 4 the hard one. The evidence inverts that, from two directions. Human annotators agree poorly on argument *relations* — the edges, which is precisely what a dependency graph is — substantially worse than on the units those relations connect [@lauscher-2018-argument-annotated-corpus; @peldszus-2014-towards-segment-based]. And long-context retrieval degrades sharply on material buried mid-document [@liu-2024-lost-middle-language], which is where load-bearing lemmas and implicit assumptions live. Meanwhile re-rendering for an audience is the operation current systems perform cheaply and reliably.

**Extraction is the expensive, brittle, research-frontier step; re-rendering is the cheap one.** This relocates the contribution to where the difficulty actually is, and it makes the extraction-agreement measurement load-bearing rather than a formality.

### *The measurement stack, and one instrument this paper does not invent.*

Instruments for the acceptance test exist and are adopted rather than built. Clauses (a) and (b) use a two-tier diagnostic format — identify, then justify — whose distractors are supplied by step 2's confusion list [@treagust-1988-development-use-diagnostic], scored on established self-explanation rubrics [@mcnamara-2004-sert-self-explanation]. Clause (c) uses transfer-taxonomy classification of the chosen open fork, with its distance declared *before* administration [@barnett-ceci-2002-where-apply-learn]. The last is not optional: the skeptical baseline is that spontaneous far transfer is close to absent, so a fork chosen too near proves nothing and one chosen too far makes failure uninformative.

For extraction agreement over typed graphs the natural construction is not available. Graph edit distance is a real distance [@sanfeliu-fu-1983-distance-measure-between] and chance-corrected agreement coefficients admit user-supplied distance functions, but composing them requires an expected-disagreement term over the combinatorial space of random typed graphs, for which no published approximation exists to adopt. Using it would mean inventing and defending a new agreement instrument on the paper's most load-bearing robustness check. **The paper declines to do so** and reports agreement in the layered form.

**That unavailability is narrow, and two instruments the layered form gives up are named here rather than discovered by a reader.** For *unitization* — annotators freely placing units of arbitrary extent and category on a continuum — a chance-corrected treatment does exist, in the unitizing-reliability family [@krippendorff-2016-reliability-unitizing-continua] and in the unified coefficient that scores positional and categorical discrepancy together under a principled alignment [@mathet-2015-unified-holistic-gamma]. And for argument mining specifically, segmentation and structure agreement have been composed into a single score for a decade [@duthie-2016-cass-technique-evaluating], so the layered form is this paper's *choice* and not the field's only option. The choice is made for comparability — the layers are what the reference class publishes, and a single composite would hide which layer fired, which is the paper's stated reason for separating them. **The cost of that choice is real and is stated where it lands**: Layer 1 is computed over the nodes the two operators matched, so a boundary miss leaves the coefficient rather than counting against it, and the node-layer statistic is correspondingly more favourable than a joint unitizing coefficient would be. Boundary precision and recall are reported beside it for exactly that reason, and the Results section reads the two together rather than reading $\alpha$ alone.

### *The pre-declared decision rule.*

Fixed before any run and not revisable in light of a result. Reported in three layers, because the failure modes differ by layer and a single graph-level number hides which one fired.

**Table 1.** Pre-Declared Agreement Layers and Thresholds for Extraction (RC1).

| Layer | Unit | Statistic | Threshold |
|---|---|---|---|
| 1 | Typed spine node | Nominal chance-corrected agreement over node-type assignments on unitized spans, with node-boundary precision and recall | $\alpha \ge .65$ |
| 2 | Dependency edge, over nodes both operators recovered | Triple-overlap $F_1$ in the Smatch sense [@cai-knight-2013-smatch-evaluation-metric], against a random-graph null | $F_1 \ge .60$, null exceeded at the 99th percentile |
| 3 | Load ranking, over the agreed node set | Rank correlation under the pre-committed centrality definition | $\rho \ge .50$, reported and inspected rather than gated |

*Notes*: Layer 1's threshold sits deliberately below the flat-label conventions. Those conventions originate in categorical diagnostic agreement [@landis-1977-measurement-observer-agreement] and their transfer to structured annotation is specifically criticised [@artstein-poesio-2008-inter-coder-agreement]; scientific argument annotation is the right reference class and sits lower than essay-scoring work does [@lauscher-2018-argument-annotated-corpus; @stab-gurevych-2014-identifying-argumentative-discourse]. Layer 2's threshold sits below the expert ceiling reported for semantic-graph annotation [@banarescu-2013-abstract-meaning-representation] because that ceiling is for a fixed scheme and a trained pool on sentence-scale semantics, whereas this is document-scale dependency extraction with a schema not designed for it. That $F_1$ is not chance-corrected is conceded in advance, which is why the random-graph null is part of the rule rather than an appendix.

**Table 2.** Pre-Declared Threshold Sensitivity. How the conclusion changes if each threshold is raised. Stated before any run, so that the reported outcome cannot be read as the only outcome the rule would have permitted.

| Layer | Declared | +.05 | +.10 | What a reversal across this range would mean |
|---|---|---|---|---|
| 1 (node) | $\alpha \ge .65$ | .70 | .75 | At .70 the threshold matches the flat-label convention whose transfer to structured annotation is contested; a result passing at .65 but failing at .70 is reported as such, and the paper argues the reference class rather than the number. |
| 2 (edge) | $F_1 \ge .60$ | .65 | .70 | The gate. A result passing at .60 but failing at .65 does **not** license the downstream claims at the higher standard, and the abstract reports the level at which AA1 survives. At .70 the threshold approaches the expert ceiling for a fixed scheme on sentence-scale semantics, which this task is not. |
| 3 (rank) | $\rho \ge .50$ | .55 | .60 | Descriptive and un-gated at every level, so no conclusion turns on it. See the note below on why this layer is not gated. |

*Notes*: The table is published empty of data deliberately. Its purpose is to pre-empt the objection that thresholds were chosen to be passable, by fixing in advance what each alternative threshold would have implied. **Layer 3 is not gated, and the reason is arithmetic**: at the sample sizes realistic for span-level ranking within a single specimen, the critical value for a rank correlation at conventional significance sits at or above the declared $\rho$, so gating on it would either require a sample the design does not have or guarantee a null. Reporting it descriptively is the honest option; raising the threshold without raising the sample would not fix it.

**Why Layer 2 is gated when Layer 3 is not.** The arithmetic that un-gates Layer 3 does not transfer, and the asymmetry is deliberate. Layer 3 is a correlation whose critical value the design's sample cannot reach, so gating it would decide the question by sample size rather than by evidence. Layer 2 is not a test of that kind: it is the minimal condition under which any downstream quantity is *defined at all*. A miracle count, a preservation check and a load ranking are each computed over an extracted graph, so if the two operators do not recover the same graph there is no object for the downstream quantities to be about. Layer 2 is gated because it is a precondition, not because it is the most powerful statistic available — and a precondition that fails on a small sample has still failed.

A **pilot** runs first on material that is neither specimen. It may refine annotation guidelines, inform the number of documents in the main run, or cause the study to be abandoned before the main run. **It may not move a threshold.** Allowing a pilot to reset thresholds is how a pre-declaration is quietly converted into a post-hoc rationalisation.

**If Layer 2 fails**, AA1 is refuted at the declared level and the paper says so in the abstract. It does not proceed to report downstream miracle counts as though the input were sound. The honest paper in that world is a negative result about the extraction frontier.

### *Acceptance-test pass criteria.*

Clause (a) passes when the reader's unaided restatement recovers the graph's nodes and dependency edges at the same triple-overlap threshold two operators are held to; using a higher standard for readers than for operators would be arbitrary. Clause (b) passes when the reader names a node in the top decile of the load ranking **and** states a consequence of its removal that a blind rater judges correct — both conjuncts, because the clause tests whether the reader holds the dependency, not whether they can point at it. Clause (c) passes when the reader produces an output satisfying an acceptance condition written before administration and checkable without reference to the reader's reasoning.

**A comprehension claim requires all three clauses.** The contract is conjunctive by construction: clauses (a) and (b) are structure recovery and clause (c) is transfer, and the paper's own argument is that the third is what separates the contract from a satisfaction rating. Per-clause pass rates are reported regardless of the overall verdict, because passing (a) and (b) while failing (c) would be the most interesting available finding — it would say the pipeline delivers structure without delivering transfer.

## Validation Design

### *Two specimens, and why the second is not mathematical.*

**VC1** is a working mathematician's published digestion of a recently announced counterexample to a long-standing conjecture in polynomial algebra [@tao-2026-digestion-jacobian-counterexample], used as labeled ground truth. It states its own objective in the paper's own vocabulary — to write the explanation "in a manner that minimizes the amount of 'miracles' required", while noting that a few places of remarkable phenomena remain — rebases the statement to an equivalent form, generates the construction from one object, and explicitly marks residuals it cannot dissolve, including one the author says he has no completely satisfactory explanation for but can nonetheless verify.

**This is the specimen that makes the metric adopted rather than invented**, and it is the only one that does. The vocabulary is the author's, used unprompted, as the thing he was optimizing.

The pipeline is pointed at the **digestion**, not at the raw counterexample it expounds. The author states he sought to explain the construction "with relatively little use of algebraic geometry" — that is, he deliberately re-rendered the object in a different ontology. Asking a pipeline to reproduce that independently would be asking for mathematical *discovery*, which is a claim this paper neither makes nor could support.

**VC3 is the ladder.** Three renderings of one fixed result, at increasing degrees of internalization. **R0**, the verbatim raw output of an automated system, reproduced before any grading or rewriting, about 1,400 words. **R1**, the human-edited exposition of that same output, produced afterwards with reorganized proofs and added explanatory material, about 6,310 words — a factor of roughly 4.5, published in the same document, which states the provenance itself [@openai-2026-planar-point-sets]. **R2**, an independent expert digestion of the same result, authored outside the producing organization, about 5,136 words [@tao-2026-digestion-unit-distance].

**VC3 and VC1 are separate chains on different results, not one chain.** R2 and VC1 are digestion posts by the same mathematician published weeks apart, but they expound different theorems. VC1 supplies the labeled-ground-truth case, with an author-stated objective and marked residuals; VC3 supplies the fixed-result ladder, on which no author-marked residuals exist below R2.

Because all three expound the identical construction, **the result is held fixed structurally rather than by assumption**, and C3 is satisfied by the artifacts themselves rather than by the design. No other specimen in this paper achieves that.

*The pipeline is never asked to reproduce one rendering from another.* Each rung is extracted on its own, and the resulting spines are then compared. This distinction carries weight, because a superficially similar design would not be defensible: asking whether the pipeline, run on the raw result, *independently surfaces* the expert's decomposition would be asking it to reproduce an insight — mathematical discovery, a claim this paper neither makes nor could support. The ladder asks nothing of the kind. It is a measurement over three artifacts, not a reconstruction of anyone's reasoning.

Three quantities are pre-declared. **Pairwise spine preservation** across R0–R1, R1–R2 and R0–R2, each at the Layer-2 threshold of Table 1 — which turns the fidelity precondition AA4 from an assumption into a *measurement*, at every rung. **A monotonic miracle ordering** under a single declared reader model: $\mathrm{MC}(R_0) > \mathrm{MC}(R_1) > \mathrm{MC}(R_2)$. And **the prose-mass divergence**: prose mass across the rungs against structural load across the rungs, which is P2 measured on a real artifact rather than argued analytically.

The ordering is the reason for using all three rungs rather than the pair alone. A strict ordering over three points is far harder to obtain by chance than a single directional difference, and **any inversion disconfirms it**. Each pairwise preservation check gates only the comparison it spans: if R0–R1 preserves and R1–R2 does not, the first differential is reported and the second is not. A count that falls over an unpreserved spine is never reported as a lowered count — that is the gaming path the precondition forbids.

**One outcome is worth declaring in advance because it would be a finding rather than a null.** If the expert rendering does not preserve the structure of what it digests, then expert internalization sometimes *replaces* structure rather than preserving it. That would bound P5 and the inherited rendering-equivalence result — both hold only under spine preservation, and would simply not apply to that rung — and it would say the operation specified here is narrower than what a human expert actually does. Declaring it now is what prevents it from being narrated as a success afterwards.

Three qualifications. Provenance is a **stated claim, not a verified fact**: that R0 is verbatim pre-grading output is asserted by the publishing organization and cannot be independently checked, which places it in the same class as the ground-truth assumption AA3, and the same exposure applies to the rung *order*, which is taken from documented provenance rather than measured. The rungs were produced by different agents with different purposes, so the ordering **confounds internalization with authorship, and the confound grows at R2**, which is independently authored — the claim licensed is that the ladder *exhibits* the predicted ordering, not that internalization *caused* it. And R0 and R1 mark no residuals of their own, so the T3 criterion below is vacuous for them and applies at R2 alone.

**VC2** is a canonical philosophical argument [@turing-1950-computing-machinery-intelligence] whose author states his decomposition in running prose, declares his objective for the explanation, and concedes one residual he cannot resolve rather than dismissing it. Its purpose is to separate *method failure* from *domain hostility*: informal mathematical prose omits dependencies by convention, so a failure on VC1 alone would be uninterpretable. With two specimens the outcomes separate — both pass; mathematics fails and the second passes (domain hostility); both fail (the method does not recover author-stated structure); or mathematics passes and the second fails.

An engineering design-rationale document was considered and rejected as the primary second specimen. Where the genre mandates a template enumerating alternatives and unresolved questions in its section headings, a successful extraction may have recovered the *template* rather than the argument — a soft test dressed as a hard one, and the mirror image of VC1's weakness. It is retained as a floor test and contamination control.

### *What counts as recovery.*

Three targets per specimen, scored separately so a partial recovery implicates a specific step, by two raters blind to the pipeline's provenance, against the text's own statements.

**Table 3.** Pre-Declared Recovery Targets and Criteria.

| Target | Recovered when |
|---|---|
| T1 — the generative object | The extracted graph contains a single node from which the derivation edges to the separable goals originate, corresponding to the object the text presents as generative. No partial credit. |
| T2 — the stated decomposition | The author's separable goals appear as distinct nodes, with the decomposition represented as edges from the rebased statement, and no goal merged with or split from the author's own division. |
| T3 — the marked residuals | Every step the author explicitly marks as unexplained is classified `miracle`, and no step the author derives is so classified. Two error counts, both required to be zero. |

*Notes*: **The success rule is T2 and T3 both recovered. T1 is reported and is not part of the rule.** T2 is the structural claim — failure to recover a decomposition the author states in the text means step 1 has failed the easiest available case. T3 is the measurement contribution. T1 is excluded deliberately: it is the target most exposed to the discovery-versus-extraction confusion, and a rule depending on it would be a rule about mathematical insight rather than about extraction. T3 is the strictest criterion here and is meant to be; a looser rule would be unfalsifiable at $N = 1$ per specimen. **These targets are scored only on renderings whose authors state a decomposition and mark residuals** — the expert rung and VC2. They are not scored on R0 or R1, where scoring a self-unlabeled rendering against T1–T3 would measure the analyst's reconstruction rather than the author's declaration; those rungs carry the ladder's own criteria instead.

### *Threats this design carries.*

**Operator contamination.** Both specimens have been read by the operator, so the extraction arm must be blinded or independently operated. In the run reported here it was independently operated: each extraction is a single call carrying the schema, the reader model and the document, with no conversational context and no knowledge of the study, its hypotheses, or which rung of a comparison the document occupies. The raters who scored the recovery targets never learn which operator produced the graph in front of them, and are drawn from model families that produced neither.

**Training-data contamination on VC2, and it is the serious one.** The specimen is among the most reproduced texts in its field, so an extraction arm has seen both it and decades of commentary *about* its structure, and may reproduce the consensus reading rather than perform an extraction. The concern is not hypothetical: how deeply these models have absorbed the scientific literature and its citation practices, as against reconstructing them on demand, is itself under measurement [@algaba-2026-internalize-scientific-literature]. This inflates a **positive** result specifically, and cannot be removed by blinding, because the contamination sits in the extractor rather than in the operator's memory. Three mitigations are declared: score only against the text's own statements, never the secondary literature; report the threat as a bound on the claim rather than a footnote, since a success establishes that the pipeline *can* recover author-stated structure from non-mathematical prose but not that it would do so on unseen prose; and hold the design-rationale document in reserve as the contamination control.

**The operators are machines, and P1's falsifier says "two competent operators."** Whether two hosted models instantiate that clause is the hinge the whole result turns on, so the design states its position rather than leaving it implied. Two arms from different model families are treated as two operators, and two arms of one family as one operator run twice — the disagreement of interest is between extractors that do not share a training lineage, not between samples from one distribution. The claim being made is correspondingly narrow: these operators are *an* instantiation of the procedure, not the privileged one, and a failure by them bounds what may be assumed rather than what is achievable. The literature the design leans on for its expectations is about *human* annotators disagreeing on argument relations, which makes the machine result a transfer rather than a confirmation, and the paper reports it as one. What the run cannot do is separate three candidate sources of disagreement — the schema, the prompt version, and the operators — because it varies only the last.

**$N$ remains small.** Two specimens answer the domain confound. They do not answer generalizability, and this release claims an existence proof rather than a general result.

## Results

**The pre-registered validation was run, and its gate failed. AA1 is refuted at the declared level: two independent machine operators do not recover the dependency structure of these artifacts at the agreement the design requires.** Layer 2 — edge recovery over the nodes both operators found, the layer on which every downstream quantity depends — fell below the declared threshold on all five documents. What follows reports that, and then reports the downstream stages as the decision rule requires: as *not evaluable*, rather than as unevaluated.

### *How the run was conducted.*

The operators are hosted models, not people, and the result is a result about them. **Arm A is `claude-opus-5`; arm B is `gemini-3.1-pro-preview`** — different families, per the rule that two arms of one family are one operator run twice. The two blind target raters are `gpt-5.5` and `grok-4.3`, with `deepseek-v4-pro` resolving their disagreements, and the ladder's node aligner is `grok-4.3`. No arm scores its own extraction, and no rater belongs to either operator's family. Extraction guidelines are frozen at prompt version `internalization/1.2.0`; every reported statistic is conditional on that version, and on the epoch at which those hosted models were called.

**The pilot ran, and it did what the declaration permits and nothing more.** Three rounds on three non-specimen argumentative documents under a pilot-only reader model, two of them discarded and all three reported. Round 1 exposed a corrupted input on one document and a grain gap of a factor of six between the arms; the guidelines gained an explicit unit rule, and the alternative fix — tying node count to document length — was rejected because forcing node count to scale with words prejudges the very divergence the ladder exists to measure. Round 2 closed the grain gap and showed roughly half the edge disagreement to be about what to call an edge rather than whether it is there; the guidelines gained an edge-completeness step and an ordered type rule. Round 3 froze them. **No threshold was moved at any round**, and no pilot quantity is compared with any specimen quantity.

**Three harness defects surfaced during the run and are disclosed rather than tidied away**, because a run reported only in its final configuration is indistinguishable from one tuned until it worked. First, one provider counts reasoning against the output cap; a call spent its entire budget reasoning and returned nothing, so the cap was raised and reasoning depth bounded. Second, verbatim spans quoting mathematics are not valid JSON as emitted, and the failure is worse than a broken parse: sequences such as `\binom` and `\frac` are *valid* JSON escapes that silently consume the macro's first letter, so a parse can succeed while corrupting the quotation. The parser now prefers the literal reading, and every saved graph was checked for control-character corruption; none was found. Third, and the only one that touches a reported quantity: bounding arm B's reasoning changed that arm's node counts, and two ladder rungs had already been extracted unbounded. **All three rungs were therefore re-extracted on that arm** under the bounded configuration, so the ladder's ordering claim is not confounded with a configuration change, and the superseded extractions are retained rather than deleted. None of the three moved a threshold, a guideline, or a scoring rule.

### *Extraction agreement.*

Two operators from different model families extracted each document independently under the declared reader models. Table 4 reports the three layers.

**Table 4.** Extraction Agreement by Layer, per Specimen Document.

| Document | Nodes A / B | Matched | Layer 1 $\alpha$ | Layer 2 $F_1$ | Untyped $F_1$ | Null 99th | Edge retention A / B | Layer 3 $\rho$ |
|---|---|---|---|---|---|---|---|---|
| VC1 | 53 / 25 | 9 | .663 | .000 | .000 | .500 | .044 / .033 | .957 |
| VC2 | 119 / 39 | 20 | .637 | .400 | .400 | .000 | .016 / .081 | .627 |
| VC3 R0 | 47 / 19 | 11 | 1.000 | .500 | .750 | .250 | .072 / .231 | −.116 |
| VC3 R1 | 85 / 14 | 3 | — | .000 | .000 | .000 | .000 / .077 | 1.000 |
| VC3 R2 | 57 / 21 | 8 | .769 | .000 | .800 | .400 | .029 / .158 | .096 |

*Notes*: Thresholds from Table 1 — $\alpha \ge .65$, $F_1 \ge .60$ and above the null's 99th percentile, $\rho \ge .50$ reported not gated. Edge retention is the share of each operator's edges whose **both** endpoints survive the restriction to the agreed node set. VC3 R1's $\alpha$ is undefined: three matched nodes, all of one type. Layer 3 on VC3 R1 is computed over those three nodes and is reported for completeness rather than read.

**The node layer is closer to workable than the edge layer, and the comparison is not a clean one.** Layer 1 clears its threshold on three of five documents, misses it by .013 on VC2, and is undefined on the fourth. Layer 2 clears its threshold on none. The asymmetry is real but it is flattered by the design: Layer 1 scores the nodes the operators matched, so the boundary misses that dominate this run — precision .035 to .234 — sit outside the coefficient instead of inside it, where a joint unitizing measure would put them [@krippendorff-2016-reliability-unitizing-continua; @mathet-2015-unified-holistic-gamma]. Read with its boundary statistics rather than alone, the node layer is not a layer that nearly worked; it is the same failure one step earlier, and the edge layer inherits it. The best edge agreement observed anywhere is $F_1 = .500$, on the shortest document, against a declared gate of .60; on two documents the operators share no edge at all. **Table 2's sensitivity analysis is not needed to interpret this**: the result is not near the line, so no alternative threshold in the declared range changes the verdict.

**The failure is not mainly about naming the edges.** Erasing the edge type — the diagnostic that separates disagreement about *whether* an edge exists from disagreement about *what to call it* — leaves three of five documents unchanged and lifts the other two to .750 and .800 — the only two edge-agreement figures anywhere in the run that reach .60. The gate is declared on the typed statistic and is unmoved by this: the diagnostic carries no threshold of its own and cannot rescue a layer that failed. What it says is narrower and worth having. Where the operators drew the same edge they usually typed it the same way. Mostly they did not draw the same edge.

**A large part of the reason is upstream of the edges.** Between .0% and 23.1% of each operator's edges have both endpoints in the agreed node set, so the Layer-2 statistic is computed on between zero and five triples per document. The operators disagree about *which nodes exist* before they can disagree about how those nodes connect: node-boundary precision runs from .035 to .234, meaning the more prolific operator's nodes are largely unmatched. This is the design's own restriction working as declared — Layer 2 is defined over nodes both operators recovered — but it means the edge layer failed for want of a shared node set as much as for want of shared edges.

**A statistic computed on at most five triples is a coarse instrument, and that cuts both ways.** At those sample sizes the random-graph null is correspondingly coarse — its 99th percentile takes the values .000, .250, .400 and .500 across the five documents, which are the granularities a handful of triples can produce and not fine thresholds. The consequence has to be stated plainly: this design could not have distinguished moderate agreement from none on these documents, so *failed the gate* and *could not have passed the gate* are not fully separable here. That does not soften the verdict, because the gate is a precondition and a precondition unmet is unmet however coarsely it was measured. It does bound the inference in one direction — the run licenses "agreement at the declared level cannot be assumed", not "agreement at the declared level is absent".

**RC2, the centrality sensitivity, is the one robustness check that came back clean.** Rank correlation between the pre-committed support-mass definition and the alternative reverse-PageRank ranking runs .584 to .978 across nine of the ten extractions, with a single outlier (.143, on the 14-node graph). Whatever the operators disagree about, they do not disagree because the load ranking is an artifact of the centrality definition.

### *What this run does not license.*

The decision rule fixed in advance what a Layer-2 failure means, and it means this: no downstream quantity computed here is licensed. The miracle counts, the preservation results and the recovery-target verdicts were nevertheless computed, and they are reported — collected in Appendix A rather than interleaved with the result — because the study undertook to report whatever came out, and because a reader checking the pre-registration is entitled to see the numbers the declared procedure produced. They are **not** offered as measurements of explanatory quality, of internalization, or of the pipeline's fidelity. A count computed over a graph two competent operators do not agree on measures the operator as much as the artifact.

Three findings survive the gate failure, because none of them is a downstream measurement of the pipeline, and each is stated here rather than in the appendix.

**The pre-declared monotonic miracle ordering is disconfirmed.** The rule required the ordering to hold on both arms; it holds on one arm and inverts on the other (Appendix A, Table A1). That is a statement about whether the pre-registration was honoured — reporting the arm that ran the right way is exactly the selection the pre-declaration exists to prevent — and not a measurement of the pipeline.

**The two blind target raters disagreed with each other on 8 of 18 target judgments, a recourse rate of .444.** That is a result about the *scoring instrument* rather than about the pipeline, and it is the reason the verdicts in Appendix A are reported without a claim attached: an instrument on which two blind raters split almost half the time is not one that can settle a criterion as strict as T3, which requires two error counts to be exactly zero. Whether the disagreement reflects genuine ambiguity in the criteria or noise in the raters is not separable here, and the design did not anticipate needing to separate them.

**The specimens keep the roles the design gave them.** The stopping rule reserved demotion for the case where the recovery targets fail on the mathematical specimen and pass on the non-mathematical one. They failed on both (Appendix A, Table A2), in a run whose extraction step had already failed its gate, so the rule's antecedent is not satisfied and no demotion follows.

Nor is the acceptance test of M5 reported: it requires readers, none were recruited, and no clause of it was administered. P4 remains stated and untested.

## Discussion

### *Rival explanations, and what would rule each out.*

**A1 — capability, not input.** Machine explanations may miss because models are not yet good enough, so better models close the gap without structural intervention. Discriminating evidence is a capability-controlled comparison: the same renderer given prose alone versus prose plus the extracted graph. If the graph condition wins at fixed capability, A1 is rejected. Existing work showing that extracted argument structure adds predictive power over strong surface baselines is suggestive but not decisive, because it measures a different outcome [@nguyen-litman-2018-argument-mining-improving; @wachsmuth-2016-using-argument-mining]. **Open.**

**A2 — prior-knowledge activation.** The benefit may be entirely that of activating prior knowledge, long established in the learning sciences, with the structural apparatus adding nothing. Discriminating evidence is a comparison against a strong prior-knowledge-activation baseline built without the computed difference. If the computed difference does not beat it, the contribution reduces to a re-labelling. **Open.**

**A3 — attention, not legibility.** As output scales the binding constraint may be finite attention and prestige signalling rather than structural illegibility. The bibliometric evidence supports the attention account and is not in conflict with the narrower claim: for a reader who has already decided to engage, structural illegibility remains a distinct constraint. A3 bounds the motivating claim rather than defeating it. **Partially ruled out.**

**A4 — understanding is not graph-shaped.** The strongest objection, and it comes from inside mathematics rather than from a hostile outsider: assimilation rests irreducibly on intuition, examples, spatial translation and tacit knowledge, and formal derivation is what one produces *after* understanding rather than the vehicle of it [@thurston-1994-proof-progress-mathematics]. If that is right, the pipeline automates the wrong cognitive operation, in the domain chosen for validation. The paper does not need to defeat A4, because its claim is that the graph is the *input a renderer needs and currently lacks*, not that the graph is the understanding. Discriminating evidence for the narrow claim already exists in expert reading behaviour [@inglis-alcock-2012-expert-novice-approaches]. **The risk is drift**: a single sentence claiming the graph *is* the understanding concedes the objection, and every draft pass must be checked against it. **Open.**

**A5 — explanatory power is objective.** Addressed above as a scope distinction rather than a rival thesis. **Scoped out.**

### *What this release does not establish.*

The run establishes one thing and refuses several others. **What it establishes is negative and specific**: on five argumentative artifacts, two competent operators from different model families did not agree on the dependency structure at the level this design declared in advance. That is a result about the state of the extraction frontier under five conditions, all of them named: this schema, this frozen prompt version, these two operators, these five documents, and the epoch at which those hosted models were called. It is not a result about whether the artifacts have a dependency structure, and it is not evidence that they do not.

**What it does not establish**: that the miracle count orders explanations as experts would; that the acceptance contract discriminates; that internalization lowers the count. Each remains a pre-registered question whose test is gated behind an extraction step that did not pass. It does not establish that understanding is a dependency graph, and does not claim it. And it does not establish that extraction at this agreement level is unreachable — a different schema, a trained annotator pool, a shared unitization imposed before extraction rather than negotiated after it, or human operators rather than machine ones might all clear the bar. What it does establish is that **none of that can be assumed**, which is what the paper's own starting position quietly did.

**The most useful thing the run produced is a located failure.** The operators diverge on which nodes exist before they diverge on how nodes connect: node-boundary precision runs from .035 to .234 while type agreement on the nodes they do share reaches .663 to 1.000 on three of five documents. Unitization, not relation labelling, is where the next attempt should be spent — and unlike the closure this paper specifies, that is a target with an established task definition, a published benchmark and a known cross-domain failure mode already attached to it [@ajjour-2017-unit-segmentation-argumentative]. A next attempt would impose a shared unitization before extraction rather than negotiating one after it, and would score it with a coefficient that charges for boundary disagreement rather than conditioning it away.

## Limitations

**L0 — extraction, not rendering, is the weak link. This is now measured rather than anticipated.** The literature predicted it: human annotators agree substantially worse on argument relations than on the units those relations connect. The run reproduces the pattern with machine operators and a document-scale schema, and the mitigation held — agreement was reported as the headline number, and no downstream claim is made at an agreement level not demonstrated. The limitation has become the finding.

**L1 — mathematical faithfulness is untested, and the run does not settle it.** L1's mitigation was that if agreement is poor on the mathematical specimen alone, that specimen is demoted to illustration and the non-mathematical one carries the validation. The mitigation does not fire, because agreement did not clear the gate on either. Domain hostility cannot be separated from method failure by a design in which the method failed everywhere: the non-mathematical specimen produced the second-best edge agreement observed (.400) and the second-best node-boundary recall (.513), both behind a mathematical document, which is suggestive of nothing at all. **This is a hard limit on what the run generalizes to, not an open question the same design could still settle.** Separating the two would take a specimen set on which the method clears its gate somewhere, and this one does not; the confound VC2 was added to resolve is therefore untouched, and no reading of these five documents can address it.

**L2 — the miracle count is reader-relative by construction**, so it measures an explanation-reader pair rather than an explanation, and cross-reader comparison is not licensed. Mitigation: report every count with its reader model, the discipline under which an item-difficulty statistic is reported with its population.

**L3 — the acceptance contract is administered per reader**, which bounds the generality of any single result and makes the third clause expensive to score at scale. The declared mitigation — report cost per administration alongside the result — was never exercised, because the contract was never administered: no reader was recruited and P4 remains stated and untested. No scalability is claimed here that has not been demonstrated, which at present is none.

**L4 — there is no within-operator baseline, and without one the between-arm disagreement is not cleanly attributable.** Each document was extracted once per arm. Machine judges are unreliable against *themselves* across repeated runs [@haldar-2025-rating-roulette-selfinconsistency], so a critic may read the disagreement reported here as run-to-run variance rather than as a difference between operators, and this design cannot separate the two. The pilot rounds bear on it only indirectly, having varied the guidelines rather than repeated a call. A test-retest arm — same operator, same prompt, same document, repeated — is the cheapest correction available and is not in this run. **It belongs to a new pre-registration rather than to this one**: adding it now, after the result, would be a protocol change made in light of an outcome.

**L5 — treating two model families as two independent operators is an operational separation, not a statistical one**, and the direction of the error is worth stating because it runs in the paper's favour. Nothing guarantees that extractors from different families make *uncorrelated* mistakes; where they share training material or inductive bias, their errors are positively correlated, and positively correlated errors make agreement **easier** to obtain, not harder. An agreement pass under this design would therefore have been weaker evidence than it appeared. A failure is the conservative outcome, and it is the one observed.

## Data and Code Availability

### *Companion computation scripts.*

Every number reported above is computed by scripts published with this record, from inputs a reader
can reconstruct. `prepare_specimens.py` fetches each specimen from its public source and verifies it
against a recorded digest; `extract_spines.py` runs the two operator arms; `score_agreement.py`,
`score_ladder.py` and `score_targets.py` compute the layered agreement statistics, the ladder
quantities and the recovery targets; `emit_results_summary.py` renders them into the table the
Results section is written from, so a reported value and a computed value cannot drift apart. The
measurement primitives live in `metrics_lib.py` and are checked against hand-worked cases in
`code/tests/` before any specimen is scored.

One command reproduces the analysis:

```
./reproduce.sh
```

This requires no API keys and no network access. It recomputes every reported statistic from the
committed extractions under the fixed seed 20260809, including the random-graph null. Re-running the
collection itself (`./reproduce.sh --collect`) requires provider credentials and yields a **new
epoch rather than a replication**: the operators are hosted models whose behaviour is pinned to a
point in time. That is why the extracted graphs, not the models, are the dataset of record.

### *What is published, and what is not.*

Published with the record: the pre-declared protocol, decision rule and reader models; the
extraction harness and every scoring script; the extracted graphs for all five documents and both
arms, including the discarded pilot rounds; the blind alignments and the per-rater target
judgments; and a JSONL log of every model call carrying its prompts, prompt hash, parameters,
response and token usage. The code and the machine-readable bundle are in the paper's public
repository at
[github.com/spectralbranding/meaningfulness-papers](https://github.com/spectralbranding/meaningfulness-papers/tree/main/internalization);
the protocol layers, the records and the complete call logs are archived together as a Hugging Face
dataset (DOI [10.57967/hf/9898](https://doi.org/10.57967/hf/9898)).

Not redistributed: the specimen texts themselves, which are third-party works. The three specimens
are publicly available — the matched pair, R0 and R1, in a single document from its producing
organization [@openai-2026-planar-point-sets], the independent expert digestions on the author's
weblog [@tao-2026-digestion-unit-distance; @tao-2026-digestion-jacobian-counterexample], and the
philosophical argument in the journal record [@turing-1950-computing-machinery-intelligence] — and
the fetch script reconstructs the exact inputs and verifies them against their digests. No specimen
is proprietary and none was obtained under restriction.

Version of record and all subsequent versions: concept DOI
[10.5281/zenodo.21828980](https://doi.org/10.5281/zenodo.21828980), which resolves to the most
recent version and is the identifier to cite unless a specific version is intended. This record is
version v1.0.0, whose version DOI is
[10.5281/zenodo.21828981](https://doi.org/10.5281/zenodo.21828981).

## Acknowledgments

The author thanks the practitioners whose independent statement of the same bottleneck — that results now arrive faster than they can be turned into something a human can hold, teach, and build on — motivated this work.

AI assistants (Claude Opus 5, Gemini 3.1 Pro, GPT-5.5, Grok 4.3, DeepSeek V4 Pro) were used for initial literature search, for software development — authoring the experiment harness and the analysis and scoring scripts — and for orchestrating and running the reported experiments through those scripts, as well as for editorial refinement; all theoretical claims, propositions, and interpretations are the author's sole responsibility.

The models named above also appear in this study as its *instruments*: two of them are the independent extraction operators whose agreement the run measures, two more score the recovery targets blind to which operator produced the graph they score, and a fifth resolves rater disagreement. The separation is deliberate and is part of the design rather than an artifact of tooling — no arm grades its own extraction, and the arms are drawn from different model families so that two runs of one model cannot be mistaken for two operators.

## References

::: {#refs}
:::

## Appendix A: Quantities Computed but Not Licensed by the Decision Rule

The quantities collected here were produced by the declared procedure and are reported because the pre-registration undertook to report whatever came out. Under the decision rule stated in the Method section none of them is licensed: each is downstream of an extraction step that failed its Layer-2 gate on every document. They are a record of what the procedure produced, not measurements of explanatory quality, of internalization, or of the pipeline's fidelity. The three findings that survive the gate failure are not here; they are stated in Results, because none of them is a downstream measurement of the pipeline.

### *The ladder.*

**Table A1.** VC3 Ladder: Prose Mass, Structural Load, and Miracle Count by Rung and Arm.

| Arm | Rung | Prose mass | Nodes | Edges | Mean support mass | Miracle count |
|---|---|---|---|---|---|---|
| A | R0 raw output | 1,386 | 47 | 69 | 17.13 | 8 |
| A | R1 human exposition | 7,012 | 85 | 128 | 13.53 | 0 |
| A | R2 expert digestion | 3,335 | 57 | 70 | 8.74 | 7 |
| B | R0 raw output | 1,386 | 19 | 13 | 1.16 | 7 |
| B | R1 human exposition | 7,012 | 14 | 13 | 1.79 | 5 |
| B | R2 expert digestion | 3,335 | 21 | 19 | 2.52 | 2 |

*Notes*: **The miracle counts in this table are computed but not licensed** — Layer 2 failed, so they are reported as the pre-registration requires and are not offered as measurements of anything. Prose mass counts each inline mathematical expression as one token. Both arms extracted all three rungs under the same declared reader model and, within each arm, the same configuration.

**The monotonic ordering is disconfirmed under the pre-declared rule**, which required it to hold on both arms. It holds on arm B — 7 > 5 > 2, a strict decrease across all three rungs — and fails on arm A, which assigned the human exposition a miracle count of zero and so inverted at the second step. Reporting the arm that ran the right way is exactly the selection the pre-declaration exists to prevent, so the ordering is recorded as disconfirmed.

**Pairwise spine preservation fails at five of six checks.** The single pass is R0 → R1 on arm B ($F_1 = .727$ against a null of .364, and .750 under the deterministic lexical alignment, which agrees). Every check spanning the expert digestion fails on both arms and under both alignment methods. The pre-declared branch for that outcome — that expert internalization sometimes *replaces* structure rather than preserving it — is the reading the data admits, but it cannot be asserted here: with extraction agreement below the Layer-2 gate, a failure to detect preservation is not distinguishable from a failure to extract. **The count differentials that would rest on those checks are therefore not reported**, which is what the fidelity precondition requires.

**One pre-declared quantity did behave as P2 predicts, and it is the one that does not depend on cross-operator agreement.** Arm B's structural load stays nearly flat across the ladder — 19, 14 and 21 nodes — while prose mass moves from 1,386 to 7,012 to 3,335 words, a swing of a factor of five. The human exposition is five times the length of the raw output and carries, by that arm's reading, slightly *fewer* structural nodes. Arm A does not reproduce the pattern: its node counts track length (47, 85, 57). One arm of one ladder is an observation, not evidence, and it is recorded as such.

### *Recovery targets.*

Each extracted graph was scored against the text it came from by two raters drawn from model families that produced neither graph, blind to which operator produced it, with a third rater resolving disagreement. Table A2 reports the final verdicts.

**Table A2.** Recovery Targets by Specimen and Operator Arm.

| Document | Arm | T1 generative object | T2 stated decomposition | T3 marked residuals | T2 and T3 both |
|---|---|---|---|---|---|
| VC1 | A | not recovered | not recovered | not recovered | no |
| VC1 | B | not recovered | not recovered | recovered | no |
| VC2 | A | not recovered | not recovered | not recovered | no |
| VC2 | B | not recovered | not recovered | not recovered | no |
| VC3 R2 | A | not recovered | not recovered | recovered | no |
| VC3 R2 | B | not recovered | not recovered | not recovered | no |

*Notes*: **These verdicts are computed but not licensed**, for the same reason as Table A1: they are scored on graphs whose extraction failed the Layer-2 gate. The pre-declared success rule is T2 **and** T3 both recovered; T1 is reported and is not part of the rule. Verdicts are the majority of three raters where the first two disagreed.

**The success rule is not met on any specimen, on either arm.** T2 — recovering a decomposition the author states in the text, which the design called the easiest available case — was not recovered anywhere. T3 was recovered on two of six graphs. T1 was recovered on none.
