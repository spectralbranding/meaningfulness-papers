# Declared Reader Models — Internalization (2026bk)

**Status: PRE-DECLARED 2026-08-06, before any extraction, before any measurement.** C2 requires a
reader model to be fixed before any quantity is measured, because every quantity the paper reports
travels with it. This document supplies the models. Like `DECISION_RULE.md`, nothing here may be
revised in the light of a result; a change made before data collection is a FORK with a changelog
row and a reason that does not refer to an observed outcome.

Three models are declared, one per specimen chain. **They are not interchangeable and no quantity
is compared across them** — C2 forbids it and L2 states why: the miracle count measures an
explanation-reader pair, not an explanation. Within the VC3 ladder a single model is used at all
three rungs, which is what makes the monotonic ordering a comparison at all.

## What a reader model has to supply

The count $\mathrm{MC}(R \mid M)$ asks, of every node in an extracted graph, whether it is
`derived` from something the reader holds, `verified_only`, or `miracle`. That question is not
answerable against a description of a reader; it is answerable against a **list**. So each model
below is stated in the form C4 requires — a module of held terms and held results, plus an
explicit **not-held** list, because the negotiation step differences against absence as much as
against presence.

Two properties are declared once, for all three models:

- **Granularity** (AA2): a term is held or not held at the granularity of a named definition or a
  named theorem. Partial familiarity is recorded as not held. This is the conservative direction:
  it can only raise a miracle count, never lower it, so it cannot flatter the result.
- **Not-held is closed, held is open in one direction only.** Anything not on the held list and
  not derivable from it counts as not held. The not-held lists below are therefore illustrative of
  the boundary, not exhaustive — they name the items an operator is most likely to mis-assign.

---

## M-alg — the reader model for VC1

The specimen's author declares his own target reader: he sought to write the explanation "with
relatively little use of algebraic geometry". The model takes him at his word and fixes the reader
he wrote for.

**Held terms.** Polynomial ring over the complex numbers; polynomial map; degree; Jacobian
determinant and the chain rule; invertibility of a map; injectivity, local injectivity; the
inverse function theorem; linear algebra over a field (basis, rank, determinant); elementary
complex analysis (holomorphic function, power series, the identity theorem); systems of polynomial
equations and their solution sets as subsets of $\mathbf{C}^n$; change of variables by polynomial
substitution; the statement of Bezout's theorem for plane curves.

**Held results.** The Jacobian conjecture as a statement. That a polynomial map with nonvanishing
Jacobian is locally injective. Elementary symmetric-function identities. Nothing about the
counterexample itself.

**Not held.** Affine and projective variety, scheme, morphism of varieties, generic point,
degeneration, blow-up, the line at infinity as a geometric object, symmetric powers
$\mathrm{Sym}^k$, group actions of $SL_2$ on polynomial spaces, differential operators as
geometric objects, Galois theory beyond the definition of a field extension, sheaves, cohomology.

**Consequence, stated in advance.** This reader is *below* the specimen's incidental machinery on
purpose. A step that the author dispatches by an algebro-geometric appeal is `verified_only` or
`miracle` under M-alg even where a specialist would call it routine. That is the intended
behaviour: the count is a property of the explanation-reader pair, and this pair is the one the
author himself chose to write for.

---

## M-nt — the reader model for the VC3 ladder

One model, used at R0, R1 and R2 alike. The three rungs expound one result, so the ordering
$\mathrm{MC}(R_0) > \mathrm{MC}(R_1) > \mathrm{MC}(R_2)$ is a statement about three renderings and
one reader.

**Held terms.** Number field, degree of a field extension, ring of integers, discriminant, real
and complex embeddings, totally real field, prime splitting and ramification, Galois group,
quadratic and cyclotomic fields; finite group, $p$-group, generators and relations, group
presentation; the plane as $\mathbf{C}$; Euclidean distance; asymptotic notation $O(\cdot)$,
$o(\cdot)$ and "for all sufficiently large $n$"; graph, incidence, counting pairs; lattice and
packing in the elementary sense.

**Held results.** The unit-distance problem as a statement, and that the best known upper bound is
of order $n^{4/3}$. The finiteness of the class number. The Dirichlet unit theorem as a statement.
The pigeonhole and Cauchy–Schwarz inequalities.

**Not held.** Pro-$p$ group, Frattini subgroup, generator and relation rank of a pro-$p$ group,
the Golod–Shafarevich inequality, maximal unramified $p$-extension, class field theory, CM field
and complex conjugation on it, Minkowski's convex body theorem in the form used for these
estimates, Odlyzko discriminant bounds, the specific tower construction the result rests on.

**Consequence.** The gap between held and not-held is deliberately placed **exactly where the
construction lives**. If the ordering fails under this model it fails at the place the ladder is
supposed to be measuring, not at an artefact of an over-strong or over-weak reader.

---

## M-phil — the reader model for VC2

**Held terms.** Digital computer, program, instruction, memory, storage capacity; algorithm in the
informal sense; the notion of a rule; probability in the informal sense; the distinction between a
question of fact and a question of meaning; ordinary logical vocabulary — premise, conclusion,
contradiction, counterexample.

**Held results.** That machines of the period could be built and programmed. That a game can be
described by rules. Nothing about computability theory.

**Not held.** Turing machine as a formal object, universality proof, the halting problem,
Gödel's incompleteness theorems and their proof, the arithmetization of syntax, formal semantics,
statistical learning, the subsequent literature about this text.

**Consequence.** The specimen's own decomposition is stated in ordinary prose and its residual is
conceded in ordinary prose, so a reader holding ordinary vocabulary is the right one to score
against. The not-held list matters most at the one place the specimen leans on a formal result:
the mathematical objection.

---

## M-gen — the pilot-only reader model

Declared for completeness, because the pilot documents also need a referent and
because leaving one undeclared would let the pilot's counts float. **No reported specimen quantity
is computed under M-gen**, and no pilot count is compared with any specimen count.

**Held terms.** General education to first-degree level; the vocabulary of computing and of
research method as it appears in a serious general periodical — program, compiler, operating
system, experiment, hypothesis, control, measurement, sample, bias; ordinary logical vocabulary.

**Held results.** Nothing domain-specific.

**Not held.** Any formal apparatus stated in symbols; any named theorem; any construct proprietary
to one research programme.

---

## The one thing these models are not

They are not claims about any real reader. They are declarations that fix a referent so a count
has one, in the sense in which an item-difficulty statistic is reported with the population it was
estimated on. No reader was consulted, and none is claimed. The acceptance test of M5, which does
require actual readers, is not run in this release, and no clause of it is scored here.

## Forked into the spine

Recorded as `reader_models` in `SPINE.yaml` at spine_doc_version 0.8.0, with C2 and P3 pointing at
it. The prose statement of the models belongs to the paper's Method section; the lists above are
the operative artifact and are what the harness is given.
