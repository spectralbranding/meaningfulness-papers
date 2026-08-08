# Amendments to the deposited design

The pre-registration is deposited and unchangeable: v1.0.0, DOI
[10.5281/zenodo.21830221](https://doi.org/10.5281/zenodo.21830221), 2026-08-07. Every departure from
it is recorded here, with its date, its reason, and whether it was decided before or after the
quantity it touches was observed. The results version reports this list in full.

**No threshold in Table 2 moves. Nothing in this file is a revision made in the light of a result.**

---

## A1 — The Layer S adjudicators are machine, not human

**Declared 2026-08-08, before any call of any kind.**

**What the deposit says.** M1a: "two adjudicators segment each document independently under the
declared rule, blind to the study's hypotheses and to which condition the inventory will serve; a
third resolves disagreements". Table 2 derives the $\kappa \geq .80$ gate as a discount on the
$.874$ human blind segmentation floor, "because rule-vs-adjudication is harder than human-vs-human",
and M4a describes the comparison as "a deterministic rule against human adjudication".

**What is run instead.** Two adjudicator models from families used in no other role in this study
(`ADJ_1` xai, `ADJ_2` deepseek) segment each document independently under the declared rule, blind
to the hypotheses and to which condition the inventory serves; a third family (`ADJ_3` mistral)
resolves disagreements. The two-adjudicator-plus-resolver structure, the blinding, and the
requirement that the adjudicators' own agreement be reported beside the segmenter's are all
preserved. What changes is the kind of adjudicator.

**Why.** Human adjudication of five documents, twice over plus resolution, is days of work by people
who must be blind to the study. The alternative to this substitution was not a better instrument; it
was no Layer S, and therefore no operator call at all, since the ordering is itself pre-registered.

**What it costs, stated rather than absorbed.** The $.80$ gate's derivation assumed the harder
comparison of a deterministic rule against *human* adjudication. Machine adjudicators may be more
rule-following than humans, which would make the comparison easier and the gate correspondingly less
demanding; they may equally share the segmenter's failure modes, which would inflate agreement for a
reason that has nothing to do with the segmenter being right. **Neither direction is known, so the
threshold is not adjusted in either direction** — adjusting it would require a number that does not
exist, which is the same move the paper refuses for the Layer 3 document-scale discount. Layer S is
therefore reported as *machine-adjudicated fidelity*, the adjudicators' own agreement is reported
beside the segmenter's exactly as the design requires, and any claim resting on Layer S is read at
that width.

**Decided before the quantity was observed.** No segmentation, adjudication or extraction call had
been made when this was decided.

---

## A2 — Layer S adjudication is elicited in chunks, not one call per document

**Introduced 2026-08-08 in the harness as first written (commit `759567bf`), before any
adjudication quantity was observed.**

**What the deposit says.** M1a: "two adjudicators segment each document independently under the
declared rule". It does not specify how the decision is put to an adjudicator, because at deposit
time that was not a design question.

**What is run instead.** Each document's candidate positions are divided into **chunks of 25**, in
document order, and each chunk is put to the adjudicator as its own call with its own passage — the
text from the previous chunk's last candidate to 240 characters past its own. Every candidate is
still decided exactly once, under the same rule, by the same model.

**Why.** A whole document in one call did not survive contact with the providers. On the first
attempt one adjudicator spent its entire 32,000-token budget reasoning and returned empty content,
and another answered a 614-candidate document with 64 boundaries — an answer shorter than the
question. The alternative to chunking was not a better instrument; it was an adjudicator that does
not answer.

**What it costs, stated rather than absorbed.** A chunked adjudicator sees less context than a
whole-document one, and a boundary judgement near a chunk edge is made with the preceding chunk's
tail rather than the whole preceding argument. The 240-character overlap bounds this but does not
remove it. The direction is not known: less context could make an adjudicator more literal about the
declared rule, or less able to recognise a continuation. **The gate is not adjusted**, for the same
reason it was not adjusted for A1 — adjusting it would require a number that does not exist.

## A3 — An unparseable chunk is recorded UNANSWERED and the pass continues

**Introduced 2026-08-08 (commit `c58fa7cf`), before any Layer S coefficient was computed.**

**What the deposit says.** Nothing; this is a failure mode the deposited design did not anticipate.

**What is run instead.** A chunk whose answer will not parse is recorded as UNANSWERED, its index is
written to the inventory's `unanswered` list, and the pass continues. Previously such a chunk raised
out of the whole document, which is what killed three of the five Layer S jobs on their first
attempt.

**What it costs, and it is measured rather than described.** An unanswered chunk contributes no
boundary from that adjudicator. For the positions inside it, the design's *two independent
adjudicators* reduces to **one adjudicator plus the resolver** — the resolver still decides them,
because a position one adjudicator marked and the other did not is by definition disputed, and
disputed positions are exactly what the resolver receives. The degradation is therefore bounded, but
it is real, and it is not uniform across documents:

| Document | Candidate positions | UNANSWERED chunks (ADJ_2) | Positions decided by one adjudicator | Share |
|---|---:|---:|---:|---:|
| VC1 | 668 | 0 | 0 | .000 |
| VC2 | 742 | 2 | 50 | .067 |
| VC3 R0 | 98 | 0 | 0 | .000 |
| VC3 R1 | 564 | 3 | 75 | .133 |
| VC3 R2 | 184 | 0 | 0 | .000 |

*Notes*: ADJ_1 answered every chunk on every document. Across all five documents, 125 of 2,256
candidate positions — 5.5% — were decided by one adjudicator plus the resolver rather than by two.
Computed by `code/report_adjudication_coverage.py`, which writes
`output/tables/adjudication_coverage.json`.

**This bears on one reported quantity in particular and the paper must say so.** VC3 R1 has both the
largest share of singly-adjudicated positions (13.3%) and the lowest inter-adjudicator agreement of
the five documents ($\kappa = .631$). Those two facts are not independent: an unanswered chunk
depresses ADJ_2's boundary count in a region where boundaries exist, which lowers the adjudicators'
measured agreement with each other. **The inter-adjudicator figure for VC3 R1 is therefore a floor
rather than an estimate**, and the same holds more weakly for VC2. The Layer S coefficient itself is
less affected, because the resolver restores the disputed positions before it is computed.

**Decided before the quantity was observed.** Both A2 and A3 were in place before any Layer S
coefficient was computed for any document.

## A4 — The two operators are not sampled the same way, and cannot be

**Configuration fixed 2026-08-08 in the harness before any operator call; its consequence discovered
during the run and reported here rather than repaired.**

**What the deposit says.** M3: every extraction is repeated $k$ times per operator, per document, per
condition, **"under identical parameters"**. The natural reading is that all parameters are identical
across the whole design.

**What is run instead.** Parameters are identical across the $k$ repetitions *within* an operator,
which is what the within-operator baseline requires. They are **not** identical *between* the two
operators, because this provider pair offers no common setting. OP_B is called at `temperature 0`
with the study seed. OP_A's family rejects sampling parameters outright on its current flagship, so
temperature cannot be set at all and reasoning depth is bounded by an effort level instead.

**Why it was not equalised.** There is no setting that both providers accept. Choosing a pair that
did would have meant abandoning the predecessor's operator pair, and comparability with the run whose
failure this design decomposes is the reason that pair is used at all (PROTOCOL, `extraction_operators`).

**What it costs, and it is visible in the results rather than hypothetical.** A deterministic
operator has no run-to-run variance, so its within-operator agreement is **1.000 by construction
rather than by measurement**. OP_B returned byte-identical answers across all five repetitions on
most cells — identical selected sets, identical edges, and identical token counts in the call log.
The declared Layer B pools both operators' same-operator pairs and takes the mean (M3), so on those
cells the pooled baseline is **an average of a measured quantity and a constant**.

This matters for one inference in particular. **P2's separation test reads the between-operator
quantity against the within-operator baseline, so a baseline inflated toward 1.000 makes separation
easier to obtain** — that is, it biases the design *against* P2's falsifier firing. Any reported
separation must be read at that width.

**What is done about it.** Nothing to the declared statistic: `within_mean` is computed exactly as
M3 specifies and is not adjusted. What is added is **reporting**, in the spirit of M4b's requirement
that a summary never travel without the marginals behind it: `score_layers.py` now emits
`within_by_operator` beside every pooled figure, with each operator's own mean and a `zero_variance`
flag that says outright when an operator contributed a constant. On VC3 R0 under U-mod, for example,
Layer 1's pooled within-operator baseline is $.938$, composed of OP_A at $.876$ (measured) and OP_B
at $1.000$ (zero variance).

**Decided before, discovered during.** The configuration was fixed before any call; its consequence
for Layer B was discovered while the run was in progress. Nothing about the design, the thresholds or
the statistic was changed in response — only what is reported about them.

## A5 — OP_B's graphs are small on long documents, and this is not truncation

**Observed during the run 2026-08-08. Recorded because the alternative explanation had to be excluded
before the number could be read as a finding.**

On the four longer documents OP_B returns graphs of roughly 14 to 16 nodes almost regardless of
document length or inventory size — 14 nodes on VC1, VC3 R1 and VC3 R2 under U-free; 16 of 421 units
on VC3 R1 under U-det; 15 of 406 under U-mod — while OP_A returns 50 to 170. A recurring number of
that kind is exactly what a truncated response looks like, and the design's own prompt says a graph
that stops early is wrong, so the possibility was checked rather than assumed away.

**It is not truncation.** Every such call returned `finishReason: STOP`, not a length stop, and used
about 1,751 output tokens against a cap of 96,000. The JSON parsed completely and the schema
validators reported no problems. OP_B is answering fully and briefly.

**It replicates the predecessor.** The predecessor's published record for VC3 R1 gives OP_B **14**
nodes; this study's U-free arm gives **14**. The asymmetry is therefore a stable property of that
operator across two studies and two harnesses, not an artifact of this one.

**What it means for the reading, stated before the coefficients are interpreted.** The
between-operator disagreement this design decomposes is dominated, on the long documents, by a gross
difference in how much of a document each operator considers node-worthy — and **fixing the inventory
does not remove it**: given 421 units, OP_B still selects 16. That is P4's unfavourable branch in its
starkest available form, and it is the reason the decomposition rather than the verdict is the
contribution.

## A6 — The composite's sampler is seeded, applying a rule the protocol already declares

**Found and fixed 2026-08-08, after the first composite pass and before the results were written
into the paper.**

**What the deposit and protocol say.** M5a requires the published joint coefficient to be computed
in-study from a maintained, version-pinned implementation. `PROTOCOL.yaml`
`separation_test.stream_seeding` states the study's reproducibility rule in general terms: *"Every
permutation and bootstrap stream is seeded from a stable digest of (seed, document, condition, layer,
operator_pair), never from a process hash, so a re-run reproduces the same intervals."*

**What was wrong.** That rule was implemented for the separation test and **missed for the
composite**. The coefficient's expected disorder is estimated by sampling random continua, and the
library does not seed that sampler. Unseeded, one cell (VC3 R0, U-det) returned $\gamma = .589$,
$.593$, $.594$ and $.597$ across four runs of identical input — a spread of about $.008$ that is
invisible in any single report and fatal to a reproduction attempt.

**What is done.** The sampler is seeded from `stream_seed(document, condition, "composite",
"OP_A|OP_B")`, the same stable-digest construction the separation test uses. Verified: two full
passes over all fifteen cells now agree to six decimal places.

**Why this is applying the pre-registration and not amending it.** The seeding rule was declared
before any data existed; the composite was simply not wired to it. Fixing that makes a declared
property true rather than changing what was declared. And it **cannot move a verdict**: M4 declares
the composite secondary in inferential status and non-gating, so no conclusion rests on it. The
seeded values differ from the first pass in the third decimal ($.594 \to .596$ on VC3 R0 U-det;
$.034 \to .031$ on VC1 U-free), which is the sampling spread and not a change of finding.

**The solver was checked at the same time and is not a degree of freedom.** The alignment is an exact
mixed-integer program. CBC is absent in this environment so cvxpy falls back to GLPK\_MI, which
reports `INTEGER OPTIMAL SOLUTION FOUND` at a proven $0.0\%$ gap — an exact optimum, not a heuristic
one, so CBC would return the same objective value. The solver is recorded in `composite.json`
(`solver`, `sampler_seeded`) and named in the availability note for completeness, not because it is a
choice that affects a number.

**Found after the quantity was observed, and the direction is stated for that reason.** The first
composite pass had been computed and seen before this defect was noticed. Nothing was selected on the
basis of the numbers: the fix was applied to every cell at once, under a rule fixed in advance, on a
quantity that gates nothing.
