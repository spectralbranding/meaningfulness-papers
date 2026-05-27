# Companion Computation Scripts — Paper B 2026ap v1.0.0

These scripts reproduce the numerical figures cited in Paper B 2026ap "Same Meaning, Different Prose: Spine Preservation and Rendering Equivalence in Organizational Knowledge Work" v1.0.0 per `research/PAPER_QUALITY_STANDARDS.md` items 37a–37e (mandatory).

## What each script reproduces

### `rec_metric.py`

Reproduces the focal-pair recombination metric reported in paper.md §Results:
- **Rec(G_EM, G_ZW) = 4** on linked propositions with preserved antecedents

Method: parses two YAML-encoded spines per Paper A's typed-DAG schema (10 node types; 17 edge types) and counts linked propositions where (a) the edge type is in the valid 17-type catalog and (b) at least one antecedent edge is preserved across both members of the pair. At v1.0.0 the linkage counts the rows of the operator-supplied alignment table in `TWIN_PAIR_ISOMORPHISM_PB_FOCAL.md`; v1.1.0 adds inter-coder κ measurement on this alignment.

### `null_baseline.py` (v1.0.0 addition)

Reproduces the random-graph null-baseline distribution reported in paper.md §Results §Null-baseline subsection. For each real twin-pair spine, generates `n_shadows = 1000` random "shadow spines" matched on node count and node-type distribution but with antecedent edges drawn at random from the pooled antecedent set across the five real Paper B spines. Computes Rec(real, shadow) for each shadow and reports the distribution.

Key figures it reproduces:
- Random-shadow Rec distribution: mean ≈ .05, sd ≈ .22, p95 = 1, p99 = 1, max observed = 1 (focal) / 2 (KBV)
- Pr(Rec ≥ 3 by chance) = .000 across n = 1000 shadows
- Pr(Rec ≥ 4 by chance) = .000 across n = 1000 shadows
- Observed Rec = 4 on focal pair sits above the random-shadow distribution at the 100th percentile (no shadow at or above 4 observed)
- Effect size: (4 − .05) / .22 ≈ 18 standard deviations above the null mean

Run command: `uv run python null_baseline.py --n-shadows 1000 --seed 42`

### `cost_function_calibration.py`

Reproduces the β/δ point estimates reported in paper.md §Results:
- β̂(G_EM) grid-anchor = .7 (fit .70)
- β̂(G_ZW) grid-anchor = .7 (fit .70)
- β̂(G_TO) grid-anchor = .7 (fit .70)
- δ̂(R_EM) grid-anchor = 1.3 (fit 1.24)
- δ̂(R_ZW) grid-anchor = 1.3 (fit 1.25)
- δ̂(R_TO) grid-anchor = 1.3 (fit 1.24)

Method: fits the exponents β and δ from the cost-function specification c_AI(S) = α · |V|^β and c_human(R) = γ · |tokens|^δ assuming α and γ scale constants calibrated to the harness throughput. Reports grid-anchored estimates against Paper A's specified parameter grid (β ∈ {.5, .7, .9}; δ ∈ {1.1, 1.3, 1.5}). At v1.0.0 the data is single-observation-per-target (illustrative); v1.0.1 lands multi-observation-per-target harness with bootstrap intervals.

## Run commands

```bash
cd <public-mirror>/sbt-papers/meaningfulness-empirical/code/

# Recombination metric on focal pair
uv run --with pyyaml python rec_metric.py \
    --spine1 ../VALIDATION_CASE_PB_FOCAL_EISENHARDT_MARTIN_SPINE.yaml \
    --spine2 ../VALIDATION_CASE_PB_FOCAL_ZOLLO_WINTER_SPINE.yaml \
    --alignment-table ../TWIN_PAIR_ISOMORPHISM_PB_FOCAL.md

# Cost-function calibration on three spines / three renderings
uv run python cost_function_calibration.py --print-only
```

## Random seed

Fixed at `SEED = 42` in both scripts per `PAPER_QUALITY_STANDARDS.md` item 37a default. No RNG is actually invoked at v1.0.0 (both scripts are deterministic on their inputs); the seed is included for forward compatibility with v1.0.1+ bootstrap intervals.

## Dependencies

- `pyyaml` (for `rec_metric.py` only; invoke via `uv run --with pyyaml python ...`)
- Standard library only for `cost_function_calibration.py`

## Provenance

This `code/` directory is a public mirror of the internal SSOT at `research/meaningfulness_empirical_companion/code/` in the corpus repository. The two directories are kept synchronized at each Zenodo release per `PAPER_QUALITY_STANDARDS.md` item 37e (Mirror obligation).

Paper B 2026ap Zenodo DOI: [reserved at joint Zenodo upload with Paper A 2026ao]

## What v1.0.0 does NOT include

- Bootstrap confidence intervals on β and δ (v2.0.0; requires multi-observation-per-target harness).
- Inter-coder κ measurement on the spine alignment table (v1.1.0 execution; protocol pre-registered at `PHASE4_KAPPA_MEASUREMENT_2026-05-27.md`).
- Third-party-coder substitution for δ (v2.0.0+).
- Matched-non-twin Rec baseline (v2.0.0+; the v1.0.0 `null_baseline.py` is the random-shadow null comparison, not a real-non-twin discriminant-validity check).
- Multi-pair Rec distribution (v2.0.0 N=15–20).
- Prospective lab-cohort data (v2.0.0+).

Each deferred item carries an explicit release-version commitment in paper.md §Discussion §Versioning trajectory.
