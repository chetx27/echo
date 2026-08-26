# Methodology (V0)

## Problem

Let \(\mathcal{S}\) be an unknown scientific system. At time \(t\) the agent has data \(D_t\) and a finite candidate set \(\mathcal{X}_t = \{x_1,\ldots,x_n\}\). It may run \(B\) experiments. A policy \(\pi\) selects

\[
x_t = \pi(D_t, \mathcal{X}_t),
\qquad
y_t \sim P(y \mid x_t, D_t),
\qquad
D_{t+1} = D_t \cup \{(x_t, y_t)\}.
\]

The agent never observes the hidden law. Evaluation uses the hidden law after the fact.

## Environments

**Linear.** \(y = 3x_1 + 2x_2 - 4x_3 + \varepsilon\).

**Nonlinear (first experiment).** \(y = 3x_1 + 2x_2^2 - 4\sin(x_3) + \varepsilon\).

Domain: \([-2,2]^3\). Noise \(\varepsilon \sim \mathcal{N}(0, \sigma^2)\) with \(\sigma = 0.1\) unless configured otherwise. Each seed draws a fresh candidate set and a per-candidate noise vector so that two policies querying the same index receive the same \(y\).

Candidates and a held-out test set are drawn independently. The test set is evaluator-only.

## Belief model

ECHO V0 uses exact Gaussian process regression with an RBF kernel and Gaussian observation noise. Inputs are scaled to the unit cube using the known domain bounds. Outputs are standardized using the mean and standard deviation of the initial design; that scale is then frozen.

Hyperparameters (lengthscale, signal variance, noise variance) are fit by maximizing the log marginal likelihood (L-BFGS-B, bounded). This is a modelling choice, not a claim that the GP is the true scientific model. The GP is misspecified for both hidden laws.

## Initial design

The first \(n_{\mathrm{init}}\) experiments (default 3) are chosen uniformly without replacement, using a seed-derived stream that is **shared across algorithms**. Those points count toward the budget. Adaptive selection then proceeds one experiment at a time, refitting the GP after every observation.

## Acquisition functions

**Random.** Uniform among remaining candidates.

**Uncertainty.** \(x^\star = \arg\max_x \sigma_f(x)\), posterior std of the latent function.

**Expected improvement (minimization, Jones et al. 1998).**

\[
\mathrm{EI}(x) = (y_{\min} - \mu(x))\Phi(z) + \sigma_f(x)\phi(z),
\quad
z = (y_{\min}-\mu(x))/\sigma_f(x).
\]

This is an optimization baseline. It is not a discovery objective.

**Local information gain.**

\[
I(y; f(x)\mid D) = \tfrac12 \log\bigl(1 + \sigma_f^2(x)/\sigma_n^2\bigr).
\]

For homoscedastic GP regression this ranking is identical to uncertainty sampling.

**ECHO V0: global expected knowledge change.**

Let \(f_{\mathrm{probe}}\) be the latent function on a fixed probe set in the domain (not the evaluation test set). The score is

\[
I(y(x); f_{\mathrm{probe}}\mid D) = H[f_{\mathrm{probe}}\mid D] - H[f_{\mathrm{probe}}\mid D, y(x)].
\]

The GP posterior covariance does not depend on the realized \(y\), so this is closed form (matrix-determinant lemma). The probe set is a scientific-design choice of the algorithm. It is not hidden-state leakage: the agent never sees \(f\) there.

This is one interpretable score, not a weighted sum of unrelated terms. It is closely related to GP mutual-information design (MacKay 1992; Krause et al. 2008). What is being tested is whether that objective aligns with mechanism/parameter recovery under a small budget.

## Metrics

All metrics are computed after every observation.

| Metric | Meaning |
| --- | --- |
| Function recovery / prediction error | RMSE of GP mean vs noiseless \(f\) on the held-out test set |
| Parameter recovery | RMSE of OLS coefficients in the **oracle** feature basis vs true \(\theta\) (evaluator only) |
| Probe entropy | Differential entropy of the GP posterior on the algorithm probe set |
| Discovery-efficiency curve | Function-recovery RMSE versus number of experiments (the primary plot) |

Parameter recovery asks whether the **design** is informative for the true mechanism if an oracle model class were used. The agent does not have that class.

## Statistics

Seeds are paired (same environment seed ⇒ same candidates, noise, and initial design). Report mean, median, standard deviation, and a normal-approximation 95% CI over seeds. Pairwise tests: Wilcoxon signed-rank, paired t-test, paired Cohen's \(d\). A "win" is a strictly lower final function RMSE.

## Failure analysis

A run is recorded as a failure if ECHO V0's final function RMSE is worse than uncertainty sampling on the same seed. The record includes the experiment sequence and a short note. Failures are evidence, not something to hide.

## Limitations (V0)

- Two synthetic worlds only.
- GP is misspecified; no discrete hypotheses yet.
- Local IG and uncertainty are mathematically equivalent here.
- EI minimizes \(y\), which may be the wrong scientific target.
- Probe-set size and kernel family are fixed, not ablated.
- 30 seeds is a start, not a comprehensive study.
- No real scientific data.
