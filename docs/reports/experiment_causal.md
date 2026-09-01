# Causal comparison

**Status:** executed, 30 seeds.  
**Date:** 2026-09-01  
**Config:** `configs/experiment_causal.yaml`  
**Config hash:** `4717093f690d9431`  
**Raw summary:** `results/experiment_causal/summary.json`  
**Figures:** `figures/experiment_causal/`

## Question

Under the hidden SCM \(A\to C\to D\), \(B\to C\) and candidates \(\mathrm{do}(A=a,B=b)\), which sequential policy recovers the graph (evaluator-only BIC parent search, structural Hamming distance) more efficiently?

This is not a claim that ECHO is a causal-discovery method.

## Result (final SHD, 30 seeds)

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| Random | 1.467 | 1.000 | 0.860 | [1.159, 1.775] |
| Uncertainty | 1.333 | 1.000 | 0.844 | [1.031, 1.635] |
| ECHO V0 | 1.267 | 1.000 | 0.740 | [1.002, 1.531] |
| Diversity | 1.200 | 1.000 | 0.551 | [1.003, 1.397] |
| ECHO open-loop | 1.200 | 1.000 | 0.551 | [1.003, 1.397] |

ECHO V0 vs uncertainty: mean diff −0.067, \(d=-0.08\), Wilcoxon \(p=0.60\), 5/30 lower-SHD wins. ECHO V0 vs random: \(p=0.24\).

Reduced-form function RMSE: diversity 0.065, ECHO V0 0.069, uncertainty 0.072, random 0.087, open-loop 0.204.

ECHO V0 was worse than uncertainty on SHD for 5/30 seeds (5, 8, 10, 13, 21).

## Interpretation

Graph recovery with this tiny exhaustive BIC is noisy at budget 20 (median SHD is 1 for every method). ECHO V0 is not distinguishable from uncertainty. Diversity and even open-loop match or beat it on mean SHD; that is a warning against over-interpreting the evaluator, not a reason to prefer open-loop for surface recovery (open-loop RMSE is 3× worse).

## What this does not support

- ECHO as a causal discovery algorithm.
- A stable ranking of sequential designs on SHD in this protocol.
