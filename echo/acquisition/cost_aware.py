"""Cost-aware wrappers.

U_ratio(x) = score(x) / cost(x)
U_penalty(x) = score(x) - λ cost(x)

Default λ = 0.05 is a scale choice for scores that are typically O(1)
and costs in [1, 20]. It is not claimed to be optimal.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from echo.policies.state import DecisionState

ScoreFn = Callable[[DecisionState], np.ndarray]


def per_cost(score_fn: ScoreFn) -> ScoreFn:
    def wrapped(state: DecisionState) -> np.ndarray:
        scores = np.asarray(score_fn(state), dtype=float)
        return scores / np.maximum(state.costs, 1e-12)

    return wrapped


def minus_lambda_cost(score_fn: ScoreFn, lam: float = 0.05) -> ScoreFn:
    def wrapped(state: DecisionState) -> np.ndarray:
        scores = np.asarray(score_fn(state), dtype=float)
        return scores - float(lam) * state.costs

    return wrapped
