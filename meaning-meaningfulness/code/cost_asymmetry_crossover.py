"""
Cost-asymmetry crossover chart for Zharnikov (2026ao)
=====================================================
Companion computation script for the cost-asymmetry result in:
  "Spec-Based Research in the Post-AI Era"
  DOI: 10.5281/zenodo.20409683

Run command:
    python cost_asymmetry_crossover.py
    # or:
    uv run python cost_asymmetry_crossover.py

Expected outputs (written to same directory as this script):
    cost_asymmetry_crossover.png  — 300 dpi, 1600x1000 px publication-quality raster
    cost_asymmetry_crossover.svg  — vector, same chart

Crossover x-coordinate is printed to stdout for paper reproducibility
(per PAPER_QUALITY_STANDARDS items 37a-37e numerical alignment).

Companion Computation
---------------------
This script implements the P3 cost-asymmetry result from Section 3 of
the working paper. Parameters are set as named constants at the top of
the file. The crossover is the unique x* where c_AI(x*) = c_human(x*),
solved analytically as x* = (gamma / alpha) ** (1 / (beta - delta)).

Suggested public mirror path (spectralbranding/meaningfulness-papers):
    meaningfulness-papers/meaning-meaningfulness/code/cost_asymmetry_crossover.py
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# Parameters — all values are CONSTANTS; edit here to reproduce variants
# ---------------------------------------------------------------------------

ALPHA = 1.0  # AI cost scale factor
BETA = 0.7  # AI cost exponent  (sub-linear:  beta  < 1)

GAMMA = 0.05  # Human cost scale factor
DELTA = 1.4  # Human cost exponent (super-linear: delta > 1)

# Asymmetry condition: BETA < 1 < DELTA  (must hold; script asserts this)
assert (
    BETA < 1 < DELTA
), f"Asymmetry condition violated: need beta<1<delta, got {BETA}, {DELTA}"

# Plot range (artifact size, on log scale)
X_MIN = 1.0
X_MAX = 1000.0
N_POINTS = 2000

# DPI and figure size
DPI = 300
FIG_WIDTH_IN = 1600 / DPI  # ~5.33 in (will be saved at 300 dpi → 1600 px wide)
FIG_HEIGHT_IN = 1000 / DPI  # ~3.33 in

# Override to standard publication-friendly inches; matplotlib saves at DPI so
# final pixel count = inches * DPI.  12 x 7.5 in @ 300 dpi = 3600 x 2250 px.
FIG_WIDTH_IN = 12.0
FIG_HEIGHT_IN = 7.5

# Y-axis display range (on log scale; keep curves visible without extreme tails)
Y_MIN = 0.01
Y_MAX = 400.0

# SBT-canonical color palette
COLOR_AI = "#14B8A6"  # teal
COLOR_HUMAN = "#F59E0B"  # amber
COLOR_GRID = "#0A0A10"  # near-black, used at 20% opacity
COLOR_SHADE_AI = "#14B8A6"
COLOR_SHADE_HUMAN = "#F59E0B"
COLOR_CROSSOVER = "#6366F1"  # indigo — distinct from both curves

BACKGROUND = "white"

# ---------------------------------------------------------------------------
# Analytic crossover solution
# ---------------------------------------------------------------------------


def crossover_x(alpha, beta, gamma, delta):
    """Return x* where alpha * x^beta == gamma * x^delta.

    Derivation:
        alpha * x^beta = gamma * x^delta
        (alpha / gamma) = x^(delta - beta)
        x* = (alpha / gamma) ^ (1 / (delta - beta))
    """
    exponent = 1.0 / (delta - beta)
    x_star = (alpha / gamma) ** exponent
    return x_star


def c_ai(x, alpha=ALPHA, beta=BETA):
    return alpha * np.power(x, beta)


def c_human(x, gamma=GAMMA, delta=DELTA):
    return gamma * np.power(x, delta)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    x_star = crossover_x(ALPHA, BETA, GAMMA, DELTA)
    y_star = c_ai(x_star)  # == c_human(x_star) by definition

    # Print to stdout for reproducibility record
    print(f"Crossover x-coordinate: {x_star:.4f}")
    print(f"Crossover y-coordinate (cost): {y_star:.4f}")
    print(f"Parameters: alpha={ALPHA}, beta={BETA}, gamma={GAMMA}, delta={DELTA}")

    x = np.logspace(np.log10(X_MIN), np.log10(X_MAX), N_POINTS)
    y_ai = c_ai(x)
    y_human = c_human(x)

    # ---------------------------------------------------------------------------
    # Figure
    # ---------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN), facecolor=BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    # Set explicit axis limits BEFORE drawing shaded regions + labels
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)

    # Shaded regions (use finite Y_MIN so fill_between works on log scale)
    ax.fill_between(
        x,
        Y_MIN,
        np.maximum(y_ai, y_human),
        where=(x < x_star),
        color=COLOR_SHADE_HUMAN,
        alpha=0.10,
        zorder=1,
    )
    ax.fill_between(
        x,
        Y_MIN,
        np.maximum(y_ai, y_human),
        where=(x >= x_star),
        color=COLOR_SHADE_AI,
        alpha=0.10,
        zorder=1,
    )

    # Zone labels — use axes-fraction coordinates so placement is stable
    ax.text(
        0.18,
        0.12,  # left zone, lower portion
        "Human-projection\nefficient zone",
        fontsize=11,
        color=COLOR_HUMAN,
        fontweight="bold",
        ha="center",
        va="bottom",
        transform=ax.transAxes,
        zorder=5,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=3),
    )
    ax.text(
        0.78,
        0.12,  # right zone, lower portion
        "AI-projection\nefficient zone",
        fontsize=11,
        color=COLOR_AI,
        fontweight="bold",
        ha="center",
        va="bottom",
        transform=ax.transAxes,
        zorder=5,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=3),
    )

    # Cost curves
    ax.plot(
        x,
        y_ai,
        color=COLOR_AI,
        linewidth=2.8,
        label="AI verification cost  (scales sub-linearly)",
        zorder=4,
    )
    ax.plot(
        x,
        y_human,
        color=COLOR_HUMAN,
        linewidth=2.8,
        label="Human verification cost  (scales super-linearly)",
        zorder=4,
    )

    # Crossover vertical dashed line
    ax.axvline(
        x=x_star,
        color=COLOR_CROSSOVER,
        linestyle="--",
        linewidth=1.8,
        zorder=3,
        alpha=0.85,
    )

    # Crossover annotation
    ax.annotate(
        f"Crossover\nhuman cost exceeds AI cost\n(artifact size ≈ {x_star:.0f})",
        xy=(x_star, y_star),
        xytext=(x_star * 2.2, y_star * 2.0),
        fontsize=10,
        color=COLOR_CROSSOVER,
        fontweight="bold",
        ha="left",
        arrowprops=dict(
            arrowstyle="->",
            color=COLOR_CROSSOVER,
            lw=1.5,
        ),
        zorder=6,
        bbox=dict(
            facecolor="white",
            edgecolor=COLOR_CROSSOVER,
            alpha=0.85,
            boxstyle="round,pad=0.4",
            linewidth=1.2,
        ),
    )

    # Crossover dot
    ax.scatter([x_star], [y_star], color=COLOR_CROSSOVER, s=80, zorder=7)

    # Grid
    ax.grid(True, which="both", color=COLOR_GRID, alpha=0.18, linewidth=0.7)
    ax.set_axisbelow(True)

    # Axis labels
    ax.set_xlabel(
        "Artifact size  (tokens, propositions, or structural units — log scale)",
        fontsize=13,
        labelpad=10,
    )
    ax.set_ylabel(
        "Verification cost  (relative, log scale)",
        fontsize=13,
        labelpad=10,
    )

    # Legend
    legend_handles = [
        Line2D(
            [0],
            [0],
            color=COLOR_AI,
            linewidth=2.8,
            label="AI verification cost  (sub-linear, β < 1)",
        ),
        Line2D(
            [0],
            [0],
            color=COLOR_HUMAN,
            linewidth=2.8,
            label="Human verification cost  (super-linear, δ > 1)",
        ),
        Line2D(
            [0],
            [0],
            color=COLOR_CROSSOVER,
            linestyle="--",
            linewidth=1.8,
            label="Crossover point",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper left",
        fontsize=11,
        framealpha=0.9,
        edgecolor="#cccccc",
    )

    # Title and subtitle
    fig.text(
        0.5,
        0.97,
        "AI vs human verification cost — the crossover",
        ha="center",
        va="top",
        fontsize=16,
        fontweight="bold",
        color="#0A0A10",
    )
    fig.text(
        0.5,
        0.935,
        "Cost-asymmetry result from Spec-Based Research in the Post-AI Era"
        "  (DOI: 10.5281/zenodo.20409683)",
        ha="center",
        va="top",
        fontsize=10,
        color="#444444",
        style="italic",
    )

    # Adjust subplot margins to accommodate suptitle
    plt.subplots_adjust(top=0.88, bottom=0.10, left=0.09, right=0.97)

    # ---------------------------------------------------------------------------
    # Save outputs
    # ---------------------------------------------------------------------------
    script_dir = os.path.dirname(os.path.abspath(__file__))
    png_path = os.path.join(script_dir, "cost_asymmetry_crossover.png")
    svg_path = os.path.join(script_dir, "cost_asymmetry_crossover.svg")

    fig.savefig(png_path, dpi=DPI, bbox_inches="tight", facecolor=BACKGROUND)
    fig.savefig(svg_path, bbox_inches="tight", facecolor=BACKGROUND)

    print(f"Saved: {png_path}")
    print(f"Saved: {svg_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
