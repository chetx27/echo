# Decision: Remaining BO/AL baselines for V1

**Decision:** Implement greedy mean, diversity, GP-UCB, and mean-field Thompson sampling as named baselines.

**Reason:** The original protocol listed these. Experiment 1 omitted them to keep the first comparison small. They are now available for any config.

**Alternatives:** Exact joint Thompson (full posterior covariance); minimization-form UCB.

**Rejected because:** Joint TS on 10,000 points is O(n³). Mean-field TS is an explicit approximation. UCB uses the common maximization form μ+κσ; EI remains the minimization form from Jones et al. 1998. That mix is documented, not hidden.
