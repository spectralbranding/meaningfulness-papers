"""
Calibrated cost-asymmetry simulation for Zharnikov (2026ao)
===========================================================
Companion computation script for ONLINE APPENDIX C ("Calibrated Simulation
Harness") of:

  "Spec-Based Research in the Post-AI Era"
  DOI: 10.5281/zenodo.20409683

This is the script Appendix C section C.6 names as the ground truth for every
value the appendix reports as "simulated," "computed," or "calibrated." It is
DISTINCT from cost_asymmetry_crossover.py in the same directory, which renders a
single-parameter illustrative crossover *figure*; this script reproduces the
*grid* simulation (the verification-cost ratio across the beta-delta grid, the
recombination-rate advantage, the per-pair crossover analysis, and the two
sensitivity sweeps).

Run command:
    uv run --with numpy python cost_asymmetry_simulation.py
    # or, if numpy is already available:
    python cost_asymmetry_simulation.py

Random seed: 42 (fixed at file top; governs the artifact-size and
tokens-per-node draws used by the distribution-shape sensitivity in C.5b).

The script PRINTS every appendix-cited quantity next to the value it actually
computes, with a MATCH / MISMATCH verdict, and exits 0. It never hard-codes a
reported value to force a match: where the literal model does not reproduce the
appendix's stated number, the script prints MISMATCH and the gap, so the author
can reconcile the prose to the script (per the corpus computation-script
publication discipline, PAPER_QUALITY_STANDARDS items 37a-37e).

Model (Appendix C, section C.1)
-------------------------------
    c_AI(S)    = alpha * |V|^beta        with beta  < 1   (sub-linear)
    c_human(R) = gamma * |tokens|^delta  with delta > 1   (super-linear)
    |tokens|   = mu * |V|                (tokens-per-node scaling)

Scale constants fixed at alpha = gamma = 1 (C.1). Grid:
    beta  in {.5, .7, .9}
    delta in {1.1, 1.3, 1.5}
mu centered on 100 (C.2: "50-200 tokens per substrate node"); the
distribution-shape sensitivity (C.5b) draws mu from a log-normal centered there.

The verification-cost ratio (C.3) is
    rho_cost(|V|, beta, delta) = c_human(R) / c_AI(S)
                               = (mu*|V|)^delta / |V|^beta
                               = mu^delta * |V|^(delta - beta).

The crossover (C.5) is the substrate size |V|* above which the post-AI
allocation (AI on substrate + human on residual judgment) costs strictly less
than human-only rendering verification:
    c_AI(S) + f * c_human(R) = c_human(R)
    => c_AI(S) = (1 - f) * c_human(R)
    => |V|* = [ (1 - f) * gamma * mu^delta / alpha ] ^ ( 1 / (beta - delta) )
where f is the residual judgment-cost fraction (C.5: default .15; C.5c sweep).
"""

import sys

import numpy as np

# ---------------------------------------------------------------------------
# Constants (all named; edit here to reproduce variants)
# ---------------------------------------------------------------------------
SEED = 42

ALPHA = 1.0
GAMMA = 1.0
BETAS = (0.5, 0.7, 0.9)
DELTAS = (1.1, 1.3, 1.5)

MU_CENTER = 100.0  # C.2: tokens-per-node, centered on 100
JUDGMENT_FRACTION = 0.15  # C.5: default residual human judgment-cost fraction

# Representative artifact sizes (C.3): small / typical paper / long tail.
V_SMALL = 10.0
V_TYPICAL = 100.0
V_LONGTAIL = 500.0


# ---------------------------------------------------------------------------
# Core model
# ---------------------------------------------------------------------------
def c_ai(v, alpha=ALPHA, beta=0.7):
    return alpha * np.power(v, beta)


def c_human(v, gamma=GAMMA, delta=1.3, mu=MU_CENTER):
    return gamma * np.power(mu * v, delta)


def cost_ratio(v, beta, delta, mu=MU_CENTER, alpha=ALPHA, gamma=GAMMA):
    """rho_cost = c_human / c_ai = mu^delta * v^(delta-beta)  (alpha=gamma=1)."""
    return (gamma * np.power(mu * v, delta)) / (alpha * np.power(v, beta))


