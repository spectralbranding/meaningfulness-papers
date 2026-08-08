# 2026bk — validation code

Everything the paper reports is produced by the scripts in this directory, from
public inputs, under the pre-declarations in `../PROTOCOL.yaml`,
`../DECISION_RULE.md` and `../READER_MODEL.md`.

## 1 | Getting started

```bash
uv --version                 # the only prerequisite; scripts declare their own deps
../reproduce.sh              # analysis only: no keys, no network, deterministic
bws run -- ../reproduce.sh --collect   # additionally re-runs the model calls
```

## 2 | Layout

| Path | What it holds |
|---|---|
| `../specimens/` | Prepared specimen and pilot texts (git-ignored: third-party copyright) plus `MANIFEST.json` with the sha256 of each |
| `../data/` | One JSON per (document, operator) extraction, plus alignments and ratings |
| `../logs/` | One JSONL per model call: prompts, parameters, prompt hash, response, tokens, latency |
| `../output/tables/` | The computed statistics |

## 3 | Script map

| Script | Produces | Needs keys |
|---|---|---|
| `prepare_specimens.py` | `../specimens/*.txt`, `MANIFEST.json` | no (network) |
| `extract_spines.py` | `../data/spine_<doc>__<OP>.json` | yes |
| `score_agreement.py` | `../output/tables/agreement_{pilot,main}.json` | no |
| `score_ladder.py` | `../output/tables/ladder.json`, `../data/align_*.json` | only for a new alignment |
| `score_targets.py` | `../output/tables/targets.json`, `../data/rating_*.json` | only for a new rating |
| `metrics_lib.py` | every statistic, implemented once | — |
| `tests/test_metrics.py` | the estimators checked against hand-worked cases | — |

## 4 | Two things the design turns on

**Cross-operator separation.** The two extraction arms are different model
families. Two arms of one family would be one operator run twice, and the
agreement number would measure sampling noise rather than operator independence.
The raters who score the recovery targets are drawn from families that did not
produce the graph they score, and never see which operator produced it.

**Idempotence.** An extraction, alignment or rating that already exists on disk
is never re-called and never overwritten. A result cannot be quietly re-rolled,
and a resumed run costs nothing.

## 5 | Reproducibility

Analysis is deterministic under the seed in `PROTOCOL.yaml` (20260809),
including the random-graph null. Extraction is not: the operators are hosted
models whose behaviour is epoch-pinned, so `--collect` yields a new epoch rather
than a byte-identical replication. Every call is logged, so every reported
number is reproducible from the committed artifacts with no API access at all —
which is the property that matters for checking the paper.

## 6 | Citation

See `../../../CITATION.cff` at the mirror root and the paper's Data and Code
Availability section.

## 7 | Licence

Code MIT; data and generated artifacts CC BY 4.0. Specimen texts remain under
their own authors' terms and are not redistributed here — `prepare_specimens.py`
fetches them from their public sources and verifies the digests.

*Last updated: 2026-08-06*
