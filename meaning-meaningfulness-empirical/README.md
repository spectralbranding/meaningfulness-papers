[![MIT License](https://img.shields.io/badge/Code-MIT-blue.svg)](../LICENSE)
[![CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY_4.0-lightgrey.svg)](../LICENSE-data)
![Last Updated](https://img.shields.io/badge/updated-2026--05--29-success)

# meaning-meaningfulness-empirical — Paper B 2026ap

**Same Meaning, Different Prose: Spine Preservation and Rendering Equivalence in Organizational Knowledge Work**

Working Paper v1.0.0 — Dmitry Zharnikov ([ORCID 0009-0000-6893-9231](https://orcid.org/0009-0000-6893-9231))

- **Concept DOI**: [10.5281/zenodo.20409701](https://doi.org/10.5281/zenodo.20409701) — always resolves to latest version
- **v1.0.0 DOI**: [10.5281/zenodo.20409702](https://doi.org/10.5281/zenodo.20409702)
- **License**: CC BY 4.0 (paper) + MIT (code + logs)

## Companion theory paper

This empirical paper supplements [**Paper A 2026ao**](../meaning-meaningfulness/) (concept DOI [10.5281/zenodo.20409683](https://doi.org/10.5281/zenodo.20409683)), which introduces the Operator role + three-layer L/S/R decomposition + preservation theorem P4 + axiom A1.

## 1 | Getting Started

This is a paper-slug mirror under the hub at [`meaningfulness-papers/`](..). Hub-level discipline (LICENSE, LICENSE-data, .gitignore, repo-anchor) is inherited from the parent. Slug-level work focuses on the empirical artifacts (spines, renderings, isomorphism analyses, computation code, LLM-call logs).

To work locally:

```bash
git clone https://github.com/spectralbranding/meaningfulness-papers.git
cd meaningfulness-papers/meaning-meaningfulness-empirical
```

Computation scripts under `code/` use Python 3.12 + `uv`. Random seed `42` is fixed at the top of every computation script.

## 2 | Project Layout

### Companion dataset

Cross-language experiment data is published as a Hugging Face dataset with DOI [`10.57967/hf/8971`](https://doi.org/10.57967/hf/8971) — `spectralbranding/meaningfulness-cross-language-rendering` (English + Russian + Chinese renderings across five LLMs from three training-corpus families).

### Headline empirical findings

| Evidence point | Result |
|---|---|
| Focal twin pair Rec (EM2000 + ZW2002 dynamic capabilities) | **Rec = 4** with preserved antecedents |
| KBV twin pair Rec (Grant 1996 + Liebeskind 1996) | **Rec = 4** with preserved antecedents |
| Random-shadow null baseline (n=1,000 size-matched shadows) | Pr(Rec ≥ 4 by chance) = **.000**; observed values ≈ 18 SDs above null mean |
| Substack self-application of Paper B's own substrate (Phase 2) | 11/14 strict / 14/14 semantic / 0 contradicted (within-operator); 9/14 / 14/14 / 0 (cross-operator GPT-4o) |
| Cross-paper Substack rendering of Paper A's full theoretical apparatus (Phase 2.5) | **12/15 / 15/15 / 0 within-operator; 10/15 / 14/15 / 0 cross-operator** — strongest single P4 evidence point |
| Third LinkedIn rendering of focal-pair shared substrate (Phase 3) | **Rec = 4 with all four antecedent edges preserved** |
| Within-vs-cross-operator delta (memory contamination bound) | ~15 percentage-points strict / ~0 semantic |
| Bibliographic-hallucination audit (12 AI-suggested anchors) | 2 verified / 10 negative findings (~83% hallucination rate) |
| β/δ ordering across 5 spines + 5 renderings | β < 1 < δ across all 10 estimates (supportive of Paper A P3 ordering) |

### Repository layout

```
meaning-meaningfulness-empirical/
├── README.md                                              # this file
├── paper.md                                                # ~10,779 words
├── paper.yaml                                              # frontmatter
├── CITATION.cff                                            # citation metadata
├── CONTRIBUTORS.yaml                                       # CRediT roles + AI disclosure
├── PROVENANCE.yaml                                         # public drafting trail
├── SPINE.yaml                                              # v0.4.x semantic substrate
├── VALIDATION_CASE_PB_FOCAL_*.yaml                         # focal-pair source spines + cross-op extractions
├── VALIDATION_CASE_PB_KBV_*.yaml                           # KBV-pair source spines
├── VALIDATION_CASE_PB_SECONDARY_PRECURSOR_*.yaml           # Tushman-O'Reilly standalone precursor
├── VALIDATION_CASE_PB_SELF_APPLICATION_*.yaml              # Phase 2 self-application within + cross-op
├── VALIDATION_CASE_PA_PRACTITIONER_*.yaml                  # Phase 2.5 cross-paper within + cross-op
├── RENDERING_PB_SUBSTACK_PRACTITIONER.md                   # Phase 2 Substack 1,615w
├── RENDERING_PA_PRACTITIONER.md                            # Phase 2.5 cross-paper Substack 2,102w
├── RENDERING_FOCAL_PAIR_THIRD_PROSE.md                     # Phase 3 LinkedIn 1,044w
├── TWIN_PAIR_ISOMORPHISM_PB_FOCAL.md                       # focal-pair preservation analysis
├── TWIN_PAIR_ISOMORPHISM_PB_KBV.md                         # KBV-pair preservation analysis
├── SELF_APPLICATION_ISOMORPHISM_PB.md                      # Phase 2 preservation analysis
├── CROSS_PAPER_P4_ISOMORPHISM.md                           # Phase 2.5 preservation analysis
├── CROSS_OPERATOR_EXTRACTION_RESULTS.md                    # within-vs-cross-operator analysis
├── PHASE1_ANCHOR_VERIFICATION_2026-05-27.md                # SF1 hallucination audit
├── PHASE3_5A_RUSSIAN_RENDERING_PROTOCOL.md                 # v1.1.0 pre-registered Russian protocol
├── PHASE3_5B_MULTI_LLM_OPERATOR_PROTOCOL.md                # v1.1.0 pre-registered multi-LLM protocol
├── PHASE4_KAPPA_MEASUREMENT_2026-05-27.md                  # v1.1.0 pre-registered kappa protocol
├── code/                                                   # companion computation
│   ├── rec_metric.py                                       # twin-pair Rec computation
│   ├── null_baseline.py                                    # random-shadow null distribution
│   ├── cost_function_calibration.py                        # β/δ grid-anchored estimates
│   ├── cross_operator_extraction.py                        # Operator-C extractor harness
│   ├── multi_llm_rendering.py                              # Phase 3.5b execution-ready
│   ├── llm_call_logger.py                                  # JSONL logging single-source schema
│   ├── reconstruct_session_h_logs.py                       # post-hoc reconstruction utility
│   └── README.md
└── logs/                                                   # experimental LLM call provenance (JSONL)
    ├── phase_1_crossref_anchor_verification_calls.jsonl
    ├── phase_2_render_PB_spine_to_substack_practitioner_calls.jsonl
    ├── phase_2_extract_spine_from_substack_rendering_calls.jsonl
    ├── phase_2_prime_extract_spine_from_substack_rendering_PB_via_GPT4_calls.jsonl
    ├── phase_2.5_render_PA_spine_to_substack_practitioner_calls.jsonl
    ├── phase_2.5_extract_spine_from_PA_practitioner_rendering_calls.jsonl
    ├── phase_2.5_prime_extract_spine_from_PA_practitioner_rendering_via_GPT4_calls.jsonl
    ├── phase_3_render_focal_pair_shared_substrate_to_linkedin_calls.jsonl
    ├── phase_3_prime_extract_spine_from_focal_pair_third_rendering_via_GPT4_calls.jsonl
    └── README.md
```

## 3 | Quick Start

All numerical figures cited in `paper.md` are reproducible from companion scripts in `code/` against the published spines in this mirror. Random seed `42` is fixed at the top of every computation script.

```bash
# Twin-pair Rec
uv run python code/rec_metric.py --spine1 VALIDATION_CASE_PB_FOCAL_EISENHARDT_MARTIN_SPINE.yaml --spine2 VALIDATION_CASE_PB_FOCAL_ZOLLO_WINTER_SPINE.yaml

# Null-baseline
uv run python code/null_baseline.py --n-shadows 1000 --seed 42

# Cost-function calibration
uv run python code/cost_function_calibration.py --spines <paths> --renderings <paths> --output cost_calibration.csv

# Cross-operator extraction (requires OPENAI_API_KEY in environment)
uv run python code/cross_operator_extraction.py --rendering RENDERING_PB_SUBSTACK_PRACTITIONER.md --codebook appendix_A_schema --extractor gpt-4o-2024-08-06
```

## 4 | Dependencies

Python 3.12 + `uv` for package management. Cross-operator scripts require `OPENAI_API_KEY` (cross-operator extractor uses `gpt-4o-2024-08-06`); multi-LLM rendering uses additional provider keys per `code/multi_llm_rendering.py`. See per-script docstrings for full requirements.

### LLM-call provenance

Every experimental LLM call producing cited evidence in `paper.md` is logged in JSONL under `logs/` with operator identifier, model version, full prompts, parameters, response, tokens, latency, cost-USD estimate, git SHA, and a redaction pass that strips API keys before write. Internal authoring-process LLM calls (drafting assistance, internal peer-review cycles, AI-assisted literature exploration that does not produce a cited result) are NOT in the public log per the experiment-scope-only publication rule. See [`logs/README.md`](logs/README.md) for schema details and reproduction instructions.

### Versioning trajectory (public)

| Release | Scope addition | Estimated wall-clock |
|---|---|---|
| **v1.0.0** (this release) | Two twin pairs + null baseline + 3 self-application renderings + cross-operator extraction + LLM-call provenance | 2026-05-27 |
| v1.1.0 | Task δ inter-coder κ + Task γ Russian human-native + Phase 3.5b multi-LLM cross-FAMILY | 4–8 weeks post-v1.0.0 |
| v2.0.0 | First prospective lab cohort + larger-N twin-pair extension + β/δ confidence intervals | 6–12 months post-v1.0.0 |
| v3.0.0 | Multi-cohort prospective tracking + DiD identification on Zenodo spine-publication events | 12–18 months post-v1.0.0 |
| v4.0.0 | Submission-scale; falsificational P3 test at organizational-outcome scale | 18–24 months post-v1.0.0 |

Internal drafting across Sessions E + F + G + H was consolidated into this public v1.0.0 release per the project's version-only-at-Zenodo discipline. See [PROVENANCE.yaml](PROVENANCE.yaml) for phase-level drafting summary.

## 5 | Citation

Verbatim title: *Same Meaning, Different Prose: Spine Preservation and Rendering Equivalence in Organizational Knowledge Work*. Concept DOI [10.5281/zenodo.20409701](https://doi.org/10.5281/zenodo.20409701); v1.0.0 version DOI [10.5281/zenodo.20409702](https://doi.org/10.5281/zenodo.20409702). Companion cross-language Hugging Face dataset DOI [10.57967/hf/8971](https://doi.org/10.57967/hf/8971). See [CITATION.cff](CITATION.cff) for machine-readable metadata.

## 6 | Licence

Code (if any): MIT — see hub-level [../LICENSE](../LICENSE). Data, figures, tables: CC BY 4.0 — see hub-level [../LICENSE-data](../LICENSE-data). Paper text: CC BY-NC-ND 4.0 (matches published Zenodo PDF; see [CITATION.cff](CITATION.cff)).

*Last updated: 2026-05-29*
