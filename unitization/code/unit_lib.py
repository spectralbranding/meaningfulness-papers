#!/usr/bin/env python3
"""Shared library for the 2026bl run: prompts, providers, inventories, schema.

Adapted from the predecessor's harness (2026bk `spine_lib.py`) rather than
written fresh, so that the U-free arm runs as close to the predecessor's task
as a re-implementation can: the node and edge vocabularies, the ordered type
rule and the provider layer are carried over unchanged. What is new is the
fixed-inventory task (M2), where an operator selects and types over units it is
given and may not re-cut them.

Every prompt keeps the study's hypotheses out of the model's view. No model in
any role is told which condition it serves, that a repetition is a repetition,
what the predecessor found, or which other models participate.

Keys come from the environment, injected by `bws run --`; nothing here reads or
writes a key value. Every call is logged to output/logs/*.jsonl by the corpus
logger.
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
LOGS_DIR = PAPER_DIR / "output" / "logs"
DATA_DIR = PAPER_DIR / "data"
OUTPUT_DIR = PAPER_DIR / "output"

# The logger ships beside this module in the published bundle, so the import
# resolves without a repo-relative path that only exists in the working tree.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_call_logger import log_call  # noqa: E402

# The 2026bl prompt set. There is no pilot and no iteration: this study's
# instrument decisions were fixed in the deposited pre-registration and in
# PROTOCOL.yaml before any call, so a prompt tuned until a number improved would
# convert a pre-declaration into a search. The node and edge vocabularies and
# the ordered type rule are inherited verbatim from the predecessor's frozen
# guidelines (internalization/1.2.0), because the U-free arm has to run the
# predecessor's task rather than a near-neighbour of it.
PROMPT_VERSION = "unitization/1.0.0"

# --- providers -------------------------------------------------------------

FAMILY_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "openai": "OPENAI_API_KEY",
    "xai": "GROK_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "mistral": "MISTRAL_API_KEY",
}
# Families whose OpenAI-shaped endpoint accepts `reasoning_effort`. Sending it
# to one that does not is a 400 on every retry, which is how the Layer S
# resolver failed on its first document: the parameter is not universal.
REASONING_EFFORT_FAMILIES = {"openai", "deepseek", "xai"}

FAMILY_ENDPOINTS = {
    "anthropic": "https://api.anthropic.com/v1/messages",
    "google": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    "openai": "https://api.openai.com/v1/chat/completions",
    "xai": "https://api.x.ai/v1/chat/completions",
    "deepseek": "https://api.deepseek.com/chat/completions",
    "mistral": "https://api.mistral.ai/v1/chat/completions",
}


def protocol() -> dict:
    return yaml.safe_load((PAPER_DIR / "PROTOCOL.yaml").read_text(encoding="utf-8"))


def seed() -> int:
    return int(protocol()["seed"])


def specimen_text(name: str) -> str:
    return (SPECIMENS / f"{name}.txt").read_text(encoding="utf-8")


# --- schema ----------------------------------------------------------------

NODE_TYPES = ["proposition", "method", "evidence", "assumption", "boundary_condition"]
EDGE_TYPES = ["depends_on", "derives", "supports", "assumes", "bounds"]
# The predecessor also carried an explanatory_status per node. This study does
# not: it measures selection, typing and edge recovery, and a status judgement
# would add a decision the design does not score.

# --- prompts ---------------------------------------------------------------
#
# Three tasks, one vocabulary. FREE is the predecessor's task, unmodified: the
# operator cuts its own units. FIXED is the intervention (M2): the operator is
# given the inventory and may not re-cut it. UNITIZE produces U-mod's inventory.
# SEGMENT is Layer S adjudication, and its prompt knows nothing about any of the
# others.

_UNIT_RULE = """UNIT RULE. Create exactly one node for each of the following, and nothing else:
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
rule produces on this text."""

_EDGE_RULE = f"""EDGES. Each edge has "from", "to" and "type", one of {EDGE_TYPES}.
Direction: {{"from": "n5", "to": "n2"}} always means n5 STANDS ON n2 -- n2 must
hold first.

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
comparable between one extraction and another."""

FREE_SYSTEM = f"""You extract the dependency structure of a written argument.

You are given a text whose paragraphs are numbered [P1], [P2], .... Return the
text's dependency graph as JSON and nothing else.

{_UNIT_RULE}

NODES. Each node has:
  "id"    -- a short unique string, e.g. "n1"
  "type"  -- one of {NODE_TYPES}
  "statement" -- one sentence, in your own words, saying what the node claims
  "para"  -- the number of the paragraph the node is stated in, as an integer
  "span"  -- a VERBATIM quotation of between 5 and 25 words copied exactly from
             that paragraph, locating where the node is stated. It must appear
             in the text character for character, without the [P..] marker.

