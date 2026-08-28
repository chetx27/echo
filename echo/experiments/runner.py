"""Sequential experiment loop.

The policy never receives the environment object. Ground truth is read
only by the evaluator after each observation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

from echo.environments.base import ScientificEnvironment
from echo.evaluation.metrics import evaluate_belief
from echo.models.gp import GaussianProcessModel
from echo.policies.acquisition_policy import AcquisitionPolicy
from echo.policies.base import Policy
from echo.policies.state import DecisionState
from echo.utils.io import ExperimentConfig
from echo.utils.seeding import rng_for


@dataclass
class RunResult:
    run_id: str
    environment: str
    algorithm: str
    seed: int
    config_hash: str
    metrics: List[Dict[str, float]] = field(default_factory=list)
    sequence: List[Dict[str, Any]] = field(default_factory=list)
    final_metrics: Dict[str, float] = field(default_factory=dict)
    hyperparameters: List[dict] = field(default_factory=list)
    n_candidates: int = 0
    budget: int = 0
    noise: float = 0.0

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "environment": self.environment,
            "algorithm": self.algorithm,
            "seed": self.seed,
            "config_hash": self.config_hash,
            "n_candidates": self.n_candidates,
            "budget": self.budget,
            "noise": self.noise,
            "metrics": self.metrics,
            "sequence": self.sequence,
            "final_metrics": self.final_metrics,
            "hyperparameters": self.hyperparameters,
        }


def run_sequential(
    env: ScientificEnvironment,
    policy: Policy,
    config: ExperimentConfig,
    seed: int,
) -> RunResult:
    env.reset(seed)
    candidates = env.get_candidates()
    costs = env.get_costs()
    n = len(candidates)
    available = np.ones(n, dtype=bool)
    x_low, x_high = env.bounds

    init_rng = rng_for(seed, 1)
    policy_rng = rng_for(seed, 2)
    gp_rng = rng_for(seed, 3)
    probe_rng = rng_for(seed, 17)
    X_probe = x_low + probe_rng.random((config.n_probe, env.dim)) * (x_high - x_low)

    model = GaussianProcessModel(x_low=x_low, x_high=x_high)
    X_obs: List[np.ndarray] = []
    y_obs: List[float] = []
    sequence: List[Dict[str, Any]] = []
    metrics_over_time: List[Dict[str, float]] = []
    hypers: List[dict] = []

    n_init = min(config.n_init, config.budget)
    init_idx = init_rng.choice(n, size=n_init, replace=False)
    for idx in init_idx:
        outcome = env.perform_experiment(int(idx))
        available[int(idx)] = False
        X_obs.append(outcome.x)
        y_obs.append(outcome.y)
        sequence.append(
            {
                "step": len(X_obs),
                "index": outcome.index,
                "x": outcome.x.tolist(),
                "y": outcome.y,
                "cost": outcome.cost,
                "phase": "init",
                "acquisition_score": None,
            }
        )

    X_arr = np.vstack(X_obs)
    y_arr = np.asarray(y_obs, dtype=float)
    model.fit(X_arr, y_arr, optimize=True, rng=gp_rng, n_restarts=config.n_restarts)
    belief = _maybe_belief(env, config.noise, X_arr, y_arr)
    gt = env.get_ground_truth_for_evaluation()
    metrics_over_time.append(evaluate_belief(model, X_arr, y_arr, gt, X_probe, belief))
    hypers.append(model.hyperparameters())

    while len(X_obs) < config.budget:
        state = DecisionState(
            candidates=candidates,
            available_mask=available,
            X_obs=X_arr,
            y_obs=y_arr,
            costs=costs,
            step=len(X_obs),
            budget=config.budget,
            model=model,
            rng=policy_rng,
            X_probe=X_probe,
            hypothesis_belief=belief,
        )
        idx = int(policy.select(state))
        if not available[idx]:
            raise RuntimeError(f"{policy.name} selected an unavailable candidate {idx}")
        score = None
        if isinstance(policy, AcquisitionPolicy) and policy.last_scores is not None:
            score = float(policy.last_scores[idx])
        outcome = env.perform_experiment(idx)
        available[idx] = False
        X_obs.append(outcome.x)
        y_obs.append(outcome.y)
        sequence.append(
            {
                "step": len(X_obs),
                "index": outcome.index,
                "x": outcome.x.tolist(),
                "y": outcome.y,
                "cost": outcome.cost,
                "phase": "adaptive",
                "acquisition_score": score,
            }
        )
        X_arr = np.vstack(X_obs)
        y_arr = np.asarray(y_obs, dtype=float)
        model.fit(X_arr, y_arr, optimize=True, rng=gp_rng, n_restarts=config.n_restarts)
        if belief is not None:
            belief.fit(X_arr, y_arr)
        metrics_over_time.append(evaluate_belief(model, X_arr, y_arr, gt, X_probe, belief))
        hypers.append(model.hyperparameters())

    run_id = f"{env.name}_{policy.name}_seed{seed}_{config.config_hash()}"
    return RunResult(
        run_id=run_id,
        environment=env.name,
        algorithm=policy.name,
        seed=seed,
        config_hash=config.config_hash(),
        metrics=metrics_over_time,
        sequence=sequence,
        final_metrics=metrics_over_time[-1],
        hyperparameters=hypers,
        n_candidates=n,
        budget=config.budget,
        noise=config.noise,
    )


def _maybe_belief(env, noise: float, X: np.ndarray, y: np.ndarray):
    getter = getattr(env, "get_candidate_hypotheses", None)
    if getter is None:
        return None
    from echo.hypotheses.belief import HypothesisBelief

    belief = HypothesisBelief(getter(), noise_std=noise)
    belief.fit(X, y)
    return belief
