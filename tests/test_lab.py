from __future__ import annotations

from pathlib import Path

import numpy as np

from echo.environments import available_environments, make_environment, register_function
from echo.experiments.compare import compare
from echo.experiments.runner import run_sequential
from echo.lab import FunctionWorld, TabularWorld, compare_policies, tabular_from_csv
from echo.policies import available_algorithms, make_policy, register_acquisition
from echo.utils.io import ExperimentConfig, load_config


def test_plugin_config_registers_environment() -> None:
    cfg = load_config("configs/example_oscillator.yaml")
    assert cfg.environment == "oscillator"
    assert "oscillator" in available_environments()
    env = make_environment("oscillator", n_candidates=12, n_test=4, noise_std=0.1)
    env.reset(0)
    assert env.dim == 1
    assert env.name == "oscillator"


def test_first_experiment_hash_is_stable() -> None:
    cfg = load_config("configs/first_experiment.yaml")
    assert cfg.config_hash() == "6ffdacd9e99772df"
    assert cfg.plugin is None


def test_register_function_and_run() -> None:
    def f(X):
        X = np.asarray(X, dtype=float)
        return X[:, 0] ** 2

    register_function("unit_quad", f, dim=1, formula="x^2")
    assert "unit_quad" in available_environments()
    env = make_environment("unit_quad", n_candidates=30, n_test=8, noise_std=0.05)
    result = run_sequential(
        env,
        make_policy("random"),
        ExperimentConfig(
            name="test",
            environment="unit_quad",
            n_candidates=30,
            budget=5,
            n_init=2,
            n_test=8,
            n_probe=6,
            n_restarts=0,
        ),
        seed=0,
    )
    assert result.environment == "unit_quad"
    assert result.final_metrics["n_obs"] == 5.0
    assert np.isfinite(result.final_metrics["function_recovery_rmse"])


def test_tabular_held_out_split() -> None:
    rng = np.random.default_rng(0)
    X = rng.uniform(-1, 1, size=(40, 2))
    f = X[:, 0] - 0.5 * X[:, 1]
    y = f + rng.normal(0, 0.01, size=40)
    env = TabularWorld(X, y, f=f, n_test=8)
    env.reset(1)
    assert env.get_candidates().shape[0] == 32
    gt = env.get_ground_truth_for_evaluation()
    assert gt["X_test"].shape == (8, 2)
    out = env.perform_experiment(0)
    assert np.isfinite(out.y)


def test_tabular_from_csv(tmp_path: Path) -> None:
    path = tmp_path / "table.csv"
    path.write_text("x1,y,f\n0,0,0\n1,1.1,1\n2,3.9,4\n3,9.2,9\n4,16.1,16\n5,24.8,25\n")
    env = tabular_from_csv(path, ["x1"], "y", f_column="f", n_test=2)
    env.reset(0)
    assert env.dim == 1
    assert env.get_candidates().shape[0] == 4


def test_custom_acquisition_is_listed() -> None:
    def edge_score(state):
        return np.abs(state.candidates[:, 0])

    register_acquisition("unit_edge", edge_score)
    assert "unit_edge" in available_algorithms()
    policy = make_policy("unit_edge")
    env = FunctionWorld(lambda X: np.asarray(X)[:, 0], dim=1, n_candidates=20, n_test=5, noise_std=0.0)
    result = run_sequential(
        env,
        policy,
        ExperimentConfig(name="test", n_candidates=20, budget=4, n_init=2, n_test=5, n_probe=4, n_restarts=0),
        seed=2,
    )
    assert len(result.sequence) == 4


def test_compare_resume(tmp_path: Path) -> None:
    def f(X):
        return np.asarray(X, dtype=float)[:, 0]

    register_function("unit_line", f, dim=1)
    cfg = ExperimentConfig(
        name="resume_unit",
        environment="unit_line",
        algorithms=["random"],
        n_candidates=20,
        budget=4,
        n_init=2,
        n_test=5,
        n_probe=4,
        n_seeds=1,
        n_restarts=0,
        output_dir=str(tmp_path),
        plot_metrics=["function_recovery_rmse"],
    )
    a = compare(cfg, n_jobs=1, resume=True)
    runs = list((tmp_path / "resume_unit" / "runs").glob("*.json"))
    assert len(runs) == 1
    stamp = runs[0].stat().st_mtime
    b = compare(cfg, n_jobs=1, resume=True)
    assert len(list((tmp_path / "resume_unit" / "runs").glob("*.json"))) == 1
    assert (tmp_path / "resume_unit" / "runs" / runs[0].name).stat().st_mtime == stamp
    assert a["config_hash"] == b["config_hash"]


def test_compare_policies_callable(tmp_path: Path) -> None:
    summary = compare_policies(
        lambda X: np.sin(np.asarray(X)[:, 0]),
        algorithms=["random", "uncertainty"],
        name="lab_api_unit",
        dim=1,
        budget=4,
        n_candidates=25,
        n_seeds=1,
        n_init=2,
        n_test=6,
        n_probe=4,
        n_jobs=1,
        output_dir=str(tmp_path),
        n_restarts=0,
        plot_metrics=["function_recovery_rmse"],
    )
    assert summary["n_seeds"] == 1
    assert "random" in summary["final"]["function_recovery_rmse"]
    assert (tmp_path / "lab_api_unit" / "report.md").is_file()
