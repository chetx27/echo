"""Hidden nonlinear scientific law: y = 3 x1 + 2 x2^2 - 4 sin(x3) + ε.

The domain is [-2, 2]^3 so that sin(x3) is not locally linear and x2^2 is
a visibly curved mechanism. The agent does not receive this formula.
"""

from __future__ import annotations

import numpy as np

from echo.environments.base import SyntheticRegressionEnvironment


def nonlinear_true_fn(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return 3.0 * X[:, 0] + 2.0 * X[:, 1] ** 2 - 4.0 * np.sin(X[:, 2])


def nonlinear_features(X: np.ndarray) -> np.ndarray:
    """Oracle features for evaluator-only parameter recovery."""
    X = np.asarray(X, dtype=float)
    return np.column_stack([X[:, 0], X[:, 1] ** 2, np.sin(X[:, 2])])


class NonlinearScientificSystem(SyntheticRegressionEnvironment):
    name = "nonlinear"

    def __init__(self, **kwargs) -> None:
        super().__init__(
            true_fn=nonlinear_true_fn,
            theta=np.array([3.0, 2.0, -4.0]),
            feature_fn=nonlinear_features,
            feature_names=["x1", "x2^2", "sin(x3)"],
            formula="y = 3*x1 + 2*x2**2 - 4*sin(x3) + eps",
            **kwargs,
        )
