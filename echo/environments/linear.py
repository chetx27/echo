"""Hidden linear scientific law: y = 3 x1 + 2 x2 - 4 x3 + ε."""

from __future__ import annotations

import numpy as np

from echo.environments.base import SyntheticRegressionEnvironment


def linear_true_fn(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return 3.0 * X[:, 0] + 2.0 * X[:, 1] - 4.0 * X[:, 2]


def linear_features(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return np.column_stack([X[:, 0], X[:, 1], X[:, 2]])


class LinearScientificSystem(SyntheticRegressionEnvironment):
    name = "linear"

    def __init__(self, **kwargs) -> None:
        super().__init__(
            true_fn=linear_true_fn,
            theta=np.array([3.0, 2.0, -4.0]),
            feature_fn=linear_features,
            feature_names=["x1", "x2", "x3"],
            formula="y = 3*x1 + 2*x2 - 4*x3 + eps",
            **kwargs,
        )
