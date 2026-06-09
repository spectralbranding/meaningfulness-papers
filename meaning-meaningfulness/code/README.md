# code/ — companion computation for Paper A 2026ao

Companion scripts for *Spec-Based Research in the Post-AI Era* (concept DOI [10.5281/zenodo.20409683](https://doi.org/10.5281/zenodo.20409683)).

## Script map

| Script | Purpose | Run command | Outputs |
|--------|---------|-------------|---------|
| `cost_asymmetry_crossover.py` | Analytic AI-vs-human verification-cost crossover chart for the P3 cost-asymmetry result (Section 3). Deterministic — no random seed; the crossover is solved in closed form as `x* = (alpha/gamma)^(1/(delta-beta))`. | `python cost_asymmetry_crossover.py` (or `uv run python cost_asymmetry_crossover.py`) | `cost_asymmetry_crossover.png` (300 dpi), `cost_asymmetry_crossover.svg` |

Parameters (named constants at the top of the script): `alpha=1.0`, `beta=0.7` (AI, sub-linear), `gamma=0.05`, `delta=1.4` (human, super-linear). With these values the crossover prints to stdout at `x* ≈ 72.21` (artifact size, log scale) — the point where human verification cost overtakes AI verification cost. Edit the constants to reproduce variants.

## Dependencies

`numpy`, `matplotlib`. No network access, no API keys, no data files — the chart is generated from the closed-form parameters above.

## Note on the simulation scaffold

The cost-asymmetry *simulation* harness referenced in Appendix C (`cost_asymmetry_simulation.py`, random seed `42`) is a separate, Monte-Carlo artifact deferred to v1.1.0. `cost_asymmetry_crossover.py` here is the analytic companion chart and is self-contained.

---

*Last updated: 2026-06-09*
