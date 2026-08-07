#!/bin/bash
# reproduce.sh -- 2026bk (Internalization as an Operation) pipeline orchestrator.
#
# Two modes.
#
#   analysis-only (default): re-runs every reported statistic from the
#     committed extractions and ratings in data/. No API keys, no network,
#     deterministic under the seed in PROTOCOL.yaml. This reproduces every
#     number in the paper.
#
#   --collect: additionally re-runs the extraction, alignment and rating calls
#     (requires ANTHROPIC_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY, GROK_API_KEY,
#     DEEPSEEK_API_KEY -- inject with `bws run -- ./reproduce.sh --collect`).
#     The operators are hosted models whose behaviour is epoch-pinned, so
#     re-collection yields a new epoch rather than a byte-identical replication;
#     existing extractions are never overwritten, so a re-collection is additive
#     unless data/ is cleared first.
#
#   --fetch: re-fetches the specimen texts from their public sources and
#     re-verifies them against specimens/MANIFEST.json.
#
# Order matters and is pre-declared in PROTOCOL.yaml: the pilot runs before the
# main extraction, and nothing downstream may inform anything upstream.
set -euo pipefail
cd "$(dirname "$0")"

command -v uv >/dev/null || { echo "uv required"; exit 1; }

mkdir -p output/tables output/logs data logs
LOG=output/logs/master_run.log
: > "$LOG"

DEPS_ANALYSIS="--with numpy --with scipy --with pyyaml --with httpx"
DEPS_COLLECT="--with httpx --with pyyaml"

echo "== unit suite (must pass before anything) ==" | tee -a "$LOG"
# The suite must run under the SAME dependency set as the analysis it
# guards. Declaring a narrower set here let two tests fail on an import
# in the published bundle while passing wherever the deps happened to be
# cached -- the failure mode a reproduction script exists to prevent.
uv run --with pytest $DEPS_ANALYSIS python -m pytest code/tests -q 2>&1 | tee -a "$LOG"

# The specimen texts are third-party works and are NOT redistributed, so a
# fresh clone has none and the ladder's prose-mass step would die on a missing
# file. Fetch them when they are absent rather than failing: this is the one
# step that touches the network, it needs no credentials, and every file is
# verified against the digests in specimens/MANIFEST.json before use.
NEED_SPECIMENS=0
while read -r name; do
    [ -f "specimens/${name}.txt" ] || NEED_SPECIMENS=1
done < <(uv run --with pyyaml python -c "
import json,pathlib
m=json.loads(pathlib.Path('specimens/MANIFEST.json').read_text())
print('\n'.join((m.get('specimens') or m).keys()))
")

if [[ "${1:-}" == "--fetch" || "$NEED_SPECIMENS" == "1" ]]; then
    echo "== specimens: fetch and hash ==" | tee -a "$LOG"
    uv run --with requests --with beautifulsoup4 python code/prepare_specimens.py 2>&1 | tee -a "$LOG"
fi

if [[ "${1:-}" == "--collect" ]]; then
    echo "== pilot extraction (guidelines may be refined here; thresholds may not) ==" | tee -a "$LOG"
    uv run $DEPS_COLLECT python -u code/extract_spines.py --set pilot 2>&1 | tee -a "$LOG"
    echo "== main extraction, both arms ==" | tee -a "$LOG"
    uv run $DEPS_COLLECT python -u code/extract_spines.py --set main 2>&1 | tee -a "$LOG"
fi

echo "== RC1 agreement: pilot ==" | tee -a "$LOG"
uv run $DEPS_ANALYSIS python code/score_agreement.py --set pilot 2>&1 | tee -a "$LOG"

echo "== RC1 agreement: specimens ==" | tee -a "$LOG"
uv run $DEPS_ANALYSIS python code/score_agreement.py --set main 2>&1 | tee -a "$LOG"

echo "== VC3 ladder ==" | tee -a "$LOG"
uv run $DEPS_ANALYSIS python code/score_ladder.py 2>&1 | tee -a "$LOG"

echo "== recovery targets T1-T3 ==" | tee -a "$LOG"
uv run $DEPS_COLLECT python code/score_targets.py 2>&1 | tee -a "$LOG"

echo "== results summary (what the paper is written from) ==" | tee -a "$LOG"
uv run $DEPS_ANALYSIS python code/emit_results_summary.py 2>&1 | tee -a "$LOG"

echo "== done ==" | tee -a "$LOG"
