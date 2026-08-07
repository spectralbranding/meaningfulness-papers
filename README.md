[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--08--07-success)

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

### Paper C — [invention-as-structure/](invention-as-structure/) (2026bg)

**Invention as a Structural Operation: Why the Abductive Jump Is a Re-Coordinatization of the Space of Description, Not a Sensory Leap**

- Concept DOI: [10.5281/zenodo.21653102](https://doi.org/10.5281/zenodo.21653102)
- v1.0.0 DOI: [10.5281/zenodo.21653103](https://doi.org/10.5281/zenodo.21653103)
- License: CC BY 4.0 (paper) + MIT (code)

Position paper relocating the abductive "jump" from an embodied sensory leap to a typed re-coordinatization of the space of description, realized by four atomic moves (adjoin a dimension, rescale or requantize, re-topologize, glue across domains). Within representational systems whose compatibility predicate is decidable the operator set is enumerable and the selection is computable; a deterministic companion demonstration classifies each of the four moves as the account predicts.

### Paper D — [internalization/](internalization/) (2026bk)

**Internalization as an Operation: Recovering the Dependency Structure of a Result, and a Pre-Registered Failure to Do So**

- Concept DOI: [10.5281/zenodo.21828980](https://doi.org/10.5281/zenodo.21828980)
- v1.0.0 DOI: [10.5281/zenodo.21828981](https://doi.org/10.5281/zenodo.21828981)
- License: CC BY 4.0 (paper + data) + MIT (harness, scoring code and call logs)

Specifies internalization — the inverse of Paper A's drafting direction — as a five-step operation that recovers a typed dependency graph from a rendered artifact, negotiates it against a declared reader model, ranks nodes by structural load rather than prose mass, re-renders, and submits the result to an acceptance contract; and supplies its measurement, a reader-relative count of steps verified but not derived. The pre-registered validation failed at its first gate: two machine operators from different model families did not agree on the dependency structure at the declared level, and they diverge on which nodes exist before they diverge on how nodes connect. Under the pre-declared decision rule no downstream quantity is licensed, and the quantities the run nonetheless computed are reported in an appendix rather than in Results. The specification, the instrument, the pilot, three harness defects and the negative result ship together.

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

This hub aggregates four paper-slug subdirectories — Paper A (`meaning-meaningfulness/`) and Paper B (`meaning-meaningfulness-empirical/`), both first published 2026-05-29, Paper C (`invention-as-structure/`, 2026-07-28) and Paper D (`internalization/`, 2026-08-07) — each with its own Zenodo concept DOI. New paper-slugs added to this programme follow the same convention: each subdirectory is a self-contained mirror with its own `paper.md` / `paper.yaml`, `CITATION.cff`, `LICENSE`, `LICENSE-data`, and (where applicable) `reproduce.sh`.

---

## 2 | Project Layout

```
.
├── meaning-meaningfulness/             # Paper A (2026ao) — theory paper
├── meaning-meaningfulness-empirical/   # Paper B (2026ap) — empirical companion
├── invention-as-structure/             # Paper C (2026bg) — position paper + demo
├── internalization/                    # Paper D (2026bk) — specification + pre-registered validation
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
- `invention-as-structure/` — deterministic demonstration; Python 3.12 + PyYAML, no LLM calls.
- `internalization/` — analysis-only reproduction needs no keys and no network (`./reproduce.sh`); re-running the collection itself (`./reproduce.sh --collect`) is a multi-operator LLM pipeline and requires provider credentials.

---

## 5 | Script Map

| Paper-slug | Role | Reproduce entry |
|---|---|---|
| `meaning-meaningfulness/` | Theory paper (P4 preservation theorem + L/S/R decomposition + Operator role) | `paper.md` + appendices; no computational reproduction |
| `meaning-meaningfulness-empirical/` | Empirical companion (Rec = 4 on twin pairs; cross-operator extraction) | `reproduce.sh` inside the slug |
| `invention-as-structure/` | Position paper (four atomic moves of representation change) | `code/four_moves_demo.py` inside the slug |
| `internalization/` | Specification + pre-registered validation (extraction agreement, miracle count) | `reproduce.sh` inside the slug |

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
