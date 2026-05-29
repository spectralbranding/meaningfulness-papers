#!/usr/bin/env bash
# reproduce.sh — Hub-level pipeline orchestrator
#
# Iterates over paper-slug subdirectories at this hub root that contain
# either paper.md or paper.yaml. For each one, invokes the per-paper
# reproduce.sh if present. Logs to output/logs/hub_run.log.
#
# Conforms to PUBLIC_MIRROR_STANDARD.md v1.0.0.
#
# Usage:
#   ./reproduce.sh                  # Run every per-paper pipeline
#   ./reproduce.sh --check-only     # Verify per-paper orchestrators exist; do not run
#   ./reproduce.sh --fast           # Pass --fast through to each per-paper script

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

mkdir -p output/figures output/tables output/logs
LOG_FILE="output/logs/hub_run.log"

CHECK_ONLY=0
FAST=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --fast) FAST=1 ;;
    *) echo "Unknown flag: $arg"; exit 2 ;;
  esac
done

echo "==================================================" | tee -a "$LOG_FILE"
echo "Hub pipeline run: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "Repo: $REPO_ROOT" | tee -a "$LOG_FILE"
echo "Git SHA: $(git rev-parse HEAD 2>/dev/null || echo 'not-a-repo')" | tee -a "$LOG_FILE"
echo "Mode: check_only=$CHECK_ONLY fast=$FAST" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"

FOUND=0
RAN=0
SKIPPED=0

for dir in */; do
  slug="${dir%/}"
  # Skip non-paper-slug dirs
  case "$slug" in
    output|.git|.github|templates|docs) continue ;;
  esac

  if [[ -f "$slug/paper.md" || -f "$slug/paper.yaml" ]]; then
    FOUND=$((FOUND + 1))
    echo ">>> Paper-slug detected: $slug" | tee -a "$LOG_FILE"

    if [[ -x "$slug/reproduce.sh" ]]; then
      if [[ "$CHECK_ONLY" == "1" ]]; then
        echo "    check-only: per-paper reproduce.sh present at $slug/reproduce.sh" | tee -a "$LOG_FILE"
      else
        echo "    running $slug/reproduce.sh" | tee -a "$LOG_FILE"
        if [[ "$FAST" == "1" ]]; then
          ( cd "$slug" && ./reproduce.sh --fast ) 2>&1 | tee -a "$LOG_FILE"
        else
          ( cd "$slug" && ./reproduce.sh ) 2>&1 | tee -a "$LOG_FILE"
        fi
        RAN=$((RAN + 1))
      fi
    else
      echo "    SKIP: no executable reproduce.sh in $slug" | tee -a "$LOG_FILE"
      SKIPPED=$((SKIPPED + 1))
    fi
  fi
done

echo "==================================================" | tee -a "$LOG_FILE"
echo "Hub pipeline complete: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "Paper-slugs found: $FOUND ; ran: $RAN ; skipped: $SKIPPED" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"
