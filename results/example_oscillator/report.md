# example_oscillator

**Status:** generated from `results/example_oscillator/summary.json`.
**Date:** 2026-09-01
**Environment:** `oscillator`
**Config hash:** `9ba590b83215a3df`
**Seeds:** 5  |  **Budget:** 12  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

On a 1-D oscillator, does ECHO V0 recover the surface better than uncertainty sampling?

Primary algorithm: `echo_v0`. Comparator: `uncertainty`.
Primary metric: `function_recovery_rmse` (lower is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| random | 0.217 | 0.238 | 0.091 | [0.137, 0.297] |
| uncertainty | 0.094 | 0.092 | 0.021 | [0.076, 0.112] |
| echo_v0 | 0.111 | 0.113 | 0.039 | [0.077, 0.145] |

### `parameter_recovery_rmse`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.022 | 9.89e-03 |
| uncertainty | 0.029 | 0.032 |
| echo_v0 | 0.026 | 0.025 |

## Pairwise vs primary

mean_diff = `echo_v0` − other. Negative favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_v0_vs_random | -0.1063 | -1.17 | 0.0625 | 5 / 5 |
| echo_v0_vs_uncertainty | 0.0165 | 0.40 | 0.438 | 1 / 5 |

## Failures

The primary method was worse than `uncertainty` on `function_recovery_rmse` for **4 / 5** seeds.
Seeds: 0, 2, 3, 4.
Records: `results/example_oscillator/failures/`.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/example_oscillator.yaml
python -m echo analyze --run results/example_oscillator
```
