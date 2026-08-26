from __future__ import annotations

import numpy as np

from echo.environments.linear import LinearScientificSystem
from echo.environments.nonlinear import NonlinearScientificSystem
from echo.experiments.runner import run_sequential
from echo.policies import make_policy
from echo.utils.io import ExperimentConfig


def _config(**kwargs) -> ExperimentConfig:
    base = dict(
        name="test",
        environment="nonlinear",
        n_candidates=40,
        budget=5,
        n_init=2,
        noise=0.1,
        n_test=15,
        n_probe=8,
        n_seeds=1,
        n_restarts=0,
    )
    base.update(kwargs)
    return ExperimentConfig(**base)


def test_budget_and_unique_indices() -> None:
    env = NonlinearScientificSystem(n_candidates=40, n_test=15, noise_std=0.1)
    result = run_sequential(env, make_policy("random"), _config(), seed=0)
    assert len(result.sequence) == 5
    idx = [s["index"] for s in result.sequence]
    assert len(set(idx)) == 5
    assert result.final_metrics["n_obs"] == 5.0


def test_same_seed_same_random_trajectory() -> None:
    cfg = _config()
    env_a = NonlinearScientificSystem(n_candidates=40, n_test=15, noise_std=0.1)
    env_b = NonlinearScientificSystem(n_candidates=40, n_test=15, noise_std=0.1)
    a = run_sequential(env_a, make_policy("random"), cfg, seed=11)
    b = run_sequential(env_b, make_policy("random"), cfg, seed=11)
    assert [s["index"] for s in a.sequence] == [s["index"] for s in b.sequence]


def test_oracle_parameter_recovery_on_linear_system() -> None:
    env = LinearScientificSystem(n_candidates=80, n_test=20, noise_std=0.05)
    cfg = _config(environment="linear", n_candidates=80, budget=25, n_init=5, n_test=20)
    result = run_sequential(env, make_policy("random"), cfg, seed=4)
    assert result.final_metrics["parameter_recovery_rmse"] < 0.5
