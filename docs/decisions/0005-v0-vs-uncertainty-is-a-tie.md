# Decision: Treat V0 vs uncertainty as a tie

**Decision:** After the first 30-seed nonlinear experiment, do not describe ECHO V0 as outperforming uncertainty sampling. Report a tie on function RMSE and a clear win only against expected improvement.

**Reason:** Mean difference −0.010 RMSE, Cohen's d −0.06, Wilcoxon p = 0.52. Advertising a 1% mean gap would be cherry-picking.

**Alternatives:** Keep iterating on GP-MI weights until the curve looks better; switch immediately to a more complex agent.

**Rejected because:** The evaluation protocol already did its job. The next scientific change is a setting where objectives can disagree (competing hypotheses), not a more ornate acquisition on the same task.
