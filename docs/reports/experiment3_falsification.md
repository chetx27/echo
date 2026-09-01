# Experiment 3 — falsification

**Status:** executed, 30 seeds.  
**Date:** 2026-09-01  
**Config:** `configs/experiment3_falsification.yaml`  
**Config hash:** `82f24b26223be8bc`  
**Raw summary:** `results/experiment3_falsification/summary.json`  
**Figures:** `figures/experiment3_falsification/`

## Question

Does scoring disagreement with the leading hypothesis (`echo_falsify`) identify the true class faster than Box–Hill discrimination (`echo_hypothesis`)?

## Result

Final \(P(H_{\mathrm{true}}\mid D) = 1\) for random, uncertainty, `echo_hypothesis`, and `echo_falsify` (30/30 seeds). Open-loop ECHO also reached identification (mean 1.000, std \(5\times 10^{-9}\)).

Function-recovery RMSE: uncertainty 0.065, hypothesis 0.073, falsify 0.076, random 0.124, **open-loop 0.642**.

Falsify vs hypothesis on \(P(H_{\mathrm{true}})\): mean diff 0, 0 wins.

## Interpretation

Falsification cannot beat discrimination when both hit the ceiling after the initial design. The scientifically useful contrast in this run is **sequential vs open-loop**: scoring once after init and never re-ranking wrecks surface recovery (RMSE 0.64 vs ~0.07) even though the discrete hypothesis class is still identified.

## What this does not support

- Falsification as a faster identifier of \(H_{\mathrm{true}}\) on this world.
