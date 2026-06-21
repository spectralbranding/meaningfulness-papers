# Online Appendix C — Calibrated Simulation Harness

This appendix specifies the calibrated simulation that illustrates the cost-asymmetry result in the main body. The simulation does not estimate the parameters α, β, γ, δ from data; it varies β and δ over a plausible parameter grid and verifies that the cost-allocation prescription dominates across the grid. Empirical estimation of the parameters from twin-pair extractions is the scope of the companion empirical working paper (Zharnikov 2026ap).

## C.1 Cost-function specification

The cost functions main-body Section *The Three-Level Hierarchy* introduces are:

$$ c_{AI}(S) = \alpha \cdot |V|^\beta, \quad \beta < 1 $$

$$ c_{human}(R) = \gamma \cdot |\text{tokens}|^\delta, \quad \delta > 1 $$

α and γ are scale constants. The central structure is the relative exponent $\beta < 1 < \delta$. The simulation fixes α = γ = 1 (the prescription's dominance does not depend on the scale constants; setting them equal isolates the exponent effect) and varies β and δ over the grid:

- β ∈ {.5, .7, .9}
- δ ∈ {1.1, 1.3, 1.5}

## C.2 Artifact size distribution

The simulation models a population of artifacts with varying complexity. Each artifact has a substrate size $|V|$ and a corresponding rendering size $|\text{tokens}|$. The token count scales with substrate size at a rate that empirical observation in the corpus has placed at approximately 50–200 tokens per substrate node (a 100-node spine renders to approximately 5,000–20,000 tokens of prose). The simulation parameterizes this scaling as $|\text{tokens}| = \mu \cdot |V|$ with μ drawn from a log-normal distribution centered on 100.

Artifact sizes are drawn from a power-law distribution that approximates the empirical artifact-size distribution in management-research publication: most artifacts are 50–150 substrate nodes (typical paper); a minority are 200–500 nodes (substantial review article or theory paper); a long tail extends to 1000+ nodes (book-length artifacts). The simulation reports cost-allocation outcomes both for the typical-artifact case and for the long-tail case.

## C.3 Verification-cost ratio

For each (β, δ) pair and each artifact size, the simulation computes the verification-cost ratio:

$$ \rho_{\text{cost}}(|V|, \beta, \delta) = \frac{c_{human}(R)}{c_{AI}(S)} = \frac{|tokens|^\delta}{|V|^\beta} = \frac{(\mu |V|)^\delta}{|V|^\beta} = \mu^\delta \cdot |V|^{\delta - \beta} $$

Since δ - β > 0 across the entire grid (the minimum is .2 at β = .9, δ = 1.1; the maximum is 1.0 at β = .5, δ = 1.5), $\rho_{\text{cost}}$ is strictly increasing in $|V|$. The cost-asymmetry advantage of AI projection on substrate grows with artifact complexity. Under the stated scale constants (α = γ = 1) and tokens-per-node scaling (μ = 100), the advantage is already substantial at small artifact size: at |V| = 10 it is between roughly 2.4 and 4.0 orders of magnitude depending on (β, δ); at typical paper size (|V| ≈ 100) it is between roughly 2.6 and 5.0 orders of magnitude; at long-tail size (|V| ≥ 500) between roughly 2.7 and 5.7 orders of magnitude.

## C.4 Recombination-rate simulation

A second illustration estimates the recombination-rate advantage when an organization publishes the substrate as a first-class artifact. The simulation models two organizations: one that publishes S alongside R (the spine-publishing organization), and one that publishes R only (the rendering-only organization). Downstream consuming agents (representing other research labs, AI literature-review tools, and standards bodies) interact with each organization's output. For each interaction, the consuming agent attempts a recombination: they query the source artifact's substrate for a subgraph satisfying $\mathrm{Rec}(G_{\text{new}}, G_{\text{prior}}) \geq 3$ on linked propositions with preserved antecedents.

For the spine-publishing organization, the consuming agent queries the published substrate directly: query cost is $c_{AI}(S_{\text{query}}) = \alpha \cdot |V_{\text{query}}|^\beta$. For the rendering-only organization, the consuming agent must re-extract a substrate from the rendering before querying: total cost is $c_{\text{extract}}(R) + c_{AI}(S_{\text{extracted}}) = \gamma \cdot |\text{tokens}|^\delta + \alpha \cdot |V|^\beta$. The re-extraction cost dominates by orders of magnitude across the grid.

Under a fixed downstream-agent compute budget, the spine-publishing organization receives more recombination interactions per unit compute budget than the rendering-only organization. The advantage scales with artifact complexity exactly as the verification-cost ratio scales: by roughly 2.6 to 5.0 orders of magnitude at typical paper size (|V| ≈ 100), by roughly 2.7 to 5.7 at long-tail size (|V| ≥ 500).

## C.5 Cross-over point analysis

For each (β, δ) pair, the simulation identifies the artifact-size cross-over point at which the cost-allocation prescription becomes economically dominant — that is, the substrate size above which AI-projection on substrate plus human-projection on rendering costs strictly less than human-projection on rendering only. Formally, the cross-over $|V|^*$ is the substrate size at which $c_{AI}(S) + c_{human}^{\text{judgment}}(S) = c_{human}(R)$, where $c_{human}^{\text{judgment}}$ is the residual human-attention cost on judgment operations the Operator retains under the post-AI projection composition. The simulation parameterizes $c_{human}^{\text{judgment}}$ as a small fixed fraction of $c_{human}(R)$ (the framework's claim is that judgment cost remains era-invariant; the projection composition shifts only the structural-substrate cost from human to AI).

Across the (β, δ) grid, the cross-over substrate size lies below a single node ($|V|^*$ between approximately $10^{-11}$ and $10^{-3}$ depending on the parameter pair): under the stated cost functions with α = γ = 1 and μ = 100, the post-AI allocation costs strictly less than human-only rendering verification at every artifact size of one node or larger. The cost-allocation prescription therefore dominates unconditionally across the entire artifact-size distribution observed in management research publication. The cross-over is largest (closest to one node) where the exponent gap δ − β is widest (β = .5, δ = 1.5) and smallest where the gap is narrowest (β = .9, δ = 1.1); in both corners it remains far below the typical paper substrate size of 50–150 nodes. The prescription's dominance is robust to parameter uncertainty within the plausible range.

Under the stated cost functions there is no positive-size neutral zone: the prescription is neutral only in the degenerate sub-node regime ($|V| < 1$), which lies below any real artifact. (A small-artifact neutral zone would emerge near $|V| \approx 1$ if an AI-projection fixed setup cost were added to $c_{AI}(S)$; the present model omits such a term, and the qualitative dominance on within-scope artifacts is unaffected by it.) For the smallest real artifacts — short notes, brief commentaries — the framework's boundary condition C4 (volume of artifacts exceeds unaided human reviewer verification capacity) typically fails at the per-artifact level, so those artifacts are outside the framework's scope regardless.

## C.5b Sensitivity to artifact-size distribution shape

The simulation's primary results assume a power-law artifact-size distribution with exponent fit to empirical observation in management-research publication. Two sensitivity analyses are reported. *First*, replacing the power-law distribution with a log-normal distribution at matched median yields qualitatively identical results: the cross-over remains below a single node across the grid under both distributions, so essentially every artifact in either distribution exceeds it and the cost-allocation prescription dominates (the simulation confirms a fraction above the cross-over of 1.0000 under both the power-law and the log-normal draws). *Second*, restricting the artifact-size distribution to the typical-paper range only (50 ≤ |V| ≤ 150) yields cross-over results trivially: every artifact in the restricted range exceeds the cross-over by many orders of magnitude, and the prescription's dominance is unconditional.

## C.5c Sensitivity to the judgment-cost fraction

The simulation's residual human judgment-cost fraction is set to .15 of the full rendering cost by default. Sensitivity sweep over fractions in {.05, .15, .30, .50}: the cross-over remains below a single node across the grid for all four fractions (raising the fraction shifts the cross-over upward only in relative terms, never above one node), so the prescription's dominance on typical-paper-sized artifacts is preserved across all four fractions. The framework's central claim does not depend on a precise judgment-cost fraction; it depends on the fraction being small relative to the full rendering cost, which all empirically plausible values satisfy.

## C.6 Companion computation script

The simulation is reproducible from the companion script published at:

```
https://github.com/spectralbranding/meaningfulness-papers/tree/main/meaning-meaningfulness/code/cost_asymmetry_simulation.py
```

Random seed: 42 (fixed at file top). Run command:

```
uv run --with numpy python cost_asymmetry_simulation.py
```

The script reproduces every value this appendix reports as "simulated," "computed," or "calibrated" — the verification-cost ratio across the (β, δ) grid, the sub-node cross-over analysis, the recombination-rate advantage, and the C.5b/C.5c sensitivity sweeps — and prints each reported value next to the value it computes with a per-value MATCH verdict, so the appendix and the script cannot silently drift apart. The script's docstring documents the model and the run command, and the `code/README.md` in the same directory supplies the per-script provenance note linking back to the paper DOI. The separate illustrative crossover *figure* (an exposition of the cost-asymmetry shape at a single, deliberately visible parameter set) is rendered by `cost_asymmetry_crossover.py` in the same directory and is not the source of any value reported here.

The script is the ground truth for any value cited in the main body as "simulated," "computed," or "calibrated." Paper-to-script numerical alignment is maintained per the corpus's computation-script-publication discipline; if a script revision changes a number, the main body is updated to match (or the script docstring explains and dates the divergence).

## C.7 What the simulation does not do

The simulation is calibrated, not estimating. It does not supply empirical estimates of α, β, γ, or δ from observed data. The parameter grid covers a plausible range informed by domain reasoning (sub-linear substrate verification because graph-traversal cost scales below linear in node count under typical algorithm choices; super-linear rendering verification because human reading cost scales above linear in token count under typical attention-budget constraints), but the grid is not anchored to specific empirical observations. Anchoring the grid to empirical parameter estimates from twin-pair extractions is the v2.0.0 deliverable of Zharnikov (2026ap). The grid range may shift after empirical estimation; the cost-allocation prescription's dominance across a plausible range is what the calibrated simulation here establishes.
