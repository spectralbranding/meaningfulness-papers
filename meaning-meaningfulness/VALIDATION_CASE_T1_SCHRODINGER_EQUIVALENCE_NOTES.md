# Validation Case T1 — Schrödinger 1926 Equivalence Paper: Focused Notes

**Source document**: E. Schrödinger, *Collected Papers on Wave Mechanics*, Blackie & Son, London, 1928 (English translation of *Abhandlungen zur Wellenmechanik*, 2nd German ed., J.A. Barth, 1928). Pages cited below refer to this English edition.

**Paper of focus**: "On the Relation between the Quantum Mechanics of Heisenberg, Born, and Jordan, and that of Schrödinger" (*Annalen der Physik* (4), vol. 79, 1926; collected ed. pp. 45–61).

**File location**: `research/references/schrodinger_1928_collected_papers_wave_mechanics.pdf`.

---

## 1. Schrödinger's own framing of the equivalence claim

Schrödinger opens by stressing the *apparent* incommensurability of the two formulations:

> "Considering the extraordinary differences between the starting-points and the concepts of Heisenberg's quantum mechanics and of the theory which has been designated 'undulatory' or 'physical' mechanics, and has lately been described here, it is very strange that these two new theories agree with one another with regard to the known facts, where they differ from the old quantum theory… starting-points, presentations, methods, and in fact the whole mathematical apparatus, seem fundamentally different. Above all, however, the departure from classical mechanics in the two theories seems to occur in diametrically opposed directions." (p. 45)

He then commits the paper's central claim explicitly:

> "In what follows the very intimate inner connection between Heisenberg's quantum mechanics and my wave mechanics will be disclosed. From the formal mathematical standpoint, one might well speak of the **identity of the two theories**." (p. 46, emphasis his)

And the consequence in §5:

> "If the two theories — I might reasonably have used the singular — should be tenable in the form just given… then every discussion of the superiority of the one over the other has only an illusory object, in a certain sense. For **they are completely equivalent from the mathematical point of view**, and it can only be a question of the subordinate point of convenience of calculation." (p. 57)

## 2. The mathematical move

The construction (§§2–4) is operator-theoretic. To each function F(qₖ, pₖ) of the canonical variables, Schrödinger associates (i) a differential operator on q-space (replacing pᵣ by K∂/∂qᵣ, with K = h / 2πi) and (ii) — via an arbitrary complete orthonormal system {uᵢ(x)} on q-space — a matrix Fᵏˡ = ∫ρ(x) uₖ(x) [F, uₗ(x)] dx (eq. 6, p. 47). He then proves that addition and multiplication of these matrices reproduce Heisenberg–Born–Jordan matrix multiplication, including the commutator relation pq − qp = K (Heisenberg's "quantum condition", §3, eq. 11–12, p. 50).

The headline result (§4, p. 56):

> "Hence the solution of the whole [system] of matrix equations of Heisenberg, Born, and Jordan is reduced to the natural boundary value problem of a linear partial differential equation. If we have solved the boundary value problem, then by the use of (6) we can calculate by differentiations and quadratures every matrix element we are interested in."

And explicitly bidirectional (p. 58):

> "The equivalence actually exists, and it also exists conversely. Not only can the matrices be constructed from the proper functions as shown above, but also, conversely, the functions can be constructed from the numerically given matrices."

## 3. Prior contact with Heisenberg–Born–Jordan

Schrödinger discloses his prior exposure in a footnote on p. 46:

> "My theory was inspired by L. de Broglie… and by brief, but infinitely far-seeing remarks of A. Einstein… **I did not at all suspect any relation to Heisenberg's theory at the beginning. I naturally knew about his theory, but was discouraged, if not repelled, by the very difficult methods of transcendental algebra, and by the want of perspicuity (Anschaulichkeit).**" (footnote 1, p. 46)

This is the load-bearing biographical attestation that the two formulations were authored **without coordination on framework or notation** — i.e., that any structural coincidence between them is a discovery, not a construction.

## 4. Why this paper is load-bearing for P4 of the meaningfulness paper

P4 of the meaningfulness paper claims **rendering-equivalence under spine-preservation**: two artifacts authored from different rendering vocabularies, on different presentation surfaces, can converge on identical conclusions when their underlying claim-graphs (S-layer) coincide. The Schrödinger 1926 equivalence paper supplies the strongest possible historical instance of this claim, because:

1. **Disjoint rendering substrates**. Matrix mechanics (Heisenberg, Born, Jordan 1925) and wave mechanics (Schrödinger Part I, January 1926) share no sentences in common — one operates on infinite arrays of complex numbers indexed by stationary states; the other on continuous PDEs in configuration space. Sentence-by-sentence translation is *impossible*; the formalisms have no common surface.
2. **Independently authored**. Schrödinger's own footnote attests he did not consult, and was repelled by, Heisenberg's apparatus when constructing wave mechanics.
3. **Same conclusions, provably**. Schrödinger derives the equivalence via the operator-matrix correspondence and proves it bidirectional; von Neumann (1932) later supplies the rigorous Hilbert-space formulation.
4. **Same observations**. Both theories reproduce the Balmer series, Lyman series, hydrogen fine-structure, harmonic oscillator, rigid rotator, Stark effect — i.e., the empirical substrate is shared (Abstract, pp. ix–xiii).

This is exactly the structural pattern P4 predicts: spine-preserved, rendering-disjoint, conclusion-equivalent. The natural-experiment status comes from (2): neither author could have engineered the convergence, so the convergence is evidence about the underlying claim-graph, not about coordinated writing. The Schrödinger paper is therefore the empirical-historical instance of P4 the meaningfulness paper requires.
