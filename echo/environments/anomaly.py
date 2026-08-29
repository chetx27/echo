"""Anomaly world: a compact structured violation of an otherwise linear law.

Background:  y = 2 x1 + 0.5 x2 + ε

Anomaly box (evaluator-only): x1 ∈ [1.0, 1.6], x2 ∈ [-0.4, 0.4]
adds a constant offset of +4. The deviation is structured, not a
single outlier. The scientific target is to notice that the background
model is incomplete, not to maximize a detection score on a full dataset.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from echo.environments.base import SyntheticRegressionEnvironment

ANOMALY_X1 = (1.0, 1.6)
ANOMALY_X2 = (-0.4, 0.4)
ANOMALY_OFFSET = 4.0


def in_anomaly_region(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return (
        (X[:, 0] >= ANOMALY_X1[0])
        & (X[:, 0] <= ANOMALY_X1[1])
        & (X[:, 1] >= ANOMALY_X2[0])
        & (X[:, 1] <= ANOMALY_X2[1])
    )


def anomaly_true_fn(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    y = 2.0 * X[:, 0] + 0.5 * X[:, 1]
    return np.where(in_anomaly_region(X), y + ANOMALY_OFFSET, y)


def anomaly_features(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return np.column_stack([X[:, 0], X[:, 1]])


class AnomalyScientificSystem(SyntheticRegressionEnvironment):
    name = "anomaly"

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("dim", 2)
        super().__init__(
            true_fn=anomaly_true_fn,
            theta=np.array([2.0, 0.5]),
            feature_fn=anomaly_features,
            feature_names=["x1", "x2"],
            formula="y = 2*x1 + 0.5*x2 + 4*1_{anomaly box} + eps",
            **kwargs,
        )

    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        gt = super().get_ground_truth_for_evaluation()
        self._require_reset()
        assert self._candidates is not None
        cand_mask = in_anomaly_region(self._candidates)
        test_mask = in_anomaly_region(gt["X_test"])
        gt["kind"] = "anomaly"
        gt["n_anomaly_candidates"] = int(np.sum(cand_mask))
        gt["anomaly_base_rate"] = float(np.mean(cand_mask)) if len(cand_mask) else 0.0
        gt["anomaly_test_mask"] = test_mask
        return gt

    def get_hidden_state_for_evaluation(self) -> Dict[str, Any]:
        hidden = super().get_hidden_state_for_evaluation()
        hidden["kind"] = "anomaly"
        hidden["anomaly_box"] = {"x1": ANOMALY_X1, "x2": ANOMALY_X2, "offset": ANOMALY_OFFSET}
        return hidden
