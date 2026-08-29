# Experiment 5 — unseen functional form

**Status:** to be filled from `results/experiment5_generalization/summary.json` after

`python -m echo compare --config configs/experiment5_generalization.yaml`

If this file still says "not yet run", do not invent numbers.

## Question

Do the same hand-designed policies (random, uncertainty, EI, local IG, ECHO V0) keep their Phase-1 ranking on a functional form that was not used to develop them?

This is not a meta-learning transfer experiment. No acquisition function in this repository is trained on other environments.

## Pre-specified comparison

Primary algorithm: `echo_v0`. Comparator: `uncertainty`. Metric: function-recovery RMSE.
Hidden law: \(y = 2\exp(-x_1^2) + 0.5 x_2 x_3 - \tanh(x_3) + \varepsilon\).
