from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from echo.models.gp import GaussianProcessModel


@dataclass
class DecisionState:
    """Everything a policy may use. No hidden scientific law."""

    candidates: np.ndarray
    available_mask: np.ndarray
    X_obs: np.ndarray
    y_obs: np.ndarray
    costs: np.ndarray
    step: int
    budget: int
    model: GaussianProcessModel
    rng: np.random.Generator
    X_probe: np.ndarray
    hypothesis_belief: object | None = None
