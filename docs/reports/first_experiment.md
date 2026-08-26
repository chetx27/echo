# First experiment report

**Status:** executed, prototype.  
**Date:** 2026-08-26  
**Config:** `configs/first_experiment.yaml`  
**Config hash:** `6ffdacd9e99772df`  
**Raw summary:** `results/first_experiment/summary.json`  
**Figures:** `figures/first_experiment/`

Numbers below are copied from that summary. If they disagree, the JSON is the record.

## Question

Under a hidden nonlinear response

\[
y = 3x_1 + 2x_2^2 - 4\sin(x_3) + \varepsilon,\quad \varepsilon\sim\mathcal{N}(0,0.1^2),
\]

with 10,000 candidate experiments, budget 20 (3 shared random initial points), and a misspecified Gaussian process agent, which sequential policy recovers the function more efficiently: random, uncertainty sampling, expected improvement, local information gain, or ECHO V0 (global expected knowledge change)?

## Hypothesis (pre-specified)

1. Local information gain and uncertainty sampling rank candidates nearly identically (homoscedastic GP).
2. Expected improvement, which minimizes \(y\), recovers the surface worse than uncertainty-style design.
3. ECHO V0, which reduces entropy of \(f\) on a domain probe set, recovers the surface at least as well as local uncertainty. This was a hypothesis, not a claim.

## Result (final function-recovery RMSE, 30 seeds)

| Algorithm | Mean | Median | Std | 95% CI |
| --- | ---: | ---: | ---: | --- |
| Random | 0.969 | 0.907 | 0.267 | [0.873, 1.064] |
| Uncertainty | 0.888 | 0.880 | 0.122 | [0.844, 0.932] |
| Expected improvement | 1.920 | 1.912 | 0.592 | [1.708, 2.132] |
| Local information gain | 0.885 | 0.878 | 0.122 | [0.841, 0.928] |
| ECHO V0 | 0.877 | 0.845 | 0.173 | [0.816, 0.939] |

Paired comparisons of **ECHO V0 minus the named baseline** on function RMSE (negative favors ECHO):

| Contrast | Mean diff | Cohen's \(d\) | Wilcoxon \(p\) | ECHO wins |
| --- | ---: | ---: | ---: | ---: |
| vs random | −0.091 | −0.36 | 0.080 | 18 / 30 |
| vs uncertainty | −0.010 | −0.06 | 0.52 | 16 / 30 |
| vs expected improvement | −1.042 | −1.77 | \(1.9\times 10^{-9}\) | 30 / 30 |
| vs local IG | −0.007 | −0.04 | 0.60 | 15 / 30 |

All methods started at the same mean RMSE 5.669 after the shared 3-point initial design (sanity check).

At **t = 10**, mean function RMSE was random 2.589, ECHO V0 2.713, EI 2.848, local IG 3.605, uncertainty 3.710. Random was ahead of uncertainty-style policies at mid-budget; those policies caught up by t = 20.

## What this does and does not support

**Supported on this environment, with this budget and model.**

- Treating the scientific system as a black-box to be *minimized* (Jones et al. 1998 EI) produced much worse GP function recovery than information/uncertainty design (mean RMSE 1.92 vs ~0.88). The difference is large and consistent across seeds.
- Local information gain and uncertainty sampling were essentially the same policy, as the GP math predicted. Sequences matched on 29/30 seeds; seed 20 differed by 0.10 RMSE, which is treated as a numerical/tie artifact until proven otherwise.
- Oracle OLS parameter error dropped to ~0.015–0.019 for every method by t = 20, including EI. Surface recovery and parameter recovery **disagreed**: EI was a disaster for interpolating \(f\) and competitive for recovering \(\theta\) in the true feature basis. A single metric would have hidden that.

**Not supported.**

- ECHO V0 as a better scientific policy than uncertainty sampling. The mean improvement is 0.010 RMSE (about 1%), \(d \approx 0.06\), \(p \approx 0.52\). That is a tie.
- A significant improvement over random at \(\alpha = 0.05\) (Wilcoxon \(p = 0.080\); paired \(t\) \(p = 0.059\)). The effect vs random is modest (~9% mean RMSE) and 12/30 seeds still favored random.
- Any statement about real scientific data, LLMs, or autonomy.

## Failures

ECHO V0 had **higher** final function RMSE than uncertainty on 14/30 seeds. Records: `results/first_experiment/failures/`.

Largest gaps: seed 8 (1.232 vs 0.717), seed 25 (1.220 vs 0.864), seed 12 (0.996 vs 0.751). Seed 8 is a useful illustration of multi-metric conflict: ECHO was worse on the surface and *better* on oracle parameter RMSE (0.005 vs 0.023). Those selected points were not collapsed to a small region of the domain.

The first run of this experiment wrote zero failure files because of a bug (`echo_runs` is keyed by seed, not by algorithm name). That is fixed. The 14 reports were generated from the saved trajectories; the 150 sequential runs were not repeated.

## Interpretation

ECHO V0, as implemented, is sequential GP mutual-information design over a probe set. On this task it behaved like a slightly more expensive cousin of uncertainty sampling. That is a limitation of the *method class*, not a reason to drop the evaluation protocol.

The scientifically useful outcome of this first comparison is the **objective mismatch**: EI optimized the wrong thing for reconstructing a hidden law, and parameter recovery was too easy to separate the remaining methods.

## Limitations

- One synthetic law, isotropic RBF GP, one noise level, budget 20, 30 seeds.
- The GP cannot represent \(x_2^2\) or \(\sin(x_3)\) except by local smoothing; residual RMSE ~0.88 is far above measurement noise 0.1.
- Oracle parameter recovery uses the true features. It measures design information, not what the agent believes.
- Probe-set differential entropy is often negative (a concentrated Gaussian). It is comparable across methods, not a percentage of “knowledge.”
- Hyperparameter fits with \(n \le 20\) are unstable; the mid-budget spike in predictive std for uncertainty/IG is consistent with that.

## Next experiment

Do **not** add architecture. Change the scientific question.

Introduce competing parametric hypotheses \(H_1, H_2, H_3\) that are all plausible at \(t=0\), maintain \(P(H_i\mid D_t)\), and ask whether a hypothesis-discrimination acquisition outperforms generic uncertainty reduction on posterior entropy of \(H\), time-to-identification, and false-hypothesis elimination.

If those objectives still collapse, that is also a result.
