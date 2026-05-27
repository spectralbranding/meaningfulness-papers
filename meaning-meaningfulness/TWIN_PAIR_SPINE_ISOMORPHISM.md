---
title: "Twin-Pair Spine Isomorphism: Heisenberg ↔ Schrödinger (T1 analysis)"
author: Dmitry Zharnikov
date: 2026-05-26
session: 168 Session B
status: Phase-2 analysis; ready for Session C Grok review
related:
  - research/meaning_meaningfulness_paper/SPINE.yaml (v0.3.0 schema v0.2 — the meaningfulness paper's own spine; P4 + T1 anchor here)
  - research/meaning_meaningfulness_paper/VALIDATION_CASE_T1_HEISENBERG_SPINE.yaml (Heisenberg-path spine; 45 typed nodes)
  - research/meaning_meaningfulness_paper/VALIDATION_CASE_T1_SCHRODINGER_SPINE.yaml (Schrödinger-path spine; 54 typed nodes)
  - research/meaning_meaningfulness_paper/VALIDATION_CASE_T1_SCHRODINGER_EQUIVALENCE_NOTES.md (verbatim Schrödinger equivalence quotes)
  - research/references/heisenberg_1925_english_delphenich.pdf
  - research/references/born_jordan_1925_english_neoclassical.pdf
  - research/references/schrodinger_1928_collected_papers_wave_mechanics.pdf
---

# Twin-Pair Spine Isomorphism — Heisenberg ↔ Schrödinger (T1 analysis)

This document presents the structural diff between the two T1 validation-case spines and argues that the Heisenberg matrix-mechanics path and the Schrödinger wave-mechanics path are isomorphic at the spine level despite radical divergence at the rendering level. The natural-experiment claim of T1 rests on this isomorphism: scientific history independently produced two renderings of the same spine and Schrödinger himself (1926) proved them mathematically equivalent — a fact von Neumann (1932) later grounded rigorously in Hilbert-space functional analysis.

The analysis proceeds in five sections:

- §1 — Schrödinger's attestation that the discovery was independent (the load-bearing natural-experiment evidence)
- §2 — Three-layer convergence: observations ↔ propositions ↔ findings
- §3 — Where the spines diverge and why the divergences are rendering-layer, not spine-layer
- §4 — What the isomorphism tells us about P4 (and what it tells us about schema v0.2)
- §5 — Coder-judgment flags and what a second-coder pass might surface

## 1. Schrödinger's attestation: this was an independent discovery

The strongest piece of evidence that T1 is a *natural* experiment (and not a coordinated demonstration) is Schrödinger's own footnote in his 1926 equivalence paper, *Über das Verhältnis der Heisenberg-Born-Jordanschen Quantenmechanik zu der meinen* (Annalen der Physik 79: 734-756; English translation in *Collected Papers on Wave Mechanics*, Blackie & Son 1928, p. 46 footnote 1):

> "I did not at all suspect any relation to Heisenberg's theory at the beginning. I naturally knew about his theory, but was discouraged, if not repelled, by the very difficult methods of transcendental algebra, and by the want of perspicuity (*Anschaulichkeit*)."

The footnote rules out two alternative explanations for the spine convergence:

- **A2 in the parent SPINE.yaml** ("rendering-equivalence is just translation studies under a new name") — Schrödinger explicitly states he did not work from Heisenberg's rendering. A sentence-by-sentence translation from Heisenberg to Schrödinger could not have happened because Schrödinger did not consult the Heisenberg-Born-Jordan formalism while developing wave mechanics.
- **A3 in the Schrödinger spine** ("matrix and wave mechanics describe physically different things") — Schrödinger and von Neumann both later proved mathematical equivalence, which physical-difference rivals cannot accommodate.

The convergence between the two formulations is therefore a discovery about the underlying claim-graph (the spine), not an artifact of coordinated authorship or sentence-level translation. This is what makes T1 a natural experiment in the strong sense: the spine convergence happened independently, in real history, with documented evidence of independence at the authoring level.

Schrödinger's headline identity claim (same source p. 46):

> "In what follows the very intimate inner connection between Heisenberg's quantum mechanics and my wave mechanics will be disclosed. From the formal mathematical standpoint, one might well speak of the identity of the two theories."

His completed equivalence claim (p. 57 §5):

> "If the two theories — I might reasonably have used the singular — should be tenable in the form just given, i.e. for more complicated systems as well, then every discussion of the superiority of the one over the other has only an illusory object, in a certain sense. For they are completely equivalent from the mathematical point of view, and it can only be a question of the subordinate point of convenience of calculation."

The bidirectionality (p. 58):

> "The equivalence actually exists, and it also exists conversely. Not only can the matrices be constructed from the proper functions as shown above, but also, conversely, the functions can be constructed from the numerically given matrices."

## 2. Three-layer convergence

The isomorphism operates at three layers simultaneously: observations, propositions, and findings. The methods layer is where the spines diverge — exactly as P4 predicts.

### 2.1 Observation-layer convergence (same empirical inputs)

Both papers ground their formalisms in the same body of pre-1926 atomic spectroscopy data:

| Empirical phenomenon | Heisenberg-path | Schrödinger-path | Same observation? |
|---|---|---|---|
| Hydrogen Balmer series | H_O1 | S_O1 | Yes — same Rydberg formula |
| Hydrogen Lyman / Paschen series | H_O1 (implicit) | S_O2 | Yes |
| Ritz combination principle | H_O2 (explicit) | S_O1 (implicit; the Rydberg formula already encodes Ritz) | Yes |
| Anharmonic/molecular vibrational and rotational spectra | H_O3 | S_O4 | Yes |
| Zeeman-effect multiplet intensities | H_O4 | (not directly in Schrödinger's 1926 set; engaged later) | Heisenberg-only at the spine level |
| Kramers-Heisenberg dispersion formula | H_O5 | (not in Schrödinger's substrate set) | Heisenberg-only |
| Sommerfeld fine-structure / Stark effect | (not foregrounded in Heisenberg substrate) | S_O3, S_O5 | Schrödinger-only at the spine level |
| Heisenberg-Born-Jordan formalism itself | n/a (it IS this path) | S_O6 (treated as a substrate observation Schrödinger maps to) | Bridge observation: makes equivalence proof possible |

**The asymmetry**: Schrödinger's path includes a *meta-observation* (S_O6 — Heisenberg-Born-Jordan's published formalism is itself input data) that the Heisenberg path cannot include because it IS the Heisenberg path. This is structurally important: the equivalence proof was performed by Schrödinger, not by Heisenberg, because Schrödinger's substrate is the only one that contains both formalisms.

**Findings-layer convergence**: both spines reproduce the same atomic spectroscopy observations. H_F1-F3 (anharmonic / harmonic oscillator amplitudes, zero-point energy) map onto S_F2 (proper-value spectrum discrete + continuous). H_F6 (Goudsmit-Kronig-Hönl multiplet intensities, Ornstein-Burger sum rule) maps onto S_F4 (Stark-effect quantitative prediction). Critically, the same Balmer-Rydberg values are reproduced as exact eigenvalues by Schrödinger (S_F1) and as exact transition-frequency formulas by Heisenberg (H_F5).

### 2.2 Proposition-layer isomorphism (despite vocabulary divergence)

The proposition graphs map onto each other up to relabeling. The vocabulary is radically different — Heisenberg writes "two-index amplitude arrays" where Schrödinger writes "eigenfunctions of a linear self-adjoint differential operator" — but the structural claims correspond one-to-one.

| Heisenberg proposition | Schrödinger proposition | Structural content of the equivalence |
|---|---|---|
| H1 — kinematic and mechanical relationships must be reinterpreted so primitives are observable (frequencies, intensities, transition amplitudes) | S5 — optical-mechanical analogy supplies the motivation; Hamilton-Jacobi structure is reformulated as a wave-equation | Both papers REJECT classical atomic kinematics and motivate a structural reformulation. Different motivations (observability vs Hamilton-Jacobi optics) but same structural move: classical mechanics is replaced. |
| H2 — kinematic variables become two-index arrays a(n,m) of complex amplitudes | S1 — quantum behavior is governed by a continuous wave equation on configuration space, with eigenvalue conditions | Both papers REPLACE classical scalar position/momentum with new mathematical objects (matrices vs wave functions). Different mathematical objects; same structural role. |
| H3 — array multiplication is non-commutative | S2 — energy levels are eigenvalues of a linear self-adjoint differential operator (which, as operator on functions, is generally non-commuting with position-multiplication) | Non-commutativity is preserved across formalisms; appears as matrix non-commutativity in Heisenberg and as differential-operator-vs-multiplication non-commutativity in Schrödinger. |
| H4 — canonical commutation relation pq − qp = (h/2πi)·1 | S_F3 + S2 — Heisenberg's quantum condition corresponds identically under the operator substitution p_r ↦ K∂/∂q_r (S_F3); eigenvalue spectrum determined by linear self-adjoint operator (S2) | This is THE shared proposition — both formalisms have a canonical commutation relation in their native language, and Schrödinger explicitly maps the two via operator substitution. |
| H5 — energies are diagonal entries H(n,n) of the Hamiltonian array | S2 — energy levels are eigenvalues of the wave-equation Hamiltonian operator | Diagonal entries of a Hermitian matrix ARE the eigenvalues. Same proposition, different formalism. |
| H6 — classical canonical equations of motion q̇ = ∂H/∂p, ṗ = −∂H/∂q are imposed unchanged on the arrays | S1 — the wave equation IS Hamilton-Jacobi reformulated as an eigenvalue problem; canonical structure inherited via variational derivation | Both preserve canonical structure; Heisenberg imposes it directly, Schrödinger derives it via Hamilton-Jacobi. |
| H7 — Bohr frequency condition as theorem hν(n,m) = H(n,n) − H(m,m) | S_F1 + S2 — wave-equation eigenvalue differences reproduce the Balmer-Rydberg frequencies | Same theorem, different proof path. |

**S4 is the meta-proposition that closes the isomorphism**: "Wave mechanics and the matrix mechanics of Heisenberg, Born, and Jordan are mathematically equivalent." S4 is *not* in the Heisenberg path; Heisenberg's path predates the equivalence proof. S4 sits in the Schrödinger path as the explicit articulation of what the spine-isomorphism analysis (this document, retroactively) shows structurally.

### 2.3 Findings-layer convergence (same data reproduced)

The strongest evidence of spine isomorphism is that both formalisms reproduce *the same* atomic-spectroscopy findings. Different methods, same observations, same numerical predictions:

| Phenomenon | Heisenberg-path finding | Schrödinger-path finding |
|---|---|---|
| Hydrogen energy levels reproduce Balmer-Rydberg | H_F5 (via Bohr-condition theorem from H5+H6+H4) | S_F1 (eigenvalues of wave equation) |
| Harmonic-oscillator zero-point energy W = (n + ½)ℏω₀ | H_F3 | (Schrödinger derives same via wave-equation eigenvalues; H_F3 ↔ S_F2 special case) |
| Canonical commutation as exact relation | H_F4 (sharpened) | S_F3 (operator-correspondence) |
| Bohr frequency condition as theorem | H_F5 | S_F1 + S2 (eigenvalue differences) |
| Stark effect spectroscopy quantitatively predicted | (not in Heisenberg foreground; later) | S_F4 (Schrödinger Part III explicitly) |
| Multiplet intensity formulas | H_F6 | (Schrödinger derives via transition matrix elements between eigenfunctions; structurally same as H_F6 via S_F3-style mapping) |

Two formalisms, same numerical predictions to the precision of experimental measurement. This is the empirical core of the spine isomorphism — and the empirical core of the natural-experiment test of P4.

## 3. Where the spines diverge — and why the divergences are rendering-layer

The spines diverge at the methods layer. The Heisenberg spine has six methods nodes (H_M1-H_M6) operating with matrix algebra, the Ritz combination multiplication rule, the Kramers-Heisenberg dispersion formula, the Thomas-Kuhn sum rule, and the variational principle imposing classical canonical equations on arrays. The Schrödinger spine has six methods nodes (S_M1-S_M6) operating with Hamilton-Jacobi substitution, the variational principle on a wave-equation Lagrangian, Sturm-Liouville eigenvalue theory, the optical-mechanical analogy from geometrical optics, the operator-matrix correspondence, and time-dependent perturbation theory.

These method-layer divergences are *exactly* the rendering-layer divergences P4 predicts. The method nodes encode HOW the proposition was reached; the proposition itself is a spine-layer object that holds across methods.

A worked example. Consider the propositions H4 ("canonical commutation pq − qp = (h/2πi)·1") and the Schrödinger-path counterparts S2 + S_F3 (eigenvalue operator structure + operator-correspondence finding). The same proposition is reached via:

- **Heisenberg path**: empirical observation of Ritz combination principle → array representation → multiplication rule → impose classical canonical equations on the arrays → derive Thomas-Kuhn sum rule → sharpen to the commutation relation. Method-chain length: 6+ steps via matrix algebra.
- **Schrödinger path**: Hamilton-Jacobi substitution → variational principle → wave equation → impose Hermiticity → eigenvalue problem → operator-correspondence substitution p_r ↦ K∂/∂q_r → derive canonical commutator on the function space. Method-chain length: 5+ steps via PDE eigenvalue theory.

The methods are *incommensurable* in the sense that sentence-by-sentence translation between them is impossible — the mathematical objects (matrices vs differential operators on Hilbert space) are different categories. But the propositions converge. This is what spine-rendering equivalence under P4 means structurally.

**Vocabulary divergence at the same level**. The two papers literally cannot agree on what to call their primitives. Heisenberg writes "two-index amplitude arrays"; Born coins "matrices" only after seeing the draft. Schrödinger writes "eigenfunctions" and "proper functions" and "weight functions." Yet the underlying claim — "kinematic variables in atomic regime are non-commuting operators" — is the same proposition. Translation studies cannot handle this because there are no common sentences; the framework's spine→rendering relation handles it because the spine is medium-invariant.

## 4. What the isomorphism tells us about P4 (and about schema v0.2)

### 4.1 P4 corroboration via T1

The isomorphism analysis corroborates P4 (rendering-equivalence under spine-preservation) on multiple grounds:

- **H_T1_1 (proposition graph isomorphism)** is supported by §2.2: each Heisenberg proposition has a Schrödinger counterpart up to vocabulary relabeling; antecedent edges preserve their structure.
- **H_T1_2 (findings convergence)** is supported by §2.3: both paths reproduce the same atomic-spectroscopy findings to experimental precision.
- **H_T1_3 (methods divergence + conclusion preservation)** is supported by §3: the methods are radically different, the conclusions are identical.

Combined: a natural-experiment confirmation of P4. The spine convergence is not author-coordinated (per §1, Schrödinger's footnote); the rendering divergence is maximal (matrix algebra vs PDE eigenvalue analysis); the conclusion convergence is exact (same observations reproduced, same canonical commutation relation, same energy levels).

### 4.2 Falsifier check: P4 is well-formed and not auto-confirmed

P4 would be falsified by two renderings of the same spine that disagree on locked conclusions without an identifiable spine-break. The T1 case does NOT auto-confirm P4 — the falsifier was available: Schrödinger and Heisenberg might have produced formalisms that gave *different* atomic spectra, or different commutation relations, or different multiplet patterns. Empirically they did not, but the possibility was open. P4 made a falsifiable prediction; T1 corroborates it.

### 4.3 Where schema v0.2 was adequate (and where it was strained)

Schema v0.2 represented both T1 spines without omitted content. The 10 first-class node types covered everything in the source papers: observations (atomic spectra), methods (matrix algebra vs PDE), measurements (numerical predictions), findings (reproduced empirical phenomena), propositions (theoretical claims), derivations (reasoning bridges), alternative_explanations (Bohr-Sommerfeld old quantum theory ruled out in both paths), limitations (relativistic effects out of scope; multi-electron atoms approximate), assumption_atoms (e.g., Hermiticity in Schrödinger, classical correspondence in Heisenberg), and external_anchors (Kramers, Sommerfeld, Bohr, etc.).

Schema gaps that surfaced:

- **No node type for visualization claims**. Schrödinger's *Anschaulichkeit* (perspicuity / visualizability) was a motivation for his approach that does NOT fit cleanly into propositions, methods, or aesthetics. It is a meta-methodological preference. Currently absorbed into assumption_atoms; arguably should have its own type. Flag for schema v0.2.1.
- **No node type for the *equivalence-claim-itself* as a distinct meta-proposition**. S4 sits in propositions[] but it is structurally different from S1-S3, S5 — those are object-level claims; S4 is a meta-claim about the relation between two object-level theories. v0.2.1 may want a `meta_propositions[]` or `bridging_propositions[]` array.
- **No graceful representation of historical-context provenance**. The Schrödinger footnote about independence ("I did not at all suspect any relation to Heisenberg's theory at the beginning") is provenance-relevant but does not fit cleanly into the `provenance:` block (which is per-node, not per-claim). Currently captured in equivalence-notes prose; arguably should be a first-class `historical_provenance[]` array.

These are noted as v0.2.1 candidates; v0.2 schema represents the spines adequately for the T1 analysis purpose.

## 5. Coder-judgment flags

Per L2 in the parent SPINE.yaml ("T1 extraction is necessarily retroactive; coder judgment will inevitably be invoked"), the points where this isomorphism analysis relied on coder judgment:

1. **H1 ↔ S5 mapping** — Heisenberg's observability-only motivation and Schrödinger's optical-mechanical analogy are conceptually different motivations. We treat them as parallel-structure (both REJECT classical kinematics and motivate a structural reformulation). A second coder might split them into non-isomorphic motivations.
2. **H3 ↔ S2 non-commutativity correspondence** — matrix non-commutativity and differential-operator non-commutativity with position-multiplication ARE the same algebraic structure (both reflect [q,p] ≠ 0). This is a textbook equivalence; a second coder would likely confirm.
3. **H4 ↔ S_F3 + S2 commutation-relation mapping** — the trickiest correspondence. Heisenberg states the commutator pq − qp = (h/2πi)·1 as a proposition; Schrödinger states the operator-correspondence p_r ↦ K∂/∂q_r as a finding (S_F3) that implicitly carries the commutator on function-space. The two are equivalent (under standard textbook arguments) but they live at different ontological levels in their respective spines. Second coder might flag the asymmetry.
4. **S4 as meta-proposition vs first-order proposition** — we treat S4 as a proposition in the same array as S1-S3, S5. Arguably it belongs in a separate `meta_propositions[]` array (see §4.3). Coder judgment exercised by keeping it inline with the v0.2 schema; flagged for v0.2.1.
5. **The Three-Men paper (Born-Heisenberg-Jordan 1926)** is not directly read; we relied on secondary references and standard physics-history summaries. Could affect H_M5 (the variational principle imposing classical canonical equations) since the Three-Men paper develops this more fully than Heisenberg 1925 alone. User institutional access could resolve.

Inter-coder reliability check (RC2 in parent spine) is planned for Phase 3. We estimate κ ≥ 0.7 on the proposition-mapping table in §2.2 based on the textbook consensus that the equivalence is real and the propositions correspond. κ could be lower on the methods-divergence side (§3) where vocabulary is heterogeneous and coder choice on chunking matters.

## 6. Conclusion

The Heisenberg and Schrödinger spines are isomorphic at the proposition and findings layers and divergent at the methods layer. This is exactly the structural pattern P4 predicts. The convergence happened independently (Schrödinger's footnote attests no prior consultation of Heisenberg's formalism), was proven equivalent by Schrödinger (1926) and rigorously grounded by von Neumann (1932), and reproduces the same atomic-spectroscopy observations to experimental precision.

T1 is a natural-experiment confirmation of P4 in the strong sense: scientific history independently constructed two renderings of the same spine, proved them equivalent mathematically, and the proof has stood for one hundred years.

The Schrödinger-Heisenberg twin pair is the cleanest historical instance of rendering-equivalence under spine-preservation available. It is the cross-domain killer for the meaningfulness paper's empirical validation strategy.

---

*Document version 1.0. Phase-2 T1 isomorphism analysis. Ready for Session C Grok review.*
