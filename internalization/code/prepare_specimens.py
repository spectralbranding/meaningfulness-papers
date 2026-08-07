#!/usr/bin/env python3
"""Fetch and normalize the specimen and pilot texts for the 2026bk validation run.

Every text the extraction harness sees is produced by this script, so that a
reader can reconstruct the exact inputs from public sources. Nothing here is
hand-edited: the cut points for the VC3 rungs are declared as literal anchor
strings taken from the source document's own provenance sentence, and the
script fails loudly if an anchor is not found.

Raw specimen text is NOT committed (third-party copyright). What is committed
is this script and the manifest of sha256 digests and word counts it emits, so
a re-run can be checked byte-for-byte against the recorded digests.

Run:
    uv run --with requests --with beautifulsoup4 python \
        code/prepare_specimens.py

Outputs:
    specimens/<id>.txt
    specimens/MANIFEST.json
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

PAPER_DIR = Path(__file__).resolve().parents[1]
OUT = PAPER_DIR / "specimens"
# Optional local copies. Present in the authoring tree; absent from a published
# clone, where the public URL beside each one is used instead.
LOCAL_CACHE = PAPER_DIR.parents[2] / "research" / "references"
UA = {"User-Agent": "Mozilla/5.0 (compatible; 2026bk-specimen-fetch/1.0)"}

# --- source declarations ---------------------------------------------------

WORDPRESS_POSTS = {
    # VC1 -- the labeled-ground-truth specimen (author-stated objective, marked residuals).
    "vc1": "https://terrytao.wordpress.com/2026/07/21/"
    "a-digestion-of-the-jacobian-conjecture-counterexample/",
    # VC3 rung R2 -- the independent expert digestion.
    "vc3_r2": "https://terrytao.wordpress.com/2026/07/03/"
    "a-digestion-of-unit-distance-constructions/",
}

# VC2 -- Turing (1950), Mind LIX(236):433-460. Public teaching mirror; the
# canonical record is doi:10.1093/mind/LIX.236.433.
TURING_PDF = "https://courses.cs.umbc.edu/471/papers/turing.pdf"

# VC3 rungs R0/R1 -- one document, published by the producing organization,
# which states the provenance of the verbatim block itself.
PLANAR_PDF_LOCAL = LOCAL_CACHE / "openai-2026-planar-point-sets.pdf"
PLANAR_PDF_URL = "https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf"
# Declared anchors, verbatim from the source document.
R0_START = "Final Response from Internal Model."
R0_END = "The remainder of the paper explains the above proof in more detail."

# Pilot material -- neither specimen, per DECISION_RULE.md section 1.
PILOT_HTML = {
    "pilot_dijkstra": "https://www.cs.utexas.edu/~EWD/transcriptions/EWD10xx/EWD1036.html",
    # Single-column transcription. The two-column scan of the same essay was
    # tried first and rejected during the pilot: column-interleaved extraction
    # destroys sentence contiguity, and every span-located statistic then reads
    # as disagreement between operators when the disagreement is in the input.
    "pilot_thompson": "https://www.win.tue.nl/~aeb/linux/hh/thompson/trust.html",
}
PILOT_PDF: dict[str, str] = {}
PILOT_LOCAL_MD = {
    # A spine-first-drafted corpus paper: the one pilot document for which an
    # authored reference spine exists, which is why it is in the pilot set.
    # Resolved in the authoring tree OR in the public mirror, where the same
    # paper is a sibling slug. Keeping it reachable in BOTH matters: the
    # random-graph null draws from one stream across all documents, so a run
    # that silently skips a document produces different null summaries. Gate
    # verdicts and reported statistics are unaffected either way, but a
    # reproduction should not diverge at all when it does not have to.
    "pilot_2026ao": [
        PAPER_DIR.parent / "2026ao" / "paper.md",
        PAPER_DIR.parent / "meaning-meaningfulness" / "paper.md",
    ],
}


# --- helpers ---------------------------------------------------------------


def norm(text: str) -> str:
    """Collapse whitespace runs, strip page furniture, keep paragraph breaks."""
    text = text.replace("\r\n", "\n").replace("\xa0", " ")
    # Drop bare page numbers left by pdftotext.
    text = re.sub(r"\n\s*\d{1,3}\s*\n", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def wordpress_body(url: str) -> str:
    html = requests.get(url, headers=UA, timeout=60).text
    soup = BeautifulSoup(html, "html.parser")
    # Selectors are tried in priority order. A comma-joined selector would
    # return the first match in *document order*, which on this theme is a
    # sidebar element, not the post body.
    node = None
    for sel in ("div.post-content", "div.entry-content", "div.entry", "div.post"):
        node = soup.select_one(sel)
        if node is not None:
            break
    if node is None:
        raise SystemExit(f"post body not found at {url}")
    for tag in node.select("script, style, .sharedaddy, .wpcnt, #jp-post-flair"):
        tag.decompose()
    # This platform renders inline mathematics as images whose alt text carries
    # the LaTeX. Dropping them would delete most of the argument, so each image
    # is replaced by its alt text before the text is taken.
    for img in node.find_all("img"):
        alt = (img.get("alt") or "").strip()
        img.replace_with(f" ${alt}$ " if alt else " ")
    # Take block elements one per paragraph and keep their inner text
    # contiguous. Taking the whole subtree with a newline separator would put
    # every inline mathematical expression on a line of its own, which breaks
    # sentence contiguity and with it both quotation and paragraph numbering.
    # Direct children only, so every piece of the post is taken exactly once.
    paras: list[str] = []
    for child in node.children:
        text = child.get_text(" ") if hasattr(child, "get_text") else str(child)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            paras.append(text)
    if not paras:
        return norm(node.get_text(" "))
    return norm("\n\n".join(paras))


def pdf_text(path: Path) -> str:
    proc = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout


def pdf_text_from_url(url: str) -> str:
    """Same as pdf_text, for the case where no local copy is held. A published
    clone has no authoring-tree cache, so it takes the declared public URL."""
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        dest = Path(td) / "source.pdf"
        fetch_pdf(url, dest)
        return pdf_text(dest)


def fetch_pdf(url: str, dest: Path) -> Path:
    dest.write_bytes(requests.get(url, headers=UA, timeout=120).content)
    return dest


def cut(text: str, start: str, end: str) -> tuple[str, str]:
    """Split `text` into (inside, outside) at the two declared anchors."""
    i = text.find(start)
    j = text.find(end)
    if i < 0 or j < 0 or j <= i:
        raise SystemExit(f"declared anchor not found (start={i}, end={j})")
    inside = text[i + len(start) : j]
    outside = text[:i] + "\n\n" + text[j + len(end) :]
    return inside, outside


def strip_references(text: str) -> str:
    """Drop a trailing bibliography; it is not part of the argument."""
    m = list(re.finditer(r"\n\s*(References|Bibliography)\s*\n", text))
    return text[: m[-1].start()] if m else text


def emit(name: str, text: str, meta: dict, manifest: dict) -> None:
    text = norm(text)
    path = OUT / f"{name}.txt"
    path.write_text(text, encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    # A displayed equation is legitimately a short line; a fragment of a
    # sentence is not. Only the latter is what this diagnostic is looking for.
    short = sum(1 for ln in lines if len(ln.split()) < 5 and "$" not in ln)
    manifest[name] = {
        **meta,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "chars": len(text),
        "words": len(text.split()),
        # Input-quality diagnostic, added during the pilot. A high share of very
        # short lines is the signature of column-interleaved or letterspaced PDF
        # extraction, which breaks sentence contiguity and makes every
        # span-located statistic read as operator disagreement.
        "short_line_share": round(short / len(lines), 3) if lines else 0.0,
    }
    print(
        f"  {name:16s} {manifest[name]['words']:>6d} words  {manifest[name]['sha256'][:12]}"
    )


# --- main ------------------------------------------------------------------


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: dict = {}
    print("specimens:")

    for name, url in WORDPRESS_POSTS.items():
        emit(
            name, wordpress_body(url), {"source": url, "kind": "weblog post"}, manifest
        )

    turing = fetch_pdf(TURING_PDF, OUT / "_turing.pdf")
    body = pdf_text(turing)
    # Drop the mirror's header line and the trailing bibliography.
    body = body.split("COMPUTING MACHINERY AND INTELLIGENCE", 1)[-1]
    emit(
        "vc2",
        strip_references(body),
        {
            "source": TURING_PDF,
            "doi": "10.1093/mind/LIX.236.433",
            "kind": "journal article (public teaching mirror)",
        },
        manifest,
    )

    if PLANAR_PDF_LOCAL.is_file():
        planar = pdf_text(PLANAR_PDF_LOCAL)
    else:
        planar = pdf_text_from_url(PLANAR_PDF_URL)
    r0, r1 = cut(planar, R0_START, R0_END)
    emit(
        "vc3_r0",
        r0,
        {
            "source": PLANAR_PDF_URL,
            "kind": "verbatim automated output (stated provenance)",
            "cut": [R0_START, R0_END],
        },
        manifest,
    )
    emit(
        "vc3_r1",
        strip_references(r1),
        {
            "source": PLANAR_PDF_URL,
            "kind": "human-edited exposition of the same result",
            "cut": ["document minus the verbatim block and bibliography"],
        },
        manifest,
    )

    print("pilot:")
    for name, url in PILOT_HTML.items():
        html = requests.get(url, headers=UA, timeout=60).text
        soup = BeautifulSoup(html, "html.parser")
        emit(name, soup.get_text("\n"), {"source": url, "kind": "essay"}, manifest)
    for name, url in PILOT_PDF.items():
        pdf = fetch_pdf(url, OUT / f"_{name}.pdf")
        emit(
            name,
            strip_references(pdf_text(pdf)),
            {"source": url, "kind": "essay"},
            manifest,
        )
    for name, candidates in PILOT_LOCAL_MD.items():
        path = next((c for c in candidates if c.is_file()), None)
        if path is None:
            print(
                f"  skip {name}: not present in this checkout (discarded pilot round)"
            )
            continue
        emit(
            name,
            strip_references(path.read_text(encoding="utf-8")),
            {
                "source": "https://doi.org/10.5281/zenodo.20409683",
                "kind": "spine-first-drafted corpus paper",
            },
            manifest,
        )

    (OUT / "MANIFEST.json").write_text(
        json.dumps({"retrieved": str(date.today()), "items": manifest}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    for tmp in OUT.glob("_*.pdf"):
        tmp.unlink()
    print(f"\nmanifest -> {(OUT / 'MANIFEST.json').relative_to(PAPER_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
