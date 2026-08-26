from __future__ import annotations

import numpy as np

from echo.models.gp import GaussianProcessModel


def _toy_data(n: int = 12, seed: int = 0):
    rng = np.random.default_rng(seed)
    X = rng.uniform(-2, 2, size=(n, 2))
    y = 0.4 * X[:, 0] - 0.7 * X[:, 1] + rng.normal(0, 0.05, size=n)
    return X, y


def test_gp_predict_shape() -> None:
    X, y = _toy_data()
    model = GaussianProcessModel(x_low=np.array([-2.0, -2.0]), x_high=np.array([2.0, 2.0]))
    model.fit(X, y, optimize=True, rng=np.random.default_rng(0), n_restarts=0)
    Xs = np.zeros((5, 2))
    mu, std = model.predict(Xs)
    assert mu.shape == (5,)
    assert std.shape == (5,)
    assert np.all(std >= 0)


def test_gp_interpolates_observed_point_approximately() -> None:
    X, y = _toy_data(n=15)
    model = GaussianProcessModel(x_low=np.array([-2.0, -2.0]), x_high=np.array([2.0, 2.0]))
    model.fit(X, y, optimize=True, rng=np.random.default_rng(1), n_restarts=1)
    mu, std = model.predict(X[:1])
    assert abs(float(mu[0]) - float(y[0])) < 0.5
    assert float(std[0]) < 1.0


def test_same_fit_is_deterministic() -> None:
    X, y = _toy_data()
    a = GaussianProcessModel(x_low=np.array([-2.0, -2.0]), x_high=np.array([2.0, 2.0]))
    b = GaussianProcessModel(x_low=np.array([-2.0, -2.0]), x_high=np.array([2.0, 2.0]))
    a.fit(X, y, optimize=True, rng=np.random.default_rng(2), n_restarts=1)
    b.fit(X, y, optimize=True, rng=np.random.default_rng(2), n_restarts=1)
    Xs = np.array([[0.1, -0.2], [1.0, 1.0]])
    mu_a, std_a = a.predict(Xs)
    mu_b, std_b = b.predict(Xs)
    np.testing.assert_allclose(mu_a, mu_b, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(std_a, std_b, rtol=1e-5, atol=1e-5)
