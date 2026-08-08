#!/usr/bin/env python3
"""Step 0 of the 2026bl run: take the predecessor's five specimens, unchanged.

This study reuses 2026bk's corpus deliberately: a changed corpus would confound
the mechanism with the material, which is what makes this a diagnostic rather
than an integrative replication. So the specimens are not re-fetched from their
original sources here -- re-fetching could return a revised page and would
silently change the corpus. They are taken from the predecessor's record and
verified byte-for-byte against the digests it published.

Raw specimen text is NOT committed (third-party copyright). What is committed is
this script and the manifest of sha256 digests, so a re-run can be checked
against the recorded values. A published clone that lacks the predecessor's
texts re-creates them with the predecessor's own `prepare_specimens.py`, whose
sources and cut points are declared there.

Run:
    uv run python code/prepare_specimens.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402

PREDECESSOR = L.PAPER_DIR.parent / "internalization" / "specimens"

# --- line unwrapping, declared 2026-08-08 before any call ------------------
#
# Three of the five specimens come from PDFs and carry hard line wrapping: a
# line break every ~90 characters, inside sentences. A sentence segmenter
# applied to that text divides at the wrap and returns fragments -- on the
# largest specimen, 1,265 "units" against 742 positions where a sentence could
# possibly end. That is not the segmenter describing the document; it is the
# segmenter describing the PDF extractor.
#
# So intra-paragraph line breaks are joined before anything in this study sees
# the text, uniformly across all five documents and all three conditions, and a
# word split across a wrap by a hyphen is rejoined. Paragraph breaks (blank
# lines) are preserved: they are the document's own structure, not the
# extractor's. Both digests are recorded, and the counts are reported per
# document, so the change is auditable and so is its size.
#
# This touches whitespace, never words. The corpus is still the predecessor's.

_HYPHEN_WRAP = re.compile(r"([A-Za-z])-\n[ \t]*([a-z])")
_LINE_WRAP = re.compile(r"(?<!\n)\n(?!\n)[ \t]*")


def unwrap(text: str) -> tuple[str, dict]:
    """Join intra-paragraph line breaks; preserve blank-line paragraph breaks."""
    dehyphenated = len(_HYPHEN_WRAP.findall(text))
    text2 = _HYPHEN_WRAP.sub(r"\1\2", text)
    joined = len(_LINE_WRAP.findall(text2))
    text3 = _LINE_WRAP.sub(" ", text2)
    return text3, {"dehyphenated": dehyphenated, "lines_joined": joined}


def main() -> int:
    proto = L.protocol()
    docs = list(proto["specimens"])

    src_manifest = PREDECESSOR / "MANIFEST.json"
    if not src_manifest.exists():
        raise SystemExit(
            f"predecessor specimens not found at {PREDECESSOR}. Re-create them with "
            "the 2026bk record's own prepare_specimens.py, then re-run this."
        )
    src = json.loads(src_manifest.read_text(encoding="utf-8"))

    L.SPECIMENS.mkdir(parents=True, exist_ok=True)
    items = {}
    for doc in docs:
        declared = src["items"][doc]
        path = PREDECESSOR / f"{doc}.txt"
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != declared["sha256"]:
            raise SystemExit(
                f"{doc}: digest {digest} != the predecessor's published "
                f"{declared['sha256']}. The corpus must be the predecessor's, "
                "unmodified; stopping rather than running on a changed text."
            )
        text, counts = unwrap(raw.decode("utf-8"))
        (L.SPECIMENS / f"{doc}.txt").write_text(text, encoding="utf-8")
        items[doc] = {
            "source": declared["source"],
            "sha256_predecessor": digest,
            "sha256_unwrapped": hashlib.sha256(text.encode()).hexdigest(),
            "chars": len(text),
            "words": declared["words"],
            "unwrapping": counts,
            "from": "2026bk record (10.5281/zenodo.21828980), verified by digest",
        }
        print(
            f"  {doc:8s} {declared['words']:6d} words  {digest[:12]}  verified  "
            f"joined={counts['lines_joined']:4d} dehyphenated={counts['dehyphenated']:3d}"
        )

    (L.SPECIMENS / "MANIFEST.json").write_text(
        json.dumps({"prepared": date.today().isoformat(), "items": items}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
