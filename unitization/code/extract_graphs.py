#!/usr/bin/env python3
"""Step 4 of the 2026bl run: the 150 extraction calls.

3 conditions x 5 documents x 2 operators x k = 5 repetitions (M3). The condition
order is pre-declared in PROTOCOL.yaml so that a result cannot be reported from
whichever condition ran the better way; this script walks that order and does
not accept a different one.

Every repetition is written to its own file and is never overwritten: the k
repetitions ARE the within-operator baseline, so a run that re-rolled one would
destroy the quantity Layer B is computed from. A resumed run costs nothing.

Nothing tells an operator that a repetition is a repetition, which condition it
is serving, or that another operator exists.

Run (keys injected, never printed):
    bws run -- uv run --with httpx --with pyyaml python \\
        code/extract_graphs.py
    ... --conditions u_det --docs vc1 --reps 1 2      # a slice, same rules
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402

INVENTORY_FOR = {"u_det": "segmenter", "u_mod": "unitizer"}


def one(doc: str, condition: str, op: dict, rep: int) -> dict:
    out = L.extraction_path(doc, condition, op["id"], rep)
    if out.exists():
        cached = L.load_json(out)
        n = len(cached.get("selected") or cached.get("nodes") or [])
        print(f"  {doc:8s} {condition:7s} {op['id']:5s} r{rep} cached  n={n}")
        return cached

    text = L.specimen_text(doc)
    if condition == "u_free":
        system, user = L.FREE_SYSTEM, L.FREE_USER.format(text=L.numbered(text))
        n_units = None
    else:
        inv = L.load_json(L.inventory_path(doc, INVENTORY_FOR[condition]))
        units = inv["units"]
        n_units = len(units)
        system, user = L.FIXED_SYSTEM, L.FIXED_USER.format(units=L.units_block(units))

    raw = L.call_model(
        op["model"],
        op["family"],
        system,
        user,
        role="extraction_operator",
        operation=f"extract|{op['id']}|{doc}|{condition}|r{rep}",
        phase="unitization_extraction",
        # A fixed-inventory answer is a list of integers and types, which is far
        # smaller than a free extraction's verbatim spans -- but the free arm
        # has to clear a 12,000-word document without truncating, and a
        # truncated graph is an unparseable one.
        max_out=48000,
    )
    result = L.parse_json_block(raw)
    problems = (
        L.validate_free(result)
        if condition == "u_free"
        else L.validate_fixed(result, n_units)
    )
    result["_meta"] = {
        "document": doc,
        "condition": condition,
        "operator": op["id"],
        "model": op["model"],
        "family": op["family"],
        "repetition": rep,
        "inventory": INVENTORY_FOR.get(condition, "none"),
        "inventory_units": n_units,
        "prompt_version": L.PROMPT_VERSION,
        "schema_problems": problems,
    }
    L.write_json(out, result)
    n = len(result.get("selected") or result.get("nodes") or [])
    e = len(result.get("edges") or [])
    flag = f"  SCHEMA: {len(problems)}" if problems else ""
    print(
        f"  {doc:8s} {condition:7s} {op['id']:5s} r{rep} new     n={n} e={e}{flag}",
        flush=True,
    )
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="*")
    ap.add_argument("--conditions", nargs="*")
    ap.add_argument("--ops", nargs="*")
    ap.add_argument("--reps", nargs="*", type=int)
    args = ap.parse_args()

    proto = L.protocol()
    k = int(proto["repetitions_k"])
    conditions = [
        c
        for c in proto["condition_order"]
        if not args.conditions or c in args.conditions
    ]
    docs = [d for d in proto["specimens"] if not args.docs or d in args.docs]
    ops = [
        o for o in proto["extraction_operators"] if not args.ops or o["id"] in args.ops
    ]
    reps = args.reps or list(range(1, k + 1))

    print(
        f"extraction: conditions={conditions} docs={docs} "
        f"ops={[o['id'] for o in ops]} reps={reps} "
        f"({len(conditions) * len(docs) * len(ops) * len(reps)} calls)"
    )
    failures = 0
    for condition in conditions:  # the pre-declared order
        for doc in docs:
            for op in ops:
                for rep in reps:
                    try:
                        one(doc, condition, op, rep)
                    except Exception as exc:  # noqa: BLE001 -- reported, run continues
                        failures += 1
                        print(
                            f"  {doc:8s} {condition:7s} {op['id']:5s} r{rep} FAILED "
                            f"{type(exc).__name__}: {str(exc)[:160]}",
                            flush=True,
                        )
                    # All repetitions for a document run in as tight a window as
                    # rate limits permit (M3); this is the only pause.
                    time.sleep(1)
    print(f"\n{'FAILURES: ' + str(failures) if failures else 'all calls complete'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
