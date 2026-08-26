from __future__ import annotations

from typing import Callable

import numpy as np

from echo.policies.base import Policy
from echo.policies.state import DecisionState

ScoreFn = Callable[[DecisionState], np.ndarray]


class AcquisitionPolicy(Policy):
    """Select the available candidate with the highest acquisition score."""

    def __init__(self, name: str, score_fn: ScoreFn) -> None:
        self.name = name
        self._score_fn = score_fn
        self.last_scores: np.ndarray | None = None

    def select(self, state: DecisionState) -> int:
        scores = np.asarray(self._score_fn(state), dtype=float)
        scores = np.where(state.available_mask, scores, -np.inf)
        self.last_scores = scores
        if not np.any(np.isfinite(scores)):
            raise RuntimeError("no finite acquisition scores")
        return int(np.argmax(scores))
