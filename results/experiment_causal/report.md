# experiment_causal

**Status:** generated from `results/experiment_causal/summary.json`.
**Date:** 2026-09-01
**Environment:** `causal`
**Config hash:** `4717093f690d9431`
**Seeds:** 30  |  **Budget:** 20  |  **Init:** 3

If these numbers disagree with the JSON, the JSON is the record. Do not treat this file as a claim of superiority.

## Question

Do sequential designs recover a hidden four-node SCM better than random?

Primary algorithm: `echo_v0`. Comparator: `uncertainty`.
Primary metric: `structural_hamming_distance` (lower is better).

## Final results

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| random | 1.467 | 1.000 | 0.860 | [1.159, 1.775] |
| uncertainty | 1.333 | 1.000 | 0.844 | [1.031, 1.635] |
| diversity | 1.200 | 1.000 | 0.551 | [1.003, 1.397] |
| echo_v0 | 1.267 | 1.000 | 0.740 | [1.002, 1.531] |
| echo_no_sequential | 1.200 | 1.000 | 0.551 | [1.003, 1.397] |

### `parent_set_f1`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.797 | 0.857 |
| uncertainty | 0.795 | 0.857 |
| diversity | 0.837 | 0.857 |
| echo_v0 | 0.812 | 0.857 |
| echo_no_sequential | 0.838 | 0.857 |

### `function_recovery_rmse`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | 0.087 | 0.077 |
| uncertainty | 0.072 | 0.067 |
| diversity | 0.065 | 0.062 |
| echo_v0 | 0.069 | 0.062 |
| echo_no_sequential | 0.204 | 0.123 |

### `probe_entropy`

| Algorithm | Mean | Median |
| --- | ---: | ---: |
| random | -395.124 | -401.515 |
| uncertainty | -400.486 | -405.101 |
| diversity | -400.923 | -404.724 |
| echo_v0 | -400.196 | -405.477 |
| echo_no_sequential | -375.973 | -391.546 |

## Pairwise vs primary

mean_diff = `echo_v0` − other. Negative favors the primary method on this metric.

| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |
| --- | ---: | ---: | ---: | ---: |
| echo_v0_vs_random | -0.2000 | -0.19 | 0.238 | 6 / 30 |
| echo_v0_vs_uncertainty | -0.0667 | -0.08 | 0.599 | 5 / 30 |
| echo_v0_vs_diversity | 0.0667 | 0.08 | 0.539 | 5 / 30 |
| echo_v0_vs_echo_no_sequential | 0.0667 | 0.07 | 0.663 | 8 / 30 |

## Failures

The primary method was worse than `uncertainty` on `structural_hamming_distance` for **5 / 30** seeds.
Seeds: 5, 8, 10, 13, 21.
Records: `results/experiment_causal/failures/`.

## What this does not support

- A claim that ECHO is a general scientific agent.
- Transfer to real laboratory data unless a tabular/CSV world was used.
- Any LLM or autonomy result. This repository does not use a language model.

## How to reproduce

```bash
python -m echo compare --config configs/experiment_causal.yaml
python -m echo analyze --run results/experiment_causal
```
