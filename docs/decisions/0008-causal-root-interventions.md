# Decision: Root interventions for the V2 causal world

**Decision:** Represent the four-node SCM as candidates \(x=(a,b)=\mathrm{do}(A=a,B=b)\). The agent observes \(D\). Graph recovery is evaluator-only.

**Reason:** The existing sequential loop is scalar-\(y\) GP design. Simultaneous hard interventions on the two roots fit that loop without encoding a discrete intervention target as a continuous GP input.

**Alternatives:** One-hot intervention targets; observational-only sampling; full search over \(\mathrm{do}(V=v)\) for \(V\in\{A,B,C,D\}\).

**Rejected because:** A discrete target mixed into a continuous RBF GP is a modelling artefact that would confound the scientific comparison. Single-target intervention choice remains a later experiment.

**Consequences:** This world tests whether adaptive sampling of a two-factor design recovers \(A\to C\to D\), \(B\to C\). It does not test "which variable should I intervene on." Evaluator-only BIC treats A and B as known intervention targets (empty parent sets).
