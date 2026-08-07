#!/usr/bin/env python3
"""Stage 3 of the 2026bk run: the VC3 ladder.

Three pre-declared quantities, computed per operator arm:

  1. Pairwise spine preservation across R0-R1, R1-R2 and R0-R2, each at the
     Layer-2 threshold, against a random-graph null.
  2. The monotonic miracle ordering MC(R0) > MC(R1) > MC(R2), which the
     protocol requires to hold on BOTH arms to survive.
  3. Prose mass against structural load across the rungs.

Cross-rendering node alignment cannot use spans -- the texts differ. Two
alignments are computed and both are reported: a blind LLM alignment (the
aligner sees two shuffled, unlabelled lists of statements and never learns
which rendering either came from) and a deterministic lexical alignment.

Run:
    bws run -- uv run --with httpx --with pyyaml --with numpy --with scipy \
        python code/score_ladder.py
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
from collections import Counter

import metrics_lib as M
import numpy as np
import spine_lib as L
from scipy.optimize import linear_sum_assignment

L2_F1 = 0.60
RUNGS = ["vc3_r0", "vc3_r1", "vc3_r2"]
PAIRS = [("vc3_r0", "vc3_r1"), ("vc3_r1", "vc3_r2"), ("vc3_r0", "vc3_r2")]


# --- lexical alignment (deterministic sensitivity check) -------------------

_TOKEN = re.compile(r"[a-z0-9]+")


def _tfidf(docs: list[str]) -> np.ndarray:
    toks = [_TOKEN.findall(d.lower()) for d in docs]
    vocab = sorted({t for d in toks for t in d})
    index = {t: i for i, t in enumerate(vocab)}
    tf = np.zeros((len(docs), len(vocab)))
    for i, d in enumerate(toks):
        for t, c in Counter(d).items():
            tf[i, index[t]] = c
    df = (tf > 0).sum(axis=0)
    idf = np.log((1 + len(docs)) / (1 + df)) + 1
    mat = tf * idf
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    return mat / np.where(norms == 0, 1, norms)


def lexical_alignment(
    ga: dict, gb: dict, threshold: float = 0.25
) -> list[tuple[str, str, float]]:
    a_ids = [n["id"] for n in ga["nodes"]]
    b_ids = [n["id"] for n in gb["nodes"]]
    if not a_ids or not b_ids:
        return []
    texts = [n.get("statement", "") for n in ga["nodes"]] + [
        n.get("statement", "") for n in gb["nodes"]
    ]
    vecs = _tfidf(texts)
    sim = vecs[: len(a_ids)] @ vecs[len(a_ids) :].T
    rows, cols = linear_sum_assignment(-sim)
    return [
        (a_ids[r], b_ids[c], float(sim[r, c]))
        for r, c in zip(rows, cols)
        if sim[r, c] >= threshold
    ]


# --- blind LLM alignment ---------------------------------------------------


def llm_alignment(
    ga: dict, gb: dict, key: str, aligner: dict, seed: int
) -> list[tuple[str, str]]:
    """Ask the aligner which claim in one list is which claim in the other.

    The lists are shuffled and relabelled, so the aligner cannot infer which
    rendering is which, nor the order the study cares about.
    """
    cache = L.DATA_DIR / f"align_{key}.json"
    if cache.exists():
        data = json.loads(cache.read_text(encoding="utf-8"))
        return [(p["a"], p["b"]) for p in data["pairs"]]

    rng = random.Random(seed)
    xa = [
        (f"x{i + 1}", n["id"], n.get("statement", ""))
        for i, n in enumerate(ga["nodes"])
    ]
    yb = [
        (f"y{i + 1}", n["id"], n.get("statement", ""))
        for i, n in enumerate(gb["nodes"])
    ]
    rng.shuffle(xa)
    rng.shuffle(yb)

    def listing(rows):
        return "\n".join(f"{lab}: {st}" for lab, _real, st in rows)

    raw = L.call_model(
        aligner["model"],
        aligner["family"],
        L.ALIGN_SYSTEM,
        L.ALIGN_USER.format(x=listing(xa), y=listing(yb)),
        role="ladder_aligner",
        operation=f"align|{key}",
        phase="internalization_alignment",
    )
    parsed = L.parse_json_block(raw)
    to_a = {lab: real for lab, real, _ in xa}
    to_b = {lab: real for lab, real, _ in yb}
    pairs, used_a, used_b = [], set(), set()
    for p in parsed.get("pairs", []):
        a, b = to_a.get(p.get("x")), to_b.get(p.get("y"))
        if a and b and a not in used_a and b not in used_b:
            used_a.add(a)
            used_b.add(b)
            pairs.append({"a": a, "b": b, "confidence": p.get("confidence")})
    cache.write_text(json.dumps({"pairs": pairs}, indent=1) + "\n", encoding="utf-8")
    return [(p["a"], p["b"]) for p in pairs]


# --- preservation ----------------------------------------------------------


def preservation(
    ga: dict, gb: dict, pairs: list[tuple[str, str]], seed: int, draws: int
) -> dict:
    alias_a = {a: f"m{k}" for k, (a, _b) in enumerate(pairs)}
    alias_b = {b: f"m{k}" for k, (_a, b) in enumerate(pairs)}
    ta, tb = M.triples(ga, alias_a), M.triples(gb, alias_b)
    f1 = M.triple_f1(ta, tb)
    null = M.random_graph_null(ta, tb, list(alias_a.values()), draws=draws, seed=seed)
    return {
        "aligned_nodes": len(pairs),
        "triples": {"a": len(ta), "b": len(tb)},
        "shared_triples": len(ta & tb),
        "triple_f1": f1,
        "null": null,
        "threshold": L2_F1,
        "beats_null_p99": bool(f1 > null["p99"]),
        "preserves": bool(f1 >= L2_F1 and f1 > null["p99"]),
    }


# --- structural load vs prose mass -----------------------------------------


def node_prose_mass(graph: dict, text: str) -> dict[str, float]:
    """Paragraph word count, split evenly among the nodes anchored in it."""
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    counts = Counter()
    for n in graph["nodes"]:
        p = n.get("para")
        if isinstance(p, int) and 1 <= p <= len(paras):
            counts[p] += 1
    out = {}
    for n in graph["nodes"]:
        p = n.get("para")
        if isinstance(p, int) and 1 <= p <= len(paras) and counts[p]:
            out[n["id"]] = len(paras[p - 1].split()) / counts[p]
    return out


def rung_profile(doc: str, op_id: str) -> dict:
    graph = L.load_graph(doc, op_id)
    text = L.specimen_text(doc)
    sm = M.support_mass(graph)
    npm = node_prose_mass(graph, text)
    ids = [i for i in sm if i in npm]
    rho, n = M.spearman([npm[i] for i in ids], [float(sm[i]) for i in ids])
    return {
        "prose_mass": M.prose_mass(text),
        "nodes": len(graph["nodes"]),
        "edges": len(graph.get("edges", [])),
        "mean_support_mass": (sum(sm.values()) / len(sm)) if sm else 0.0,
        "status_counts": M.status_counts(graph),
        "miracle_count": M.miracle_count(graph),
        "node_prose_mass_vs_support_mass": {"spearman_rho": rho, "n": n},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=10000)
    args = ap.parse_args()

    proto = L.protocol()
    seed = int(proto["seed"])
    ops = proto["extraction_operators"]
    aligner = proto["ladder_aligner"]

    result: dict = {
        "rungs": {},
        "preservation": {},
        "ordering": {},
        "aligner": aligner["model"],
    }

    for op in ops:
        result["rungs"][op["id"]] = {r: rung_profile(r, op["id"]) for r in RUNGS}

    for op in ops:
        per_op = {}
        for a, b in PAIRS:
            ga, gb = L.load_graph(a, op["id"]), L.load_graph(b, op["id"])
            key = f"{a}__{b}__{op['id']}"
            llm_pairs = llm_alignment(ga, gb, key, aligner, seed)
            lex_pairs = [(x, y) for x, y, _s in lexical_alignment(ga, gb)]
            per_op[f"{a}->{b}"] = {
                "llm_alignment": preservation(ga, gb, llm_pairs, seed, args.draws),
                "lexical_alignment": preservation(ga, gb, lex_pairs, seed, args.draws),
            }
        result["preservation"][op["id"]] = per_op

    for op in ops:
        mc = [result["rungs"][op["id"]][r]["miracle_count"] for r in RUNGS]
        result["ordering"][op["id"]] = {
            "MC": dict(zip(RUNGS, mc)),
            "strictly_decreasing": bool(mc[0] > mc[1] > mc[2]),
            "inversions": [
                f"{RUNGS[i]}<={RUNGS[i + 1]}" for i in range(2) if not mc[i] > mc[i + 1]
            ],
        }
    result["ordering"]["survives_on_both_arms"] = all(
        result["ordering"][op["id"]]["strictly_decreasing"] for op in ops
    )

    out = L.OUTPUT_DIR / "tables" / "ladder.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")

    print("\nVC3 ladder")
    for op in ops:
        print(f"\n  arm {op['id']} ({op['model']})")
        print(
            f"    {'rung':8s} {'words':>7s} {'nodes':>6s} {'edges':>6s} "
            f"{'meanSM':>7s} {'MC':>4s}"
        )
        for r in RUNGS:
            p = result["rungs"][op["id"]][r]
            print(
                f"    {r:8s} {p['prose_mass']['words_math_collapsed']:>7d} {p['nodes']:>6d} "
                f"{p['edges']:>6d} {p['mean_support_mass']:>7.2f} {p['miracle_count']:>4d}"
            )
        o = result["ordering"][op["id"]]
        print(
            f"    ordering strictly decreasing: {o['strictly_decreasing']} {o['inversions']}"
        )
        for pair, v in result["preservation"][op["id"]].items():
            llm, lex = v["llm_alignment"], v["lexical_alignment"]
            print(
                f"    {pair:20s} F1(llm)={llm['triple_f1']:.3f} null99={llm['null']['p99']:.3f} "
                f"preserves={llm['preserves']} | F1(lex)={lex['triple_f1']:.3f} "
                f"preserves={lex['preserves']}"
            )
    print(
        f"\n  ordering survives on both arms: {result['ordering']['survives_on_both_arms']}"
    )
    print(f"\nwritten -> {out.relative_to(L.PAPER_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
