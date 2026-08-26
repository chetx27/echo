# Foster, A., Ivanova, D. R., Malik, I., & Rainforth, T. (2021)

- **Citation:** Foster, A., Ivanova, D. R., Malik, I., & Rainforth, T. (2021). Deep Adaptive Design: Amortizing sequential Bayesian experimental design. In *Proceedings of the 38th International Conference on Machine Learning*.
- **Year:** 2021
- **Problem:** Sequential Bayesian experimental design is often too expensive if one recomputes an optimal design after every observation.
- **Method:** Amortized (learned) sequential design policies (DAD).
- **Dataset/environment:** Simulated Bayesian design tasks in the paper.
- **Objective:** Expected information gain (or related BED utilities), amortized.
- **Baseline:** Conventional (non-amortized) sequential design; greedy BED.
- **Limitations:** Requires a specified inference model and training distribution of tasks. Transfer is a research question, not a given.
- **Relevance to ECHO:** A later ECHO question is whether a *learned* acquisition can beat hand-designed scores. DAD is prior art for learned sequential design, not a gap ECHO can claim as original.
- **Potential research gap:** Whether policies trained to maximize EIG also maximize mechanism-recovery metrics on held-out scientific systems.
