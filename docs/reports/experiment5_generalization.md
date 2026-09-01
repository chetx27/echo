# Experiment 5 — unseen functional form

**Status:** executed, 30 seeds.  
**Date:** 2026-09-01  
**Config:** `configs/experiment5_generalization.yaml`  
**Config hash:** `7ddcb47494cd7a37`  
**Raw summary:** `results/experiment5_generalization/summary.json`  
**Figures:** `figures/experiment5_generalization/`

This is not a meta-learning transfer experiment. Policies are not trained on other worlds.

## Question

Do the same hand-designed policies (random, uncertainty, EI, local IG, ECHO V0) keep their Phase-1 ranking on

\[
y = 2\exp(-x_1^2) + 0.5 x_2 x_3 - \tanh(x_3) + \varepsilon
\]

?

## Result (final function-recovery RMSE, 30 seeds)

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| Expected improvement | 0.749 | 0.670 | 0.264 | [0.655, 0.843] |
| Random | 0.544 | 0.517 | 0.138 | [0.494, 0.593] |
| Local information gain | 0.419 | 0.403 | 0.048 | [0.402, 0.436] |
| Uncertainty | 0.416 | 0.403 | 0.051 | [0.398, 0.434] |
| ECHO V0 | 0.385 | 0.383 | 0.034 | [0.373, 0.397] |

ECHO V0 vs uncertainty: mean diff −0.031, \(d=-0.47\), Wilcoxon \(p=0.036\), 19/30.  
ECHO V0 vs local IG: −0.034, \(p=0.018\), 20/30.  
ECHO V0 vs random: −0.159, \(p=8\times 10^{-8}\), 27/30.  
ECHO V0 vs EI: −0.364, \(p=3.7\times 10^{-9}\), 29/30.

ECHO V0 lost to uncertainty on 11/30 seeds.

Oracle parameter RMSE stayed easy (~0.026–0.049) for all methods.

## Interpretation

**What held from Phase 1.** EI is still the wrong objective for reconstructing \(f\). Local IG still matches uncertainty (homoscedastic GP). Random is worse than uncertainty-style design.

**What changed.** On this unused form, ECHO V0 is no longer a statistical tie with uncertainty: the ~7% mean RMSE gap is significant at \(\alpha=0.05\), with a moderate paired effect. It is still the same method class (global probe-set mutual information vs local variance). Do not generalize from one extra environment to “ECHO is better.”

## What this does not support

- A trained acquisition that transferred. Nothing was trained.
- A claim that ECHO V0 will beat uncertainty on the next unused form.
