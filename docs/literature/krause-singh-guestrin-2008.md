# Krause, A., Singh, A., & Guestrin, C. (2008)

- **Citation:** Krause, A., Singh, A., & Guestrin, C. (2008). Near-optimal sensor placements in Gaussian processes: Theory, efficient algorithms and empirical studies. *Journal of Machine Learning Research*, 9, 235–284.
- **Year:** 2008
- **Problem:** Place a budget of sensors to maximize information about a GP field.
- **Method:** Mutual information between observed locations and the remaining space; greedy algorithm with near-optimality guarantees (submodularity).
- **Dataset/environment:** Spatial sensing / GP fields.
- **Objective:** Mutual information / coverage of a field.
- **Baseline:** Entropy, random, uncertainty heuristics.
- **Limitations:** Batch or greedy placement for a GP field; not multi-metric scientific-mechanism evaluation; typically not sequential refitting of a misspecified model of an unknown law.
- **Relevance to ECHO:** The closest standard mathematics to ECHO V0's global expected knowledge change. V0 must not be described as a new information-theoretic criterion.
- **Potential research gap:** Using MI-style sequential selection as a *baseline scientific policy* and scoring it on hidden-law recovery, hypothesis tests, and failure modes—not treating MI itself as the definition of discovery.
