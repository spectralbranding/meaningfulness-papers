#!/usr/bin/env python3
"""The coefficients this study reports, and nothing else.

Every function here returns the full marginal picture beside the coefficient
(M4b): the 2x2 cells, both raw agreement and expected agreement, both marginals,
the prevalence index and F1. A chance-corrected number reported alone is what
this paper criticises elsewhere.

The chance model is the observed-marginal one throughout, kept rather than
replaced (M4b): the depression it produces under skewed base rates is the
coefficient reporting correctly.

Pure functions on data structures. No network, no provider, no protocol.
"""

from __future__ import annotations

import random
from itertools import combinations


def cohen_kappa_binary(a: set, b: set, universe: set) -> dict:
    """Selection agreement over a shared index set, with its whole 2x2 picture."""
    n = len(universe)
    a, b = a & universe, b & universe
    both = len(a & b)
    neither = n - len(a | b)
    only_a, only_b = len(a - b), len(b - a)
    po = (both + neither) / n if n else 0.0
    pa, pb = (len(a) / n if n else 0.0), (len(b) / n if n else 0.0)
    pe = pa * pb + (1 - pa) * (1 - pb)
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    denom = 2 * both + only_a + only_b
    return {
        "n": n,
        "both": both,
        "neither": neither,
        "only_a": only_a,
        "only_b": only_b,
        "raw_agreement": po,
        "expected_agreement": pe,
        "kappa": kappa,
        "marginal_a": pa,
        "marginal_b": pb,
        # Byrt's prevalence index: the observed one, now that the data exist.
        "prevalence_index": abs(both - neither) / n if n else 0.0,
        "bias_index": abs(only_a - only_b) / n if n else 0.0,
        "f1": (2 * both / denom) if denom else 0.0,
    }


def cohen_kappa_nominal(pairs: list[tuple[str, str]], categories: list[str]) -> dict:
    """Typing agreement over the units both operators selected (M4's conditioning).

    `pairs` are (label_a, label_b) for each jointly selected unit -- positions
    no one selected are not locations at all and are not scored, which is the
    published two-stage rule this design applies.
    """
    n = len(pairs)
    if n == 0:
        return {
            "n": 0,
            "kappa": None,
            "raw_agreement": None,
            "note": "no jointly selected units",
        }
    agree = sum(1 for x, y in pairs if x == y)
    po = agree / n
    ca = {c: sum(1 for x, _ in pairs if x == c) / n for c in categories}
    cb = {c: sum(1 for _, y in pairs if y == c) / n for c in categories}
    pe = sum(ca[c] * cb[c] for c in categories)
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return {
        "n": n,
        "agree": agree,
        "raw_agreement": po,
        "expected_agreement": pe,
        "kappa": kappa,
        "marginals_a": ca,
        "marginals_b": cb,
    }


def triple_f1(a: set, b: set) -> dict:
    """Typed triple overlap -- the gold-free graph-annotation statistic.

    Reported as F1 over (from, to, type) triples, which is what the reference
    class this design imports its threshold from reports.
    """
    shared = len(a & b)
    p = shared / len(a) if a else 0.0
    r = shared / len(b) if b else 0.0
    f1 = (2 * p * r / (p + r)) if (p + r) else 0.0
    return {
        "triples_a": len(a),
        "triples_b": len(b),
        "shared": shared,
        "precision": p,
        "recall": r,
        "f1": f1,
    }


def mean(xs: list[float]) -> float | None:
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def pairwise(values: dict[int, object]) -> list[tuple[object, object]]:
    """Every unordered pair of repetitions, for a within-operator baseline."""
    keys = sorted(values)
    return [(values[i], values[j]) for i, j in combinations(keys, 2)]


def separation_test(
    between: list[float],
    within: list[float],
    seed: int,
    *,
    permutations: int = 10000,
    bootstrap: int = 10000,
    alpha: float = 0.05,
) -> dict:
    """P2's test: is the between-operator number separated below the noise floor?

    The statistic is mean(within) - mean(between): positive means the operators
    agree with each other LESS than each agrees with itself, which is the
    direction that would say a real disagreement is present rather than run-to-
    run variance. A paired permutation gives the p-value; a bootstrap gives the
    interval. Both streams are seeded from a stable digest of the cell, never
    from a process hash, so a re-run reproduces the interval.
    """
    between = [x for x in between if x is not None]
    within = [x for x in within if x is not None]
    if not between or not within:
        return {
            "note": "not computable",
            "n_between": len(between),
            "n_within": len(within),
        }

    observed = mean(within) - mean(between)
    pool = between + within
    n_b = len(between)
    rng = random.Random(seed)
    hits = 0
    for _ in range(permutations):
        shuffled = pool[:]
        rng.shuffle(shuffled)
        stat = mean(shuffled[n_b:]) - mean(shuffled[:n_b])
        if abs(stat) >= abs(observed):
            hits += 1
    p_value = (hits + 1) / (permutations + 1)

    rng_b = random.Random(seed ^ 0x5EED)
    diffs = []
    for _ in range(bootstrap):
        rb = [between[rng_b.randrange(len(between))] for _ in between]
        rw = [within[rng_b.randrange(len(within))] for _ in within]
        diffs.append(mean(rw) - mean(rb))
    diffs.sort()
    lo = diffs[int((alpha / 2) * bootstrap)]
    hi = diffs[min(bootstrap - 1, int((1 - alpha / 2) * bootstrap))]
    return {
        "mean_between": mean(between),
        "mean_within": mean(within),
        "difference": observed,
        "p_value": p_value,
        "ci_low": lo,
        "ci_high": hi,
        "interval_includes_zero": lo <= 0 <= hi,
        "separated": (p_value < alpha) and not (lo <= 0 <= hi),
        "permutations": permutations,
        "bootstrap": bootstrap,
        "alpha": alpha,
        "seed": seed,
    }
