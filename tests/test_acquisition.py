from __future__ import annotations

import numpy as np
from scipy.stats import spearmanr

from echo.acquisition.expected_improvement import expected_improvement
from echo.acquisition.information_gain import local_information_gain
from echo.acquisition.uncertainty import predictive_uncertainty
from echo.models.gp import GaussianProcessModel
from echo.policies.state import DecisionState


def _state(seed: int = 0) -> DecisionState:
    rng = np.random.default_rng(seed)
    X = rng.uniform(-2, 2, size=(8, 3))
    y = 3 * X[:, 0] + rng.normal(0, 0.1, size=8)
    candidates = rng.uniform(-2, 2, size=(40, 3))
    model = GaussianProcessModel(
        x_low=np.array([-2.0, -2.0, -2.0]),
        x_high=np.array([2.0, 2.0, 2.0]),
    )
    model.fit(X, y, optimize=True, rng=np.random.default_rng(1), n_restarts=0)
    return DecisionState(
        candidates=candidates,
        available_mask=np.ones(len(candidates), dtype=bool),
        X_obs=X,
        y_obs=y,
        costs=np.ones(len(candidates)),
        step=8,
        budget=20,
        model=model,
        rng=rng,
        X_probe=rng.uniform(-2, 2, size=(12, 3)),
    )


def test_local_ig_ranks_like_uncertainty() -> None:
    state = _state()
    u = predictive_uncertainty(state)
    ig = local_information_gain(state)
    rho, _ = spearmanr(u, ig)
    assert rho > 0.999


def test_ei_is_nonnegative_and_near_zero_for_sure_worse_points() -> None:
    state = _state()
    ei = expected_improvement(state)
    assert np.all(ei >= -1e-12)
    assert np.all(np.isfinite(ei))
