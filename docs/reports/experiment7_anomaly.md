# Experiment 7 — anomaly box

**Status:** executed, 30 seeds.  
**Date:** 2026-09-01  
**Config:** `configs/experiment7_anomaly.yaml`  
**Config hash:** `e0d70d728032bfb6`  
**Raw summary:** `results/experiment7_anomaly/summary.json`  
**Figures:** `figures/experiment7_anomaly/`

## Question

When most of the domain obeys a linear law, does sequential design find a compact structured violation (the +4 offset box)?

## Result (anomaly-box recall, 30 seeds)

| Algorithm | Mean recall | Hit rate | Function RMSE |
| --- | ---: | ---: | ---: |
| Random | 0.0103 | 0.0300 | 0.754 |
| ECHO V0 | 0.0021 | 0.0067 | 0.694 |
| Uncertainty | 0.0019 | 0.0050 | 0.695 |

ECHO V0 vs random on recall: mean diff −0.008, \(d=-0.61\), Wilcoxon \(p=0.0029\) (**random better**).  
ECHO V0 vs uncertainty: ~0, \(p=1\).

Uncertainty-style methods reconstruct the *background* surface slightly better than random (RMSE 0.69 vs 0.75) and almost never query the box after the shared init.

## Interpretation

This is a clean **failure of uncertainty / ECHO V0 for structured incompleteness**. A compact offset does not look like high GP posterior variance on the rest of the domain; random luck finds it more often. If the scientific target is “notice that the linear law is wrong in a region,” these acquisition functions are the wrong objective.

## What this does not support

- Using ECHO V0 (or uncertainty sampling) as an anomaly / model-incompleteness hunter on this geometry.
