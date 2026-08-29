# Experiment 3 — falsification

**Status:** to be filled from `results/experiment3_falsification/summary.json` after

`python -m echo compare --config configs/experiment3_falsification.yaml`

If this file still says "not yet run", do not invent numbers.

## Question

Does actively scoring experiments that disagree with the current leading hypothesis identify the true class faster than Box–Hill discrimination or uncertainty sampling?

## Pre-specified comparison

Primary algorithm: `echo_falsify`. Comparator: `echo_hypothesis`. Metric: \(P(H_{\mathrm{true}}\mid D)\).
