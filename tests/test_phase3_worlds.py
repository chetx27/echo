from __future__ import annotations

import numpy as np

from echo.bench import available_tasks, get_task
from echo.environments.anomaly import AnomalyScientificSystem, in_anomaly_region
from echo.environments.causal import CausalScientificSystem, TRUE_PARENTS, causal_reduced_fn
from echo.environments.multimodal import MultimodalScientificSystem, N_REGIONS, region_id
from echo.environments.unseen import UnseenScientificSystem, unseen_true_fn
from echo.evaluation.causal import parent_set_f1, recover_parents_bic, structural_hamming_distance
from echo.experiments.runner import run_sequential
from echo.policies import make_policy
from echo.utils.io import ExperimentConfig


def test_causal_reduced_form() -> None:
    X = np.array([[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(causal_reduced_fn(X), [1.2, 0.96])


def test_causal_hides_graph_from_candidates() -> None:
    env = CausalScientificSystem(n_candidates=30, n_test=8, noise_std=0.05, dim=2)
    env.reset(0)
    X = env.get_candidates()
    assert X.shape == (30, 2)
    hidden = env.get_hidden_state_for_evaluation()
    assert hidden["true_parents"]["C"] == ["A", "B"]
    outcome = env.perform_experiment(0)
    gt = env.get_ground_truth_for_evaluation()
    assert gt["kind"] == "causal"
    assert len(gt["system_observations"]) == 1
    assert outcome.y == gt["system_observations"][0]["D"]


def test_shd_zero_on_true_graph() -> None:
    assert structural_hamming_distance(TRUE_PARENTS, TRUE_PARENTS) == 0.0
    assert parent_set_f1(TRUE_PARENTS, TRUE_PARENTS) == 1.0
    extra = {k: set(v) for k, v in TRUE_PARENTS.items()}
    extra["D"] = {"C", "A"}
    assert structural_hamming_distance(extra, TRUE_PARENTS) == 1.0


def test_bic_recovers_parents_with_enough_low_noise_data() -> None:
    env = CausalScientificSystem(n_candidates=120, n_test=10, noise_std=0.01, dim=2)
    env.reset(1)
    for i in range(80):
        env.perform_experiment(i)
    obs = env.get_ground_truth_for_evaluation()["system_observations"]
    pred = recover_parents_bic(obs, intervened=("A", "B"))
    assert pred["A"] == set() and pred["B"] == set()
    assert {"A", "B"} <= pred["C"]
    assert "C" in pred["D"]
    assert structural_hamming_distance(pred, TRUE_PARENTS) <= 2.0


def test_multimodal_regions_partition_the_domain() -> None:
    X = np.array([[-1.5, 0.0], [0.0, 0.0], [1.5, 0.0]])
    np.testing.assert_array_equal(region_id(X), [0, 1, 2])
    env = MultimodalScientificSystem(n_candidates=40, n_test=12, noise_std=0.0, dim=2)
    env.reset(2)
    gt = env.get_ground_truth_for_evaluation()
    assert set(np.unique(gt["region_ids_test"]).tolist()).issubset({0, 1, 2})
    assert gt["n_regions"] == N_REGIONS


def test_anomaly_box_is_a_structured_offset() -> None:
    inside = np.array([[1.3, 0.0]])
    outside = np.array([[0.0, 0.0]])
    assert in_anomaly_region(inside)[0]
    assert not in_anomaly_region(outside)[0]
    env = AnomalyScientificSystem(n_candidates=200, n_test=20, noise_std=0.0, dim=2)
    env.reset(3)
    gt = env.get_ground_truth_for_evaluation()
    assert gt["n_anomaly_candidates"] >= 1
    assert gt["anomaly_base_rate"] < 0.5


def test_unseen_form_is_not_the_v0_laws() -> None:
    X = np.array([[0.0, 1.0, 1.0]])
    y = unseen_true_fn(X)[0]
    assert abs(y - (2.0 + 0.5 - np.tanh(1.0))) < 1e-12
    env = UnseenScientificSystem(n_candidates=25, n_test=8, noise_std=0.1)
    env.reset(4)
    assert env.dim == 3
    result = run_sequential(
        env,
        make_policy("random"),
        ExperimentConfig(
            name="test",
            environment="unseen",
            n_candidates=25,
            budget=5,
            n_init=2,
            n_test=8,
            n_probe=8,
            n_restarts=0,
        ),
        seed=4,
    )
    assert result.final_metrics["n_obs"] == 5.0
    assert np.isfinite(result.final_metrics["function_recovery_rmse"])


def test_open_loop_policy_does_not_reorder_after_init() -> None:
    env = UnseenScientificSystem(n_candidates=30, n_test=8, noise_std=0.1)
    cfg = ExperimentConfig(
        name="test",
        environment="unseen",
        n_candidates=30,
        budget=6,
        n_init=2,
        n_test=8,
        n_probe=8,
        n_restarts=0,
    )
    a = run_sequential(env, make_policy("echo_no_sequential"), cfg, seed=5)
    env_b = UnseenScientificSystem(n_candidates=30, n_test=8, noise_std=0.1)
    b = run_sequential(env_b, make_policy("echo_no_sequential"), cfg, seed=5)
    assert [s["index"] for s in a.sequence] == [s["index"] for s in b.sequence]
    assert len(a.sequence) == 6


def test_bench_registry_lists_core_tasks() -> None:
    names = available_tasks()
    for required in (
        "nonlinear_surface",
        "competing_hypotheses",
        "falsification",
        "cost_aware",
        "causal_roots",
        "unseen_form",
        "multimodal_regions",
        "anomaly_box",
    ):
        assert required in names
    task = get_task("causal_roots")
    assert task.environment == "causal"
    assert task.primary_metric == "structural_hamming_distance"
