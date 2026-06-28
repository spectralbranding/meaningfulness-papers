---
title: "Phase 1 anchor verification — 12 AI-suggested anchors"
date: 2026-05-27
method: Crossref Stage-1 query.title+query.author bibliographic match, rows=5
---

# Phase 1 anchor verification

Every AI-suggested anchor must be Crossref-verified before integration into paper.md or external_anchors.

## Verification verdict table

| ID | AI-suggested claim | Verdict | DOI | Best Crossref match |
|---|---|---|---|---|
| A01 | Kaplan, S., & Vakili, K. (2015). The double-edged sword of recombination in breakthrough innovation. SMJ.… | **NF-NEAR-MATCH** | 10.1002/smj.2294 | The double‐edged sword of recombination in breakthrough innovation (2014) in Strategic Management Journal |
| A02 | Felin, T., & Zenger, T. R. (2023). The theory of the firm and AI: Beyond black boxes. Strategy Science. [flagged for verification… | **NF-FABRICATED** | 10.2139/ssrn.2156951 | Open Innovation, Problem Solving, and the Theory of the (Innovative) Firm (2012) in SSRN Electronic Journal |
| A03 | Raisch, S., & Furr, N. (2024). The generative lens: AI as a catalyst for new theory. Academy of Management Review. [flagged for verification… | **NF-FABRICATED** | 10.5465/amproc.2024.21431abstract | Collaboration Between Humans and AI: Complementarities Within and Across Skill (2024) in Academy of Management Proceedings |
| A04 | Puranam, P., et al. (2024). Generative AI and the future of organizational theory. Organization Science.… | **NF-FABRICATED** | 10.2139/ssrn.6028034 | The Impact of Generative AI Adoption on Organizational Networks: Evidence From A Field Experiment (2026) in SSRN Electronic Journal |
| A05 | Girotra, K., Meincke, L., Terwiesch, C., & Ulrich, K. T. (2023). Ideas are dimes a dozen: The value of ideation in innov… | **NF-NEAR-MATCH** | 10.2139/ssrn.4526071 | Ideas are Dimes a Dozen: Large Language Models for Idea Generation in Innovation (2023) in SSRN Electronic Journal |
| A06 | Lifshitz-Assaf, H., et al. (2024). AI and the transformation of R&D. Research Policy.… | **NF-FABRICATED** | 10.5465/amproc.2025.12158symposium | Innovating with AI: Exploring the Impact of Generative AI on Creative Processes (2025) in Academy of Management Proceedings |
| A07 | Bingham, C. B., & Eisenhardt, K. M. (2024). The search for simplicity in strategy. SMJ. [flagged for verification; audit flag… | **NF-FABRICATED** | 10.1093/acrefore/9780190224851.013.458 | Simple Rules and Other Heuristics in Strategy and Organizational Research (2025) in Oxford Research Encyclopedia of Business and Management |
| A08 | Teece, D. J. (2023). Dynamic capabilities in the age of AI. Industrial and Corporate Change.… | **NF-NEAR-MATCH** | 10.1017/9781009562713 | Dynamic Capabilities (2025) in — |
| A09 | von Krogh, G., et al. (2024). Artificial intelligence in management: A review and research agenda. Journal of Management… | **NF-FABRICATED** | 10.5465/amj.2023.4002 | Recognizing and Utilizing Novel Research Opportunities with Artificial Intelligence (2023) in Academy of Management Journal |
| A10 | Levinthal, D., & March, J. G. (1993/2025 retrospective). The myopia of learning [updated commentary].… | **VERIFIED** | 10.1002/smj.4250141009 | The myopia of learning (1993) in Strategic Management Journal |
| A11 | Camuffo, A., et al. (2024). Scientific decision-making and the replication crisis in management. SMJ.… | **NF-FABRICATED** | 10.1002/smj.3580 | A scientific approach to entrepreneurial decision‐making: Large‐scale replication and extension (2024) in Strategic Management Journal |
| A12 | Ethiraj, S. K., et al. (2024). The next frontier in strategy research: Computational approaches. Strategic Management Jo… | **NF-FABRICATED** | 10.2514/6.1989-129 | Computational studies of hard-body and 3-D effects in plume flows (1989) in 27th Aerospace Sciences Meeting |

## Per-anchor detail

### A01 — NF-NEAR-MATCH

- **AI-suggested claim**: Kaplan, S., & Vakili, K. (2015). The double-edged sword of recombination in breakthrough innovation. SMJ.
- **Note**: Already cited in v1.0.0 (NF15-era verification); already in external_anchors v0.1.1
- **Verdict**: NF-NEAR-MATCH
- **DOI**: 10.1002/smj.2294
- **Matched title**: The double‐edged sword of recombination in breakthrough innovation
- **Matched authors**: sarah kaplan keyvan vakili
- **Matched year / venue**: 2014 / Strategic Management Journal
- **Jaccard+year score**: 0.85
- **Rationale**: Adjacent paper found: 'The double‐edged sword of recombination in breakthrough innovation' (2014) by sarah kaplan keyvan vakili in 'Strategic Management Journal'. Year/title diverges from the AI-suggested claim (2015 / 'The double-edged sword of recombination in breakthrough innovation').

### A02 — NF-FABRICATED

- **AI-suggested claim**: Felin, T., & Zenger, T. R. (2023). The theory of the firm and AI: Beyond black boxes. Strategy Science. [flagged for verification]
- **Verdict**: NF-FABRICATED
- **DOI**: 10.2139/ssrn.2156951
- **Matched title**: Open Innovation, Problem Solving, and the Theory of the (Innovative) Firm
- **Matched authors**: teppo felin todd r. zenger
- **Matched year / venue**: 2012 / SSRN Electronic Journal
- **Jaccard+year score**: 0.25
- **Rationale**: Best Crossref hit 'Open Innovation, Problem Solving, and the Theory of the (Innovative) Firm' (2012) by teppo felin todd r. zenger does not match the AI-suggested claim (2023 / 'The theory of the firm and AI: Beyond black boxes'). Likely hallucination.

### A03 — NF-FABRICATED

- **AI-suggested claim**: Raisch, S., & Furr, N. (2024). The generative lens: AI as a catalyst for new theory. Academy of Management Review. [flagged for verification]
- **Verdict**: NF-FABRICATED
- **DOI**: 10.5465/amproc.2024.21431abstract
- **Matched title**: Collaboration Between Humans and AI: Complementarities Within and Across Skill
- **Matched authors**: kateryna fomina sebastian raisch
- **Matched year / venue**: 2024 / Academy of Management Proceedings
- **Jaccard+year score**: 0.339
- **Rationale**: Best Crossref hit 'Collaboration Between Humans and AI: Complementarities Within and Across Skill' (2024) by kateryna fomina sebastian raisch does not match the AI-suggested claim (2024 / 'The generative lens: AI as a catalyst for new theory'). Likely hallucination.

### A04 — NF-FABRICATED

- **AI-suggested claim**: Puranam, P., et al. (2024). Generative AI and the future of organizational theory. Organization Science.
- **Verdict**: NF-FABRICATED
- **DOI**: 10.2139/ssrn.6028034
- **Matched title**: The Impact of Generative AI Adoption on Organizational Networks: Evidence From A Field Experiment
- **Matched authors**: ralf buechsenschuss irmela koch-bayram dr. torsten biemann phanish puranam
- **Matched year / venue**: 2026 / SSRN Electronic Journal
- **Jaccard+year score**: 0.356
- **Rationale**: Best Crossref hit 'The Impact of Generative AI Adoption on Organizational Networks: Evidence From A Field Experiment' (2026) by ralf buechsenschuss irmela koch-bayram dr. torsten biemann phanish puranam does not match the AI-suggested claim (2024 / 'Generative AI and the future of organizational theory'). Likely hallucination.

### A05 — NF-NEAR-MATCH

- **AI-suggested claim**: Girotra, K., Meincke, L., Terwiesch, C., & Ulrich, K. T. (2023). Ideas are dimes a dozen: The value of ideation in innovation contests. Management Science.
- **Verdict**: NF-NEAR-MATCH
- **DOI**: 10.2139/ssrn.4526071
- **Matched title**: Ideas are Dimes a Dozen: Large Language Models for Idea Generation in Innovation
- **Matched authors**: karan girotra lennart meincke christian terwiesch karl t. ulrich
- **Matched year / venue**: 2023 / SSRN Electronic Journal
- **Jaccard+year score**: 0.572
- **Rationale**: Adjacent paper found: 'Ideas are Dimes a Dozen: Large Language Models for Idea Generation in Innovation' (2023) by karan girotra lennart meincke christian terwiesch karl t. ulrich in 'SSRN Electronic Journal'. Year/title diverges from the AI-suggested claim (2023 / 'Ideas are dimes a dozen: The value of ideation in innovation contests').

### A06 — NF-FABRICATED

- **AI-suggested claim**: Lifshitz-Assaf, H., et al. (2024). AI and the transformation of R&D. Research Policy.
- **Verdict**: NF-FABRICATED
- **DOI**: 10.5465/amproc.2025.12158symposium
- **Matched title**: Innovating with AI: Exploring the Impact of Generative AI on Creative Processes
- **Matched authors**: moran lazar deborah mateja lebogang nthoiwa hila lifshitz-assaf sebastian raisch rembrand michael koning
- **Matched year / venue**: 2025 / Academy of Management Proceedings
- **Jaccard+year score**: 0.3
- **Rationale**: Best Crossref hit 'Innovating with AI: Exploring the Impact of Generative AI on Creative Processes' (2025) by moran lazar deborah mateja lebogang nthoiwa hila lifshitz-assaf sebastian raisch rembrand michael koning does not match the AI-suggested claim (2024 / 'AI and the transformation of R&D'). Likely hallucination.

### A07 — NF-FABRICATED

- **AI-suggested claim**: Bingham, C. B., & Eisenhardt, K. M. (2024). The search for simplicity in strategy. SMJ. [flagged for verification; audit flagged prior hallucination NF15-adjacent]
- **Verdict**: NF-FABRICATED
- **DOI**: 10.1093/acrefore/9780190224851.013.458
- **Matched title**: Simple Rules and Other Heuristics in Strategy and Organizational Research
- **Matched authors**: kathleen m. eisenhardt christopher b. bingham
- **Matched year / venue**: 2025 / Oxford Research Encyclopedia of Business and Management
- **Jaccard+year score**: 0.258
- **Rationale**: Best Crossref hit 'Simple Rules and Other Heuristics in Strategy and Organizational Research' (2025) by kathleen m. eisenhardt christopher b. bingham does not match the AI-suggested claim (2024 / 'The search for simplicity in strategy'). Likely hallucination.

### A08 — NF-NEAR-MATCH

- **AI-suggested claim**: Teece, D. J. (2023). Dynamic capabilities in the age of AI. Industrial and Corporate Change.
- **Verdict**: NF-NEAR-MATCH
- **DOI**: 10.1017/9781009562713
- **Matched title**: Dynamic Capabilities
- **Matched authors**: david j. teece
- **Matched year / venue**: 2025 / —
- **Jaccard+year score**: 0.35
- **Rationale**: Adjacent paper found: 'Dynamic Capabilities' (2025) by david j. teece in ''. Year/title diverges from the AI-suggested claim (2023 / 'Dynamic capabilities in the age of AI').

### A09 — NF-FABRICATED

- **AI-suggested claim**: von Krogh, G., et al. (2024). Artificial intelligence in management: A review and research agenda. Journal of Management.
- **Verdict**: NF-FABRICATED
- **DOI**: 10.5465/amj.2023.4002
- **Matched title**: Recognizing and Utilizing Novel Research Opportunities with Artificial Intelligence
- **Matched authors**: georg von krogh quinetta roberson marc gruber
- **Matched year / venue**: 2023 / Academy of Management Journal
- **Jaccard+year score**: 0.35
- **Rationale**: Best Crossref hit 'Recognizing and Utilizing Novel Research Opportunities with Artificial Intelligence' (2023) by georg von krogh quinetta roberson marc gruber does not match the AI-suggested claim (2024 / 'Artificial intelligence in management: A review and research agenda'). Likely hallucination.

### A10 — VERIFIED

- **AI-suggested claim**: Levinthal, D., & March, J. G. (1993/2025 retrospective). The myopia of learning [updated commentary].
- **Note**: the AI reviewer claimed a 2025 retrospective commentary; 1993 original is verifiable
- **Verdict**: VERIFIED
- **DOI**: 10.1002/smj.4250141009
- **Matched title**: The myopia of learning
- **Matched authors**: daniel a. levinthal james g. march
- **Matched year / venue**: 1993 / Strategic Management Journal
- **Jaccard+year score**: 1.0
- **Rationale**: Title exact/subset match; year 1993 matches; author overlap on ['Levinthal', 'March'].

### A11 — NF-FABRICATED

- **AI-suggested claim**: Camuffo, A., et al. (2024). Scientific decision-making and the replication crisis in management. SMJ.
- **Verdict**: NF-FABRICATED
- **DOI**: 10.1002/smj.3580
- **Matched title**: A scientific approach to entrepreneurial decision‐making: Large‐scale replication and extension
- **Matched authors**: arnaldo camuffo alfonso gambardella danilo messinese elena novelli emilio paolucci chiara spina
- **Matched year / venue**: 2024 / Strategic Management Journal
- **Jaccard+year score**: 0.5
- **Rationale**: Best Crossref hit 'A scientific approach to entrepreneurial decision‐making: Large‐scale replication and extension' (2024) by arnaldo camuffo alfonso gambardella danilo messinese elena novelli emilio paolucci chiara spina does not match the AI-suggested claim (2024 / 'Scientific decision-making and the replication crisis in management'). Likely hallucination.

### A12 — NF-FABRICATED

- **AI-suggested claim**: Ethiraj, S. K., et al. (2024). The next frontier in strategy research: Computational approaches. Strategic Management Journal.
- **Verdict**: NF-FABRICATED
- **DOI**: 10.2514/6.1989-129
- **Matched title**: Computational studies of hard-body and 3-D effects in plume flows
- **Matched authors**: ethiraj venkatapathy william feiereisen shigeru obayashi
- **Matched year / venue**: 1989 / 27th Aerospace Sciences Meeting
- **Jaccard+year score**: 0.087
- **Rationale**: Best Crossref hit 'Computational studies of hard-body and 3-D effects in plume flows' (1989) by ethiraj venkatapathy william feiereisen shigeru obayashi does not match the AI-suggested claim (2024 / 'The next frontier in strategy research: Computational approaches'). Likely hallucination.

## Aggregate

- VERIFIED: 1/12
- NF-NEAR-MATCH: 3/12
- NF-FABRICATED: 8/12
- ERROR: 0/12

Hallucination rate (NF-FABRICATED + NF-NEAR-MATCH): 92% — corpus precedent ~57%. The unusually high rate this round reflects the AI reviewer's tendency to retrofit citation patterns for tier-1 management venues (SMJ / AMR / Org Sci / JoM / MS) where authoritative-sounding 2023-2024 titles get fabricated to fit the requested integration-with-strategy-literature gap.

## Final integration verdict (post-script human review)

The raw classifier flags A01 as NF-NEAR-MATCH on a year mismatch (Crossref's metadata records 2014 early-view publication; the paper IS in SMJ 36(10) 2015 with DOI 10.1002/smj.2294 — Wiley's early-view-vs-issue date convention). Human override: A01 is **VERIFIED** and is already in SPINE.yaml v0.2.0 external_anchors as `kaplan-vakili-2015-double-edged-sword-recombination`.

For A10 (Levinthal-March 1993), the underlying 1993 paper IS verifiable (DOI 10.1002/smj.4250141009; SMJ 14(S2):95-112), but the AI-suggested "2025 retrospective commentary" component is unverified and is dropped from the integration claim. The integration claim becomes: cite Levinthal & March 1993 myopia-of-learning original as antecedent for the dynamic-capabilities pair's learning-mechanism nodes (L2 in TWIN_PAIR_ISOMORPHISM_PB_FOCAL.md already names "Levitt and March (1988) organizational learning" as antecedent — Levinthal-March 1993 is the adjacent extension applicable to the KBV pair's K1/K3 knowledge-integration nodes).

### Integration-ready anchors (2 of 12)

| ID | Citation | DOI | Integration scope in v1.0.0 |
|---|---|---|---|
| A01 | Kaplan, S., & Vakili, K. (2015). The double-edged sword of recombination in breakthrough innovation. *Strategic Management Journal*, 36(10), 1435–1457. | 10.1002/smj.2294 | Already in spine v0.2.0 external_anchors. Strengthen theoretical link in §Theory (recombinant search positioning of Rec metric); already referenced in Method §Rec metric construct-validity contrast. |
| A10 | Levinthal, D. A., & March, J. G. (1993). The myopia of learning. *Strategic Management Journal*, 14(S2), 95–112. | 10.1002/smj.4250141009 | NEW external_anchor at v0.3.1. Integrate into §Theory as organizational-learning antecedent for the KBV pair's K1 / K3 substrate nodes (knowledge-integration / tacit-vs-explicit). Discard the unverifiable "2025 retrospective" embellishment. |

### NF entries to add to SPINE.yaml v0.3.1 (10 of 12)

NF19 through NF28 record each non-integrating anchor with the actual adjacent Crossref hit (where one was found) so future cycles do not re-suggest the same hallucination:

| New NF ID | AI-suggested claim | Real adjacent paper (or "no adjacent") |
|---|---|---|
| NF19 (A02) | Felin & Zenger 2023 *Strategy Science* "The theory of the firm and AI: Beyond black boxes" | Felin & Zenger 2012 SSRN "Open Innovation, Problem Solving, and the Theory of the (Innovative) Firm" — different topic, 11 years off |
| NF20 (A03) | Raisch & Furr 2024 *AMR* "The generative lens: AI as a catalyst for new theory" | Fomina & Raisch 2024 *AMP* "Collaboration Between Humans and AI" — Raisch is author but Furr is not; title/venue differ |
| NF21 (A04) | Puranam et al. 2024 *Org Sci* "Generative AI and the future of organizational theory" | Buechsenschuss-Koch-Bayram-Biemann-Puranam 2026 SSRN "Impact of Generative AI Adoption on Organizational Networks" — Puranam is author but topic/venue/year differ |
| NF22 (A05) | Girotra-Meincke-Terwiesch-Ulrich 2023 *Management Science* "Ideas are dimes a dozen: The value of ideation in innovation contests" | Same author quartet at SSRN 2023 "Ideas are Dimes a Dozen: Large Language Models for Idea Generation in Innovation" — author + half-title match; venue (SSRN preprint not MS) and subtitle differ. Real paper exists as preprint; not yet published in MS as of Crossref query time. |
| NF23 (A06) | Lifshitz-Assaf et al. 2024 *Research Policy* "AI and the transformation of R&D" | Lazar-Mateja-Nthoiwa-Lifshitz-Assaf-Raisch-Bommasani et al. 2025 AMP "Innovating with AI: Exploring the Impact of Generative AI on Creative Processes" — Lifshitz-Assaf is author but venue/year/title differ |
| NF24 (A07) | Bingham & Eisenhardt 2024 SMJ "The search for simplicity in strategy" | Eisenhardt & Bingham 2025 Oxford Research Encyclopedia "Simple Rules and Other Heuristics in Strategy and Organizational Research" — author pair real but venue/year/title differ. NF15-adjacent (prior r1 hallucination). |
| NF25 (A08) | Teece 2023 *ICC* "Dynamic capabilities in the age of AI" | Teece 2025 Cambridge book "Dynamic Capabilities" — Teece + DC topic real, but no 2023 ICC paper on AI-DC. Likely hallucination. |
| NF26 (A09) | von Krogh et al. 2024 *Journal of Management* "Artificial intelligence in management: A review and research agenda" | von Krogh-Roberson-Gruber 2023 *AMJ* "Recognizing and Utilizing Novel Research Opportunities with Artificial Intelligence" — von Krogh + AI topic real, but venue (AMJ not JoM) / year / title differ |
| NF27 (A11) | Camuffo et al. 2024 SMJ "Scientific decision-making and the replication crisis in management" | Camuffo-Gambardella-Messinese-Novelli-Paolucci-Spina 2024 SMJ "A scientific approach to entrepreneurial decision-making: Large-scale replication and extension" — Camuffo + 2024 SMJ + replication theme real, but title differs substantially. Title appears retrofitted to Grok's "replication crisis" framing. |
| NF28 (A12) | Ethiraj et al. 2024 SMJ "The next frontier in strategy research: Computational approaches" | No adjacent paper found. Closest Crossref hit is a 1989 aerospace engineering paper by an unrelated "Ethiraj Venkatapathy." Fully fabricated. |

### Recommendation to Phase 5 integration pass

- INTEGRATE A01 and A10 only (2 anchors); add A10 as new external_anchor in SPINE.yaml v0.3.1.
- DO NOT integrate A02-A09, A11, A12.
- Record NF19-NF28 in SPINE.yaml v0.3.1 negative_findings.
- Phase 5b jargon-translation pass may engage the broader recombinant-search / cognitive-frames / knowledge-representation literature using verified anchors already in the corpus or already in SPINE v0.2.0 external_anchors (Carlile 2004, Raisch & Krakowski 2021, Nickerson & Zenger 2004, Felin-Kauffman-Zenger 2023, Kaplan & Vakili 2015) without relying on the AI reviewer's hallucinated suggestions.

