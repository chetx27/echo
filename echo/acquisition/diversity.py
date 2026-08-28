"""Diversity sampling: maximize distance to the nearest observed experiment."""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist

from echo.policies.state import DecisionState


def diversity_score(state: DecisionState) -> np.ndarray:
    if len(state.X_obs) == 0:
        return np.ones(len(state.candidates), dtype=float)
    dist = cdist(state.candidates, state.X_obs).min(axis=1)
    return np.asarray(dist, dtype=float)
