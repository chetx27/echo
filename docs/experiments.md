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

Remaining 30-seed runs (2026-09-01) are in `docs/reports/`. Short version: competing-hypothesis identification saturates for every policy; cost wrappers change spend not \(P(H_{\mathrm{true}})\); causal SHD does not rank designs; multimodal coverage is complete for all methods with diversity best on region RMSE; the anomaly box is found more often by **random** than by uncertainty/ECHO V0; on the unseen form ECHO V0 beat uncertainty at \(p=0.036\) (19/30) while EI stayed worst.

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

## Third experiment (falsification)

**Config:** `configs/experiment3_falsification.yaml`

Same competing-hypotheses world as experiment 2. Primary algorithm: `echo_falsify`. Comparator: `echo_hypothesis`.

```bash
python -m echo compare --config configs/experiment3_falsification.yaml
```

**Report:** `docs/reports/experiment3_falsification.md` (fill from `summary.json`).

## Fourth experiment (cost)

**Config:** `configs/experiment4_cost.yaml`

`cost_mode: x_right`. Compare un-normalized discrimination, discrimination/cost, and discrimination \(-\lambda\cdot\mathrm{cost}\).

```bash
python -m echo compare --config configs/experiment4_cost.yaml
```

**Report:** `docs/reports/experiment4_cost.md`.

## Fifth experiment (unseen form)

**Config:** `configs/experiment5_generalization.yaml`

Unseen functional form, 10,000 candidates, budget 20, 30 seeds. Same policy set as the first experiment. This is not a learned-policy transfer test.

```bash
python -m echo compare --config configs/experiment5_generalization.yaml
```

**Report:** `docs/reports/experiment5_generalization.md`.

## Sixth experiment (multimodal regions)

**Config:** `configs/experiment6_multimodal.yaml`

Three piecewise mechanisms in \(x_1\). Primary metric: mean per-region RMSE. Also report region coverage.

```bash
python -m echo compare --config configs/experiment6_multimodal.yaml --jobs 4
```

**Report:** `docs/reports/experiment6_multimodal.md`.

## Seventh experiment (anomaly box)

**Config:** `configs/experiment7_anomaly.yaml`

Linear background plus a compact structured offset. Primary metric: anomaly-box recall.

```bash
python -m echo compare --config configs/experiment7_anomaly.yaml --jobs 4
```

**Report:** `docs/reports/experiment7_anomaly.md`.

## Causal comparison

**Config:** `configs/experiment_causal.yaml`

```bash
python -m echo compare --config configs/experiment_causal.yaml --jobs 4
```

**Report:** `docs/reports/experiment_causal.md`.

## Custom systems

See `docs/using_echo.md`. Minimal example: `examples/oscillator.py` and `configs/example_oscillator.yaml`.

Smoke checks: `configs/smoke.yaml`, `configs/smoke_hypotheses.yaml`, `configs/smoke_phase3.yaml`, `configs/smoke_multimodal.yaml`, `configs/smoke_anomaly.yaml`.

Cheap sweeps (5 seeds, not paper-grade): `scripts/run_noise_sweep.py`, `scripts/run_budget_sweep.py`.

Task index: `python -m echo bench`.

`compare` resumes completed seed/algorithm trajectories. Use `--no-resume` to force a rerun.
