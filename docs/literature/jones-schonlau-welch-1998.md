# Jones, D. R., Schonlau, M., & Welch, W. J. (1998)

- **Citation:** Jones, D. R., Schonlau, M., & Welch, W. J. (1998). Efficient global optimization of expensive black-box functions. *Journal of Global Optimization*, 13(4), 455–492.
- **Year:** 1998
- **Problem:** Globally optimize an expensive black-box function with few evaluations.
- **Method:** Expected improvement (EGO) on a Gaussian process surrogate; minimization form.
- **Dataset/environment:** Deterministic (or lightly noisy) black-box test functions.
- **Objective:** Find a minimum of \(y(x)\).
- **Baseline:** Other global optimization methods of the period.
- **Limitations:** The scientific target is an optimum, not a mechanism. Concentration near basins of attraction can undersample other structure.
- **Relevance to ECHO:** Implemented as the EI baseline in V0, with the Jones minimization formula.
- **Potential research gap:** How badly (or not) optimum-seeking acquisition performs when the evaluation target is function/parameter recovery rather than \(\min y\).
