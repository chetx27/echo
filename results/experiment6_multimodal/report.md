# experiment6_multimodal

**Status:** generated from `results/experiment6_multimodal/summary.json`.
**Date:** 2026-09-01
**Environment:** `multimodal`
**Config hash:** `c808f14467b4f892`
**Seeds:** 30  |  **Budget:** 20  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

Does sequential design visit and reconstruct three distinct mechanisms, or lock onto one region?

Primary algorithm: `echo_v0`. Comparator: `uncertainty`.
Primary metric: `mean_region_rmse` (lower is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| random | 0.769 | 0.763 | 0.140 | [0.718, 0.819] |
| uncertainty | 0.593 | 0.590 | 0.070 | [0.568, 0.619] |
| diversity | 0.576 | 0.568 | 0.046 | [0.559, 0.592] |
| echo_v0 | 0.605 | 0.603 | 0.045 | [0.589, 0.621] |

### `region_coverage`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 1.000 | 1.000 |
| uncertainty | 1.000 | 1.000 |
| diversity | 1.000 | 1.000 |
| echo_v0 | 1.000 | 1.000 |

### `function_recovery_rmse`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.843 | 0.825 |
| uncertainty | 0.646 | 0.633 |
| diversity | 0.627 | 0.623 |
| echo_v0 | 0.655 | 0.649 |

## Pairwise vs primary

mean_diff = `echo_v0` − other. Negative favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_v0_vs_random | -0.1639 | -1.10 | 6.9e-07 | 26 / 30 |
| echo_v0_vs_uncertainty | 0.0114 | 0.14 | 0.191 | 10 / 30 |
| echo_v0_vs_diversity | 0.0292 | 0.46 | 0.012 | 8 / 30 |

## Failures

The primary method was worse than `uncertainty` on `mean_region_rmse` for **20 / 30** seeds.
Seeds: 0, 2, 4, 5, 6, 8, 10, 11, 14, 15, 16, 17, 19, 20, 21, 23, 25, 26, 27, 29.
Records: `results/experiment6_multimodal/failures/`.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/experiment6_multimodal.yaml
python -m echo analyze --run results/experiment6_multimodal
```
