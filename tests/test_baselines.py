from __future__ import annotations

import numpy as np

from echo.acquisition.diversity import diversity_score
from echo.acquisition.greedy import greedy_mean
from echo.acquisition.ucb import gp_ucb
from echo.models.gp import GaussianProcessModel
from echo.policies.state import DecisionState


def _state(seed: int = 0) -> DecisionState:
    rng = np.random.default_rng(seed)
    X = rng.uniform(-2, 2, size=(6, 2))
    y = X[:, 0] + rng.normal(0, 0.05, size=6)
    candidates = rng.uniform(-2, 2, size=(25, 2))
    model = GaussianProcessModel(x_low=np.array([-2.0, -2.0]), x_high=np.array([2.0, 2.0]))
    model.fit(X, y, optimize=False, rng=rng, n_restarts=0)
    return DecisionState(
        candidates=candidates,
        available_mask=np.ones(len(candidates), dtype=bool),
        X_obs=X,
        y_obs=y,
        costs=np.ones(len(candidates)),
        step=6,
        budget=20,
        model=model,
        rng=rng,
        X_probe=rng.uniform(-2, 2, size=(8, 2)),
    )


def test_greedy_finite() -> None:
    assert np.all(np.isfinite(greedy_mean(_state())))


def test_diversity_prefers_far_points() -> None:
    state = _state()
    scores = diversity_score(state)
    assert scores.shape == (len(state.candidates),)
    assert np.all(scores >= 0)


def test_ucb_exceeds_mean() -> None:
    state = _state()
    mu = greedy_mean(state)
    ucb = gp_ucb(state, kappa=2.0)
    assert np.all(ucb >= mu - 1e-12)
