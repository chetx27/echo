from __future__ import annotations

import numpy as np

from echo.environments.competing import CompetingHypothesesSystem
from echo.environments.interaction import interaction_true_fn
from echo.hypotheses.belief import HypothesisBelief
from echo.hypotheses.models import DEFAULT_HYPOTHESES
from echo.policies import make_policy
from echo.utils.io import ExperimentConfig
from echo.experiments.runner import run_sequential


def test_interaction_has_product_term() -> None:
    X = np.array([[1.0, 0.0, 2.0]])
    assert interaction_true_fn(X)[0] == 2.0 + 0.0 + 10.0


def test_competing_hides_true_class_from_hypothesis_list() -> None:
    env = CompetingHypothesesSystem(n_candidates=40, n_test=10, noise_std=0.1, dim=1)
    env.reset(0)
    names = [h.name for h in env.get_candidate_hypotheses()]
    assert names == ["linear", "quadratic", "sinusoid"]
    hidden = env.get_hidden_state_for_evaluation()
    assert hidden["true_hypothesis_name"] == "quadratic"
    assert "true_hypothesis_index" not in names


def test_quadratic_data_raises_quadratic_posterior() -> None:
    rng = np.random.default_rng(1)
    x = rng.uniform(-2, 2, size=(25, 1))
    y = 1.2 * x[:, 0] ** 2 + 0.5 + rng.normal(0, 0.05, size=25)
    belief = HypothesisBelief(DEFAULT_HYPOTHESES, noise_std=0.1)
    belief.fit(x, y)
    post = belief.posterior()
    assert post[1] > post[0]
    assert post[1] > post[2]


def test_hypothesis_policy_runs_on_competing_env() -> None:
    env = CompetingHypothesesSystem(n_candidates=40, n_test=12, noise_std=0.1, dim=1)
    cfg = ExperimentConfig(
        name="test",
        environment="competing_hypotheses",
        n_candidates=40,
        budget=5,
        n_init=2,
        n_test=12,
        n_probe=8,
        n_restarts=0,
        primary_algorithm="echo_hypothesis",
    )
    result = run_sequential(env, make_policy("echo_hypothesis"), cfg, seed=2)
    assert result.final_metrics["correct_hypothesis_prob"] >= 0.0
    assert result.final_metrics["n_obs"] == 5.0
