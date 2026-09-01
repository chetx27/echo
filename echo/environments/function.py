"""Wrap any Python callable as a scientific environment.

This is the extension point for a new hidden law without writing a
subclass. The callable must map an array of shape (n, d) to a length-n
vector of noiseless responses. Observation noise is added by the
synthetic environment, as with the built-in worlds.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Sequence

import numpy as np

from echo.environments.base import SyntheticRegressionEnvironment
from echo.hypotheses.models import ParametricHypothesis

ArrayFn = Callable[[np.ndarray], np.ndarray]


def _identity_features(X: np.ndarray) -> np.ndarray:
    return np.asarray(X, dtype=float)


class FunctionScientificSystem(SyntheticRegressionEnvironment):
    """User-supplied hidden function on a box domain."""

    name = "function"

    def __init__(
        self,
        fn: ArrayFn,
        dim: int = 1,
        theta: Optional[np.ndarray] = None,
        feature_fn: Optional[ArrayFn] = None,
        feature_names: Optional[Sequence[str]] = None,
        formula: str = "user-supplied f",
        name: Optional[str] = None,
        hypotheses: Optional[Sequence[ParametricHypothesis]] = None,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("dim", int(dim))
        d = int(kwargs["dim"])
        if name:
            self.name = str(name)
        self._hypotheses = list(hypotheses) if hypotheses else []
        if feature_fn is None:
            feature_fn = _identity_features
            feature_names = list(feature_names) if feature_names is not None else [f"x{i + 1}" for i in range(d)]
            if theta is None:
                theta = np.zeros(d, dtype=float)
        else:
            feature_names = list(feature_names) if feature_names is not None else ["phi"]
            if theta is None:
                probe = np.zeros((1, d), dtype=float)
                theta = np.zeros(int(np.asarray(feature_fn(probe)).shape[-1]), dtype=float)
        super().__init__(
            true_fn=fn,
            theta=np.asarray(theta, dtype=float),
            feature_fn=feature_fn,
            feature_names=list(feature_names),
            formula=str(formula),
            **kwargs,
        )

    def get_candidate_hypotheses(self):
        return list(self._hypotheses)

    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        gt = super().get_ground_truth_for_evaluation()
        gt["kind"] = "function"
        if self._hypotheses:
            names = [h.name for h in self._hypotheses]
            gt["hypothesis_names"] = names
        return gt
