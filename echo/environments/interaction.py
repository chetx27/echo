"""Hidden interaction law: y = 2 x1 + 3 x2 + 5 (x1 x3) + ε.

The scientifically important term is the x1 x3 interaction, not the
additive main effects.
"""

from __future__ import annotations

import numpy as np

from echo.environments.base import SyntheticRegressionEnvironment


def interaction_true_fn(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return 2.0 * X[:, 0] + 3.0 * X[:, 1] + 5.0 * (X[:, 0] * X[:, 2])


def interaction_features(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return np.column_stack([X[:, 0], X[:, 1], X[:, 0] * X[:, 2]])


class InteractionScientificSystem(SyntheticRegressionEnvironment):
    name = "interaction"

    def __init__(self, **kwargs) -> None:
        super().__init__(
            true_fn=interaction_true_fn,
            theta=np.array([2.0, 3.0, 5.0]),
            feature_fn=interaction_features,
            feature_names=["x1", "x2", "x1*x3"],
            formula="y = 2*x1 + 3*x2 + 5*(x1*x3) + eps",
            **kwargs,
        )
