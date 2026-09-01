# Experiment 6 — multimodal regions

**Status:** executed, 30 seeds.  
**Date:** 2026-09-01  
**Config:** `configs/experiment6_multimodal.yaml`  
**Config hash:** `c808f14467b4f892`  
**Raw summary:** `results/experiment6_multimodal/summary.json`  
**Figures:** `figures/experiment6_multimodal/`

## Question

Does sequential design visit and reconstruct three distinct mechanisms, or lock onto one region of \(x_1\)?

## Result

Region coverage is 1.0 by mid-budget for **every** method, including random. Nobody locked onto one region under budget 20 with 2,000 candidates.

Final mean per-region RMSE:

| Algorithm | Mean | Median | 95% CI |
| --- | ---: | ---: | --- |
| Random | 0.769 | 0.763 | [0.718, 0.819] |
| ECHO V0 | 0.605 | 0.603 | [0.589, 0.621] |
| Uncertainty | 0.593 | 0.590 | [0.568, 0.619] |
| Diversity | 0.576 | 0.568 | [0.559, 0.592] |

ECHO V0 vs random: mean diff −0.164, \(d=-1.10\), \(p=6.9\times 10^{-7}\), 26/30.  
ECHO V0 vs uncertainty: +0.011, \(p=0.19\) (tie).  
ECHO V0 vs diversity: +0.029, \(p=0.012\) (diversity better).  
ECHO worse than uncertainty on 20/30 seeds; most of those gaps are small.

## Interpretation

The coverage question is answered: with this budget the domain is visited. Reconstruction still favors space-filling / uncertainty-style design over random. Diversity, not ECHO V0, is the best of the adaptive set on mean region RMSE. ECHO V0 again behaves like a cousin of uncertainty sampling.

## What this does not support

- ECHO V0 as a specialized multi-mechanism explorer.
