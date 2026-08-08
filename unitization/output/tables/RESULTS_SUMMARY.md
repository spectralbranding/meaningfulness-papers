# 2026bl run -- results as computed

Protocol `2026bl/1.0.0`, prompts `unitization/1.0.0`, seed 20260808, k = 5.

Every number here is rendered from `output/tables/*.json`. Nothing is computed twice.

## Table A2 -- segmenter fidelity, established before any operator call

| Document | Units (segmenter) | Units (adjudicated) | Boundary agreement (kappa) | Adjudicators' own kappa | Displayed-mathematics merges | Gates? |
|---|---:|---:|---:|---:|---:|---|
| VC1 | 273 | 116 | .169 | .874 | 218 | FAIL |
| VC2 | 590 | 616 | -.005 | .649 | 1 | FAIL |
| VC3 R0 | 74 | 76 | .250 | 1.000 | 5 | FAIL |
| VC3 R1 | 421 | 420 | .220 | .631 | 23 | FAIL |
| VC3 R2 | 131 | 124 | .011 | .735 | 17 | FAIL |

*Gate*: kappa >= .800.

## Predicted base rates, declared before any operator call

| Document | Inventory units | Predecessor nodes (A/B) | Predicted base rate | Predicted prevalence index | Gates? |
|---|---:|---:|---:|---:|---|
| VC1 | 273 | 53/25 | .143 | .714 | yes |
| VC2 | 590 | 119/39 | .134 | .732 | yes |
| VC3 R0 | 74 | 47/19 | .446 | .108 | yes |
| VC3 R1 | 421 | 85/14 | .118 | .765 | yes |
| VC3 R2 | 131 | 57/21 | .298 | .405 | yes |

*Floor*: prevalence index > .850 is non-gating.

## Table A1 -- decomposition by document, condition and layer

Each cell is *between-operator* / *within-operator*, computed on the same statistic.

| Document | Condition | Layer 1 (select) | Layer 2 (type given selected) | Layer 3 (edges given agreed) | Layer 4 (edges over inventory) | L4/L3 |
|---|---|---|---|---|---|---:|
| VC1 | U-free | -- / -- | -- / -- | .000 / .799 | -- / -- | -- |
| VC2 | U-free | -- / -- | -- / -- | .058 / .639 | -- / -- | -- |
| VC3 R0 | U-free | -- / -- | -- / -- | .353 / .667 | -- / -- | -- |
| VC3 R1 | U-free | -- / -- | -- / -- | .367 / .691 | -- / -- | -- |
| VC3 R2 | U-free | -- / -- | -- / -- | .219 / .625 | -- / -- | -- |
| VC1 | U-det | .143 / .911 | -.051 / .922 | .259 / .845 | .036 / .780 | .140 |
| VC2 | U-det | .053 / .887 | .056 / .868 | .227 / .805 | .016 / .747 | .068 |
| VC3 R0 | U-det | .406 / .878 | .659 / .833 | .488 / .803 | .417 / .773 | .856 |
| VC3 R1 | U-det | .112 / .929 | .241 / .936 | .229 / .873 | .012 / .834 | .052 |
| VC3 R2 | U-det | .240 / .791 | .635 / .745 | .378 / .658 | .135 / .578 | .358 |
| VC1 | U-mod | .080 / .842 | .282 / .698 | .374 / .667 | .065 / .655 | .173 |
| VC2 | U-mod | .293 / .853 | .427 / .764 | .407 / .705 | .143 / .610 | .352 |
| VC3 R0 | U-mod | .737 / .938 | .498 / .968 | .481 / .850 | .475 / .849 | .989 |
| VC3 R1 | U-mod | -.048 / .946 | .600 / .932 | .000 / .851 | .000 / .822 | -- |
| VC3 R2 | U-mod | .220 / .945 | .808 / .900 | .464 / .841 | .183 / .829 | .395 |

