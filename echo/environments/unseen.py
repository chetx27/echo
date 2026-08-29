"""Unseen functional form for generalization tests.

Hidden law (evaluator-only):

    y = 2 exp(-x1^2) + 0.5 x2 x3 - tanh(x3) + ε

This form is not used in the linear, nonlinear, interaction, competing,
causal, multimodal, or anomaly worlds. Experiment 5 asks whether the
*same hand-designed policies* keep their ranking here — not whether a
meta-learned acquisition has transferred. No policy in this repository
is trained on other environments.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from echo.environments.base import SyntheticRegressionEnvironment


def unseen_true_fn(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return 2.0 * np.exp(-(X[:, 0] ** 2)) + 0.5 * X[:, 1] * X[:, 2] - np.tanh(X[:, 2])


def unseen_features(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return np.column_stack([np.exp(-(X[:, 0] ** 2)), X[:, 1] * X[:, 2], np.tanh(X[:, 2])])


class UnseenScientificSystem(SyntheticRegressionEnvironment):
    name = "unseen"

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("dim", 3)
        super().__init__(
            true_fn=unseen_true_fn,
            theta=np.array([2.0, 0.5, -1.0]),
            feature_fn=unseen_features,
            feature_names=["exp(-x1^2)", "x2*x3", "tanh(x3)"],
            formula="y = 2*exp(-x1**2) + 0.5*x2*x3 - tanh(x3) + eps",
            **kwargs,
        )

    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        gt = super().get_ground_truth_for_evaluation()
        gt["kind"] = "unseen"
        return gt

    def get_hidden_state_for_evaluation(self) -> Dict[str, Any]:
        hidden = super().get_hidden_state_for_evaluation()
        hidden["kind"] = "unseen"
        return hidden
