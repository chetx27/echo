from __future__ import annotations

import numpy as np

from echo.environments.linear import LinearScientificSystem, linear_true_fn
from echo.environments.nonlinear import NonlinearScientificSystem, nonlinear_true_fn


def test_reset_is_deterministic() -> None:
    env_a = NonlinearScientificSystem(n_candidates=50, n_test=10, noise_std=0.1)
    env_b = NonlinearScientificSystem(n_candidates=50, n_test=10, noise_std=0.1)
    env_a.reset(7)
    env_b.reset(7)
    np.testing.assert_allclose(env_a.get_candidates(), env_b.get_candidates())
    y_a = [env_a.perform_experiment(i).y for i in range(5)]
    y_b = [env_b.perform_experiment(i).y for i in range(5)]
    np.testing.assert_allclose(y_a, y_b)


def test_same_index_same_observation() -> None:
    env = LinearScientificSystem(n_candidates=20, n_test=5, noise_std=0.2)
    env.reset(3)
    y1 = env.perform_experiment(4).y
    y2 = env.perform_experiment(4).y
    assert y1 == y2


def test_ground_truth_matches_hidden_function() -> None:
    env = NonlinearScientificSystem(n_candidates=30, n_test=25, noise_std=0.0)
    env.reset(1)
    gt = env.get_ground_truth_for_evaluation()
    np.testing.assert_allclose(gt["f_test"], nonlinear_true_fn(gt["X_test"]))
    hidden = env.get_hidden_state_for_evaluation()
    assert "3*x1" in hidden["formula"]
    np.testing.assert_allclose(hidden["theta"], [3.0, 2.0, -4.0])


def test_linear_law() -> None:
    X = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    np.testing.assert_allclose(linear_true_fn(X), [3.0, 2.0, -4.0])
