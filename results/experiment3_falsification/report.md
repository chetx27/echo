# experiment3_falsification

**Status:** generated from `results/experiment3_falsification/summary.json`.
**Date:** 2026-09-01
**Environment:** `competing_hypotheses`
**Config hash:** `82f24b26223be8bc`
**Seeds:** 30  |  **Budget:** 20  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

Does scoring disagreement with the leading hypothesis identify the true class faster?

Primary algorithm: `echo_falsify`. Comparator: `echo_hypothesis`.
Primary metric: `correct_hypothesis_prob` (higher is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| random | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| uncertainty | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| echo_hypothesis | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| echo_falsify | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| echo_no_sequential | 1.000 | 1.000 | 5.01e-09 | [1.000, 1.000] |

### `hypothesis_entropy`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 6.91e-14 | 6.91e-14 |
| uncertainty | 6.91e-14 | 6.91e-14 |
| echo_hypothesis | 6.91e-14 | 6.91e-14 |
| echo_falsify | 6.91e-14 | 6.91e-14 |
| echo_no_sequential | 1.68e-08 | 6.91e-14 |

### `function_recovery_rmse`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.124 | 0.095 |
| uncertainty | 0.065 | 0.066 |
| echo_hypothesis | 0.073 | 0.069 |
| echo_falsify | 0.076 | 0.073 |
| echo_no_sequential | 0.642 | 0.621 |

### `leading_hypothesis_correct`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 1.000 | 1.000 |
| uncertainty | 1.000 | 1.000 |
| echo_hypothesis | 1.000 | 1.000 |
| echo_falsify | 1.000 | 1.000 |
| echo_no_sequential | 1.000 | 1.000 |

## Pairwise vs primary

mean_diff = `echo_falsify` − other. Positive favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_falsify_vs_random | 0.0000 | 0.00 | — | 0 / 30 |
| echo_falsify_vs_uncertainty | 0.0000 | 0.00 | — | 0 / 30 |
| echo_falsify_vs_echo_hypothesis | 0.0000 | 0.00 | — | 0 / 30 |
| echo_falsify_vs_echo_no_sequential | 9.15e-10 | 0.18 | 0.18 | 1 / 30 |

## Failures

The primary method was worse than `echo_hypothesis` on `correct_hypothesis_prob` for **0 / 30** seeds.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/experiment3_falsification.yaml
python -m echo analyze --run results/experiment3_falsification
```
