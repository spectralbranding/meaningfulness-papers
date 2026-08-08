"""Unit tests for the coefficients. These run before anything else in the pipeline.

Each test pins a value that can be checked by hand, so a refactor that changes a
number has to change a test too.

    uv run --python 3.12 --with pytest --with pyyaml pytest code/tests -q
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import metrics_lib as M  # noqa: E402
from segment_units import apply_math_rule, is_symbolic  # noqa: E402


def test_kappa_perfect_agreement():
    universe = set(range(1, 11))
    r = M.cohen_kappa_binary({1, 2, 3}, {1, 2, 3}, universe)
    assert r["kappa"] == 1.0
    assert r["raw_agreement"] == 1.0
    assert r["f1"] == 1.0


def test_kappa_no_overlap_is_negative():
    universe = set(range(1, 11))
    r = M.cohen_kappa_binary({1, 2, 3}, {4, 5, 6}, universe)
    assert r["kappa"] < 0
    assert r["f1"] == 0.0


def test_kappa_hand_computed():
    # 10 positions: both say yes on 3, both no on 5, one each disagrees.
    r = M.cohen_kappa_binary({1, 2, 3, 4}, {1, 2, 3, 5}, set(range(1, 11)))
    assert r["both"] == 3 and r["neither"] == 5
    assert abs(r["raw_agreement"] - 0.8) < 1e-9
    # pe = .4*.4 + .6*.6 = .52 ; kappa = (.8-.52)/(1-.52)
    assert abs(r["kappa"] - (0.8 - 0.52) / 0.48) < 1e-9


def test_prevalence_index_is_byrt():
    # 9 positive agreements, 1 negative agreement -> |9-1|/10
    r = M.cohen_kappa_binary(set(range(1, 10)), set(range(1, 10)), set(range(1, 11)))
    assert abs(r["prevalence_index"] - 0.8) < 1e-9


def test_conditional_typing_scores_only_joint_units():
    pairs = [("proposition", "proposition"), ("method", "evidence")]
    r = M.cohen_kappa_nominal(pairs, ["proposition", "method", "evidence"])
    assert r["n"] == 2 and r["agree"] == 1
    empty = M.cohen_kappa_nominal([], ["proposition"])
    assert empty["kappa"] is None  # no jointly selected units is not zero agreement


def test_triple_f1():
    a = {(1, 2, "derives"), (2, 3, "supports")}
    b = {(1, 2, "derives"), (3, 4, "assumes")}
    r = M.triple_f1(a, b)
    assert r["shared"] == 1
    assert abs(r["f1"] - 0.5) < 1e-9


def test_triple_f1_is_typed():
    a = {(1, 2, "derives")}
    b = {(1, 2, "supports")}
    assert M.triple_f1(a, b)["shared"] == 0


def test_separation_test_is_seed_stable():
    between = [0.2, 0.25, 0.3, 0.22, 0.28]
    within = [0.6, 0.65, 0.62, 0.58, 0.61]
    a = M.separation_test(between, within, seed=42, permutations=500, bootstrap=500)
    b = M.separation_test(between, within, seed=42, permutations=500, bootstrap=500)
    assert a == b
    assert a["difference"] > 0
    assert not a["interval_includes_zero"]


def test_separation_test_finds_no_separation_when_identical():
    xs = [0.4, 0.42, 0.38, 0.41, 0.39]
    r = M.separation_test(xs, xs, seed=7, permutations=500, bootstrap=500)
    assert r["interval_includes_zero"]
    assert not r["separated"]


def test_math_rule_attaches_display_to_introducing_sentence():
    text = "We now show the bound. $$x^2 + y^2 = z^2$$ And we are done."
    spans = [(0, 21), (22, 42), (43, len(text))]
    out, merges = apply_math_rule(spans, text)
    assert merges == 1
    assert len(out) == 2
    assert out[0] == (0, 42)  # the display joined the sentence before it


def test_math_rule_merges_a_leading_display_forward():
    text = "$$a = b$$ Then the claim follows."
    spans = [(0, 9), (10, len(text))]
    out, merges = apply_math_rule(spans, text)
    assert merges == 1 and len(out) == 1 and out[0][0] == 0


def test_is_symbolic():
    assert is_symbolic("$$\\int_0^1 x\\,dx$$")
    assert is_symbolic("${V}$")
    assert not is_symbolic("The variety is smooth.")
