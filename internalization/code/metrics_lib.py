#!/usr/bin/env python3
"""Measurement primitives for the 2026bk run.

Every statistic the decision rule names is implemented here and nowhere else,
so the scorers cannot drift from each other. All randomness is drawn from a
generator seeded with PROTOCOL.yaml's seed.

Unit tests: code/tests/test_metrics.py -- the matcher, alpha, the triple F1 and
the null are checked against hand-worked cases before any specimen is scored.
"""

from __future__ import annotations

import difflib
import re
from collections import Counter

import numpy as np

# --- span location ---------------------------------------------------------

_WS = re.compile(r"\s+")


def _normalize(text: str) -> tuple[str, list[int]]:
    """Lowercase and collapse whitespace, keeping a map back to original offsets."""
    out: list[str] = []
    idx: list[int] = []
    prev_space = True
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev_space:
                out.append(" ")
                idx.append(i)
            prev_space = True
        else:
            out.append(ch.lower())
            idx.append(i)
            prev_space = False
    return "".join(out), idx


def locate_span(span: str, text: str, *, ratio: float = 0.90) -> tuple[int, int] | None:
    """Return (start, end) character offsets of `span` in `text`, or None.

    Exact match on the whitespace-normalized text first; a sliding fuzzy match
    at the declared ratio otherwise, which is what the protocol specifies for
    an operator that lightly reflowed a quotation.
    """
    norm_text, idx = _normalize(text)
    norm_span, _ = _normalize(span.strip())
    if not norm_span:
        return None
    pos = norm_text.find(norm_span)
    if pos >= 0:
        return idx[pos], idx[min(pos + len(norm_span), len(idx)) - 1] + 1
    n = len(norm_span)
    if n < 10 or n > len(norm_text):
        return None
    step = max(1, n // 4)
    best, best_pos = 0.0, -1
    matcher = difflib.SequenceMatcher(autojunk=False)
    matcher.set_seq2(norm_span)
    for start in range(0, len(norm_text) - n + 1, step):
        matcher.set_seq1(norm_text[start : start + n])
        if matcher.real_quick_ratio() < best or matcher.quick_ratio() < best:
            continue
        r = matcher.ratio()
        if r > best:
            best, best_pos = r, start
    if best >= ratio and best_pos >= 0:
        return idx[best_pos], idx[min(best_pos + n, len(idx)) - 1] + 1
    return None


def span_offsets(
    graph: dict, text: str, paragraphs: list[tuple[int, int]] | None = None
) -> dict[str, tuple[int, int]]:
    """Map node id -> located span offsets, dropping nodes whose span is absent.

    When the operator cited a paragraph number, the span is sought inside that
    paragraph first and the document-wide search is the fallback. The cited
    paragraph is a locating aid, not a constraint: a span that is really there
    is found either way, and one that is nowhere is dropped either way.
    """
    out: dict[str, tuple[int, int]] = {}
    for node in graph.get("nodes", []):
        span = node.get("span", "")
        loc = None
        para = node.get("para")
        if paragraphs and isinstance(para, int) and 1 <= para <= len(paragraphs):
            lo, hi = paragraphs[para - 1]
            local = locate_span(span, text[lo:hi])
            if local is not None:
                loc = (lo + local[0], lo + local[1])
        if loc is None:
            loc = locate_span(span, text)
        if loc is not None:
            out[node["id"]] = loc
    return out


# --- node matching ---------------------------------------------------------


def _jaccard(a: tuple[int, int], b: tuple[int, int]) -> float:
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    inter = max(0, hi - lo)
    union = (a[1] - a[0]) + (b[1] - b[0]) - inter
    return inter / union if union else 0.0


def match_by_span(
    off_a: dict[str, tuple[int, int]],
    off_b: dict[str, tuple[int, int]],
    *,
    threshold: float = 0.5,
) -> list[tuple[str, str, float]]:
    """One-to-one node matching by maximum span overlap, Jaccard >= threshold."""
    cands = [
        (_jaccard(sa, sb), ia, ib)
        for ia, sa in off_a.items()
        for ib, sb in off_b.items()
        if _jaccard(sa, sb) >= threshold
    ]
    cands.sort(key=lambda t: (-t[0], t[1], t[2]))
    used_a: set[str] = set()
    used_b: set[str] = set()
    pairs: list[tuple[str, str, float]] = []
    for j, ia, ib in cands:
        if ia in used_a or ib in used_b:
            continue
        used_a.add(ia)
        used_b.add(ib)
        pairs.append((ia, ib, j))
    return pairs


# --- Layer 1: nominal Krippendorff alpha -----------------------------------


def krippendorff_alpha_nominal(pairs: list[tuple[str, str]]) -> float:
    """Alpha for two coders over `pairs` of nominal labels.

    Computed from the coincidence matrix in Krippendorff's own form, so it is
    defined for any number of categories and reduces to the familiar value on
    the two-category case checked in the tests.
    """
    if not pairs:
        return float("nan")
    values = sorted({v for p in pairs for v in p})
    n = 2 * len(pairs)
    coincidence = Counter()
    for a, b in pairs:
        coincidence[(a, b)] += 1
        coincidence[(b, a)] += 1
    marginal = Counter()
    for (a, _b), c in coincidence.items():
        marginal[a] += c
    observed = sum(coincidence.get((v, w), 0) for v in values for w in values if v != w)
    expected = sum(
        marginal[v] * marginal[w] for v in values for w in values if v != w
    ) / (n - 1)
    if expected == 0:
        return float("nan")
    return 1.0 - observed / expected


# --- Layer 2: triple overlap and its null ----------------------------------


def triples(graph: dict, alias: dict[str, str]) -> set[tuple[str, str, str]]:
    """Edge triples in aligned-id space, over nodes present in `alias`."""
    out = set()
    for e in graph.get("edges", []):
        u, v = alias.get(e.get("from")), alias.get(e.get("to"))
        if u and v:
            out.add((u, e.get("type"), v))
    return out


def triple_f1(ta: set, tb: set) -> float:
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    return 2 * inter / (len(ta) + len(tb)) if inter else 0.0


def random_graph_null(
    ta: set,
    tb: set,
    nodes: list[str],
    *,
    draws: int = 10000,
    seed: int = 0,
) -> dict:
    """Expected triple-overlap F1 when both operators place their edges at random.

    Each operator's edge count and edge-type marginal distribution are held
    fixed; only the endpoints are randomized over ordered pairs of distinct
    agreed nodes. Returns the null distribution's mean and 99th percentile.
    """
    rng = np.random.default_rng(seed)
    if len(nodes) < 2 or not ta or not tb:
        return {"mean": 0.0, "p99": 0.0, "draws": 0}
    types_a = [t for _, t, _ in ta]
    types_b = [t for _, t, _ in tb]
    n = len(nodes)
    scores = np.empty(draws)
    for d in range(draws):
        ra = set()
        while len(ra) < len(types_a):
            i, j = rng.integers(0, n, 2)
            if i != j:
                ra.add((nodes[i], types_a[len(ra)], nodes[j]))
        rb = set()
        while len(rb) < len(types_b):
            i, j = rng.integers(0, n, 2)
            if i != j:
                rb.add((nodes[i], types_b[len(rb)], nodes[j]))
        scores[d] = triple_f1(ra, rb)
    return {
        "mean": float(scores.mean()),
        "p99": float(np.percentile(scores, 99)),
        "max": float(scores.max()),
        "draws": draws,
    }


# --- Layer 3 / M3: structural load ----------------------------------------

DEPENDENCY_EDGES = {"depends_on", "derives", "assumes", "supports", "bounds"}


def _adjacency(graph: dict) -> dict[str, set[str]]:
    """dependent -> set of nodes it depends on."""
    adj: dict[str, set[str]] = {n["id"]: set() for n in graph.get("nodes", [])}
    for e in graph.get("edges", []):
        u, v = e.get("from"), e.get("to")
        if u in adj and v in adj and e.get("type") in DEPENDENCY_EDGES:
            adj[u].add(v)
    return adj


def support_mass(graph: dict) -> dict[str, int]:
    """M3 primary: how many nodes depend on v, directly or transitively.

    Strongly connected components are condensed first, so a cycle the schema
    forbids but an extraction may still produce cannot inflate a count.
    """
    adj = _adjacency(graph)
    ids = list(adj)
    order = {i: k for k, i in enumerate(ids)}
    reach: dict[str, set[str]] = {i: set() for i in ids}

    # Iterative DFS accumulating ancestors: for each node, who reaches it.
    for start in ids:
        seen = set()
        stack = [start]
        while stack:
            cur = stack.pop()
            for nxt in adj[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        seen.discard(start)
        for target in seen:
            reach[target].add(start)
    return {i: len(reach[i]) for i in sorted(ids, key=lambda x: order[x])}


def reverse_pagerank(
    graph: dict, *, damping: float = 0.85, iters: int = 100
) -> dict[str, float]:
    """RC2 alternative: PageRank on the reversed dependency edges."""
    adj = _adjacency(graph)
    ids = list(adj)
    n = len(ids)
    if n == 0:
        return {}
    # Reversed: weight flows from dependent to depended-upon.
    out_links = {i: sorted(adj[i]) for i in ids}
    rank = {i: 1.0 / n for i in ids}
    for _ in range(iters):
        new = {i: (1 - damping) / n for i in ids}
        dangling = 0.0
        for i in ids:
            if out_links[i]:
                share = damping * rank[i] / len(out_links[i])
                for j in out_links[i]:
                    new[j] += share
            else:
                dangling += damping * rank[i] / n
        rank = {i: new[i] + dangling for i in ids}
    return rank


def spearman(x: list[float], y: list[float]) -> tuple[float, int]:
    """Spearman rho with average ranks. Returns (rho, n)."""
    n = len(x)
    if n < 3:
        return float("nan"), n
    rx, ry = _ranks(x), _ranks(y)
    ax, ay = np.array(rx), np.array(ry)
    if ax.std() == 0 or ay.std() == 0:
        return float("nan"), n
    return float(np.corrcoef(ax, ay)[0, 1]), n


def _ranks(v: list[float]) -> list[float]:
    order = sorted(range(len(v)), key=lambda i: v[i])
    ranks = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


# --- prose mass ------------------------------------------------------------

_MATH = re.compile(r"\$[^$]*\$|\\\([^)]*\\\)|\\\[[^]]*\\]")


def prose_mass(text: str) -> dict[str, int]:
    """Words, with each inline mathematical expression counted as one token."""
    collapsed = _MATH.sub(" MATHTOKEN ", text)
    return {
        "words_raw": len(text.split()),
        "words_math_collapsed": len(collapsed.split()),
        "math_tokens": collapsed.count("MATHTOKEN"),
    }


def miracle_count(graph: dict) -> int:
    return sum(
        1 for n in graph.get("nodes", []) if n.get("explanatory_status") == "miracle"
    )


def status_counts(graph: dict) -> dict[str, int]:
    c = Counter(n.get("explanatory_status") for n in graph.get("nodes", []))
    return {s: c.get(s, 0) for s in ("derived", "verified_only", "miracle")}
