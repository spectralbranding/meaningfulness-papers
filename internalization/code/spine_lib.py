#!/usr/bin/env python3
"""Shared library for the 2026bk validation run: prompts, providers, schema.

The prompt set is frozen at `internalization/1.0.0`. It is written to keep the
paper's hypotheses out of the operator's view: an extraction prompt never says
what kind of document it is looking at, never names the rung or the specimen,
and never mentions that anything is expected to be higher or lower than
anything else. The operator is given a schema, a reader model, and a text.

Keys come from the environment, injected by `bws run --`; nothing here reads or
writes a key value. Every call is logged to logs/*.jsonl by the corpus logger.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import yaml

PAPER_DIR = Path(__file__).resolve().parents[1]
SPECIMENS = PAPER_DIR / "specimens"
LOGS_DIR = PAPER_DIR / "logs"
DATA_DIR = PAPER_DIR / "data"
OUTPUT_DIR = PAPER_DIR / "output"

# The logger ships beside this module in the published bundle, so the import
# resolves without a repo-relative path that only exists in the working tree.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_call_logger import log_call  # noqa: E402

# 1.1.0 -- the pilot's one permitted product: refined annotation guidelines.
# The pilot found the two arms extracting at grains a factor of six apart, which
# makes every agreement statistic a measurement of an underspecified prompt
# rather than of the operation. The fix is an explicit UNIT RULE plus a shared
# paragraph numbering. It fixes the grain WITHOUT fixing the node count: a rule
# tying node count to document length would have forced structural load to scale
# with prose mass, prejudging exactly what the ladder is built to measure.
#
# 1.2.0 -- the pilot's second and last product. Round 2 showed node recovery
# working and edge recovery not: the arms drew few edges, and where they drew
# the same edge they often typed it differently. The revision adds an edge
# COMPLETENESS instruction and an ORDERED type rule that decides the cases two
# readers could differ on. Again no threshold was touched, and the guidelines
# are FROZEN at this version: further iteration on pilot material until a
# number improved would convert a pre-declaration into a search. See
# PILOT_REPORT.md, which reports all three rounds including the discarded ones.
PROMPT_VERSION = "internalization/1.2.0"

# --- providers -------------------------------------------------------------

FAMILY_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "openai": "OPENAI_API_KEY",
    "xai": "GROK_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
}
FAMILY_ENDPOINTS = {
    "anthropic": "https://api.anthropic.com/v1/messages",
    "google": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    "openai": "https://api.openai.com/v1/chat/completions",
    "xai": "https://api.x.ai/v1/chat/completions",
    "deepseek": "https://api.deepseek.com/chat/completions",
}


def protocol() -> dict:
    return yaml.safe_load((PAPER_DIR / "PROTOCOL.yaml").read_text(encoding="utf-8"))


def seed() -> int:
    return int(protocol()["seed"])


def specimen_text(name: str) -> str:
    return (SPECIMENS / f"{name}.txt").read_text(encoding="utf-8")


def reader_model(model_id: str) -> str:
    """Return the declared reader model verbatim from READER_MODEL.md.

    READER_MODEL.md is the single source of truth for the models; the harness
    quotes a section of it rather than holding a second copy that could drift.
    """
    md = (PAPER_DIR / "READER_MODEL.md").read_text(encoding="utf-8")
    blocks = re.split(r"\n## ", md)
    for block in blocks:
        if block.startswith(f"{model_id} "):
            body = "## " + block
            return body.split("\n---")[0].strip()
    raise SystemExit(f"reader model {model_id!r} not found in READER_MODEL.md")


# --- schema ----------------------------------------------------------------

NODE_TYPES = ["proposition", "method", "evidence", "assumption", "boundary_condition"]
EDGE_TYPES = ["depends_on", "derives", "supports", "assumes", "bounds"]
STATUSES = ["derived", "verified_only", "miracle"]

EXTRACTION_SYSTEM = f"""You extract the dependency structure of a written argument.

