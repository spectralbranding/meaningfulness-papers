# Invention as a Structural Operation: Why the Abductive Jump Is a Re-Coordinatization of the Space of Description, Not a Sensory Leap

Dmitry Zharnikov

ORCID: 0009-0000-6893-9231

DOI: [10.5281/zenodo.21653102](https://doi.org/10.5281/zenodo.21653102)

Working Paper v1.0.0 – July 2026

## Abstract

A prevailing position holds that generative models have mastered induction and are conquering deduction but are structurally incapable of the abductive "jump" from sensory experience to new axioms, which is said to require embodied simulation and physically grounded world models. This paper argues that the jump is misdescribed. Invention is a typed structural operation on a representation — a change of the description itself — realized by four atomic moves: adjoining a dimension, rescaling or requantizing, re-topologizing, and gluing across domains. These moves are selected by a functional combining intrinsic structural signals (description length of the axioms, symmetry, and closure) with an often-weak empirical term that can act during generation rather than only downstream. Within representational systems whose compatibility predicate is decidable, the operator set is enumerable and the selection is computable, so the generative act is mechanizable, as a running artifact that performs and classifies cross-domain structural recombination demonstrates. The account is bounded: outside decidable domains the operator types describe the moves without an enumerability or completeness claim. Evolution — invention without a mind — runs on the same four moves, showing structural invention to be substrate- and cognition-independent.

**Keywords**: scientific invention, abduction, representation change, symbol grounding, world models, evolvability, philosophy of AI

---

A well-known position argues that a modern language model, however large, cannot invent. Give it
every paper, dataset, and equation available by 1905 and it will not produce general relativity,
because invention requires an abductive "jump" — abduction in the classical triad
[@peirce-1931-1958-collected-papers] — from sensory experience to new axioms, a jump that induction
(statistical pattern-fit) and deduction (proof from premises) cannot reach, and that is said to
demand embodied simulation and physically grounded world models to supply the missing sensory
content [@zahavy-2026-llms-cant-jump]. The argument is careful, and its diagnosis of what
induction and deduction *cannot* do is correct. Its localization of what invention *is*, however, is
mistaken. The same position concedes, in its own closing, that in mathematics and computer science
the substrate of study is the abstract landscape of formal systems, requiring no external world. That concession is the whole argument. If invention in formal domains needs no body,
and if — as this paper argues — invention is *fundamentally* a formal-structural act, then
embodiment is a feature of one inventor's cognition, not of invention itself.

This paper defends a structural account. Invention is not a datum obtained within a fixed
description; it is a change of the description. Its atomic moves form a small set, each selected by
signals that are largely internal to the representation and, in formalized domains, computable. The
"jump" is a re-coordinatization under joint constraints — substrate-independent in its content,
though frequently embodied in its human rendering. The account is deliberately bounded, and its
strongest evidence is that the same four moves organize invention in a domain with no mind at all.

## A structural account of invention

A representation is a typed structure over which a domain's regularities are stated. An invention is
a morphism that changes that structure — a map from one representation to another — rather than an
observation collected inside a fixed one. The unit of analysis is the representation-changing
operation. This framing is not new, and the paper claims no priority for it: scientific
change has long been read as a restructuring of the framework of description rather than an
accumulation within it [@kuhn-1962-structure-scientific-revolutions]; theories have been treated as
categorical objects whose integration proceeds by functors and pullbacks [@spivak-kent-2012-ologs];
and constitutive frameworks have been shown to undergo structural shifts that are logically
constrained rather than merely inductive [@friedman-2001-dynamics-of-reason]. What the account adds
is a proposed closed operator set, an explicit selection criterion, and — below — a running
adjudicator. A note on the unit of analysis: a *specification* (the artifact of the existence proof
below) is the decidable-compatibility instance of a *representation*, which is precisely why the
mechanized claim can be made there and not everywhere.

Let $R$ denote a representation and $\mathcal{M}$ the set of moves that transform it. The paper
conjectures — and makes falsifiable below — that $\mathcal{M}$ has four types:

1. **Adjoin a dimension** ($\alpha$): make a latent degree of freedom explicit, adding an
   independent axis to $R$. Observer-indexed time in special relativity, or the metric treated as a
   dynamical field rather than a fixed backdrop, are adjunctions.
2. **Rescale or requantize** ($\rho$): change the unit or granularity of a measurement, including
   quantizing a quantity previously treated as continuous, or moving to a logarithmic or
   renormalized scale.
3. **Re-topologize or re-specify** ($\tau$): change the connectivity of $R$ or the class of
   admissible morphisms over it — replacing a flat description with a curved one, or promoting a
   measured equality to a structural identity by a quotient.
4. **Glue, or pull back, across domains** ($\gamma$): identify a shared substructure of two
   representations $R_1, R_2$ and form their fibered combination $R_1 \times_S R_2$, yielding a
   description that spans what neither domain saw alone.

The fourth move is the formal content of the folk notion that invention "combines approaches from
different domains": it is not a mixture but a pullback over a shared substructure $S$, a change of
basis under which the merged basis is seen to span something new. Moves (1) and (3) were already
formalized as the drop-or-adjoin of a dimension in a conceptual space and the alteration of its
structure [@boden-1990-creative-mind; @gardenfors-2000-conceptual-spaces]; move (4) was formalized
as conceptual blending, in which two input spaces are mapped through a shared generic space into a
novel blend [@fauconnier-turner-2002-the-way-we-think]. The contribution here is the conjunction —
a single closed calculus — together with the selection functional and the mechanized adjudicator,
not the individual moves. The closure claim is falsifiable within its scope (below): an invention
whose minimal description requires an operation outside $\{\alpha, \rho, \tau, \gamma\}$ would
refute it.

## Selection under joint constraints

The move set says what operations are available; it does not say which to apply. The space of
possible re-coordinatizations is vast, and a selection principle is needed. Here the account departs
sharply from both the embodied-abduction position and its rival, creativity-as-compression.

### The general-relativity case, corrected

Consider the case the opposing position leans on hardest: general relativity, where there was no new
data. The equivalence of inertial and gravitational mass had been measured to high precision and sat
in the books as a numerical coincidence. Einstein's move was to promote that coincidence to a
*structural identity* — to read two axes previously held distinct (inertial versus gravitational
mass; acceleration versus gravitation) as the same axis. That is a re-topologization composed with
an adjunction, performed on the *existing* representation, not a fresh percept. The
elevator thought experiment is the human *rendering* of this move — how it was made intuitive — not
its content.

But the clean story that generation precedes validation is historically false, and the paper does
not tell it. The documentary record of the Zurich notebook shows that Einstein found the
mathematically correct curvature structure early and abandoned it for roughly three years because it
failed to reproduce the Newtonian limit; the empirical constraint actively pruned the generative
search, and at one point derailed it [@janssen-2007-genesis-general-relativity]. Generation is
therefore search under *joint* constraints. Let a candidate representation $R'$ be scored by

$$
\mathcal{S}(R') \;=\; \alpha_1\,\mathrm{DL}(A_{R'}) \;-\; \alpha_2\,\mathrm{Sym}(R') \;-\;
\alpha_3\,\mathrm{Clo}(R') \;+\; \alpha_4\,\mathcal{E}(R'),
$$

where $\mathrm{DL}(A_{R'})$ is the description length of the *axioms* of $R'$ (not of the data),
$\mathrm{Sym}$ and $\mathrm{Clo}$ reward symmetry and closure or consistency, $\mathcal{E}$ is
empirical inadequacy against whatever substrate exists, and the $\alpha_i$ are non-negative weights;
invention selects a move minimizing $\mathcal{S}$. Three points follow. First, the
operative compression is of the axioms, not the data — which dissolves the "no error signal"
objection, since data-loss can be near-zero while axiom description length falls steeply (this is
also the answer to creativity-as-compression, which measures loss on data
[@schmidhuber-2008-driven-by-compression]). Second, the empirical term $\mathcal{E}$ is often weak
but rarely absent, and it can act *during* generation, as the notebook shows. Third — and this is
the scope condition made precise below — within any domain whose compatibility predicate is
decidable, $\mathcal{M}$ is enumerable and $\mathcal{S}$ is computable; outside such domains the
paper asserts neither.

That intrinsic selection can drive discovery without a body is not a conjecture, and it is not new:
machine discovery of scientific regularities from intrinsic signals has a lineage running from the
rediscovery of quantitative laws [@langley-1987-scientific-discovery] to modern symbolic regression,
where a system recovers physical laws using exactly intrinsic structural signals — dimensional
analysis (a rescaling), symmetry, and separability — with no sensory grounding whatsoever
[@udrescu-tegmark-2020-ai-feynman].

### Grounding, relocated rather than eliminated

The strongest objection to any such account is symbol grounding: a system manipulating ungrounded
symbols has, a priori, no purchase on meaning, so structural moves driven by internal metrics are
merely shuffling form [@harnad-1990-symbol-grounding; @bender-koller-2020-climbing-towards-nlu]. The
reply is not to deny grounding but to locate it. Grounding constrains knowing *which* structural
hypothesis is true of an external world; it does not block *generating* a well-typed structural
hypothesis. And it is not wholly downstream: in empirical domains the filter for which move is
domain-coherent is exactly the empirical term $\mathcal{E}$, which co-selects during generation; in
formal domains $\mathcal{E}$ is absent and invention is fully intrinsic. This is why the
paper rejects a pipeline with separate `generate` and `validate` modules — in empirical science they
are the same module — while preserving the claim that the generative act, in formalized domains,
needs no world.

## Primitives as completions

A residual worry is that recombination cannot account for genuinely new primitives — the imaginary
unit, entropy, the field concept — which seem to arrive from nowhere. They do not. Each is a
structural completion under a consistency demand: a special case of adjunction in which an element
is adjoined to make an operation total, or a macro-coordinate is forced by the impossibility of
certain transitions. Adjoining a root to close an operation, or completing a structure under a
required law, is the formal template for "new primitive". This dissolves the
creation-from-nothing reading without claiming the space of completions is prestatable — a
limitation the scope condition marks explicitly.

## A running existence proof, scoped

The account's distinctive evidence is that its central move is not merely formalizable but already
mechanized. The corpus's modular-ontology machinery links typed specification modules under a
link-time compatibility predicate: one module *owns* the terms it introduces (an adjunction), may
*refine* an imported term (a re-specification), and *imports and glues* terms across modules (a
combination) [@zharnikov-2026-organizational-schema-theory-test-driven]. Its federated extension
classifies every cross-owner interaction between two
authors' module sets — agreement, conflict, cross-refinement, cross-import, incompatible refinement —
and proposes a reconciliation by lock, fork, rebase, or merge. This is a running artifact that
performs *and adjudicates* cross-domain structural recombination inside a specification domain. Its compatibility predicate is a finite check over typed modules — unique ownership, no
dangling import, compatible refinement, acyclicity — and is therefore decidable; this is what places
the domain inside the scope condition rather than outside it.

The point is not analogy but explanatory gain. The four-move account *predicts* the classification
of a given cross-owner interaction and the admissibility of a proposed combination — a phenomenon
that the embodied-abduction position (which offers no account of formal-domain invention mechanics),
mind-centered creativity theories, and data-compression accounts neither predict nor explain. A
companion demonstration accompanies the paper: two specification module sets, each exercising the
four moves as ontology operations, are passed to the negotiator, which classifies each interaction
exactly as the account predicts — a glue as a cross-import, a re-specification as a cross-refinement,
and a re-introduced term as admissible or inadmissible by a finite, decidable compatibility check
(reproduction command in the Data and Code Availability statement). What remains future work is a
fuller suite across more move compositions and a robustness check on the weighting of $\mathcal{S}$.

## The same moves without a mind: evolution

If invention required embodied cognition, then a process with no cognition, no body, and no intent
could not invent. Evolution refutes the antecedent, and it does so using the same four moves — strong
evidence that structural invention is substrate- *and* mind-independent.

- *Adjoining a dimension* is gene and genome duplication followed by neofunctionalization: a
  redundant copy is a new degree of freedom, free to diverge to a new function at no cost to the
  original — the mechanism identified as the chief source of evolutionary novelty
  [@ohno-1970-evolution-by-gene-duplication].
- *Rescaling* is polyploidy and whole-genome duplication, and heterochrony — change in copy number
  and in the timing and magnitude of development.
- *Re-topologizing* is exaptation and regulatory rewiring: an existing structure's admissible role
  is changed without changing the structure, exactly a change in the admissible morphisms
  [@gould-vrba-1982-exaptation].
- *Gluing across domains* is symbiogenesis: two independent lineages fused into one composite, the
  mitochondrion standing as a biological pullback of a proto-eukaryote and an endosymbiont
  [@sagan-1967-origin-of-mitosing-cells].

Selection is the joint functional of the preceding section, with fitness-in-environment as the
empirical term $\mathcal{E}$. Crucially, $\mathcal{E}$ acts *during* variation, not after it:
evolution is the paradigm case that generation and validation are one process, corroborating the
correction made to the general-relativity story. And because the biological adjacent possible is not
finitely prestatable, evolution operates *outside* a decidable-compatibility domain — which is
precisely why its search is blind, slow, and wasteful rather than the fast computable selection
available in formalized domains. Evolution is thus an honest illustration of the account's boundary,
not a counterexample to it. It is worth noting that the module operators above — fork, rebase, merge
— are the computational cognates of duplication-divergence and symbiogenesis.

## The same move in markets

The account is not confined to science and biology. In markets, category creation is an adjunction —
a demand dimension the market had no coordinate for — and owning a category is the adoption and
lock-in of that coordinate, a phenomenon on the side of meaning rather than a monopoly on cognition. This reframes a familiar strategic claim — that automation commoditizes execution but
cannot decide which category to own — as a special case of the same authoring-versus-optimizing
distinction that separates a representation-changing move from optimization within a fixed
representation.

## Scope and boundary conditions

The mechanizability and closure claims are asserted only within representational systems whose
compatibility predicate is decidable — formalized and specification domains. For open-ended
empirical science, where the adjacent possible is not finitely prestatable
[@kauffman-2000-investigations] and where the relevance of a candidate axiom is a global property of
a belief system rather than a local syntactic one [@fodor-2000-mind-doesnt-work-that-way], the
account claims only that the four operator *types* describe the observed moves; it does not assert
that the move-space is enumerable or that $\mathcal{S}$ is a complete selection principle. This boundary is not a hedge but the content: it locates exactly where a computable account of
invention stops and where blind search of the evolutionary kind begins.

## Rivals

*Embodiment.* The strongest embodied-cognition claim holds that "dimension", "topology", and
"gluing" are irreducibly sensorimotor, so a disembodied system cannot deploy them
[@lakoff-nunez-2000-where-mathematics-comes-from]. The reply distinguishes discovery from content:
embodiment may explain how a human *rendered* a move, but the formalized operation is
substrate-neutral, as intrinsic-selection discovery systems that use no body demonstrate. That the
same structure is often reached independently by different people — the pattern of multiple
discovery [@simonton-1979-multiple-discovery] — is further evidence that an invention names a
reachable structure rather than the signature of one embodied mind.

*Compression.* Creativity-as-compression measures loss on data and so cannot explain inventions
where data-loss was already near-zero; the inventions at issue compress the axioms, not the
observations [@schmidhuber-2008-driven-by-compression].

## Limitations

The claim that structural invention is mechanizable is a claim about a mechanism, scoped to
decidable domains and partly demonstrated by a running artifact. It is not a claim that a current
language model has autonomously produced a paradigm-scale invention; evidence of failure at
out-of-distribution abstraction bounds the empirical reach, and the paper does not overstep it
[@chollet-2019-measure-of-intelligence]. The existence proof is a companion
demonstration inside one specification domain; a fuller suite across more move compositions and a
robustness check on the weighting of $\mathcal{S}$ remain future work before it can bear its full
weight. And the
non-prestatability of the adjacent possible means the account does not extend to open-ended
empirical discovery without an external oracle; the joint-constraint reframe bounds this limitation
but does not remove it.

## Conclusion

The abductive jump is real, but it is not a leap from sensation to axioms that only a grounded body
can make. It is a re-coordinatization of the space of description — an adjunction, a rescaling, a
re-topologization, or a gluing — selected under joint intrinsic and empirical constraints. In
formalized domains the operators are enumerable and the selection computable, and a running
adjudicator already performs the central move; in open empirical domains the operators still
describe invention, but the search becomes the blind, prestatement-free process that evolution
exhibits. The scope condition is not a concession of the hard case. The same four moves account for
the general-relativity jump (a re-topologization on the existing representation) and for the origin
of the eukaryotic cell (a gluing of two lineages); what changes across the decidable-domain boundary
is not *whether* invention is a structural operation but only *whether the right operation can be
selected by computation* rather than by the blind, costly search of evolution. The wall the opposing
position describes is therefore real, but it does not run between humans and machines. It runs
between authoring a representation and optimizing within one — and authoring, the evidence of formal
systems and of life itself suggests, is not the exclusive property of minds.

## Acknowledgments

AI assistants (Google Gemini 3.1 Pro, xAI Grok 4, and Anthropic Claude Opus 4.x) were used for
initial literature search, for software development — implementing and running the companion
demonstration script that reproduces the paper's reported classification results — and for editorial
refinement; all theoretical claims, propositions, and interpretations are the author's sole
responsibility. Every citation was independently verified against Crossref before inclusion.

## Author Contributions (CRediT)

Dmitry Zharnikov: conceptualization, methodology, formal analysis, software, writing — original
draft, writing — review and editing.

## Funding

This research received no external funding.

## Competing Interests

The author declares no competing interests.

## Data and Code Availability

The companion demonstration for the running existence proof is `code/four_moves_demo.py`, reproducible
with `python code/four_moves_demo.py` (Python 3.12 and PyYAML; deterministic; exits 0 on success),
together with its two input module sets under `code/fixtures/` and the vendored negotiator it invokes. The public repository — paper source, the argument
spine to which every claim is traced, the ontology module, and the demonstration code — is available
at <https://github.com/spectralbranding/meaningfulness-papers/tree/main/invention-as-structure>. The
archival record is deposited on Zenodo: concept DOI (all versions)
[10.5281/zenodo.21653102](https://doi.org/10.5281/zenodo.21653102); this version (v1.0.0)
[10.5281/zenodo.21653103](https://doi.org/10.5281/zenodo.21653103). No new empirical data were
collected.

## References

::: {#refs}
:::
