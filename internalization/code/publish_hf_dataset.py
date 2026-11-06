#!/usr/bin/env python3
"""Create + populate the 2026bk campaign dataset repo on Hugging Face.

Run (token injected by BWS, never printed):
    bws run -- uv run --with huggingface_hub python \
        code/publish_hf_dataset.py

Idempotent: create_repo(exist_ok=True); upload_folder overwrites by path.
The USER mints the dataset DOI on HF after the first drop (Settings -> DOI);
the DOI then goes into the paper's availability section + Zenodo metadata.

Staged layout: README.md (card), protocol/ (the pre-declared protocol, the
decision rule, the declared reader models, the pilot report, the data manifest,
and the specimen digest manifest), records/ (extracted spines for both operator
arms including the discarded pilot rounds, the blind alignments, the per-rater
target judgments, and the generated result tables), logs/ (one JSON row per
model API call, with prompts, prompt hash, parameters, response, token usage).

The specimen TEXTS are third-party works and are not redistributed here or
anywhere else; only their SHA-256 digest manifest ships, and code/
prepare_specimens.py re-fetches and verifies them from their public sources.

No redaction pass runs in this script. The staged files are the internal
originals verbatim, because the internal copies are already free of internal
process references -- verified by the same two screens the public mirror runs.
Keep it that way: fix the internal file, never redact on the way out.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from huggingface_hub import HfApi

PAPER_DIR = Path(__file__).resolve().parents[1]
SLUG = "internalization"

PROTOCOL_FILES = [
    "PROTOCOL.yaml",
    "DECISION_RULE.md",
    "READER_MODEL.md",
    "PILOT_REPORT.md",
    "DATA_MANIFEST.yaml",
]


def stage(tmp: Path) -> Path:
    root = tmp / SLUG
    (root / "protocol").mkdir(parents=True)
    (root / "records").mkdir()
    (root / "logs").mkdir()

    (root / "README.md").write_bytes((PAPER_DIR / "HF_DATASET_CARD.md").read_bytes())

    for name in PROTOCOL_FILES:
        (root / "protocol" / name).write_bytes((PAPER_DIR / name).read_bytes())
    # The digest manifest ships; the specimen texts beside it never do.
    (root / "protocol" / "SPECIMEN_MANIFEST.json").write_bytes(
        (PAPER_DIR / "specimens" / "MANIFEST.json").read_bytes()
    )

    # Extracted graphs, alignments, rater judgments, tables and call logs, each
    # REDACTED by redact_for_release.py: verbatim spans become the offsets they
    # resolved to, rater quotations and log bodies become digests. The build
    # refuses unless its specimen gate passes. The pilot-round subdirectories
    # are kept so a discarded round cannot be mistaken for a reported one.
    import redact_for_release as R

    release = tmp / "release"
    R.build(release)
    if R.specimen_gate(release):
        raise SystemExit("ABORTED: the specimen gate failed. Nothing uploaded.")
    for f in sorted((release / "data").rglob("*")):
        if f.is_file():
            dst = root / "records" / f.relative_to(release / "data")
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(f.read_bytes())
    # The generated tables the Results section is written from, so a reported
    # value and a computed value cannot drift apart in the dataset either.
    for f in sorted((release / "tables").glob("*")):
        if f.is_file():
            (root / "records" / f.name).write_bytes(f.read_bytes())
    for f in sorted((release / "logs").rglob("*.jsonl")):
        dst = root / "logs" / f.relative_to(release / "logs")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(f.read_bytes())

    return root


def main() -> int:
    token = os.environ.get("HUGGINGFACE_API_KEY")
    if not token:
        print("ERROR: HUGGINGFACE_API_KEY not in environment (run via `bws run --`).")
        return 2
    api = HfApi(token=token)
    print(f"authenticated as: {api.whoami().get('name')!r}")
    repo_id = f"spectralbranding/{SLUG}"
    url = api.create_repo(
        repo_id=repo_id, repo_type="dataset", private=False, exist_ok=True
    )
    print(f"repo ready: {url}")
    with tempfile.TemporaryDirectory() as td:
        root = stage(Path(td))
        n = sum(1 for p in root.rglob("*") if p.is_file())
        api.upload_folder(
            folder_path=str(root),
            repo_id=repo_id,
            repo_type="dataset",
            commit_message=(
                f"{SLUG}: records and call logs redacted (spans -> offsets, "
                "quotations and log bodies -> digests); specimen texts withheld"
            ),
        )
        print(f"uploaded {n} files -> {repo_id}")
    print("DONE. USER ACTION: mint the dataset DOI on HF (Settings -> DOI).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
