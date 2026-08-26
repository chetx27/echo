"""Information-theoretic acquisition functions for GP regression.

Local information gain
----------------------
I(y; f(x) | D) = H[y | x, D] - H[y | x, f]
               = 0.5 log(1 + σ_f²(x) / σ_n²)

For homoscedastic GP regression this is a strictly increasing function of
σ_f(x), so it ranks candidates identically to uncertainty sampling. That
equivalence is a result to report, not a bug.

Global information gain (ECHO V0)
---------------------------------
I(y; f_probe | D) = H[f_probe | D] - H[f_probe | D, y(x)]

Because a GP posterior covariance does not depend on the realized y, this
has a closed form. It measures expected reduction in uncertainty about
the function over a domain-wide probe set, not only at x.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import solve_triangular

from echo.policies.state import DecisionState


def local_information_gain(state: DecisionState) -> np.ndarray:
    _, std = state.model.predict(state.candidates, return_std=True)
    std = np.asarray(std, dtype=float)
    noise = max(state.model.noise_variance_original, 1e-12)
    return 0.5 * np.log(1.0 + (std**2) / noise)


def global_information_gain(state: DecisionState) -> np.ndarray:
    """Expected entropy reduction of f on the probe set after observing y(x)."""
    model = state.model
    X_probe = state.X_probe
    X_cand = state.candidates
    _, cov_p = model.predict(X_probe, return_std=False, return_cov=True)
    _, std_c = model.predict(X_cand, return_std=True)
    k = model.posterior_cross_covariance(X_probe, X_cand)
    n_p = cov_p.shape[0]
    jitter = 1e-8 * np.trace(cov_p) / max(n_p, 1)
    L = np.linalg.cholesky(cov_p + jitter * np.eye(n_p))
    w = solve_triangular(L, k, lower=True)
    quad = np.sum(w**2, axis=0)
    s = np.asarray(std_c, dtype=float) ** 2 + model.noise_variance_original
    remaining = np.clip(s - quad, 1e-12, None)
    return 0.5 * np.log(s / remaining)
