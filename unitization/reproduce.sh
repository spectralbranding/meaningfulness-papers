#!/usr/bin/env bash
# Reproduce the 2026bl run.
#
# Default (no flags): ANALYSIS ONLY. Re-derives every reported number from the
# extraction records and needs no API key. The records are the Hugging Face
# dataset of record (DOI 10.57967/hf/9911), not files in this repository; when
# data/ is empty they are downloaded (no credentials) and unpacked into data/.
# Set BL_DATA_DIR to an existing download to skip the network. The declared
# re-analysis also reads the predecessor's graphs (2026bk); when
# ../internalization/data is empty they come from its dataset (DOI
# 10.57967/hf/9898), or from PRED_DATA_DIR if set.
#
#   ./reproduce.sh                 analysis only -- no keys
#   ./reproduce.sh --collect       re-run the collection itself (needs keys)
#   ./reproduce.sh --check-only    check the toolchain and stop
#
# The collection is a multi-provider pipeline: six model families in six roles.
# Keys are read from the environment and printed nowhere; the corpus convention
# is to inject them with `bws run -- ./reproduce.sh --collect`.
#
# The ORDER below is not a convenience. It is pre-registered (M1a): the
# segmenter's fidelity and the predicted base rates are established BEFORE any
# operator call, because measured afterwards the segmenter's error becomes
# available as an explanation for whatever the operators did. --collect walks
# that order and does not offer a way around it.

set -euo pipefail
cd "$(dirname "$0")"

COLLECT=0
CHECK_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --collect) COLLECT=1 ;;
    --check-only) CHECK_ONLY=1 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

PY_ANALYSIS=(uv run --python 3.12 --with pyyaml --with pysbd python)
PY_GAMMA=(uv run --python 3.12 --with pygamma-agreement --with pyannote.core --with pyyaml python)
PY_CALLS=(uv run --with httpx --with pyyaml --with pysbd python)

echo "== toolchain =="
"${PY_ANALYSIS[@]}" -c "import pysbd, yaml; print('pysbd', pysbd.__version__ if hasattr(pysbd,'__version__') else 'ok')"
if [ "$CHECK_ONLY" = "1" ]; then echo "check-only: ok"; exit 0; fi

if [ "$COLLECT" = "1" ]; then
  echo "== 0. specimens (the predecessor's five, verified by digest) =="
  "${PY_ANALYSIS[@]}" code/prepare_specimens.py

  echo "== smoke: every model identifier answers before anything is spent =="
  "${PY_CALLS[@]}" code/smoke_models.py

  echo "== 1. segmenter inventory (no model call) =="
  "${PY_ANALYSIS[@]}" code/segment_units.py

  echo "== 2. Layer S: adjudication, BEFORE any operator call =="
  "${PY_CALLS[@]}" code/adjudicate_segmentation.py

  echo "== 3. predicted base rates, also before any operator call =="
  "${PY_ANALYSIS[@]}" code/predict_base_rates.py

  echo "== 4. U-mod inventory =="
  "${PY_CALLS[@]}" code/build_unitizer_inventory.py

  echo "== 5. the 150 extraction calls, in the pre-declared condition order =="
  "${PY_CALLS[@]}" code/extract_graphs.py
fi

if [ "$COLLECT" = "0" ]; then
  if ! ls data/extract_*.json >/dev/null 2>&1; then
    DS="${BL_DATA_DIR:-hf-data}"
    if [ ! -d "$DS/records" ]; then
      echo "== records: download the dataset of record =="
      uvx --from huggingface_hub hf download spectralbranding/unitization-before-extraction \
        --repo-type dataset --local-dir "$DS" | tail -1
    fi
    "${PY_ANALYSIS[@]}" code/fetch_records.py --dataset-dir "$DS"
  fi
  if [ -z "${PRED_DATA_DIR:-}" ] && ! ls ../internalization/data/spine_*.json >/dev/null 2>&1; then
    PD="${BL_PRED_DIR:-hf-data-predecessor}"
    if [ ! -d "$PD/records" ]; then
      echo "== predecessor records: download the 2026bk dataset =="
      uvx --from huggingface_hub hf download spectralbranding/internalization \
        --repo-type dataset --local-dir "$PD" | tail -1
    fi
    export PRED_DATA_DIR="$PD/records"
  fi
fi

echo "== analysis: predicted base rates =="
"${PY_ANALYSIS[@]}" code/predict_base_rates.py

echo "== analysis: the decomposition (Table A1) =="
"${PY_ANALYSIS[@]}" code/score_layers.py

echo "== analysis: the published joint coefficients (M5a) =="
"${PY_GAMMA[@]}" code/score_composite.py

echo "== analysis: the declared re-analysis of the predecessor (Table A3) =="
"${PY_GAMMA[@]}" code/reanalyse_predecessor.py

echo "== analysis: results summary =="
"${PY_ANALYSIS[@]}" code/emit_results_summary.py

echo "done. Tables in output/tables/, per-call logs in output/logs/."