Layers 1, 2 and 4 are not defined in U-free, which has no shared inventory.

## The within-operator baseline, per operator (A4)

The pooled figure in Table A1 is the DECLARED statistic (M3). It is shown here split by operator, because the two are not sampled the same way and cannot be: one is called at temperature 0 with a fixed seed, the other belongs to a family that rejects sampling parameters. An operator whose $k$ repetitions are identical contributes a constant $1.000$ rather than a measurement, which inflates the pooled baseline and makes P2's separation easier to obtain.

| Document | Condition | Layer | Pooled | OP_A | OP_B | Constant contributor? |
|---|---|---|---:|---:|---:|---|
| VC1 | U-free | 3 | .799 | .599 | 1.000 | OP_B |
| VC2 | U-free | 3 | .639 | .578 | .700 | no |
| VC3 R0 | U-free | 3 | .667 | .702 | .633 | no |
| VC3 R1 | U-free | 3 | .691 | .605 | .778 | no |
| VC3 R2 | U-free | 3 | .625 | .641 | .609 | no |
| VC1 | U-det | 1 | .911 | .821 | 1.000 | OP_B |
| VC1 | U-det | 2 | .922 | .844 | 1.000 | OP_B |
| VC1 | U-det | 3 | .845 | .690 | 1.000 | OP_B |
| VC1 | U-det | 4 | .780 | .561 | 1.000 | OP_B |
| VC2 | U-det | 1 | .887 | .773 | 1.000 | OP_B |
| VC2 | U-det | 2 | .868 | .735 | 1.000 | OP_B |
| VC2 | U-det | 3 | .805 | .609 | 1.000 | OP_B |
| VC2 | U-det | 4 | .747 | .495 | 1.000 | OP_B |
| VC3 R0 | U-det | 1 | .878 | .919 | .837 | no |
| VC3 R0 | U-det | 2 | .833 | .925 | .742 | no |
| VC3 R0 | U-det | 3 | .803 | .771 | .834 | no |
| VC3 R0 | U-det | 4 | .773 | .763 | .782 | no |
| VC3 R1 | U-det | 1 | .929 | .857 | 1.000 | OP_B |
| VC3 R1 | U-det | 2 | .936 | .873 | 1.000 | OP_B |
| VC3 R1 | U-det | 3 | .873 | .746 | 1.000 | OP_B |
| VC3 R1 | U-det | 4 | .834 | .667 | 1.000 | OP_B |
| VC3 R2 | U-det | 1 | .791 | .861 | .720 | no |
| VC3 R2 | U-det | 2 | .745 | .881 | .608 | no |
| VC3 R2 | U-det | 3 | .658 | .723 | .592 | no |
| VC3 R2 | U-det | 4 | .578 | .686 | .469 | no |
| VC1 | U-mod | 1 | .842 | .900 | .783 | no |
| VC1 | U-mod | 2 | .698 | .796 | .600 | no |
| VC1 | U-mod | 3 | .667 | .734 | .600 | no |
| VC1 | U-mod | 4 | .655 | .710 | .600 | no |
| VC2 | U-mod | 1 | .853 | .823 | .883 | no |
| VC2 | U-mod | 2 | .764 | .784 | .745 | no |
| VC2 | U-mod | 3 | .705 | .607 | .803 | no |
| VC2 | U-mod | 4 | .610 | .524 | .697 | no |
| VC3 R0 | U-mod | 1 | .938 | .876 | 1.000 | OP_B |
| VC3 R0 | U-mod | 2 | .968 | .949 | .987 | no |
| VC3 R0 | U-mod | 3 | .850 | .746 | .954 | no |
| VC3 R0 | U-mod | 4 | .849 | .744 | .954 | no |
| VC3 R1 | U-mod | 1 | .946 | .891 | 1.000 | OP_B |
| VC3 R1 | U-mod | 2 | .932 | .864 | 1.000 | OP_B |
| VC3 R1 | U-mod | 3 | .851 | .703 | 1.000 | OP_B |
| VC3 R1 | U-mod | 4 | .822 | .643 | 1.000 | OP_B |
| VC3 R2 | U-mod | 1 | .945 | .889 | 1.000 | OP_B |
| VC3 R2 | U-mod | 2 | .900 | .801 | 1.000 | OP_B |
| VC3 R2 | U-mod | 3 | .841 | .682 | 1.000 | OP_B |
| VC3 R2 | U-mod | 4 | .829 | .659 | 1.000 | OP_B |

