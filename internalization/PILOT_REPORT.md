# Pilot Report — Internalization (2026bk)

**Run 2026-08-06, before the main extraction, on material that is neither specimen**, as
`DECISION_RULE.md` §1 requires. Its purpose is to check that the extraction protocol is executable
at all and to estimate variance. Under the rule the pilot may (a) refine the annotation guidelines,
(b) inform the number of documents in the main run, or (c) cause the study to be abandoned before
the main run. **It may not move a threshold, and none was moved.**

This report is written to be read against that permission. It reports every round, including the
two that were discarded, because a pilot reported only in its final state is indistinguishable from
a search for a favourable protocol.

## Pilot material

| Document | Words | Why it is here |
|---|---|---|
| Dijkstra, *On the cruelty of really teaching computing science* (EWD1036) | 6,167 | A sustained argument in ordinary prose with an explicitly staged structure |
| Thompson, *Reflections on Trusting Trust* | 1,731 | A short constructive argument in three stages, each standing on the last |
| A spine-first-drafted corpus paper | 11,062 | The one pilot document with an authored reference spine, so that a wildly wrong extraction would be visible against it |

All three are argumentative artifacts under C1, and none is a specimen. The reader model for all
three is M-gen, declared for the pilot alone; no pilot count is compared with any specimen count.

## Round 1 — prompt version `internalization/1.0.0`

**Discarded.** Two defects, both in the protocol rather than in the operation it measures.

**Defect 1: the input, not the extraction, was broken on one document.** The Thompson text was
taken from a two-column scan. Column-interleaved extraction destroys sentence contiguity, so
verbatim quotations spanning more than a few words no longer exist in the prepared text: 1 of 13
node spans could be located, against 34 of 34 on the other arm's shorter quotations. Every
span-located statistic then reads as operator disagreement when the disagreement is in the input.
Fixed by taking a single-column transcription, and guarded going forward by a short-line-share
diagnostic recorded in the specimen manifest.

**Defect 2: unspecified granularity.** The two arms extracted at grains a factor of six apart — 86
nodes against 14 on the Dijkstra text, 34 against 13 on Thompson. Only 5 nodes matched. At that
grain gap the agreement statistics measure an underspecified prompt.

**The fix, and the fix that was rejected.** A rule tying node count to document length would have
aligned the arms immediately and would have been *wrong*: forcing node count to scale with words
forces structural load to scale with prose mass, which prejudges precisely what the ladder is built
to measure. The guidelines instead gained an explicit UNIT RULE — one node per claim used or
defended, per object introduced and used, per method step performed, per piece of evidence offered,
per stated assumption or scope condition, and nothing else — together with a shared paragraph
numbering that constrains where a node may be anchored without constraining how many there are.

## Round 2 — prompt version `internalization/1.1.0`

The grain gap closed and node recovery became measurable. Edge recovery did not.

| Document | Nodes A / B | Matched | Layer 1 α | Layer 2 F₁ (typed) | Untyped | Layer 3 ρ |
|---|---|---|---|---|---|---|
| Dijkstra | 68 / 39 | 17 | .760 | .143 | .286 | .723 |
| Thompson | 29 / 31 | 16 | .638 | .235 | .353 | .598 |

*Notes*: α is nominal Krippendorff over node types on matched spans; F₁ is triple overlap over the
matched node set; the untyped column erases the edge type and is diagnostic only. All spans located
on both arms after the round-1 input fix (68/68, 39/39, 29/29, 31/31).

Two things are visible. First, **node recovery sits at or near the declared Layer-1 line while edge
recovery sits nowhere near the Layer-2 line** — which is the pattern L0 predicted from the argument-
mining literature, arrived at here independently. Second, roughly half the edge disagreement is
about *what to call* an edge rather than whether it is there: erasing the type doubles the overlap
on Dijkstra and lifts it by half on Thompson.

