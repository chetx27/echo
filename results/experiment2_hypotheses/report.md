# experiment2_hypotheses

**Status:** generated from `results/experiment2_hypotheses/summary.json`.
**Date:** 2026-09-01
**Environment:** `competing_hypotheses`
**Config hash:** `3449281d9bac8cd2`
**Seeds:** 30  |  **Budget:** 20  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

Does hypothesis discrimination beat generic uncertainty on P(H_true|D)?

Primary algorithm: `echo_hypothesis`. Comparator: `uncertainty`.
Primary metric: `correct_hypothesis_prob` (higher is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| random | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| uncertainty | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| echo_v0 | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| echo_hypothesis | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| echo_falsify | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |

### `hypothesis_entropy`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 6.91e-14 | 6.91e-14 |
| uncertainty | 6.91e-14 | 6.91e-14 |
| echo_v0 | 6.91e-14 | 6.91e-14 |
| echo_hypothesis | 6.91e-14 | 6.91e-14 |
| echo_falsify | 6.91e-14 | 6.91e-14 |

### `function_recovery_rmse`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.124 | 0.095 |
| uncertainty | 0.065 | 0.066 |
| echo_v0 | 0.062 | 0.063 |
| echo_hypothesis | 0.073 | 0.069 |
| echo_falsify | 0.076 | 0.073 |

### `leading_hypothesis_correct`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 1.000 | 1.000 |
| uncertainty | 1.000 | 1.000 |
| echo_v0 | 1.000 | 1.000 |
| echo_hypothesis | 1.000 | 1.000 |
| echo_falsify | 1.000 | 1.000 |

## Pairwise vs primary

mean_diff = `echo_hypothesis` − other. Positive favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_hypothesis_vs_random | 0.0000 | 0.00 | — | 0 / 30 |
| echo_hypothesis_vs_uncertainty | 0.0000 | 0.00 | — | 0 / 30 |
| echo_hypothesis_vs_echo_v0 | 0.0000 | 0.00 | — | 0 / 30 |
| echo_hypothesis_vs_echo_falsify | 0.0000 | 0.00 | — | 0 / 30 |

## Failures

The primary method was worse than `uncertainty` on `correct_hypothesis_prob` for **0 / 30** seeds.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/experiment2_hypotheses.yaml
python -m echo analyze --run results/experiment2_hypotheses
```
