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
    hypothesis_belief: Any = None,
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

    hyp_entropy = float("nan")
    correct_p = float("nan")
    identified = float("nan")
    leading_correct = float("nan")
    if hypothesis_belief is not None and "true_hypothesis_index" in ground_truth:
        post = np.asarray(hypothesis_belief.posterior(), dtype=float)
        true_i = int(ground_truth["true_hypothesis_index"])
        q = np.clip(post, 1e-15, 1.0)
        hyp_entropy = float(-np.sum(q * np.log(q)))
        correct_p = float(post[true_i])
        identified = float(correct_p >= 0.9)
        leading_correct = float(int(np.argmax(post)) == true_i)

    return {
        "n_obs": n_obs,
        "function_recovery_rmse": function_rmse,
        "prediction_error": function_rmse,
        "prediction_mae": prediction_mae,
        "parameter_recovery_rmse": parameter_rmse,
        "parameter_recovery_l2": parameter_l2,
        "mean_predictive_std": mean_std,
        "probe_entropy": entropy,
        "hypothesis_entropy": hyp_entropy,
        "correct_hypothesis_prob": correct_p,
        "hypothesis_identified": identified,
        "leading_hypothesis_correct": leading_correct,
    }
