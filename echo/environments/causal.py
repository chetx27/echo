"""Hidden linear Gaussian SCM with hard interventions on the roots.

True graph (evaluator-only):

    A → C → D
    B → C

Structural equations:

    A = a          (set by the experiment)
    B = b          (set by the experiment)
    C = 1.5 A + 1.2 B + ε_C
    D = 0.8 C + ε_D

Each candidate is x = (a, b) = do(A=a, B=b). The agent observes y = D.
Full tuples (A, B, C, D) are stored for evaluator-only graph recovery.

This is a designed two-factor experiment, not a search over which single
variable to intervene on. That restriction is recorded in decision 0008.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from echo.environments.base import ExperimentOutcome, SyntheticRegressionEnvironment

W_AC = 1.5
W_BC = 1.2
W_CD = 0.8

TRUE_PARENTS = {
    "A": frozenset(),
    "B": frozenset(),
    "C": frozenset({"A", "B"}),
    "D": frozenset({"C"}),
}


def causal_reduced_fn(X: np.ndarray) -> np.ndarray:
    """Noiseless reduced form D(A, B)."""
    X = np.asarray(X, dtype=float)
    c = W_AC * X[:, 0] + W_BC * X[:, 1]
    return W_CD * c


def causal_features(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    return np.column_stack([X[:, 0], X[:, 1]])


class CausalScientificSystem(SyntheticRegressionEnvironment):
    name = "causal"
    NODE_NAMES = ("A", "B", "C", "D")

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("dim", 2)
        super().__init__(
            true_fn=causal_reduced_fn,
            theta=np.array([W_AC * W_CD, W_BC * W_CD]),
            feature_fn=causal_features,
            feature_names=["A", "B"],
            formula="A->C->D, B->C; C=1.5A+1.2B, D=0.8C",
            **kwargs,
        )
        self._noise_c: np.ndarray | None = None
        self._noise_d: np.ndarray | None = None
        self._system_obs: list[dict[str, float]] = []

    def reset(self, seed: int) -> None:
        super().reset(seed)
        rng_c = np.random.default_rng(int(seed) + 91)
        rng_d = np.random.default_rng(int(seed) + 92)
        self._noise_c = rng_c.normal(0.0, self.noise_std, size=self.n_candidates)
        self._noise_d = rng_d.normal(0.0, self.noise_std, size=self.n_candidates)
        self._system_obs = []

    def perform_experiment(self, index: int) -> ExperimentOutcome:
        self._require_reset()
        assert self._candidates is not None and self._costs is not None
        assert self._noise_c is not None and self._noise_d is not None
        index = int(index)
        if index < 0 or index >= self.n_candidates:
            raise IndexError(f"candidate index {index} out of range")
        x = self._candidates[index]
        a = float(x[0])
        b = float(x[1])
        c = W_AC * a + W_BC * b + float(self._noise_c[index])
        d = W_CD * c + float(self._noise_d[index])
        self._queried.add(index)
        self._system_obs.append({"A": a, "B": b, "C": float(c), "D": float(d)})
        return ExperimentOutcome(index=index, x=x.copy(), y=float(d), cost=float(self._costs[index]))

    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        gt = super().get_ground_truth_for_evaluation()
        gt["kind"] = "causal"
        gt["true_parents"] = {k: set(v) for k, v in TRUE_PARENTS.items()}
        gt["node_names"] = list(self.NODE_NAMES)
        gt["intervened_nodes"] = ["A", "B"]
        gt["system_observations"] = [dict(row) for row in self._system_obs]
        return gt

    def get_hidden_state_for_evaluation(self) -> Dict[str, Any]:
        hidden = super().get_hidden_state_for_evaluation()
        hidden["kind"] = "causal"
        hidden["true_parents"] = {k: sorted(v) for k, v in TRUE_PARENTS.items()}
        hidden["system_observations"] = [dict(row) for row in self._system_obs]
        return hidden
