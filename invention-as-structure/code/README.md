# Companion code — invention-as-structure (P7 existence proof)

This directory holds the runnable, auditable demonstration for the paper's central
empirical claim (P7): that the four-move account of invention *predicts* how the
corpus's federated ontology negotiator classifies a cross-owner interaction between
two authors' specification modules, under a decidable compatibility predicate.

## What it demonstrates

`four_moves_demo.py` loads two specification module sets (`fixtures/authorX`,
`fixtures/authorY`), each exercising the four invention moves as ontology
operations, invokes the negotiator (`negotiate_modules.py`, vendored beside the
demo with its one dependency `build_ontology.py` as a reproduction snapshot of
the corpus ontology-negotiation tools), and asserts that every predicted
classification is observed:

| Invention move | Ontology operation | Predicted negotiation class |
|---|---|---|
| adjoin a dimension | `owns` a new term | (no cross-interaction — a pure adjunction) |
| glue across domains | `imports` the other author's term | `CROSS_IMPORT` |
| re-specify / rescale | `refines` the other author's term (`narrows_to`) | `CROSS_REFINE` |
| admissible adjunction | same key, identical definition | `AGREEMENT` |
| inadmissible adjunction | same key, incompatible definition | `CONFLICT` |

The `AGREEMENT` vs `CONFLICT` split is the admissibility predicate: the negotiator
accepts a compatible re-introduction of a term and rejects an incompatible one, by
a finite (hence decidable) check over typed modules.

## Run

Requires Python 3.12 and PyYAML (`pip install pyyaml`). From this directory's parent:

```
python code/four_moves_demo.py
```

Self-contained — no network, no randomness, no other dependencies. Exits `0` iff
every predicted class is observed; prints a per-move PASS/MISS table. Expected:
`RESULT: PASS`.

## Scope

This is a scoped existence proof inside a specification domain, not a claim that a
language model has autonomously produced a paradigm-scale invention (paper L1).
A fuller suite across more move compositions and a robustness check on the
selection functional's weighting remain future work (paper L2).
