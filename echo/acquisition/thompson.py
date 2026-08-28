"""Mean-field Thompson sampling for a GP.

A full joint posterior sample over 10,000 candidates is O(n^3). V0/V1 uses
independent draws ỹ(x) = μ(x) + σ(x) z_x, z_x ~ N(0,1), then argmax.

This is an approximation of Thompson sampling and is documented as such.
"""

from __future__ import annotations

import numpy as np

from echo.policies.state import DecisionState


def thompson_meanfield(state: DecisionState) -> np.ndarray:
    mu, std = state.model.predict(state.candidates, return_std=True)
    z = state.rng.standard_normal(len(state.candidates))
    return np.asarray(mu, dtype=float) + np.asarray(std, dtype=float) * z
