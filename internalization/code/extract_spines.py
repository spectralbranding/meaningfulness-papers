#!/usr/bin/env python3
"""Stage 1 of the 2026bk run: two independent operators extract each document.

Each (document, operator) pair is extracted exactly once and written to
data/spine_<doc>__<OP>.json. The script is idempotent: an existing extraction is
never overwritten and never re-called, so a resumed run costs nothing and a
result cannot be quietly re-rolled.

Neither operator is told what kind of document it is reading, which rung of a
comparison it belongs to, or what the study expects. The two arms are different
model families, per the corpus cross-operator rule.

Run (keys injected, never printed):
    bws run -- uv run --with httpx --with pyyaml python \
        code/extract_spines.py --set pilot
    bws run -- uv run --with httpx --with pyyaml python \
        code/extract_spines.py --set main
"""

from __future__ import annotations

import argparse
import json
import sys

import spine_lib as L


def one(doc: str, reader_model_id: str, op: dict, force: bool = False) -> dict:
    out = L.graph_path(doc, op["id"])
    if out.exists() and not force:
        graph = json.loads(out.read_text(encoding="utf-8"))
        print(f"  {doc:16s} {op['id']:5s} cached  nodes={len(graph['nodes'])}")
        return graph
    text = L.numbered(L.specimen_text(doc))
    user = L.EXTRACTION_USER.format(
        reader_model=L.reader_model(reader_model_id), text=text
    )
    raw = L.call_model(
        op["model"],
        op["family"],
        L.EXTRACTION_SYSTEM,
        user,
        role="extraction_operator",
        operation=f"extract|{op['id']}|{doc}",
        phase="internalization_extraction",
        # A 6,000-word document already produced a 13,000-token graph, so the
        # cap has to clear a document twice that length without truncating: a
        # truncated graph is an unparseable one, and silently retrying it would
        # spend the budget on the same failure.
        max_out=48000,
    )
    graph = L.parse_json_block(raw)
    problems = L.validate_graph(graph)
    graph["_meta"] = {
        "document": doc,
        "operator": op["id"],
        "model": op["model"],
        "family": op["family"],
        "reader_model": reader_model_id,
        "prompt_version": L.PROMPT_VERSION,
        "schema_problems": problems,
    }
    L.DATA_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(graph, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    flag = f"  SCHEMA: {len(problems)} problem(s)" if problems else ""
    print(
        f"  {doc:16s} {op['id']:5s} new     nodes={len(graph['nodes'])} "
        f"edges={len(graph.get('edges', []))}{flag}"
    )
    return graph


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", choices=["pilot", "main"], required=True)
    ap.add_argument("--docs", nargs="*", help="restrict to these documents")
    ap.add_argument("--ops", nargs="*", help="restrict to these operator ids")
    ap.add_argument("--force", action="store_true", help="re-call even if cached")
    args = ap.parse_args()

    proto = L.protocol()
    if args.set == "pilot":
        docs = {k: v["reader_model"] for k, v in proto["pilot_documents"].items()}
    else:
        docs = {k: v["reader_model"] for k, v in proto["specimens"].items()}
    if args.docs:
        docs = {k: v for k, v in docs.items() if k in args.docs}
    ops = proto["extraction_operators"]
    if args.ops:
        ops = [o for o in ops if o["id"] in args.ops]

    print(f"extraction set={args.set} docs={list(docs)} ops={[o['id'] for o in ops]}")
    failures = 0
    for doc, rm in docs.items():
        for op in ops:
            try:
                one(doc, rm, op, force=args.force)
            except Exception as exc:  # noqa: BLE001 -- reported, run continues
                failures += 1
                print(f"  {doc:16s} {op['id']:5s} FAILED  {type(exc).__name__}: {exc}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
