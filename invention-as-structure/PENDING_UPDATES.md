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
