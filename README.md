[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# meaningfulness-papers

Public mirror for the meaningfulness research programme by Dmitry Zharnikov (ORCID [0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231)). The programme theorizes how research-paper artifacts maintain meaning across renderings under generative-AI cost-asymmetry, with empirical demonstration on management-theory twin pairs.

The meaningfulness programme parallel-tracks but is distinct from the SBT (Spectral Branding Theory) and OST (Organizational Schema Theory) programmes. Where SBT theorizes perception-rendering at the brand level and OST theorizes specification-rendering at the organizational level, the meaningfulness programme theorizes substrate-and-rendering at the propositional-knowledge-artifact level — a level both SBT and OST artifacts instantiate.

## Papers

### Paper A — [meaning-meaningfulness/](meaning-meaningfulness/) (2026ao)

**Spec-Based Research in the Post-AI Era: A Cost-Asymmetry Theory of Meaning and Meaningfulness in Organizational Knowledge Work**

- Concept DOI: [10.5281/zenodo.20409683](https://doi.org/10.5281/zenodo.20409683)
- v1.0.0 DOI: [10.5281/zenodo.20409684](https://doi.org/10.5281/zenodo.20409684)
- License: CC BY 4.0 (paper) + MIT (code)

Theory paper introducing the **Operator role** as the level-of-analysis above the human-vs-AI instance distinction, the three-layer **L** (log substrate) → **S** (semantic spine) → **R** (rendering) decomposition, and the preservation theorem **P4** (rendering-equivalence under spine-preservation) under axiom **A1** (σ-faithfulness on locked subsets). Companion historical existence proof on Heisenberg's matrix mechanics + Schrödinger's wave mechanics. Four online appendices (substrate schema; spine-first drafting protocol; cost-asymmetry simulation; historical existence proof).

### Paper B — [meaning-meaningfulness-empirical/](meaning-meaningfulness-empirical/) (2026ap)

**Same Meaning, Different Prose: Spine Preservation and Rendering Equivalence in Organizational Knowledge Work**

- Concept DOI: [10.5281/zenodo.20409701](https://doi.org/10.5281/zenodo.20409701)
- v1.0.0 DOI: [10.5281/zenodo.20409702](https://doi.org/10.5281/zenodo.20409702)
- License: CC BY 4.0 (paper) + MIT (code + logs)

Empirical companion that demonstrates Paper A's **P4** on two management-theory twin pairs (dynamic-capabilities Eisenhardt-Martin 2000 + Zollo-Winter 2002; knowledge-based view Grant 1996 + Liebeskind 1996) at Rec = 4 with random-shadow null at 99th+ percentile, plus three self-application renderings (Substack practitioner of Paper B; LinkedIn third rendering of focal-pair shared substrate; cross-paper Substack practitioner rendering of Paper A's full theoretical apparatus). Cross-operator extraction discipline (Operator B Claude renderer ≠ Operator C GPT-4o extractor) bounds within-model memory contamination at ~15 percentage-points strict / ~0 semantic.

## License

CC BY 4.0 for the paper text and theoretical content; MIT License for companion computation code and experimental JSONL logs. See [LICENSE](LICENSE).

## Citation

For Paper A, cite the v1.0.0 DOI [10.5281/zenodo.20409684](https://doi.org/10.5281/zenodo.20409684) or the concept DOI [10.5281/zenodo.20409683](https://doi.org/10.5281/zenodo.20409683) (resolves to latest version). For Paper B, cite [10.5281/zenodo.20409702](https://doi.org/10.5281/zenodo.20409702) (v1.0.0) or [10.5281/zenodo.20409701](https://doi.org/10.5281/zenodo.20409701) (concept). Each paper directory contains a CITATION.cff for tool-friendly citation.

## Related programmes

- [sbt-papers](https://github.com/spectralbranding/sbt-papers) — Spectral Branding Theory
- [orgschema-papers](https://github.com/spectralbranding/orgschema-papers) — Organizational Schema Theory

---

## 1 | Getting Started

Clone the hub and pick a paper-slug to work with:

```bash
git clone https://github.com/spectralbranding/meaningfulness-papers.git
cd meaningfulness-papers
```

The hub itself is index-only. Reproducible computation lives inside each paper-slug subdirectory (see section 2). The hub anchor is `pyproject.toml` at the root.

This hub aggregates two paper-slug subdirectories — Paper A (`meaning-meaningfulness/`) and Paper B (`meaning-meaningfulness-empirical/`) — both first published 2026-05-29 with Zenodo concept DOIs. New paper-slugs added to this programme follow the same convention: each subdirectory is a self-contained mirror with its own `paper.md` / `paper.yaml`, `CITATION.cff`, `LICENSE`, `LICENSE-data`, and (where applicable) `reproduce.sh`.

---

## 2 | Project Layout

```
.
├── meaning-meaningfulness/             # Paper A (2026ao) — theory paper
├── meaning-meaningfulness-empirical/   # Paper B (2026ap) — empirical companion
├── output/
│   ├── figures/
│   ├── tables/
│   └── logs/                           # Hub run logs (per-paper logs live inside each slug)
├── CITATION.cff                        # Hub-level machine-readable citation
├── LICENSE                             # MIT (code) + CC BY 4.0 (text/data) — see file
├── LICENSE-data                        # CC BY 4.0 (data, figures, tables)
├── pyproject.toml                      # Hub project anchor
├── reproduce.sh                        # Hub-level orchestrator (iterates per-paper)
├── README.md                           # This file
└── .gitignore
```

Each paper-slug subdirectory is itself a self-contained mirror; consult its own `README.md` for paper-specific layout and dependencies.

---

## 3 | Quick Start

Reproduce every per-paper pipeline from this hub root:

```bash
./reproduce.sh                  # Run every per-paper reproduce.sh
./reproduce.sh --check-only     # Verify per-paper orchestrators exist
./reproduce.sh --fast           # Pass --fast through to each per-paper script
```

The hub orchestrator iterates over paper-slug subdirectories containing `paper.md` or `paper.yaml`, invoking each per-paper `reproduce.sh` if present. Hub run logs land in `output/logs/hub_run.log`; per-paper outputs land inside each paper-slug's own `output/` tree.

---

## 4 | Dependencies

### Python ≥ 3.12

Pinned in each paper-slug's `pyproject.toml`. The hub itself has no analysis dependencies beyond the orchestrator shell script.

```bash
uv sync   # inside any paper-slug subdirectory
```

### Per-paper dependencies

- `meaning-meaningfulness/` — pure-theory paper; reproduction is conceptual, no LLM calls.
- `meaning-meaningfulness-empirical/` — multi-operator LLM pipeline (renderer ≠ extractor); requires API keys per `.env.example` inside that subdirectory. See its `README.md` for the operator list and key requirements.

---

## 5 | Script Map

| Paper-slug | Role | Reproduce entry |
|---|---|---|
| `meaning-meaningfulness/` | Theory paper (P4 preservation theorem + L/S/R decomposition + Operator role) | `paper.md` + appendices; no computational reproduction |
| `meaning-meaningfulness-empirical/` | Empirical companion (Rec = 4 on twin pairs; cross-operator extraction) | `reproduce.sh` inside the slug |

---

## 6 | Citation

If you build on this work, please cite the relevant paper directly:

> Dmitry Zharnikov (2026). "Spec-Based Research in the Post-AI Era: A Cost-Asymmetry Theory of Meaning and Meaningfulness in Organizational Knowledge Work." Concept DOI [10.5281/zenodo.20409683](https://doi.org/10.5281/zenodo.20409683).

> Dmitry Zharnikov (2026). "Same Meaning, Different Prose: Spine Preservation and Rendering Equivalence in Organizational Knowledge Work." Concept DOI [10.5281/zenodo.20409701](https://doi.org/10.5281/zenodo.20409701).

Machine-readable citation: see [`CITATION.cff`](CITATION.cff) at this hub root, plus the per-paper `CITATION.cff` inside each paper-slug subdirectory.

---

## 7 | Licence

- **Code** — © Dmitry Zharnikov, 2026. [MIT Licence](LICENSE).
- **Data, figures, tables, paper text** — © Dmitry Zharnikov, 2026. [CC BY 4.0](LICENSE-data).

Both licences permit reuse with attribution. The MIT Licence permits modification and redistribution of code; CC BY 4.0 permits any reuse of data and rendered artifacts with attribution to the author and citation of the concept DOIs above.

---

*Last updated: 2026-05-29*