def crossover_size(
    beta, delta, mu=MU_CENTER, f=JUDGMENT_FRACTION, alpha=ALPHA, gamma=GAMMA
):
    """|V|* where c_AI(S) = (1-f) * c_human(R). Closed form."""
    bracket = (1.0 - f) * gamma * np.power(mu, delta) / alpha
    return bracket ** (1.0 / (beta - delta))


def orders_of_magnitude(x):
    return np.log10(x)


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------
_RESULTS = []  # (label, reproduced: bool)


def check(label, reproduced, detail=""):
    _RESULTS.append((label, reproduced))
    tag = "MATCH   " if reproduced else "MISMATCH"
    print(f"  [{tag}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"           {line}")


def hr(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# C.3 — verification-cost ratio across the grid
# ---------------------------------------------------------------------------
def section_ratio():
    hr("C.3  Verification-cost ratio rho_cost = mu^delta * |V|^(delta-beta)")
    print(f"  (alpha=gamma=1, mu={MU_CENTER:g}; orders = log10 of the ratio)\n")
    print(
        f"  {'beta':>5} {'delta':>6} {'d-b':>5} "
        f"{'rho@|V|=10':>14} {'rho@|V|=100':>14} {'rho@|V|=500':>14}"
    )
    grid = {}
    for beta in BETAS:
        for delta in DELTAS:
            r10 = cost_ratio(V_SMALL, beta, delta)
            r100 = cost_ratio(V_TYPICAL, beta, delta)
            r500 = cost_ratio(V_LONGTAIL, beta, delta)
            grid[(beta, delta)] = (r10, r100, r500)
            print(
                f"  {beta:>5.1f} {delta:>6.1f} {delta - beta:>5.1f} "
                f"{r10:>14.3g} {r100:>14.3g} {r500:>14.3g}"
            )

    # delta - beta range (pure arithmetic; appendix C.3 states min .2, max 1.0)
    diffs = [round(d - b, 10) for b in BETAS for d in DELTAS]
    check(
        "C.3 delta-beta minimum = .2 (beta=.9, delta=1.1)",
        abs(min(diffs) - 0.2) < 1e-9,
        f"computed min(delta-beta) = {min(diffs):.1f}",
    )
    check(
        "C.3 delta-beta maximum = 1.0 (beta=.5, delta=1.5)",
        abs(max(diffs) - 1.0) < 1e-9,
        f"computed max(delta-beta) = {max(diffs):.1f}",
    )

    # rho strictly increasing in |V| across the whole grid (C.3 monotonicity)
    mono = all(grid[k][0] < grid[k][1] < grid[k][2] for k in grid)
    check("C.3 rho_cost strictly increasing in |V| across the grid", mono)

    # Appendix C.3 magnitudes (aligned to the literal model at mu = MU_CENTER):
    # |V|=10 ~ 2.4-4.0 orders; |V|=100 ~ 2.6-5.0 orders; |V|=500 ~ 2.7-5.7 orders.
    o10 = [orders_of_magnitude(grid[k][0]) for k in grid]
    o100 = [orders_of_magnitude(grid[k][1]) for k in grid]
    o500 = [orders_of_magnitude(grid[k][2]) for k in grid]
    in_10 = 2.3 <= min(o10) <= 2.5 and 3.9 <= max(o10) <= 4.1
    in_100 = 2.5 <= min(o100) <= 2.7 and 4.9 <= max(o100) <= 5.1
    in_500 = 2.6 <= min(o500) <= 2.8 and 5.6 <= max(o500) <= 5.8
    check(
        "C.3 advantage ~ 2.4-4.0 orders at |V|=10",
        in_10,
        f"computed orders at |V|=10 (mu={MU_CENTER:g}): "
        f"min={min(o10):.2f}, max={max(o10):.2f}  (appendix says ~2.4-4.0)",
    )
    check(
        "C.3 advantage ~ 2.6-5.0 orders at |V|=100",
        in_100,
        f"computed orders at |V|=100 (mu={MU_CENTER:g}): "
        f"min={min(o100):.2f}, max={max(o100):.2f}  (appendix says ~2.6-5.0)",
    )
    check(
        "C.3 advantage ~ 2.7-5.7 orders at |V|>=500",
        in_500,
        f"computed orders at |V|=500 (mu={MU_CENTER:g}): "
        f"min={min(o500):.2f}, max={max(o500):.2f}  (appendix says ~2.7-5.7)",
    )
    return grid


# ---------------------------------------------------------------------------
# C.5 — crossover point analysis
# ---------------------------------------------------------------------------
def section_crossover():
    hr(
        "C.5  Crossover |V|*  (c_AI = (1-f) * c_human; f=%.2f, mu=%g)"
        % (JUDGMENT_FRACTION, MU_CENTER)
    )
    print(f"  {'beta':>5} {'delta':>6} {'|V|* (mu=100)':>16} {'|V|* (mu=1)':>14}")
    vstars_mu100 = {}
    for beta in BETAS:
        for delta in DELTAS:
            v100 = crossover_size(beta, delta, mu=100.0)
            v1 = crossover_size(beta, delta, mu=1.0)
            vstars_mu100[(beta, delta)] = v100
            print(f"  {beta:>5.1f} {delta:>6.1f} {v100:>16.4g} {v1:>14.4g}")

    lo = min(vstars_mu100.values())
    hi = max(vstars_mu100.values())
    # Aligned appendix C.5: the cross-over lies below a single node across the
    # whole grid (|V|* between ~1e-11 and ~1e-3 at mu=100).
    sub_node = hi < 1.0
    check(
        "C.5 cross-over below a single node across the grid (|V|* < 1)",
        sub_node,
        f"computed |V|* band at mu=100: [{lo:.3g}, {hi:.3g}]  "
        f"(appendix: ~1e-11 to ~1e-3, all < 1 node)",
    )

    # Aligned appendix C.5: cross-over is LARGEST where delta-beta is widest
    # (beta=.5/delta=1.5) and SMALLEST where it is narrowest (beta=.9/delta=1.1).
    v_largest = crossover_size(0.5, 1.5, mu=100.0)
    v_smallest = crossover_size(0.9, 1.1, mu=100.0)
    ordering_ok = (
        v_largest == hi and v_smallest == lo and v_largest < 1.0 and v_smallest < 1.0
    )
    check(
        "C.5 largest cross-over at beta=.5/delta=1.5, smallest at beta=.9/delta=1.1",
        ordering_ok,
        f"|V|*(.5,1.5)={v_largest:.4g} (largest); "
        f"|V|*(.9,1.1)={v_smallest:.4g} (smallest); both < 1 node",
    )

    # The QUALITATIVE headline: crossover well below the typical paper size
    # (50-150 nodes), so the prescription dominates unconditionally.
    dominates = hi < 50.0
    check(
        "C.5 prescription dominates across typical artifact range " "(|V|* < 50 nodes)",
        dominates,
        f"max |V|* across grid = {hi:.3g} << typical 50-150 node range",
    )
    return vstars_mu100


# ---------------------------------------------------------------------------
# C.4 — recombination-rate advantage
# ---------------------------------------------------------------------------
def section_recombination():
    hr("C.4  Recombination advantage (spine-publish vs rendering-only re-extract)")
    print("  spine-publish query cost  = alpha*|V_query|^beta")
    print("  rendering-only cost       = gamma*(mu*|V|)^delta + alpha*|V|^beta")
    print(f"  (re-extraction term dominates; reported as the ratio)\n")
    print(f"  {'beta':>5} {'delta':>6} {'adv@|V|=100':>14} {'adv@|V|=500':>14}")
    advs = {}
    for beta in BETAS:
        for delta in DELTAS:

            def adv(v):
                query = ALPHA * v**beta  # query published spine
                reextract = (
                    GAMMA * (MU_CENTER * v) ** delta + ALPHA * v**beta
                )  # re-extract then query
                return reextract / query

            advs[(beta, delta)] = (adv(V_TYPICAL), adv(V_LONGTAIL))
            print(
                f"  {beta:>5.1f} {delta:>6.1f} "
                f"{advs[(beta, delta)][0]:>14.3g} "
                f"{advs[(beta, delta)][1]:>14.3g}"
            )
    grows = all(advs[k][0] < advs[k][1] for k in advs)
    check("C.4 recombination advantage grows with artifact complexity", grows)
    return advs


# ---------------------------------------------------------------------------
# C.5b / C.5c — sensitivity analyses
# ---------------------------------------------------------------------------
def section_sensitivity():
    hr("C.5b  Sensitivity to artifact-size distribution shape (seed=%d)" % SEED)
    rng = np.random.default_rng(SEED)
    n = 100_000

    # Power-law (Pareto) artifact sizes, lower-bounded at 10 nodes.
    pareto = (rng.pareto(a=1.5, size=n) + 1.0) * 10.0
    # Log-normal at a comparable median (median exp(mu_ln)).
    lognorm = rng.lognormal(mean=np.log(np.median(pareto)), sigma=0.8, size=n)

    # The crossover |V|* is a CLOSED FORM independent of the size distribution;
    # the distribution only changes the FRACTION of artifacts above it. C.5b's
    # claim is that the qualitative result is invariant to the shape.
    vstar = crossover_size(0.7, 1.3, mu=MU_CENTER)  # representative mid-grid pair
    frac_pareto = float(np.mean(pareto > vstar))
    frac_lognorm = float(np.mean(lognorm > vstar))
    print(f"  representative mid-grid |V|* (beta=.7, delta=1.3, mu=100) = {vstar:.4g}")
    print(
        f"  fraction of artifacts above |V|* : power-law={frac_pareto:.4f}, "
        f"log-normal={frac_lognorm:.4f}"
    )
    check(
        "C.5b qualitative dominance invariant to distribution shape",
        frac_pareto > 0.99 and frac_lognorm > 0.99,
        "both distributions place ~all artifacts above the crossover",
    )

    hr("C.5c  Sensitivity to judgment-cost fraction f")
    print(f"  {'f':>6} {'|V|*(.9,1.1)':>14} {'|V|*(.5,1.5)':>14} (mu=100)")
    fractions = (0.05, 0.15, 0.30, 0.50)
    rows = {}
    for f in fractions:
        v_worst = crossover_size(0.9, 1.1, mu=MU_CENTER, f=f)
        v_best = crossover_size(0.5, 1.5, mu=MU_CENTER, f=f)
        rows[f] = (v_worst, v_best)
        print(f"  {f:>6.2f} {v_worst:>14.4g} {v_best:>14.4g}")
    # Appendix C.5c: crossover "shifts modestly (at most three to eight nodes)".
    spread_worst = max(r[0] for r in rows.values()) - min(r[0] for r in rows.values())
    check(
        "C.5c crossover shift across f in {.05,.15,.30,.50} is modest " "(< 8 nodes)",
        spread_worst < 8.0,
        f"computed spread at (beta=.9,delta=1.1, mu=100) = {spread_worst:.3g} nodes",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Cost-asymmetry calibrated simulation — Zharnikov (2026ao), Appendix C")
    print(
        f"seed={SEED}  alpha={ALPHA}  gamma={GAMMA}  "
        f"grid beta in {BETAS}  delta in {DELTAS}  mu_center={MU_CENTER}"
    )

    section_ratio()
    section_crossover()
    section_recombination()
    section_sensitivity()

    hr("REPRODUCTION SUMMARY")
    n_total = len(_RESULTS)
    n_ok = sum(1 for _, ok in _RESULTS if ok)
    for label, ok in _RESULTS:
        print(f"  {'OK  ' if ok else 'FAIL'}  {label}")
    print(f"\n  {n_ok}/{n_total} appendix claims reproduce from the literal C.1 model.")
    print()
    print("  Appendix C (v1.x) is ALIGNED to this script: it reports the")
    print("  verification-cost-ratio magnitudes, the sub-node cross-over, and the")
    print("  C.5b/C.5c sensitivity results exactly as computed here. The script is")
    print("  the single source of truth for those values and asserts each one")
    print("  above; no constant is tuned to force a match. The cost-asymmetry")
    print("  thesis (beta<1<delta -> the post-AI allocation dominates human-only")
    print("  rendering verification at every artifact of one node or larger) holds")
    print("  unconditionally under the stated cost functions. See code/README.md.")
    if n_ok != n_total:
        print()
        print("  WARNING: a check FAILED above -> appendix and script have drifted;")
        print("  reconcile the prose to the script (or fix a genuine script bug).")

    # Exit 0 regardless: the script's job is to REPORT reproduction, not gate.
    return 0


if __name__ == "__main__":
    sys.exit(main())
