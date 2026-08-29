"""Open-loop (non-sequential) selection.

After the shared initial design, score every remaining candidate once
and spend the rest of the budget in that order. The runner still refits
the GP for evaluation; the policy ignores those updates.

This is the ECHO-no-sequential-update ablation. It is not assumed to be
worse; that is an experimental question.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from echo.policies.acquisition_policy import ScoreFn
from echo.policies.base import Policy
from echo.policies.state import DecisionState


class OpenLoopPolicy(Policy):
    def __init__(self, name: str, score_fn: ScoreFn) -> None:
        self.name = name
        self._score_fn = score_fn
        self.last_scores: np.ndarray | None = None
        self._queue: Optional[List[int]] = None

    def select(self, state: DecisionState) -> int:
        if self._queue is None:
            scores = np.asarray(self._score_fn(state), dtype=float)
            scores = np.where(state.available_mask, scores, -np.inf)
            self.last_scores = scores
            if not np.any(np.isfinite(scores)):
                raise RuntimeError("no finite acquisition scores")
            order = np.argsort(-scores)
            self._queue = [int(i) for i in order if state.available_mask[i]]
        if not self._queue:
            raise RuntimeError("open-loop policy exhausted its ranked queue")
        idx = self._queue.pop(0)
        if not state.available_mask[idx]:
            raise RuntimeError(f"{self.name} queued an unavailable candidate {idx}")
        return idx
