# Failure analysis

Failures are recorded when ECHO V0's final function-recovery RMSE is strictly worse than uncertainty sampling on the same seed.

Location: `results/<run>/failures/seed_<k>.json`

## First experiment (nonlinear, 30 seeds)

14 / 30 seeds. Seeds: 2, 7, 8, 10, 11, 12, 13, 18, 19, 22, 23, 25, 27, 28.

### Patterns

1. **Most failures are small.** Several deltas are < 0.03 RMSE (including seed 23, which is a near-tie). These should not be over-interpreted.
2. **A few failures are large.** Seeds 8, 25, and 12. Seed 8: ECHO 1.232 vs uncertainty 0.717. The ECHO design was not collapsed in input space (coordinate-wise std ≈ 1.76 on \([-2,2]\)).
3. **Metrics disagree inside a failure.** Seed 8: ECHO worse on the GP surface, better on oracle parameter RMSE (0.005 vs 0.023). “Failure” is metric-dependent.
4. **Mid-budget, uncertainty itself can lose to random.** That is not an ECHO-only failure; it suggests GP hyperparameter instability while \(n\) is still tiny, which then affects every uncertainty-like policy.

### Implementation failure (process)

The first write of this experiment stored `n_failures_vs_comparator: 0` because failure collection looked up `"echo_v0"` in a dict keyed by integer seed. Trajectories were intact. Reports were rebuilt from `results/first_experiment/runs/` after fixing `echo/experiments/compare.py`.

Do not delete these records.

## Other 30-seed runs (2026-09-01)

Failure files exist under `results/<run>/failures/` for causal, multimodal, anomaly, and unseen-form comparisons. The metric is the run's `failure_metric`, not always function RMSE. Experiment 7 is the sharp case: uncertainty-style policies query the anomaly box less than random.
