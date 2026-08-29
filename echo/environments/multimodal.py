"""Multimodal scientific landscape.

Three contiguous regions of x1 hide different mechanisms:

    region A (x1 < -0.7):   y = 2 x1 + x2
    region B (|x1| < 0.7):  y = x1^2 - 0.5 x2
    region C (x1 > 0.7):    y = sin(2 x1) + 0.3 x2

Traditional optimum-seeking can lock onto one region. Evaluation asks
whether a sequential design visits and reconstructs all three.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from echo.environments.base import SyntheticRegressionEnvironment

N_REGIONS = 3
BOUND_LEFT = -0.7
BOUND_RIGHT = 0.7


def region_id(X: np.ndarray) -> np.ndarray:
    x1 = np.asarray(X, dtype=float)[:, 0]
    return np.where(x1 < BOUND_LEFT, 0, np.where(x1 < BOUND_RIGHT, 1, 2)).astype(int)


def multimodal_true_fn(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    r = region_id(X)
    y = np.empty(len(X), dtype=float)
    m0 = r == 0
    m1 = r == 1
    m2 = r == 2
    y[m0] = 2.0 * X[m0, 0] + X[m0, 1]
    y[m1] = X[m1, 0] ** 2 - 0.5 * X[m1, 1]
    y[m2] = np.sin(2.0 * X[m2, 0]) + 0.3 * X[m2, 1]
    return y


def multimodal_features(X: np.ndarray) -> np.ndarray:
    """Misspecified global basis used only for oracle-style OLS."""
    X = np.asarray(X, dtype=float)
    return np.column_stack([X[:, 0], X[:, 1], X[:, 0] ** 2, np.sin(2.0 * X[:, 0])])


class MultimodalScientificSystem(SyntheticRegressionEnvironment):
    name = "multimodal"

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("dim", 2)
        super().__init__(
            true_fn=multimodal_true_fn,
            theta=np.array([2.0, 1.0, 1.0, 1.0]),
            feature_fn=multimodal_features,
            feature_names=["x1", "x2", "x1^2", "sin(2 x1)"],
            formula="piecewise: 2*x1+x2 | x1^2-0.5*x2 | sin(2*x1)+0.3*x2",
            **kwargs,
        )

    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        gt = super().get_ground_truth_for_evaluation()
        gt["kind"] = "multimodal"
        gt["n_regions"] = N_REGIONS
        gt["region_ids_test"] = region_id(gt["X_test"])
        return gt

    def get_hidden_state_for_evaluation(self) -> Dict[str, Any]:
        hidden = super().get_hidden_state_for_evaluation()
        hidden["kind"] = "multimodal"
        hidden["n_regions"] = N_REGIONS
        return hidden
