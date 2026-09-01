# experiment7_anomaly

**Status:** generated from `results/experiment7_anomaly/summary.json`.
**Date:** 2026-09-01
**Environment:** `anomaly`
**Config hash:** `e0d70d728032bfb6`
**Seeds:** 30  |  **Budget:** 20  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

When most of the domain is linear, does sequential design find a compact structured violation?

Primary algorithm: `echo_v0`. Comparator: `uncertainty`.
Primary metric: `anomaly_recall` (higher is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| random | 0.010 | 0.000 | 0.014 | [5.45e-03, 0.015] |
| uncertainty | 1.92e-03 | 0.000 | 5.85e-03 | [-1.79e-04, 4.01e-03] |
| echo_v0 | 2.12e-03 | 0.000 | 5.59e-03 | [1.23e-04, 4.13e-03] |

### `anomaly_hit_rate`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.030 | 0.000 |
| uncertainty | 5.00e-03 | 0.000 |
| echo_v0 | 6.67e-03 | 0.000 |

### `function_recovery_rmse`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.754 | 0.701 |
| uncertainty | 0.695 | 0.663 |
| echo_v0 | 0.694 | 0.679 |

## Pairwise vs primary

mean_diff = `echo_v0` − other. Positive favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_v0_vs_random | -8.17e-03 | -0.61 | 0.00286 | 1 / 30 |
| echo_v0_vs_uncertainty | 2.09e-04 | 0.04 | 1 | 2 / 30 |

## Failures

The primary method was worse than `uncertainty` on `anomaly_recall` for **1 / 30** seeds.
Seeds: 1.
Records: `results/experiment7_anomaly/failures/`.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/experiment7_anomaly.yaml
python -m echo analyze --run results/experiment7_anomaly
```
