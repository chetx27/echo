# experiment4_cost

**Status:** generated from `results/experiment4_cost/summary.json`.
**Date:** 2026-09-01
**Environment:** `competing_hypotheses`
**Config hash:** `b1a4822753c8cd05`
**Seeds:** 30  |  **Budget:** 20  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

What happens when the most discriminative experiment is not the cheapest?

Primary algorithm: `echo_hypothesis_cost`. Comparator: `echo_hypothesis`.
Primary metric: `correct_hypothesis_prob` (higher is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| echo_hypothesis | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| echo_hypothesis_cost | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| echo_hypothesis_penalty | 1.000 | 1.000 | 4.83e-16 | [1.000, 1.000] |
| uncertainty | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |

### `hypothesis_entropy`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| echo_hypothesis | 6.91e-14 | 6.91e-14 |
| echo_hypothesis_cost | 6.91e-14 | 6.91e-14 |
| echo_hypothesis_penalty | 7.08e-14 | 6.91e-14 |
| uncertainty | 6.91e-14 | 6.91e-14 |

### `cost_efficiency_rmse`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| echo_hypothesis | 3.55e-04 | 3.20e-04 |
| echo_hypothesis_cost | 3.99e-04 | 3.67e-04 |
| echo_hypothesis_penalty | 0.020 | 0.018 |
| uncertainty | 3.07e-04 | 3.16e-04 |

### `total_cost`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| echo_hypothesis | 208.629 | 205.674 |
| echo_hypothesis_cost | 197.929 | 193.623 |
| echo_hypothesis_penalty | 52.914 | 53.600 |
| uncertainty | 212.443 | 212.591 |

## Pairwise vs primary

mean_diff = `echo_hypothesis_cost` − other. Positive favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_hypothesis_cost_vs_echo_hypothesis | 0.0000 | 0.00 | — | 0 / 30 |
| echo_hypothesis_cost_vs_echo_hypothesis_penalty | 1.18e-16 | 0.00 | 0.18 | 0 / 30 |
| echo_hypothesis_cost_vs_uncertainty | 0.0000 | 0.00 | — | 0 / 30 |

## Failures

The primary method was worse than `echo_hypothesis` on `correct_hypothesis_prob` for **0 / 30** seeds.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/experiment4_cost.yaml
python -m echo analyze --run results/experiment4_cost
```