{_EDGE_RULE}

OUTPUT. A single JSON object: {{"nodes": [...], "edges": [...]}}. No prose, no
markdown fence, no commentary. Extract what is there, at the granularity at
which the text argues; a long text will have more nodes than a short one."""

FREE_USER = """TEXT TO EXTRACT. Paragraphs are numbered; the numbers are not part
of the text.

{text}
"""

FIXED_SYSTEM = f"""You extract the dependency structure of a written argument.

You are given a text that has ALREADY been divided into numbered units [U1],
[U2], .... Return your analysis as JSON and nothing else.

YOU MAY NOT RE-DIVIDE THE TEXT. The units are given. You do not merge two units
into one, split a unit into two, or refer to any span other than a whole unit.
Every decision below is made about whole units, by their numbers.

Your task is exactly three decisions.

DECISION 1 -- WHICH UNITS ARE NODES. Select the units that carry the argument,
by the rule below. Most units in a document are not nodes.

{_UNIT_RULE}
Read "node" above as "selected unit": select the unit in which the claim, the
definition, the step, the evidence or the assumption is stated. Where the same
thing is stated across several consecutive units, select the one that states it,
not the ones that elaborate it.

DECISION 2 -- WHAT TYPE EACH SELECTED UNIT CARRIES. Give every selected unit a
type, one of {NODE_TYPES}.

DECISION 3 -- WHICH TYPED EDGES HOLD. Draw edges between SELECTED units only,
using their unit numbers as ids.

{_EDGE_RULE}

OUTPUT. A single JSON object with exactly these keys:
  {{"selected": [{{"unit": 12, "type": "proposition"}}, ...],
    "edges": [{{"from": 12, "to": 4, "type": "derives"}}, ...]}}
Unit numbers are integers, without the "U". Every id in "edges" must appear in
"selected". No prose, no markdown fence, no commentary."""

FIXED_USER = """TEXT, DIVIDED INTO UNITS. Each unit is prefixed with its number.
The numbers are not part of the text.

{units}
"""

UNITIZE_SYSTEM = """You divide a text into units.

A unit is the smallest span of text that states one thing on its own. Divide the
whole text, in order, so that the units partition it: every word of the text
belongs to exactly one unit, and no unit is empty.

RULES.
  1. Divide at the boundaries of what is stated, not by length. A unit may be a
     sentence, or a clause that stands on its own, or two short sentences that
     state one thing together.
  2. A displayed mathematical expression attaches to the sentence that
     introduces it and is not a unit of its own. Never place a boundary inside
     symbolic material.
  3. Headings, list items and captions are units.
  4. Do not correct, paraphrase, summarise or reorder the text.

OUTPUT. A single JSON object: {"units": ["first unit text", "second unit text",
...]}. The units, concatenated in order with single spaces where the original
had whitespace, must reproduce the input text. No prose, no markdown fence, no
commentary."""

UNITIZE_USER = """TEXT TO DIVIDE.

{text}
"""

SEGMENT_SYSTEM = """You divide a text into sentence units, under a declared rule.

THE RULE.
  1. A unit is one sentence, as an ordinary careful reader of English would
     identify it: a span ending at a full stop, question mark or exclamation
     mark that terminates a sentence rather than an abbreviation, an initial, a
     decimal, or a symbol.
  2. A displayed mathematical expression attaches to the sentence that
     introduces it and is NOT a unit of its own. Never place a boundary inside
     symbolic material.
  3. Headings, list items and captions are each one unit.
  4. Do not correct, paraphrase, summarise or reorder the text.

Apply the rule to the text you are given, and nothing else. You are not told
what the division will be used for, and you should not infer it.

OUTPUT. A single JSON object: {"units": ["first unit text", "second unit text",
...]}. The units, in order, must cover the whole text. No prose, no markdown
fence, no commentary."""

SEGMENT_USER = """TEXT TO DIVIDE.

{text}
"""

RESOLVE_SYSTEM = """You resolve a disagreement between two divisions of a text.

You are given a text and two candidate divisions of it into units, A and B, each
produced independently under this rule:

  1. A unit is one sentence, as an ordinary careful reader of English would
     identify it: a span ending at a full stop, question mark or exclamation
     mark that terminates a sentence rather than an abbreviation, an initial, a
     decimal, or a symbol.
  2. A displayed mathematical expression attaches to the sentence that
     introduces it and is NOT a unit of its own. Never place a boundary inside
     symbolic material.
  3. Headings, list items and captions are each one unit.