That second observation is a protocol defect, and it is the one thing round 2 licensed fixing.

## Round 3 — prompt version `internalization/1.2.0`, frozen

Two additions, both aimed at the edge layer, both applied identically to the two arms:

- **Edge completeness.** Go through the nodes and ask of each what it stands on; a node with no
  outgoing edge asserts that the text offers it without support, which is a real category but
  should be the minority.
- **An ordered type rule.** `derives` → `supports` → `assumes` → `bounds` → `depends_on`, first
  match wins, applied strictly rather than by preference. Where two readers could reasonably
  differ, the order decides, which is what makes a type comparable across extractions at all.

**The guidelines are frozen at 1.2.0.** Iterating further on pilot material until a number improved
would convert the pre-declaration into a search, which is the failure mode `DECISION_RULE.md` names
by name for thresholds and which applies with equal force here.

A third defect surfaced in this round and was fixed as a run parameter rather than a guideline: on
the arm whose provider counts reasoning tokens against the output cap, one call spent its entire
budget reasoning and returned nothing. The cap was raised and reasoning depth bounded at the
provider's middle effort level. Recorded in `PROTOCOL.yaml`.

| Document | Nodes A / B | Matched | Layer 1 α | Layer 2 F₁ | Untyped F₁ | Null p99 | Edge retention A / B | Layer 3 ρ |
|---|---|---|---|---|---|---|---|---|
| Dijkstra | 81 / 29 | 17 | .817 | .100 | .200 | .100 | .094 / .357 | .398 |
| Thompson | 33 / 30 | 17 | .382 | .500 | .700 | .100 | .297 / .310 | .297 |
| Corpus paper | 82 / 25 | 11 | .682 | .167 | .500 | .167 | .028 / .200 | .811 |

*Notes*: Edge retention is the share of each operator's edges whose **both** endpoints survive the
restriction to the agreed node set — declared before the specimen run, diagnostic only. All spans
located on both arms in all three documents.

Four things this round establishes, none of which decides anything about the specimens.

**The protocol is executable.** Both arms return schema-valid graphs on every document, every span
locates, and every statistic computes. That was the pilot's first purpose and it is satisfied.

**Agreement is high-variance and the two layers move independently.** Between Dijkstra and Thompson
the node-type coefficient falls by more than half while the edge statistic multiplies by five. A
single-document pilot would have produced a confident and wrong estimate of either.

**The edge layer is measured on a very small sample.** Restriction to the agreed node set is what
the decision rule requires — Layer 2 is defined over nodes both operators recovered — but it leaves
3 to 11 triples per document, because between 3% and 36% of each operator's edges have both
endpoints in that set. At that size the statistic is noisy by construction, and the random-graph
null is correspondingly coarse. This is a property of the declared design, reported rather than
repaired: repairing it would mean moving the matching threshold, which is not a guideline.

**Roughly half the edge disagreement is about naming, not existence.** Erasing the edge type raises
the overlap on every document, by between .20 and .33. The ordered type rule narrowed this without
closing it.

## What the pilot decided

**Proceed to the main run**, with the guidelines frozen at 1.2.0. The pilot's three permitted
outcomes were to refine the guidelines, to size the main run, or to abandon the study; the first
was exercised twice and the third is not warranted — the protocol executes, and the specimen set is
fixed by the design rather than by a power calculation, so there is no run to size.

**The pilot does not predict the specimen result and is not used as evidence about it.** It runs
under a different reader model, on material chosen for availability rather than for the properties
the specimens were chosen for, and no pilot number is compared with any specimen number. What it
does establish is where to look: the node layer reaches the declared line on two of three
documents, the edge layer does not reach it on any, and the edge layer is where the design's
weight sits.

That asymmetry is not a surprise. It is what L0 predicts from the argument-mining literature —
human annotators agree substantially worse on argument *relations* than on the units those
relations connect — arrived at here independently, on a different task, with machine operators.
