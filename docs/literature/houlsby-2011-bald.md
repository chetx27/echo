# Houlsby, N., Huszár, F., Ghahramani, Z., & Lengyel, M. (2011)

- **Citation:** Houlsby, N., Huszár, F., Ghahramani, Z., & Lengyel, M. (2011). Bayesian active learning for classification and preference learning. arXiv:1112.5745.
- **Year:** 2011
- **Problem:** Active selection when the model is Bayesian, especially classification and preference.
- **Method:** BALD: mutual information between a label and model parameters, \(I(y; \theta \mid x, D)\).
- **Dataset/environment:** Classification / preference-learning illustrations.
- **Objective:** Information about parameters (or the latent function).
- **Baseline:** Uncertainty sampling and related active-learning scores.
- **Limitations:** Homoscedastic GP regression collapses BALD-at-a-point to a monotone function of \(\sigma_f(x)\).
- **Relevance to ECHO:** Local information gain in V0 is the regression analogue of BALD at a single \(x\).
- **Potential research gap:** Global \(I(y; f_{\mathrm{probe}}\mid D)\) versus local BALD, evaluated on discovery metrics rather than classification accuracy.