Where A and B agree, keep what they agree on. Where they differ, decide which
division the rule requires, and apply the rule rather than splitting the
difference. You may choose neither candidate where the rule requires a third
answer.

OUTPUT. A single JSON object: {"units": ["first unit text", ...]}, the resolved
division of the whole text. No prose, no markdown fence, no commentary."""

RESOLVE_USER = """TEXT.

{text}

DIVISION A.

{a}

DIVISION B.

{b}
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
    reasoning: str | None = None,
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
                        "output_config": {"effort": reasoning or "medium"},
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
                            "thinkingConfig": {"thinkingLevel": reasoning or "low"},
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
                    # Reasoning-tier models on this shape count reasoning
                    # against the same cap: on a 60-marker passage one spent
                    # 4,000 of 4,000 tokens reasoning and returned empty
                    # content. Where the provider accepts an effort control,
                    # the caller sets it rather than paying for a larger cap.
                    if reasoning and family in REASONING_EFFORT_FAMILIES:
                        body["reasoning_effort"] = reasoning
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


# The specimens are PDF extractions, and three of them carry literal control
# characters (0x16, 0x17 and friends) where the extractor lost a glyph. A model
# quoting the text faithfully echoes them, and JSON forbids a raw control
# character inside a string -- so a perfectly good answer fails to parse for a
# reason that has nothing to do with the model or the task. They are removed
# before parsing; the raw response is preserved in the call log, so this changes
# what can be read, not what was said.
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


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
    s = _CONTROL.sub("", s)
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


def validate_free(graph: dict) -> list[str]:
    """Schema complaints for a U-free extraction; empty means clean."""
    problems: list[str] = []
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    ids = [n.get("id") for n in nodes]
    if len(set(ids)) != len(ids):
        problems.append("duplicate node ids")
    for n in nodes:
        if n.get("type") not in NODE_TYPES:
            problems.append(f"node {n.get('id')}: bad type {n.get('type')!r}")
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


def validate_fixed(result: dict, n_units: int) -> list[str]:
    """Schema complaints for a fixed-inventory extraction; empty means clean.

    The one complaint with teeth is an out-of-range unit number: an operator
    that answers about a unit the inventory does not contain has re-cut the
    text, which M2 forbids. It is recorded rather than repaired.
    """
    problems: list[str] = []
    sel = result.get("selected") or []
    edges = result.get("edges") or []
    units = []
    for item in sel:
        u = item.get("unit")
        if not isinstance(u, int):
            problems.append(f"selected: non-integer unit {u!r}")
            continue
        if not 1 <= u <= n_units:
            problems.append(f"selected: unit {u} outside inventory of {n_units}")
        if item.get("type") not in NODE_TYPES:
            problems.append(f"unit {u}: bad type {item.get('type')!r}")
        units.append(u)
    if len(set(units)) != len(units):
        problems.append("duplicate selected units")
    known = set(units)
    for e in edges:
        for endpoint in ("from", "to"):
            v = e.get(endpoint)
            if not isinstance(v, int):
                problems.append(f"edge {endpoint}: non-integer unit {v!r}")
            elif v not in known:
                problems.append(
                    f"edge {e.get('from')}->{e.get('to')}: {v} not selected"
                )
        if e.get("type") not in EDGE_TYPES:
            problems.append(
                f"edge {e.get('from')}->{e.get('to')}: bad type {e.get('type')!r}"
            )
    return problems


# --- paths -----------------------------------------------------------------
#
# One file per (document, condition, operator, repetition). The repetition index
# is part of the name because k = 5 repetitions are the noise floor: a run that
# overwrote a repetition would destroy the quantity Layer B is computed from.


def inventory_path(doc: str, source: str) -> Path:
    """source: segmenter | unitizer | adjudicated | ADJ_1 | ADJ_2"""
    return DATA_DIR / f"inventory_{doc}__{source}.json"


def extraction_path(doc: str, condition: str, operator_id: str, rep: int) -> Path:
    return DATA_DIR / f"extract_{doc}__{condition}__{operator_id}__r{rep}.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def units_block(units: list[str]) -> str:
    """The inventory as the operator sees it: numbered, whole, in order."""
    return "\n\n".join(f"[U{i + 1}] {u.strip()}" for i, u in enumerate(units))


def stream_seed(*parts: Any) -> int:
    """A stable digest seed for a permutation or bootstrap stream (P2).

    Never a process hash: the same document, condition and layer must produce
    the same interval on a re-run, on any machine.
    """
    material = "|".join([str(seed())] + [str(p) for p in parts])
    return int(hashlib.sha256(material.encode()).hexdigest()[:16], 16)
