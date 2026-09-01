# Research log

Failed and successful experiments both stay here. Entries are added after runs, never before.

---

## 2026-09-01 — Experiment 5 (unseen form, 30 seeds)

### Question

Do Phase-1 policy rankings hold on \(y=2e^{-x_1^2}+0.5 x_2 x_3-\tanh(x_3)+\varepsilon\)?

### Result

Final mean function RMSE: ECHO V0 0.385, uncertainty 0.416, local IG 0.419, random 0.544, EI 0.749.

ECHO vs uncertainty: \(d=-0.47\), Wilcoxon \(p=0.036\), 19/30. EI remains worst.

### Interpretation

EI/random/uncertainty-family ranking held. The V0 vs-uncertainty tie from the nonlinear world did **not** hold here. One environment; 11/30 seeds still favor uncertainty. Not a transfer-learning result.

---

## 2026-09-01 — Laboratory API (V2 complete)

### Question

Can the same sequential-design loop accept a user function, a CSV table, and a plugin policy without changing the evaluator isolation rules?

### Hypothesis

Registration (`register_function`, `register_policy`, YAML `plugin:`) is enough; no LLM layer is required.

### Method

`echo.lab`, `echo.environments.function`, `echo.environments.tabular`, resume/`--jobs` in `compare`, `python -m echo list|report`. Tests in `tests/test_lab.py`.

### Result

37 tests passed. First-experiment config hash still `6ffdacd9e99772df`. Example: `configs/example_oscillator.yaml`.

### Interpretation

The repository is now a reusable lab. Scientific rankings are unchanged: they still come from `summary.json`.

### Next experiment

Run remaining paper configs (2–7, causal) at 30 seeds.

---

## 2026-09-01 — Experiment 2 (competing hypotheses, 30 seeds)

### Question

Does hypothesis discrimination beat uncertainty on \(P(H_{\mathrm{true}}\mid D)\)?

### Result

Final \(P(H_{\mathrm{true}})=1\) for every algorithm, including random. Mean \(P\) at t=3 (shared init) was already 0.922. Function RMSE: ECHO V0 0.062, uncertainty 0.065, random 0.124.

### Interpretation

The class list is too easy at this noise and budget. Discrimination cannot show an advantage. Report: `docs/reports/experiment2_hypotheses.md`.

---

## 2026-09-01 — Experiment 3 (falsification, 30 seeds)

### Result

Same identification ceiling. Open-loop ECHO RMSE 0.642 vs ~0.07 sequential. Falsify vs hypothesis on \(P(H_{\mathrm{true}})\): tie.

### Interpretation

The useful contrast is sequential vs open-loop for surface recovery, not falsify vs discriminate.

---

## 2026-09-01 — Experiment 4 (cost, 30 seeds)

### Result

Identification still saturates. Mean total cost: penalty 52.9, per-cost 197.9, un-normalized discrimination 208.6, uncertainty 212.4.

### Interpretation

Cost wrappers change spend. They do not improve mechanism recovery on this world.

---

## 2026-09-01 — Causal comparison (30 seeds)

### Result

Final mean SHD: diversity/open-loop 1.20, ECHO V0 1.27, uncertainty 1.33, random 1.47. ECHO vs uncertainty Wilcoxon \(p=0.60\).

### Interpretation

Evaluator-only BIC at n=20 is too noisy to rank sequential designs. Not a causal-discovery claim.

---

## 2026-09-01 — Experiment 6 (multimodal, 30 seeds)

### Result

Region coverage 1.0 for all methods by mid-budget. Mean region RMSE: diversity 0.576, uncertainty 0.593, ECHO V0 0.605, random 0.769. ECHO vs uncertainty \(p=0.19\); vs diversity \(p=0.012\) (diversity better).

### Interpretation

No lock-in. ECHO V0 again ties uncertainty. Diversity wins reconstruction.

---

## 2026-09-01 — Experiment 7 (anomaly box, 30 seeds)

### Result

Anomaly recall: random 0.0103, ECHO V0 0.0021, uncertainty 0.0019. Random beats ECHO (\(p=0.0029\)).

### Interpretation

Uncertainty-style design does not hunt a compact structured violation. This is a method-class failure for that scientific target.

---

## 2026-08-26 — First experiment (nonlinear, 30 seeds)

### Question

Which sequential acquisition recovers a hidden nonlinear law more efficiently under budget 20: random, uncertainty, EI, local IG, or ECHO V0?

### Hypothesis

EI should be weak for surface recovery. Local IG should match uncertainty. ECHO V0 (global knowledge change) might match or beat local uncertainty.

### Method

`python -m echo compare --config configs/first_experiment.yaml`  
Config hash `6ffdacd9e99772df`. Shared 3-point initial design. Exact RBF GP.

### Configuration

Nonlinear world, 10,000 candidates, budget 20, noise 0.1, 30 seeds, \(n_{\mathrm{probe}}=256\).

### Result

Final mean function RMSE: ECHO V0 0.877, local IG 0.885, uncertainty 0.888, random 0.969, EI 1.920.

ECHO vs uncertainty: mean diff −0.010, \(d=-0.06\), Wilcoxon \(p=0.52\), 16 wins / 14 losses.

ECHO vs EI: mean diff −1.042, \(d=-1.77\), \(p=1.9\times 10^{-9}\), 30/30.

ECHO vs random: mean diff −0.091, \(p=0.080\) (not < 0.05).

Oracle parameter RMSE ~0.015–0.019 for all methods, including EI.

### Unexpected observation

At t = 10, random had lower mean function RMSE than uncertainty (2.59 vs 3.71). Uncertainty-like methods recovered by t = 20. Seed 20 is the only seed where local IG and uncertainty diverged by a non-tiny amount (0.10 RMSE).

Seed 8: ECHO worse on the surface, better on oracle \(\theta\).

### Interpretation

On this task ECHO V0 is not a distinct scientific policy relative to uncertainty sampling. EI is the wrong objective for reconstructing \(f\), and that shows up clearly. Multi-metric evaluation is doing work: parameter recovery would have ranked EI with the others.

### Limitation

One environment, misspecified GP, easy oracle parameters, 30 seeds underpowered for the ~9% vs-random effect.

### Next experiment

Competing hypotheses: maintain \(P(H_i\mid D)\) and test hypothesis-discrimination vs uncertainty reduction.

---

## 2026-08-26 — Repository V0

### Question

Can we stand up a reproducible sequential-design laboratory (environments, GP, baselines, ECHO V0, multi-seed evaluation) without an LLM?

### Hypothesis

A GP plus global expected knowledge change can be implemented as a distinct policy from local uncertainty/EI and evaluated on a nonlinear hidden law.

### Method

New repository. No prior ocean prototype was present to preserve.

### Configuration

See `configs/smoke.yaml` and `configs/first_experiment.yaml`.

### Result

Software constructed. Numerical results for the first scientific comparison are recorded in the next log entry after `python -m echo compare --config configs/first_experiment.yaml` completes.

### Unexpected observation

(none yet)

### Interpretation

Infrastructure only.

### Limitation

No scientific claim until the first experiment's summary JSON exists.

### Next experiment

Run the 30-seed nonlinear comparison. Interpret wins, ties, and failures honestly.
