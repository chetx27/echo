"""Competing-hypothesis world.

Hidden law (evaluator-only): y = 1.2 x^2 + 0.5 + ε.

The agent may consider three parametric classes, none of which is labeled
as true:

  H_linear:    y = a x + b
  H_quadratic: y = a x^2 + b
  H_sin:       y = a sin(x) + b

get_candidate_hypotheses() is agent-accessible (the scientific vocabulary).
The true class index is not.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from echo.environments.base import SyntheticRegressionEnvironment
from echo.hypotheses.models import DEFAULT_HYPOTHESES, features_quadratic


def competing_true_fn(X: np.ndarray) -> np.ndarray:
    x = np.asarray(X, dtype=float)[:, 0]
    return 1.2 * x**2 + 0.5


class CompetingHypothesesSystem(SyntheticRegressionEnvironment):
    name = "competing_hypotheses"
    TRUE_HYPOTHESIS_INDEX = 1  # quadratic in DEFAULT_HYPOTHESES

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("dim", 1)
        kwargs.setdefault("low", -2.0)
        kwargs.setdefault("high", 2.0)
        super().__init__(
            true_fn=competing_true_fn,
            theta=np.array([1.2, 0.5]),
            feature_fn=features_quadratic,
            feature_names=["x^2", "1"],
            formula="y = 1.2*x**2 + 0.5 + eps",
            **kwargs,
        )

    def get_candidate_hypotheses(self):
        """Agent-accessible model classes. Does not reveal which is true."""
        return DEFAULT_HYPOTHESES

    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        gt = super().get_ground_truth_for_evaluation()
        gt["true_hypothesis_index"] = self.TRUE_HYPOTHESIS_INDEX
        gt["true_hypothesis_name"] = DEFAULT_HYPOTHESES[self.TRUE_HYPOTHESIS_INDEX].name
        gt["hypothesis_names"] = [h.name for h in DEFAULT_HYPOTHESES]
        return gt

    def get_hidden_state_for_evaluation(self) -> Dict[str, Any]:
        hidden = super().get_hidden_state_for_evaluation()
        hidden["true_hypothesis_index"] = self.TRUE_HYPOTHESIS_INDEX
        hidden["true_hypothesis_name"] = DEFAULT_HYPOTHESES[self.TRUE_HYPOTHESIS_INDEX].name
        return hidden
