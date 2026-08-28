# Decision: ECHO hypothesis score is Box–Hill discrimination

**Decision:** `echo_hypothesis` scores a candidate by the posterior-weighted symmetrized KL between Gaussian predictive distributions of competing parametric hypotheses (Box & Hill 1967). `echo_falsify` scores expected disagreement with the current leader. `echo_hypothesis_cost` divides discrimination by experimental cost.

**Reason:** Closed form, no Monte Carlo over y, interpretable as model discrimination rather than a weighted mash of GP terms.

**Alternatives:** Expected entropy reduction of P(H|D) via nested sampling; using the GP as the only belief.

**Rejected because:** Nested sampling is slower and, for Gaussian predictives, closely related to pairwise KL. The research question is whether *any* hypothesis-aware score beats generic GP uncertainty, not whether we have the unique Bayes-optimal EIG.

**Consequences:** If the true mechanism is outside the hypothesis set, discrimination can lock onto the least-wrong class. Experiment 2 uses a true class that *is* in the set. Misspecification of the set is a later experiment.
