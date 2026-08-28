"""Parametric scientific hypotheses as linear-in-parameter feature maps.

The agent may consider these model classes. The true class remains hidden.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

FeatureFn = Callable[[np.ndarray], np.ndarray]


def _x(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    return X[:, 0]


def features_linear(X: np.ndarray) -> np.ndarray:
    x = _x(X)
    return np.column_stack([x, np.ones_like(x)])


def features_quadratic(X: np.ndarray) -> np.ndarray:
    x = _x(X)
    return np.column_stack([x**2, np.ones_like(x)])


def features_sin(X: np.ndarray) -> np.ndarray:
    x = _x(X)
    return np.column_stack([np.sin(x), np.ones_like(x)])


@dataclass(frozen=True)
class ParametricHypothesis:
    name: str
    features: FeatureFn
    description: str


DEFAULT_HYPOTHESES = (
    ParametricHypothesis("linear", features_linear, "y = a x + b"),
    ParametricHypothesis("quadratic", features_quadratic, "y = a x^2 + b"),
    ParametricHypothesis("sinusoid", features_sin, "y = a sin(x) + b"),
)