You are given (1) a reader model and (2) a text whose paragraphs are numbered
[P1], [P2], .... Return the text's dependency graph as JSON and nothing else.

UNIT RULE. Create exactly one node for each of the following, and nothing else:
  (a) each claim the text asserts and then uses, defends, or relies on;
  (b) each definition, object or construction the text introduces and later uses;
  (c) each step of a method or derivation the text says was carried out;
  (d) each piece of evidence the text offers in support of a claim;
  (e) each assumption or scope condition the text states.
Do NOT create a node for: restatement of something already a node, motivational
or historical remarks, acknowledgements, or a summary of several steps. If the
text states a step in one sentence and then elaborates it over a paragraph,
that is ONE node. If the text presents several separable steps inside one
sentence, those are SEVERAL nodes. Work through the whole text in order;
completeness matters more than brevity, and a graph that stops early is wrong.
Do not aim at any particular number of nodes -- the number is whatever the unit
rule produces on this text.

NODES. Each node has:
  "id"    -- a short unique string, e.g. "n1"
  "type"  -- one of {NODE_TYPES}
  "statement" -- one sentence, in your own words, saying what the node claims
  "para"  -- the number of the paragraph the node is stated in, as an integer
  "span"  -- a VERBATIM quotation of between 5 and 25 words copied exactly from
             that paragraph, locating where the node is stated. It must appear
             in the text character for character, without the [P..] marker.
  "explanatory_status" -- one of {STATUSES}, judged against the reader model:
      "derived"       the node follows from other nodes in this graph or from
                      something the reader model says the reader holds
      "verified_only" the node can be checked as stated, but does not follow
                      from what the reader holds or from earlier nodes
      "miracle"       neither derived nor reducible to what the reader holds:
                      it works, and the text gives the reader no account of why
  "status_reason" -- one clause saying why that status, naming the held term or
                     the missing derivation

EDGES. Each edge has "from", "to" and "type", one of {EDGE_TYPES}. Direction:
{{"from": "n5", "to": "n2"}} always means n5 STANDS ON n2 -- n2 must hold first.

COMPLETENESS. Go through the nodes one by one and ask, of each, what it stands
on; record every such dependency the text states or plainly implies by its
order of argument. A node with no outgoing edge asserts that the text offers it
without support -- a real category, covering the text's starting points, its
stated assumptions and its scope conditions, but it should be the minority. Do
not invent an edge the text does not warrant, and do not leave unrecorded a
dependency the text does state.

TYPE. Choose the FIRST type that applies, in this order:
  1. "derives"    -- the text obtains the source from the target by a stated
                     step of reasoning, calculation or construction
  2. "supports"   -- the target is evidence, an example or a citation offered
                     for the source
  3. "assumes"    -- the target is an assumption or premise the source rests on
                     without argument
  4. "bounds"     -- the target is a scope condition limiting where the source
                     holds
  5. "depends_on" -- none of the above applies and the source nonetheless
                     requires the target; this is the default
Apply the order strictly rather than by preference. Where two readers could
reasonably differ, the ordered rule decides, which is what makes the type
comparable between one extraction and another.

OUTPUT. A single JSON object: {{"nodes": [...], "edges": [...]}}. No prose, no
markdown fence, no commentary. Extract what is there, at the granularity at
which the text argues; a long text will have more nodes than a short one."""

EXTRACTION_USER = """READER MODEL. Judge every explanatory_status against this
reader and no other. A term not held by this reader is not available as a
derivation, however standard it may be in the field.

{reader_model}

TEXT TO EXTRACT. Paragraphs are numbered; the numbers are not part of the text.

