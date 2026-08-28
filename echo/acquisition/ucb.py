"""GP-UCB (Srinivas et al., 2010), maximization form.

U(x) = μ(x) + κ σ(x), with κ = 2 by default.

This is an optimization baseline. It is not a discovery objective.
"""

from __future__ import annotations

import numpy as np

from echo.policies.state import DecisionState


def gp_ucb(state: DecisionState, kappa: float = 2.0) -> np.ndarray:
    mu, std = state.model.predict(state.candidates, return_std=True)
    return np.asarray(mu, dtype=float) + float(kappa) * np.asarray(std, dtype=float)
