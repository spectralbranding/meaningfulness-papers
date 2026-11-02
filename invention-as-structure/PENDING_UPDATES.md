# Pending updates: Invention as a Structural Operation (invention-as-structure)

Status: pending; raised 2026-11-02; source: decision log dz02#l=7 and #l=11 (ARCHIVE/SMD_raw/Решения_Дмитрия_2026-11-02.md); origin: Lex Fridman Podcast #503 (27 Oct 2026), transcript ARCHIVE/lexfridman/lexfridman_transcript.md. Both items are AI drafts (черновик ИИ); the owner decides whether they enter the paper.

Owner instruction (Dmitry, 30.10, for all published papers): do not edit the paper files now; record the required updates here. Concept DOI 10.5281/zenodo.21653102; current version v1.0.0. Line numbers refer to paper.md at commit 8755291.

References marked "check" were written from memory: verify each before it enters invention-as-structure.bib.

## 1. Selection needs a way back: the return term

- Location: "Selection under joint constraints" > "The general-relativity case, corrected", the functional and the paragraph after it, paper.md lines 106-122.
- Problem: S scores the new representation only (axiom description length, symmetry, closure, empirical inadequacy). In the mathematical cases where adjoining dimensions makes a hard problem easy, the gain depends on a map back to the original space with a known loss: semidefinite relaxation followed by rounding (check: Goemans and Williamson 1995, J. ACM 42(6)); under the Unique Games Conjecture this lift-and-round scheme is optimal for every constraint satisfaction problem (check: Raghavendra 2008, STOC); Koopman embeddings that make nonlinear dynamics linear in a lifted space and are useful only through a finite-dimensional projection back (check: Koopman 1931, PNAS 17(5); Brunton, Budisic, Kaiser and Kutz 2022, SIAM Review 64(2)); the kernel trick. The paper's own example already contains the requirement: Einstein dropped the correct curvature structure because it failed the Newtonian limit (lines 100-104), that is, because the new representation did not reduce to the old one where the old one was known to work.
- Change: name the requirement and give it a place in S. Two options for the owner:
  - A. A fifth term R(R', R): the loss of the return map from R' to decisions or predictions stated in R, weighted by a5 >= 0. The Newtonian limit becomes the case where R must be recovered exactly on the old domain.
  - B. A constraint instead of a term: R' is admissible only if a return map to R is given and its loss on the old domain is bounded (a correspondence condition); S ranks only admissible candidates.
- Recommendation: B, because the Zurich notebook case reads as a hard filter (the candidate was dropped, not down-weighted), and a constraint does not add a fifth untested weight to the four the Limitations section already flags (line 254).
- Proposed text (after line 122, option B): "One constraint precedes the score. A candidate R' is admissible only with a return map to R whose loss is bounded where R is known to work. The Newtonian limit is this constraint in the general-relativity case; lift-and-round methods in optimization and Koopman embeddings in dynamics show the same structure, where adjoining dimensions makes a problem easy only because the way back is known."
- Consequence for adjunction (line 39 ff., the move table): an adjunction without a return map is a description, not yet an invention. Applied systems that record moves (the smd-engine `move` field, the orgschema-lab growth candidates) can require the return map as a field; that is an engineering change outside this paper.
- Version: minor, v1.0.0 to v1.1.0 (paper.md, CITATION.cff, README, Data and Code Availability line 306), new Zenodo version under the concept DOI.

## 2. Evolution: selection also makes instances easy for the heuristics in use

- Location: "The same moves without a mind: evolution", the paragraph after the four bullets, paper.md lines 201-209; optionally "The same move in markets", line 211 ff.
- Addition: evolution does not only select solutions; it selects problem instances that the available heuristics solve well. Protein folding is hard in the worst case, yet the sequences that exist fold reliably, because sequences whose folding the cellular process got wrong did not persist (A. Moitra in the podcast, transcript lines 949-957; check: Bryngelson and Wolynes 1987, PNAS 84(21), the principle of minimal frustration and the folding funnel). The consequence for the account: what makes a domain tractable can be a property of the instances that selection left, not of the representation alone, so a search that is blind over the problem class can be fast over the instances that occur.
- Proposed text (after line 209): "Selection acts on the instances as well as on the solutions. Sequences whose folding the available process got wrong do not persist, so the proteins that exist sit in the easy region of a problem that is hard in the worst case. Part of what an observer reads as the efficiency of a search is the selection of instances that suit it."
- Markets analogue (optional, line 211 ff.): an owner-operated firm is selected to run well under its owner's own heuristics; a successor or buyer meets the same firm as a harder instance. The organizational development of this point belongs to succession-rotation (orgschema-papers, PENDING_UPDATES item 5), not here.
- Version: part of the release in item 1.

## 3. Evidence for the glue move: finding the shared substructure is the hard step

Raised 2026-11-02; source dz02#l=19 (Dmitry asked to read the paper); AI draft (черновик ИИ). Registered in the spectral-branding substrate as `schapiro-2025-measuring-combinatorial-creativity`.

- Source: Schapiro, Jagadish, Gladstone, Liu, Shashidhar, Black, Moon, Hakkani-Tur, Ji, Stevenson, Varshney, Beaty, Griffiths and Evans, "Measuring Combinatorial Creativity in Large Language Models and Humans", arXiv:2509.21043, v6 2026-10-07, under review, CC BY 4.0; DOI 10.48550/arXiv.2509.21043.
- What it measures: the Kombine benchmark gives random cross-domain pairs of Wikidata entities and asks for an association, an analogy and a conceptual blend. A blend needs a generic space that both inputs instantiate, then a blended space. Across 35 language models, a valid generic space is found in 43.4% of blends, and given a valid generic space the blend is coherent in 97.1%. The authors call this the abstraction bottleneck.
- Location: "A structural account of invention", the gluing row and the sentence "Gluing is a pullback over a shared substructure, not a mixture" (paper.md, the move table after line 39); optionally "Rivals", where Fauconnier-Turner blending is named.
- Proposed text: "The difficulty of gluing sits in finding the shared substructure, not in forming the composite: on a cross-domain blending benchmark, models found a valid generic space in under half of the attempts, and once one was found the blend was coherent in nearly all of them [@schapiro-2025-measuring-combinatorial-creativity]. The benchmark's integration scale (single-scope, a shared slot both inputs organize, an emergent element) is a usable test of whether a proposed glue is a pullback or a juxtaposition."
- Limits to state with it: validity is judged by a panel of three language models with fair agreement (ICC 0.48-0.67), the human sample is lay and online, and the scores (utility, embedding-distance surprise, pool-relative originality) have no analogue of the axiom description length, symmetry or closure terms of S. The benchmark therefore supports the location of difficulty in the glue move; it does not test S or the mechanizability claim.
- Bibliography: add the BibTeX entry from spectral-branding `research/bibtex/schapiro-2025-measuring-combinatorial-creativity.bib` to invention-as-structure.bib.
- Version: part of the release in item 1.
