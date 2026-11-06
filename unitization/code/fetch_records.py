#!/usr/bin/env python3
"""Rebuild data/ from the Hugging Face dataset of record (DOI 10.57967/hf/9911).

The GitHub repository does not carry data/: the records are published once, as
the dataset, in the redacted form redact_for_release.py builds (free-condition
spans as located offsets, model-produced inventories as boundaries plus
digests). The dataset ships them as four JSONL splits so its viewer can load
them; the analysis reads one file per cell. This turns the first into the
second, file name for file name, and nothing else.

Run (reproduce.sh does this when data/ is empty):
    hf download spectralbranding/unitization-before-extraction \\
        --repo-type dataset --local-dir hf-data
    uv run --with pyyaml python code/fetch_records.py --dataset-dir hf-data
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PAPER_DIR / "data"

# split file -> the fields of each row that form the per-cell record
ANSWER_FIELDS = {
    "extractions_fixed.jsonl": ("selected", "edges"),
    "extractions_free.jsonl": ("nodes", "edges"),
}


def rows(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dataset-dir", required=True, type=Path)
    a = ap.parse_args()
    rec = a.dataset_dir / "records"
    if not rec.is_dir():
        print(f"ERROR: {rec} not found -- download the dataset first (see --help).")
        return 2
    DATA_DIR.mkdir(exist_ok=True)
    n = 0
    for r in rows(rec / "inventories.jsonl"):
        name = f"inventory_{r['document']}__{r['source']}.json"
        (DATA_DIR / name).write_text(json.dumps(r["record"], indent=1))
        n += 1
    for split, fields in ANSWER_FIELDS.items():
        for r in rows(rec / split):
            name = (
                f"extract_{r['document']}__{r['condition']}__{r['operator']}"
                f"__r{r['repetition']}.json"
            )
            (DATA_DIR / name).write_text(
                json.dumps({k: r[k] for k in fields}, indent=1)
            )
            n += 1
    print(f"wrote {n} records to {DATA_DIR.relative_to(PAPER_DIR)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
