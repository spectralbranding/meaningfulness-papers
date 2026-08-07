"""Unit tests for the 2026bk measurement primitives.

Each statistic is checked against a case worked by hand, so that a specimen
result is never the first time the estimator has been exercised.

Run: uv run --with pytest --with numpy python -m pytest code/tests -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import metrics_lib as M  # noqa: E402

TEXT = (
    "The notorious conjecture can be stated concretely. We first rebase the "
    "statement to an equivalent affine form. A brief calculation verifies the "
    "determinant is constant, which appears like a massive miracle."
)


# --- span location ---------------------------------------------------------


def test_locate_span_exact():
    start, end = M.locate_span(
        "rebase the statement to an equivalent affine form", TEXT
    )
    assert TEXT[start:end].startswith("rebase the statement")


def test_locate_span_whitespace_insensitive():
    assert (
        M.locate_span("A brief   calculation\nverifies the determinant", TEXT)
        is not None
    )


def test_locate_span_fuzzy_tolerates_a_light_reflow():
    # One word changed inside a long quotation: above the 0.90 ratio.
    assert (
        M.locate_span("The notorious conjecture can be stated concisely.", TEXT)
        is not None
    )


def test_locate_span_rejects_an_absent_quotation():
    assert (
        M.locate_span("a claim that does not appear anywhere in this text", TEXT)
        is None
    )


# --- node matching ---------------------------------------------------------


def test_match_by_span_is_one_to_one_and_takes_the_best_overlap():
    a = {"a1": (0, 100), "a2": (200, 300)}
    b = {"b1": (10, 105), "b2": (205, 295), "b3": (0, 90)}
    pairs = M.match_by_span(a, b)
    assert sorted((x, y) for x, y, _ in pairs) == [("a1", "b3"), ("a2", "b2")]


def test_match_by_span_drops_pairs_below_threshold():
    assert M.match_by_span({"a1": (0, 100)}, {"b1": (95, 200)}) == []


# --- Layer 1 ---------------------------------------------------------------


def test_alpha_is_one_on_perfect_agreement():
    pairs = [("p", "p"), ("m", "m"), ("e", "e"), ("p", "p")]
    assert M.krippendorff_alpha_nominal(pairs) == pytest.approx(1.0)


def test_alpha_matches_the_hand_worked_case():
    # Three items agreed, one disagreed; worked out to 1 - 14/30.
    pairs = [("a", "a"), ("a", "a"), ("b", "b"), ("a", "b")]
    assert M.krippendorff_alpha_nominal(pairs) == pytest.approx(1 - 14 / 30)


def test_alpha_is_negative_when_coders_systematically_disagree():
    pairs = [("a", "b"), ("b", "a"), ("a", "b"), ("b", "a")]
    assert M.krippendorff_alpha_nominal(pairs) < 0


# --- Layer 2 ---------------------------------------------------------------


def test_triple_f1_on_a_known_overlap():
    ta = {("n1", "depends_on", "n2"), ("n2", "derives", "n3")}
    tb = {("n1", "depends_on", "n2"), ("n3", "supports", "n1")}
    assert M.triple_f1(ta, tb) == pytest.approx(0.5)


def test_triple_f1_is_zero_without_overlap():
    assert M.triple_f1({("a", "t", "b")}, {("b", "t", "a")}) == 0.0


def test_triples_ignore_nodes_outside_the_agreed_set():
    graph = {
        "nodes": [{"id": "x1"}, {"id": "x2"}, {"id": "x3"}],
        "edges": [
            {"from": "x1", "to": "x2", "type": "depends_on"},
            {"from": "x1", "to": "x3", "type": "depends_on"},
        ],
    }
    assert M.triples(graph, {"x1": "m1", "x2": "m2"}) == {("m1", "depends_on", "m2")}


def test_null_is_low_for_sparse_graphs_over_many_nodes():
    nodes = [f"m{i}" for i in range(20)]
    ta = {("m0", "depends_on", "m1"), ("m1", "depends_on", "m2")}
    tb = {("m3", "depends_on", "m4"), ("m5", "depends_on", "m6")}
    null = M.random_graph_null(ta, tb, nodes, draws=500, seed=1)
    assert null["mean"] < 0.05
    assert null["p99"] <= 0.5


def test_null_is_deterministic_under_the_seed():
    nodes = [f"m{i}" for i in range(8)]
    ta = {("m0", "depends_on", "m1")}
    tb = {("m2", "depends_on", "m3")}
    first = M.random_graph_null(ta, tb, nodes, draws=200, seed=7)
    second = M.random_graph_null(ta, tb, nodes, draws=200, seed=7)
    assert first == second


# --- M3 --------------------------------------------------------------------

CHAIN = {
    "nodes": [{"id": "n1"}, {"id": "n2"}, {"id": "n3"}, {"id": "n4"}],
    "edges": [
        {"from": "n1", "to": "n2", "type": "depends_on"},
        {"from": "n2", "to": "n3", "type": "depends_on"},
        {"from": "n4", "to": "n3", "type": "depends_on"},
    ],
}


def test_support_mass_counts_transitive_dependents():
    sm = M.support_mass(CHAIN)
    assert sm == {"n1": 0, "n2": 1, "n3": 3, "n4": 0}


def test_support_mass_survives_a_cycle():
    cyclic = {
        "nodes": [{"id": "a"}, {"id": "b"}],
        "edges": [
            {"from": "a", "to": "b", "type": "depends_on"},
            {"from": "b", "to": "a", "type": "depends_on"},
        ],
    }
    assert M.support_mass(cyclic) == {"a": 1, "b": 1}


def test_reverse_pagerank_ranks_the_most_depended_upon_node_first():
    pr = M.reverse_pagerank(CHAIN)
    assert max(pr, key=pr.get) == "n3"


def test_spearman_is_one_on_a_monotone_pair():
    rho, n = M.spearman([1, 2, 3, 4], [10, 20, 30, 40])
    assert rho == pytest.approx(1.0)
    assert n == 4


# --- counting rules --------------------------------------------------------


def test_prose_mass_counts_each_math_expression_once():
    pm = M.prose_mass("we set $x^2 + y^2 = z^2$ and then conclude")
    assert pm["math_tokens"] == 1
    assert pm["words_math_collapsed"] == 6  # we set MATHTOKEN and then conclude
    assert pm["words_raw"] > pm["words_math_collapsed"]


def test_miracle_count_counts_only_the_third_class():
    graph = {
        "nodes": [
            {"id": "a", "explanatory_status": "miracle"},
            {"id": "b", "explanatory_status": "verified_only"},
            {"id": "c", "explanatory_status": "miracle"},
            {"id": "d", "explanatory_status": "derived"},
        ]
    }
    assert M.miracle_count(graph) == 2
    assert M.status_counts(graph) == {"derived": 1, "verified_only": 1, "miracle": 2}


# --- response parsing (mathematical specimens) -----------------------------


def test_parse_repairs_latex_escapes_that_break_json():
    """A verbatim span quoting mathematics is not valid JSON as emitted."""
    import json as _json
    import sys as _sys
    from pathlib import Path as _Path

    _sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
    import spine_lib as L

    raw = r'{"nodes": [{"id": "n1", "span": "the Jacobian \det DF is constant"}], "edges": []}'
    graph = L.parse_json_block(raw)
    assert graph["nodes"][0]["span"] == r"the Jacobian \det DF is constant"
    # Unicode escapes and control escapes not followed by a letter are honoured.
    assert L.parse_json_block(r'{"a": "é", "b": "line\n break"}') == {
        "a": "é",
        "b": "line\n break",
    }
    assert isinstance(_json.dumps(graph), str)


def test_parse_does_not_corrupt_already_valid_escapes():
    """The repair consumes a valid escape whole and keeps LaTeX macros intact."""
    import sys as _sys
    from pathlib import Path as _Path

    _sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
    import spine_lib as L

    # An already-escaped backslash pair must survive; a naive repair breaks it.
    graph = L.parse_json_block(
        r'{"nodes": [{"id": "n1", "span": "C:\\\\tmp"}], "edges": []}'
    )
    assert graph["nodes"][0]["span"] == "C:" + chr(92) + chr(92) + "tmp"

    # `\b` and `\f` are valid JSON escapes but open LaTeX macros here; reading
    # them as control characters would eat the macro's first letter.
    graph = L.parse_json_block(
        r'{"nodes": [{"id": "n1", "span": "we set \binom{n}{2} and \frac{1}{2}"}], "edges": []}'
    )
    assert graph["nodes"][0]["span"] == r"we set \binom{n}{2} and \frac{1}{2}"

    # A control escape not followed by a letter is still a control character.
    assert L.parse_json_block(r'{"a": "one\n two"}') == {"a": "one\n two"}
