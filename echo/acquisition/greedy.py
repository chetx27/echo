"""Greedy exploitation: select the candidate with the highest predicted mean.

This is conventional exploitation, not a discovery objective.
"""

from __future__ import annotations

import numpy as np

from echo.policies.state import DecisionState


def greedy_mean(state: DecisionState) -> np.ndarray:
    mu, _ = state.model.predict(state.candidates, return_std=True)
    return np.asarray(mu, dtype=float)
