# Experiment 4 — cost-aware discrimination

**Status:** to be filled from `results/experiment4_cost/summary.json` after

`python -m echo compare --config configs/experiment4_cost.yaml`

If this file still says "not yet run", do not invent numbers.

## Question

When experimental cost grows with \(x_1\) (`cost_mode: x_right`), does dividing discrimination by cost, or subtracting \(\lambda\cdot\mathrm{cost}\), change hypothesis recovery relative to un-normalized discrimination?

## Pre-specified comparison

Primary algorithm: `echo_hypothesis_cost`. Comparator: `echo_hypothesis`. Metric: \(P(H_{\mathrm{true}}\mid D)\). Also report `total_cost` and `cost_efficiency_rmse`.
