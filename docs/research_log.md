# Research log

Failed and successful experiments both stay here. Entries are added after runs, never before.

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
