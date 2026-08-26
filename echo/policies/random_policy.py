from __future__ import annotations

import numpy as np

from echo.policies.base import Policy
from echo.policies.state import DecisionState


class RandomPolicy(Policy):
    name = "random"

    def select(self, state: DecisionState) -> int:
        available = np.flatnonzero(state.available_mask)
        if len(available) == 0:
            raise RuntimeError("no remaining candidates")
        return int(state.rng.choice(available))
