# Eberhardt, F., Glymour, C., & Scheines, R. (2005)

- **Citation:** Eberhardt, F., Glymour, C., & Scheines, R. (2005). On the number of experiments sufficient and in the worst case necessary to identify all causal relations among N variables. In *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence* (pp. 178–184).
- **Year:** 2005
- **Problem:** How many experiments are needed to identify a causal structure among N variables.
- **Method:** Worst-case and sufficient bounds on sequences of interventions.
- **Dataset/environment:** Combinatorial / theoretical causal graphs.
- **Objective:** Structure identification with interventions.
- **Baseline:** Passive observation; single-variable vs multi-variable interventions.
- **Limitations:** Worst-case identification counts, not expected discovery under a misspecified GP agent.
- **Relevance to ECHO:** Justifies treating interventions as first-class experiments. ECHO's causal world is a small linear Gaussian instance of this problem, not a new identification bound.
- **Potential research gap:** Adaptive selection of *which* intervention to run next when the budget is far below the worst-case sufficient number.
