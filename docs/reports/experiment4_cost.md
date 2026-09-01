# Experiment 4 — cost-aware discrimination

**Status:** executed, 30 seeds.  
**Date:** 2026-09-01  
**Config:** `configs/experiment4_cost.yaml`  
**Config hash:** `b1a4822753c8cd05`  
**Raw summary:** `results/experiment4_cost/summary.json`  
**Figures:** `figures/experiment4_cost/`

## Question

When experimental cost grows with \(x_1\) (`cost_mode: x_right`), does dividing discrimination by cost, or subtracting \(\lambda\cdot\mathrm{cost}\), change the selected sequence?

## Result

Final \(P(H_{\mathrm{true}}\mid D) = 1\) for all four algorithms. Identification therefore does not rank them.

Mean **total cost** at t = 20:

| Algorithm | Mean total cost |
| --- | ---: |
| Uncertainty | 212.4 |
| ECHO hypothesis | 208.6 |
| ECHO hypothesis / cost | 197.9 |
| ECHO hypothesis − λ cost | 52.9 |

Cost-efficiency RMSE is ~3–4×10⁻⁴ for the first three and 0.020 for the penalty wrapper (it spends much less and reconstructs the surface worse).

## Interpretation

Cost wrappers **do change the design**. The penalty form is aggressive: it avoids the expensive side of the domain. Per-cost normalization is a mild shift (~5% lower spend than un-normalized discrimination). Because \(H_{\mathrm{true}}\) is already identified from cheap points, the interesting metric here is spend, not posterior mass.

## What this does not support

- A claim that cheaper designs recover the mechanism better. They do not, on RMSE.
