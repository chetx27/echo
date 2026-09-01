# first_experiment

**Status:** generated from `results/first_experiment/summary.json`.
**Date:** 2026-09-01
**Environment:** `nonlinear`
**Config hash:** `6ffdacd9e99772df`
**Seeds:** 30  |  **Budget:** 20  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

Which sequential policy recovers a hidden nonlinear surface under budget 20?

Primary algorithm: `echo_v0`. Comparator: `uncertainty`.
Primary metric: `function_recovery_rmse` (lower is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| random | 0.969 | 0.907 | 0.267 | [0.873, 1.064] |
| uncertainty | 0.888 | 0.880 | 0.122 | [0.844, 0.932] |
| expected_improvement | 1.920 | 1.912 | 0.592 | [1.708, 2.132] |
| information_gain | 0.885 | 0.878 | 0.122 | [0.841, 0.928] |
| echo_v0 | 0.877 | 0.845 | 0.173 | [0.816, 0.939] |

## Pairwise vs primary

mean_diff = `echo_v0` − other. Negative favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_v0_vs_random | -0.0911 | -0.36 | 0.0803 | 18 / 30 |
| echo_v0_vs_uncertainty | -0.0105 | -0.06 | 0.516 | 16 / 30 |
| echo_v0_vs_expected_improvement | -1.0423 | -1.77 | 1.9e-09 | 30 / 30 |
| echo_v0_vs_information_gain | -7.17e-03 | -0.04 | 0.598 | 15 / 30 |

## Failures

The primary method was worse than `uncertainty` on `function_recovery_rmse` for **14 / 30** seeds.
Seeds: 2, 7, 8, 10, 11, 12, 13, 18, 19, 22, 23, 25, 27, 28.
Records: `results/first_experiment/failures/`.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/first_experiment.yaml
python -m echo analyze --run results/first_experiment
```
