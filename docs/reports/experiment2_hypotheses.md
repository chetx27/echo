# Experiment 2 — competing hypotheses

**Status:** executed, 30 seeds.  
**Date:** 2026-09-01  
**Config:** `configs/experiment2_hypotheses.yaml`  
**Config hash:** `3449281d9bac8cd2`  
**Raw summary:** `results/experiment2_hypotheses/summary.json`  
**Figures:** `figures/experiment2_hypotheses/`

Numbers below are copied from that summary. If they disagree, the JSON is the record.

## Question

Does hypothesis discrimination (`echo_hypothesis`) outperform generic uncertainty reduction on \(P(H_{\mathrm{true}}\mid D)\) and posterior entropy of \(H\)?

Hidden law: \(y = 1.2 x^2 + 0.5 + \varepsilon\). Agent vocabulary: linear, quadratic, sinusoid.

## Result

By **t = 3** (shared initial design) mean \(P(H_{\mathrm{true}}\mid D)\) was already 0.922 for every algorithm. By **t ≈ 10** it was 1.0 for every algorithm, including random. Final hypothesis entropy is numerically zero.

Final function-recovery RMSE still separated the designs:

| Algorithm | Mean RMSE |
| --- | ---: |
| Random | 0.124 |
| ECHO hypothesis | 0.073 |
| ECHO falsify | 0.076 |
| Uncertainty | 0.065 |
| ECHO V0 | 0.062 |

## Interpretation

On this world, with \(\sigma=0.1\) and budget 20, **hypothesis identification is too easy to test discrimination**. The three classes are far apart once a handful of 1-D points exist. That is a result about the task, not a win for any policy.

Surface recovery still favors uncertainty-style design over random, matching Phase 1. ECHO hypothesis is not better than uncertainty on the GP surface.

## What this does not support

- Hypothesis discrimination as a better scientific policy than uncertainty sampling.
- Any claim that the hypothesis module is inactive; it saturates, it does not fail to run.

## Next

Keep the module. Change the task (harder class overlap, or stop the comparison at t = 4–6) before claiming a discrimination advantage.
