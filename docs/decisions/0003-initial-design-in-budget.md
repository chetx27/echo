# Decision: Initial design counts toward the budget

**Decision:** Each run begins with `n_init` (default 3) uniformly chosen candidates, using a seed stream shared across algorithms. Those evaluations count toward `budget`.

**Reason:** A GP cannot be fit on an empty set. Sharing the initial design makes later differences attributable to the acquisition policy, not to lucky first points.

**Alternatives:** Space-filling initial designs (Latin hypercube, Sobol); not counting init against the budget; policy-specific init.

**Rejected because:** Different init schemes would confound the first comparison. A free init would overstate the adaptive budget.

**Consequences:** Learning curves start at \(t = n_{\mathrm{init}}\) and should overlap across algorithms at that first plotted point.