{text}
"""


def numbered(text: str) -> str:
    """Number the paragraphs, giving both operators one shared unitization.

    The numbering is a locating aid only. It constrains where a node may be
    anchored, not how many nodes there are.
    """
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return "\n\n".join(f"[P{i + 1}] {p}" for i, p in enumerate(paras))


def paragraph_spans(text: str) -> list[tuple[int, int]]:
    """Character offsets of each numbered paragraph in the ORIGINAL text."""
    out: list[tuple[int, int]] = []
    pos = 0
    for para in re.split(r"\n\s*\n", text):
        stripped = para.strip()
        if not stripped:
            pos += len(para) + 2
            continue
        start = text.find(stripped, pos)
        out.append((start, start + len(stripped)))
        pos = start + len(stripped)
    return out


# --- rating (T1-T3) --------------------------------------------------------

RATING_SYSTEM = """You are scoring an extraction against the text it was
extracted from. You are given the text, an extracted dependency graph, and
three recovery targets. You do not know how the graph was produced and it does
not matter.

Score ONLY against what the text itself states. Where the text and what you
know about it from elsewhere disagree, the text wins, and you say so.

For each target return a verdict and the verbatim quotation from the text that
establishes what the author declared. If the author declares nothing of the
kind the target asks about, say so: that is "not_applicable", not a failure.

Return a single JSON object and nothing else:
{
  "T1": {"verdict": "recovered|not_recovered|not_applicable",
         "author_declaration": "verbatim quote from the text",
         "graph_evidence": "the node id(s) that do or do not correspond",
         "reasoning": "two sentences"},
  "T2": {"verdict": ..., "author_declaration": ..., "graph_evidence": ...,
         "reasoning": ..., "goals_stated": <int>, "goals_recovered": <int>,
         "goals_merged_or_split": <int>},
  "T3": {"verdict": ..., "author_declaration": ..., "graph_evidence": ...,
         "reasoning": ..., "residuals_marked_by_author": <int>,
         "missed_residuals": <int>, "false_residuals": <int>}
}"""

RATING_USER = """TARGETS.

T1 -- the generative object. Recovered when the graph contains a SINGLE node
from which the derivation edges to the author's separable goals originate, and
that node corresponds to the object the text itself presents as generative.
There is no partial credit: it is one node or it is not.

T2 -- the stated decomposition. Recovered when the author's separable goals
appear as distinct nodes, with the decomposition represented as edges from the
restated problem, and no goal is merged with another or split, relative to the
author's own division. Count the goals the author states and the goals the
graph recovers.

T3 -- the marked residuals. Recovered when EVERY step the author explicitly
marks as unexplained -- something the author says can be verified but not
explained, or concedes as unresolved -- carries explanatory_status "miracle" in
the graph, AND no step the author derives carries that status. Report two error
counts: missed residuals (author marked, graph did not) and false residuals
(graph marked, author derived). Both must be zero for "recovered".

TEXT.

{text}

EXTRACTED GRAPH.

{graph}
"""

# --- cross-rendering alignment --------------------------------------------

ALIGN_SYSTEM = """You align two lists of claims that were extracted from two
different texts. Your job is to say which claim in list X is the same claim as
which claim in list Y -- the same assertion about the same objects, however
differently worded.

Align on content, not on wording or order. A claim may have no counterpart;
leave it unaligned rather than forcing a pair. Every alignment is one-to-one.

Return a single JSON object and nothing else:
{"pairs": [{"x": "<id in list X>", "y": "<id in list Y>",
            "confidence": "high|medium|low"}]}"""

ALIGN_USER = """LIST X.

{x}

LIST Y.

