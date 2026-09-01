# experiment5_generalization

**Status:** generated from `results/experiment5_generalization/summary.json`.
**Date:** 2026-09-01
**Environment:** `unseen`
**Config hash:** `7ddcb47494cd7a37`
**Seeds:** 30  |  **Budget:** 20  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

Do the same hand-designed policies keep their ranking on an unused functional form?

Primary algorithm: `echo_v0`. Comparator: `uncertainty`.
Primary metric: `function_recovery_rmse` (lower is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| random | 0.544 | 0.517 | 0.138 | [0.494, 0.593] |
| uncertainty | 0.416 | 0.403 | 0.051 | [0.398, 0.434] |
| expected_improvement | 0.749 | 0.670 | 0.264 | [0.655, 0.843] |
| information_gain | 0.419 | 0.403 | 0.048 | [0.402, 0.436] |
| echo_v0 | 0.385 | 0.383 | 0.034 | [0.373, 0.397] |

### `parameter_recovery_rmse`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.028 | 0.023 |
| uncertainty | 0.026 | 0.027 |
| expected_improvement | 0.049 | 0.039 |
| information_gain | 0.028 | 0.027 |
| echo_v0 | 0.029 | 0.025 |

### `probe_entropy`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | -905.634 | -900.810 |
| uncertainty | -1316.887 | -1374.523 |
| expected_improvement | -1022.800 | -1054.084 |
| information_gain | -1306.201 | -1374.523 |
| echo_v0 | -1280.777 | -1343.072 |

### `mean_predictive_std`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.409 | 0.423 |
| uncertainty | 0.249 | 0.259 |
| expected_improvement | 0.621 | 0.556 |
| information_gain | 0.258 | 0.259 |
| echo_v0 | 0.257 | 0.256 |

## Pairwise vs primary

mean_diff = `echo_v0` − other. Negative favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_v0_vs_random | -0.1587 | -1.10 | 8.0e-08 | 27 / 30 |
| echo_v0_vs_uncertainty | -0.0312 | -0.47 | 0.0364 | 19 / 30 |
| echo_v0_vs_expected_improvement | -0.3643 | -1.35 | 3.7e-09 | 29 / 30 |
| echo_v0_vs_information_gain | -0.0340 | -0.51 | 0.0175 | 20 / 30 |

## Failures

The primary method was worse than `uncertainty` on `function_recovery_rmse` for **11 / 30** seeds.
Seeds: 1, 9, 11, 13, 16, 17, 19, 20, 21, 23, 27.
Records: `results/experiment5_generalization/failures/`.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/experiment5_generalization.yaml
python -m echo analyze --run results/experiment5_generalization
```
