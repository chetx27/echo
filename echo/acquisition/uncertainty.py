"""Predictive uncertainty: x* = argmax σ(x).

σ(x) is the posterior standard deviation of the latent function f(x),
not of the noisy observation y.
"""

from __future__ import annotations

import numpy as np

from echo.policies.state import DecisionState


def predictive_uncertainty(state: DecisionState) -> np.ndarray:
    _, std = state.model.predict(state.candidates, return_std=True)
    return np.asarray(std, dtype=float)
