# code/ — companion computation for Paper A 2026ao

Companion scripts for *Spec-Based Research in the Post-AI Era* (concept DOI [10.5281/zenodo.20409683](https://doi.org/10.5281/zenodo.20409683)).

## Script map

| Script | Purpose | Run command | Outputs |
|--------|---------|-------------|---------|
| `cost_asymmetry_crossover.py` | Analytic AI-vs-human verification-cost crossover chart for the P3 cost-asymmetry result (Section 3). Deterministic — no random seed; the crossover is solved in closed form as `x* = (alpha/gamma)^(1/(delta-beta))`. | `python cost_asymmetry_crossover.py` (or `uv run python cost_asymmetry_crossover.py`) | `cost_asymmetry_crossover.png` (300 dpi), `cost_asymmetry_crossover.svg` |
| `cost_asymmetry_simulation.py` | Calibrated grid simulation for **Online Appendix C** (verification-cost ratio across the beta-delta grid; per-pair crossover; recombination advantage; distribution-shape and judgment-fraction sensitivity). Reproduces every appendix-cited quantity and prints a MATCH/MISMATCH verdict for each. Random seed `42`. | `uv run --with numpy python cost_asymmetry_simulation.py` (or `python cost_asymmetry_simulation.py` if numpy present) | text report to stdout (no figure files) |

### `cost_asymmetry_crossover.py` parameters

Named constants at the top of the script: `alpha=1.0`, `beta=0.7` (AI, sub-linear), `gamma=0.05`, `delta=1.4` (human, super-linear). With these values the crossover prints to stdout at `x* ≈ 72.21` (artifact size, log scale) — the point where human verification cost overtakes AI verification cost. Edit the constants to reproduce variants.

### `cost_asymmetry_simulation.py` — model and reproduction status

Implements the Appendix C model exactly as stated (C.1): `c_AI(S) = alpha*|V|^beta` (beta<1), `c_human(R) = gamma*|tokens|^delta` (delta>1), `|tokens| = mu*|V|`, with `alpha = gamma = 1`, grid `beta in {.5,.7,.9}`, `delta in {1.1,1.3,1.5}`, and `mu` centered on 100 (C.2). The crossover `|V|*` solves `c_AI(S) = (1-f)*c_human(R)` in closed form with default judgment fraction `f = .15` (C.5).

The script does **not** hard-code any reported value; it computes from the model and asserts each appendix claim MATCH or MISMATCH. Current status: **12 / 12 claims reproduce** — Appendix C is aligned to this script (the script is the single source of truth for every value Appendix C reports as simulated/computed/calibrated).

- **Verification-cost ratio (C.3):** `delta-beta` range [.2, 1.0]; `rho_cost` strictly increasing in `|V|`; advantage ~2.4–4.0 orders at |V|=10, ~2.6–5.0 at |V|=100, ~2.7–5.7 at |V|=500.
- **Cross-over (C.5):** below a single node across the whole grid (`|V|* ≈ 1e-11` to `1e-3` at `mu=100`) — the post-AI allocation beats human-only rendering verification at every artifact of one node or larger; largest where `delta-beta` is widest (β=.5,δ=1.5), smallest where narrowest (β=.9,δ=1.1).
- **Recombination (C.4)** advantage grows with complexity; **sensitivity (C.5b/C.5c)** — the crossover stays sub-node under both distribution shapes and across the judgment-fraction sweep.

**Alignment note (history).** The first draft of this script found that the *originally published* Appendix C numbers (a crossover band of 5–25 nodes; ~22 at β=.9/δ=1.1; ~6 at β=.5/δ=1.5; "one to two orders" ratios) did **not** reproduce from the stated C.1 cost functions: with `alpha=gamma=1` and `mu=100`, the super-linear human cost dominates the sub-linear AI cost at all sizes, so the crossover sits far below one node and the per-`|V|` ratios are larger than originally stated. Appendix C was then **corrected to the literal model's actual outputs** (the resolution chosen: keep the C.1 formula as written — no AI fixed-cost term — which makes the dominance claim unconditional and stronger). The original ordering (largest crossover at β=.9/δ=1.1) was also reversed by the correction. No constant was tuned to fit; the prose was brought to the code.

## Dependencies

`numpy` (both scripts), `matplotlib` (`cost_asymmetry_crossover.py` only). No network access, no API keys, no data files.

---

*Last updated: 2026-06-21 — added `cost_asymmetry_simulation.py` (the Appendix C grid harness previously deferred to v1.1.0); Appendix C now aligned to it (12/12). `cost_asymmetry_crossover.py` is a separate illustrative figure script (single visible parameter set), not the source of any reported value.*
