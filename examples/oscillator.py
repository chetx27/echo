"""Example: plug a custom hidden law into ECHO and compare policies.

Run either:

    python examples/oscillator.py

or, after this file is imported as a plugin:

    python -m echo compare --config configs/example_oscillator.yaml
"""

from __future__ import annotations

import numpy as np

from echo.lab import compare_policies, register_function


def oscillator(X: np.ndarray) -> np.ndarray:
    x = np.asarray(X, dtype=float)[:, 0]
    return np.sin(3.0 * x) + 0.4 * x**2


register_function(
    "oscillator",
    oscillator,
    dim=1,
    formula="y = sin(3x) + 0.4 x^2 + eps",
    feature_fn=lambda X: np.column_stack(
        [np.sin(3.0 * np.asarray(X)[:, 0]), np.asarray(X)[:, 0] ** 2]
    ),
    feature_names=["sin(3x)", "x^2"],
    theta=np.array([1.0, 0.4]),
)


if __name__ == "__main__":
    summary = compare_policies(
        "oscillator",
        algorithms=["random", "uncertainty", "echo_v0"],
        name="example_oscillator",
        budget=12,
        n_candidates=400,
        n_seeds=5,
        n_init=3,
        n_test=100,
        n_probe=32,
        n_restarts=0,
        primary_algorithm="echo_v0",
        comparator="uncertainty",
        plot_metrics=["function_recovery_rmse", "parameter_recovery_rmse"],
    )
    print("wrote results/example_oscillator/")
    print("final RMSE:", {k: v["mean"] for k, v in summary["final"]["function_recovery_rmse"].items()})
