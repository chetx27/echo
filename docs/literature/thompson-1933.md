# Thompson, W. R. (1933)

- **Citation:** Thompson, W. R. (1933). On the likelihood that one unknown probability exceeds another in view of the evidence of two samples. *Biometrika*, 25(3/4), 285–294.
- **Year:** 1933
- **Problem:** Sequential allocation under posterior uncertainty.
- **Method:** Sample from the posterior and take the greedy action (Thompson sampling).
- **Dataset/environment:** Two-arm probability comparison.
- **Objective:** Identify the better option with sequential samples.
- **Baseline:** n/a (foundational).
- **Limitations:** Not a scientific-discovery objective; ECHO implements a mean-field GP approximation, not exact joint TS.
- **Relevance to ECHO:** Baseline 7. Documented as an approximation for large candidate sets.
- **Potential research gap:** Whether posterior sampling of a GP helps mechanism recovery relative to UCB/EI.
