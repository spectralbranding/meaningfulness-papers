#!/usr/bin/env python3
"""Create + populate the 2026bl run dataset repo on Hugging Face.

Run (token injected by BWS, never printed):
    bws run -- uv run --with huggingface_hub python \
        code/publish_hf_dataset.py

Idempotent: create_repo(exist_ok=True); upload_folder overwrites by path.
The USER mints the dataset DOI on HF after the first drop (Settings -> DOI);
the DOI then goes into the paper's availability section + Zenodo metadata.

WHAT IS UPLOADED IS THE REDACTED TREE, AND THAT IS THE WHOLE POINT. Unlike the
predecessor's drop, this study cannot publish its records as they sit on disk:
the free-condition records carry verbatim spans of the specimens, the segmenter
and unitizer inventories ARE the specimens cut into units, and the per-call logs
embed whole documents in their prompts. `redact_for_release.py` builds a tree
that carries what the analysis consumes and none of the source text, and it runs
three gates -- a length gate, a role gate, and a substring check against the five
specimens themselves. THIS SCRIPT REFUSES TO UPLOAD unless that build succeeds,
so there is no path from a failed gate to a public dataset.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

from huggingface_hub import HfApi

PAPER_DIR = Path(__file__).resolve().parents[1]
SLUG = "unitization-before-extraction"


def build_release(dest: Path) -> Path:
    """Run the redactor + its gates. Any failure aborts the publish."""
    out = dest / "release"
    proc = subprocess.run(
        [
            sys.executable,
            str(PAPER_DIR / "code" / "redact_for_release.py"),
            "--out",
            str(out),
            "--verify",
            "--hf-out",
            str(dest / "release_hf"),
        ],
        cwd=str(PAPER_DIR),
        capture_output=True,
        text=True,
    )
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        raise SystemExit(
            "ABORTED: the release build did not pass its gates. Nothing uploaded."
        )
    if "VERIFY OK" not in proc.stdout:
        raise SystemExit(
            "ABORTED: the redacted records did not reproduce the tables. "
            "Nothing uploaded."
        )
    hf = dest / "release_hf"
    (hf / "README.md").write_bytes((PAPER_DIR / "HF_DATASET_CARD.md").read_bytes())
    return hf


def main() -> int:
    token = os.environ.get("HUGGINGFACE_API_KEY")
    if not token:
        print("ERROR: HUGGINGFACE_API_KEY not in environment (run via `bws run --`).")
        return 2

    api = HfApi(token=token)
    print(f"authenticated as: {api.whoami().get('name')!r}")
    repo_id = f"spectralbranding/{SLUG}"

    with tempfile.TemporaryDirectory() as td:
        root = build_release(Path(td))
        n = sum(1 for p in root.rglob("*") if p.is_file())

        url = api.create_repo(
            repo_id=repo_id, repo_type="dataset", private=False, exist_ok=True
        )
        print(f"repo ready: {url}")
        api.upload_folder(
            folder_path=str(root),
            repo_id=repo_id,
            repo_type="dataset",
            commit_message=(
                "2026bl run: consolidated JSONL splits + derived tables "
                "(specimen text withheld; see the card)"
            ),
            # The first drop shipped a per-file tree that the dataset viewer
            # could not load. Clear it, or the stale paths sit beside the
            # splits that replaced them.
            delete_patterns=["records/*.json", "inventories/*", "logs/*"],
        )
        print(f"uploaded {n} files -> {repo_id}")

    print("DONE. The dataset DOI is 10.57967/hf/9911; re-minting is not needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
