"""Expected improvement for minimization (Jones, Schonlau & Welch, 1998).

EI(x) = (y_best - μ(x)) Φ(z) + σ(x) φ(z),
z = (y_best - μ(x)) / σ(x),
y_best = min observed y.

This is a black-box optimization acquisition, not a discovery objective.
It is included as a conventional Bayesian optimization baseline.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm

from echo.policies.state import DecisionState


def expected_improvement(state: DecisionState, xi: float = 0.0) -> np.ndarray:
    mu, std = state.model.predict(state.candidates, return_std=True)
    mu = np.asarray(mu, dtype=float)
    std = np.asarray(std, dtype=float)
    y_best = float(np.min(state.y_obs))
    safe = np.maximum(std, 1e-12)
    z = (y_best - xi - mu) / safe
    ei = (y_best - xi - mu) * norm.cdf(z) + safe * norm.pdf(z)
    return np.where(std > 1e-12, np.maximum(ei, 0.0), 0.0)
