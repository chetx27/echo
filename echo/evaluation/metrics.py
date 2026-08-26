from __future__ import annotations

from typing import Any, Dict

import numpy as np

from echo.models.gp import GaussianProcessModel


def evaluate_belief(
    model: GaussianProcessModel,
    X_obs: np.ndarray,
    y_obs: np.ndarray,
    ground_truth: Dict[str, Any],
    X_probe: np.ndarray,
) -> Dict[str, float]:
    """Evaluator-only metrics. Uses hidden law and oracle features."""
    X_test = ground_truth["X_test"]
    f_test = ground_truth["f_test"]
    theta = np.asarray(ground_truth["theta"], dtype=float)
    feature_fn = ground_truth["feature_fn"]

    mu, std = model.predict(X_test, return_std=True)
    mu = np.asarray(mu, dtype=float)
    std = np.asarray(std, dtype=float)
    function_rmse = float(np.sqrt(np.mean((mu - f_test) ** 2)))
    prediction_mae = float(np.mean(np.abs(mu - f_test)))
    mean_std = float(np.mean(std))

    Phi = np.asarray(feature_fn(X_obs), dtype=float)
    n, p = Phi.shape
    if n >= p:
        theta_hat, *_ = np.linalg.lstsq(Phi, y_obs, rcond=None)
        parameter_rmse = float(np.sqrt(np.mean((theta_hat - theta) ** 2)))
        parameter_l2 = float(np.linalg.norm(theta_hat - theta))
    else:
        parameter_rmse = float("nan")
        parameter_l2 = float("nan")

    entropy = float(model.probe_entropy(X_probe))
    n_obs = float(len(y_obs))

    return {
        "n_obs": n_obs,
        "function_recovery_rmse": function_rmse,
        "prediction_error": function_rmse,
        "prediction_mae": prediction_mae,
        "parameter_recovery_rmse": parameter_rmse,
        "parameter_recovery_l2": parameter_l2,
        "mean_predictive_std": mean_std,
        "probe_entropy": entropy,
    }