{y}
"""


# --- provider call ---------------------------------------------------------


def call_model(
    model_id: str,
    family: str,
    system: str,
    user: str,
    *,
    role: str,
    operation: str,
    phase: str,
    max_out: int = 16000,
) -> str:
    """One logged, retried provider call. Returns raw response text."""
    # Imported here, not at module scope: the pure parsing helpers in this
    # module must stay importable for the offline analysis path, which
    # declares no HTTP client because it makes no calls.
    import httpx

    key = os.environ[FAMILY_KEYS[family]]
    endpoint = FAMILY_ENDPOINTS[family].format(model=model_id)
    prompt_sha = hashlib.sha256((system + "\n" + user).encode()).hexdigest()
    backoffs = [5, 20, 60]
    last_exc: Exception | None = None
    for attempt in range(4):
        try:
            with log_call(
                phase=phase,
                operation=operation,
                operator=model_id,
                operator_role=role,
                endpoint=endpoint,
                sdk_version="httpx>=0.27 (raw HTTP)",
                logs_dir=LOGS_DIR,
            ) as logger:
                logger.set_system_prompt(system)
                logger.set_user_prompt(user)
                common = {"prompt_sha256": prompt_sha, "prompt_version": PROMPT_VERSION}
                if family == "anthropic":
                    # This family rejects sampling parameters, and on the current
                    # flagship `max_tokens` caps reasoning AND answer together --
                    # a first pilot call spent the whole 16k budget reasoning and
                    # returned nothing. Reasoning depth is bounded by the effort
                    # level instead, with a cap large enough for both.
                    params = {
                        "max_tokens": max_out,
                        "output_config": {"effort": "medium"},
                    }
                    logger.set_parameters(
                        params | common | {"sdk_param_note": "temperature omitted"}
                    )
                    r = httpx.post(
                        endpoint,
                        headers={
                            "x-api-key": key,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json",
                        },
                        json={
                            "model": model_id,
                            "system": system,
                            "messages": [{"role": "user", "content": user}],
                            **params,
                        },
                        timeout=900,
                    )
                    r.raise_for_status()
                    data = r.json()
                    logger.capture_response(data)
                    text = "".join(b.get("text", "") for b in data.get("content", []))
                elif family == "google":
                    body = {
                        "systemInstruction": {"parts": [{"text": system}]},
                        "contents": [{"role": "user", "parts": [{"text": user}]}],
                        "generationConfig": {
                            "temperature": 0,
                            # This provider counts reasoning tokens against the
                            # output cap, so the cap is doubled AND reasoning is
                            # bounded explicitly: on a dense mathematical
                            # document it spent 62,912 tokens reasoning and was
                            # truncated mid-graph with 2,620 left to write in.
                            "maxOutputTokens": max_out * 2,
                            # A token budget here is advisory and was ignored:
                            # the same call still spent ~63,000 tokens
                            # reasoning. The level control is what binds.
                            "thinkingConfig": {"thinkingLevel": "low"},
                            "seed": seed(),
                        },
                    }
                    logger.set_parameters(body["generationConfig"] | common)
                    r = httpx.post(
                        endpoint,
                        headers={
                            "x-goog-api-key": key,
                            "content-type": "application/json",
                        },
                        json=body,
                        timeout=900,
                    )
                    r.raise_for_status()
                    data = r.json()
                    logger.capture_response(data)
                    parts = data["candidates"][0]["content"].get("parts", [])
                    text = "".join(p.get("text", "") for p in parts)
                else:
                    body = {
                        "model": model_id,
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": user},
                        ],
                    }
                    if model_id.startswith("gpt-5"):
                        body["max_completion_tokens"] = max_out
                        body["seed"] = seed()
                    else:
                        body["temperature"] = 0
                        body["max_tokens"] = max_out
                    logger.set_parameters(
                        {k: v for k, v in body.items() if k != "messages"} | common
                    )
                    r = httpx.post(
                        endpoint,
                        headers={"Authorization": f"Bearer {key}"},
                        json=body,
                        timeout=900,
                    )
                    r.raise_for_status()
                    data = r.json()
                    logger.capture_response(data)
                    message = data["choices"][0]["message"]
                    # Reasoning-tier models on this shape sometimes spend the
                    # budget on reasoning and return empty content with the
                    # substance under a separate key. Read that rather than
                    # discarding the call.
                    text = (
                        message.get("content") or message.get("reasoning_content") or ""
                    )
            if not text.strip():
                raise RuntimeError("empty response")
            return text
        except Exception as exc:  # noqa: BLE001 -- logged and retried per policy
            last_exc = exc
            print(
                f"    retry {attempt + 1}/3 after {type(exc).__name__}: {exc}",
                flush=True,
            )
            if attempt < 3:
                time.sleep(backoffs[attempt])
    raise RuntimeError(f"{model_id} failed after retries: {last_exc}")


# --- parsing ---------------------------------------------------------------


# Escapes to keep verbatim; everything else that follows a backslash is treated
# as literal text and the backslash is doubled. Two subtleties, both learned
# from mathematical specimens:
#
#   * The alternation must consume a valid escape WHOLE, or an already-correct
#     `\\` has its second backslash doubled into a broken `\\\`.
#   * `\b` and `\f` are valid JSON escapes, but in these documents they open
#     `\binom` and `\frac`. Reading them as control characters silently eats the
#     macro's first letter, and the span then cannot be located in the source.
#     A control escape is therefore honoured only when NOT followed by a letter
#     -- which costs at most a line break, and line breaks are normalized away
#     before any span is matched.
#
# A verbatim span quoting mathematics is not valid JSON as emitted, and the
# operator has no way to know that while quoting faithfully. The raw response is
# preserved in the call log, so this changes what can be parsed, not what the
# operator said.
_ESCAPE = re.compile(r'\\(?:[\\"/]|u[0-9a-fA-F]{4}|[bfnrt](?![A-Za-z]))|\\')


def _repair_escapes(s: str) -> str:
    return _ESCAPE.sub(lambda m: m.group(0) if len(m.group(0)) > 1 else "\\\\", s)


def parse_json_block(raw: str) -> dict:
    s = raw.strip()
    if s.startswith("```"):
        s = s.split("```", 2)[1]
        s = s[4:] if s.startswith("json") else s
    s = s.strip()
    # The repaired reading is tried FIRST, not as a fallback: a span containing
    # `\binom` is valid JSON that parses to a backspace and loses the macro's
    # first letter, so the plain parse succeeds while silently corrupting the
    # quotation. Preferring the literal reading is what keeps the span
    # locatable in the source.
    for candidate in (_repair_escapes(s), s):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            i, j = candidate.find("{"), candidate.rfind("}")
            if i >= 0 and j > i:
                try:
                    return json.loads(candidate[i : j + 1])
                except json.JSONDecodeError:
                    continue
    raise json.JSONDecodeError("unparseable after escape repair", s, 0)


def validate_graph(graph: dict) -> list[str]:
    """Return a list of schema complaints; empty means clean."""
    problems: list[str] = []
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    ids = [n.get("id") for n in nodes]
    if len(set(ids)) != len(ids):
        problems.append("duplicate node ids")
    for n in nodes:
        if n.get("type") not in NODE_TYPES:
            problems.append(f"node {n.get('id')}: bad type {n.get('type')!r}")
        if n.get("explanatory_status") not in STATUSES:
            problems.append(
                f"node {n.get('id')}: bad status {n.get('explanatory_status')!r}"
            )
        if not (n.get("span") or "").strip():
            problems.append(f"node {n.get('id')}: empty span")
    known = set(ids)
    for e in edges:
        if e.get("from") not in known or e.get("to") not in known:
            problems.append(f"edge {e.get('from')}->{e.get('to')}: unknown endpoint")
        if e.get("type") not in EDGE_TYPES:
            problems.append(
                f"edge {e.get('from')}->{e.get('to')}: bad type {e.get('type')!r}"
            )
    return problems


def graph_path(doc: str, operator_id: str) -> Path:
    return DATA_DIR / f"spine_{doc}__{operator_id}.json"


def load_graph(doc: str, operator_id: str) -> dict:
    return json.loads(graph_path(doc, operator_id).read_text(encoding="utf-8"))
