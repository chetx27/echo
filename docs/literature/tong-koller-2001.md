# Tong, S., & Koller, D. (2001)

- **Citation:** Tong, S., & Koller, D. (2001). Active learning for structure in Bayesian networks. In *Proceedings of the 17th International Joint Conference on Artificial Intelligence* (pp. 863–869).
- **Year:** 2001
- **Problem:** Choose queries / experiments to learn a Bayesian-network structure.
- **Method:** Active learning using posterior uncertainty over graph structures.
- **Dataset/environment:** Synthetic Bayesian networks.
- **Objective:** Structure recovery, not optimum-seeking.
- **Baseline:** Random / passive sampling of instances.
- **Limitations:** Discrete Bayesian networks; not a GP surface-recovery setting.
- **Relevance to ECHO:** Closest named ancestor of "pick the experiment that helps recover structure." ECHO V2 evaluates whether GP uncertainty sampling accidentally does this job on a tiny linear SCM.
- **Potential research gap:** Transfer of active-structure ideas to budgeted continuous interventions when the agent model is misspecified.
