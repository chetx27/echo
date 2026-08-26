# Decision: Gaussian processes for V0

**Decision:** Use exact Gaussian process regression with an RBF kernel as the V0 belief model.

**Reason:** Sequential experiment selection needs calibrated posterior uncertainty and an interpretable update after every observation. With budget 20, exact inference is cheap and inspectable.

**Alternatives:** Random-forest uncertainty, neural ensembles, Bayesian neural nets, the true parametric family (oracle).

**Rejected because:** Neural ensembles are less interpretable at this stage. Using the true parametric family would leak the scientific law into the agent. sklearn's GP is available as a dependency for later work; V0 implements an exact GP so posterior covariances for global information gain are under our control.

**Consequences:** The agent is misspecified for both synthetic laws. Parameter recovery is therefore an *evaluator-only* OLS fit in the oracle feature basis, not something the GP reports.
