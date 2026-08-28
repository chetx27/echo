# Experiments

## First experiment (Phase 1)

**Config:** `configs/first_experiment.yaml`

| Setting | Value |
| --- | --- |
| Environment | nonlinear hidden law \(y=3x_1+2x_2^2-4\sin(x_3)+\varepsilon\) |
| Candidates | 10,000 |
| Budget | 20 (including 3 shared random init points) |
| Noise | \(\sigma=0.1\) |
| Seeds | 30 |
| Algorithms | random, uncertainty, expected improvement, local information gain, ECHO V0 |

**Metrics:** prediction/function RMSE, oracle parameter RMSE, probe entropy, discovery efficiency (RMSE / \(t\)).

**How to run:**

```bash
python -m echo compare --config configs/first_experiment.yaml
python -m echo analyze --run results/first_experiment
```

**How to read the output:** Numbers come from `results/first_experiment/summary.json`. Do not copy numbers into a paper by hand if they can be loaded from that file. Figures are written to `figures/first_experiment/`.

**Report:** `docs/reports/first_experiment.md`.

**Headline (not a claim of superiority):** EI recovered the hidden surface substantially worse than uncertainty-style design. ECHO V0 was statistically tied with uncertainty sampling on function RMSE (30 seeds).

## Smoke test

`configs/smoke.yaml` — 80 candidates, budget 6, 2 seeds. For CI and implementation checks, not for scientific claims.

## Second experiment (Phase 2)

**Config:** `configs/experiment2_hypotheses.yaml`

Competing hypotheses, 2,000 1-D candidates, budget 20, 30 seeds. Compare random, uncertainty, ECHO V0, `echo_hypothesis`, and `echo_falsify` on \(P(H_{\mathrm{true}}\mid D)\) and hypothesis entropy.

```bash
python -m echo compare --config configs/experiment2_hypotheses.yaml
```

**Report:** `docs/reports/experiment2_hypotheses.md`

Ablation (including cost): `configs/ablation_hypotheses.yaml`.