## Layer 3, both criteria

| Document | Condition | Between | Within (noise floor) | Difference | p | 95% CI | Absolute (>= .71)? | Separated below the floor? |
|---|---|---:|---:|---:|---:|---|---|---|
| VC1 | U-free | .000 | .799 | .799 | .000 | [.706, .889] | no | yes |
| VC2 | U-free | .058 | .639 | .581 | .000 | [.491, .677] | no | yes |
| VC3 R0 | U-free | .353 | .667 | .315 | .000 | [.219, .410] | no | yes |
| VC3 R1 | U-free | .367 | .691 | .325 | .000 | [.159, .489] | no | yes |
| VC3 R2 | U-free | .219 | .625 | .406 | .000 | [.256, .551] | no | yes |
| VC1 | U-det | .259 | .845 | .586 | .000 | [.507, .664] | no | yes |
| VC2 | U-det | .227 | .805 | .578 | .000 | [.487, .669] | no | yes |
| VC3 R0 | U-det | .488 | .803 | .315 | .000 | [.272, .362] | no | yes |
| VC3 R1 | U-det | .229 | .873 | .644 | .000 | [.577, .711] | no | yes |
| VC3 R2 | U-det | .378 | .658 | .280 | .000 | [.182, .377] | no | yes |
| VC1 | U-mod | .374 | .667 | .293 | .001 | [.113, .455] | no | yes |
| VC2 | U-mod | .407 | .705 | .298 | .000 | [.231, .373] | no | yes |
| VC3 R0 | U-mod | .481 | .850 | .370 | .000 | [.312, .426] | no | yes |
| VC3 R1 | U-mod | .000 | .851 | .851 | .000 | [.780, .918] | no | yes |
| VC3 R2 | U-mod | .464 | .841 | .377 | .000 | [.306, .449] | no | yes |

## The published joint coefficients, computed in-study (M5a)

| Document | Condition | gamma | gamma-cat |
|---|---|---:|---:|
| VC1 | U-free | .031 | -.100 |
| VC2 | U-free | .106 | -.097 |
| VC3 R0 | U-free | .350 | .257 |
| VC3 R1 | U-free | .308 | .139 |
| VC3 R2 | U-free | .138 | -.083 |
| VC1 | U-det | .080 | -.019 |
| VC2 | U-det | -.049 | -.134 |
| VC3 R0 | U-det | .596 | .467 |
| VC3 R1 | U-det | .031 | -.138 |
| VC3 R2 | U-det | .288 | .170 |
| VC1 | U-mod | .090 | .052 |
| VC2 | U-mod | .291 | .150 |
| VC3 R0 | U-mod | .754 | .648 |
| VC3 R1 | U-mod | -.108 | -.131 |
| VC3 R2 | U-mod | .373 | .260 |

Computed on repetition 1 of each operator.

## Table A3 -- the predecessor's node layer, as reported and as recomputed

| Document | As reported (matched nodes only) | Recomputed (charging boundary disagreement) | Difference |
|---|---:|---:|---:|
| VC1 | .663 | .136 | -.527 |
| VC2 | .637 | .228 | -.409 |
| VC3 R0 | 1.000 | .235 | -.765 |
| VC3 R1 | -- | .125 | -- |
| VC3 R2 | .769 | .245 | -.525 |

Declared direction (recomputed worse) holds on 4 of 5 documents.

