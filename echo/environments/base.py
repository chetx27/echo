"""Scientific environment interface.

Policies receive observations through the experiment runner. They never
receive the environment object, so evaluator-only methods cannot be called
during decision-making.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict

import numpy as np


@dataclass(frozen=True)
class ExperimentOutcome:
    index: int
    x: np.ndarray
    y: float
    cost: float


class ScientificEnvironment(ABC):
    """Common interface for synthetic (and later real) scientific systems."""

    name: str

    @abstractmethod
    def reset(self, seed: int) -> None:
        """Draw candidates, noise, and evaluation sets. Deterministic in seed."""

    @abstractmethod
    def get_candidates(self) -> np.ndarray:
        """Candidate experiment locations, shape (n, d)."""

    @abstractmethod
    def get_costs(self) -> np.ndarray:
        """Per-candidate experimental cost, shape (n,)."""

    @abstractmethod
    def perform_experiment(self, index: int) -> ExperimentOutcome:
        """Execute a candidate by index. Agent-accessible."""

    @abstractmethod
    def get_observation(self, candidate: np.ndarray) -> float:
        """Observe y at a location. Prefer perform_experiment in the main loop."""

    @abstractmethod
    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        """Evaluator-only. Hidden law, test set, parameters. Not for policies."""

    @abstractmethod
    def get_hidden_state_for_evaluation(self) -> Dict[str, Any]:
        """Evaluator-only. Full hidden state for failure analysis."""

    @property
    @abstractmethod
    def bounds(self) -> tuple[np.ndarray, np.ndarray]:
        """Lower and upper bounds of the experimental domain."""

    @property
    @abstractmethod
    def dim(self) -> int:
        """Input dimension."""


class SyntheticRegressionEnvironment(ScientificEnvironment):
    """Shared machinery for hidden-function regression worlds."""

    name = "synthetic"

    def __init__(
        self,
        true_fn: Callable[[np.ndarray], np.ndarray],
        theta: np.ndarray,
        feature_fn: Callable[[np.ndarray], np.ndarray],
        feature_names: list[str],
        formula: str,
        n_candidates: int = 10000,
        n_test: int = 1000,
        noise_std: float = 0.1,
        low: float = -2.0,
        high: float = 2.0,
        dim: int = 3,
        cost: float = 1.0,
        cost_mode: str = "uniform",
    ) -> None:
        self._true_fn = true_fn
        self._theta = np.asarray(theta, dtype=float)
        self._feature_fn = feature_fn
        self._feature_names = list(feature_names)
        self._formula = formula
        self.n_candidates = int(n_candidates)
        self.n_test = int(n_test)
        self.noise_std = float(noise_std)
        self._low = np.full(dim, low, dtype=float)
        self._high = np.full(dim, high, dtype=float)
        self._dim = int(dim)
        self._unit_cost = float(cost)
        self.cost_mode = str(cost_mode)
        self._seed: int | None = None
        self._candidates: np.ndarray | None = None
        self._noise: np.ndarray | None = None
        self._costs: np.ndarray | None = None
        self._X_test: np.ndarray | None = None
        self._f_test: np.ndarray | None = None
        self._queried: set[int] = set()

    @property
    def bounds(self) -> tuple[np.ndarray, np.ndarray]:
        return self._low.copy(), self._high.copy()

    @property
    def dim(self) -> int:
        return self._dim

    def reset(self, seed: int) -> None:
        self._seed = int(seed)
        rng = np.random.default_rng(self._seed)
        self._candidates = self._draw_points(rng, self.n_candidates)
        self._noise = rng.normal(0.0, self.noise_std, size=self.n_candidates)
        self._costs = self._make_costs(self._candidates)
        test_rng = np.random.default_rng(self._seed + 10_007)
        self._X_test = self._draw_points(test_rng, self.n_test)
        self._f_test = self._true_fn(self._X_test)
        self._queried = set()

    def _make_costs(self, X: np.ndarray) -> np.ndarray:
        n = len(X)
        if self.cost_mode == "uniform":
            return np.full(n, self._unit_cost, dtype=float)
        span = np.where(self._high - self._low < 1e-12, 1.0, self._high - self._low)
        if self.cost_mode == "radial":
            mid = 0.5 * (self._low + self._high)
            r = np.linalg.norm((X - mid) / span, axis=1)
            return 1.0 + 9.0 * r
        if self.cost_mode == "x_right":
            u = (X[:, 0] - self._low[0]) / span[0]
            return 1.0 + 19.0 * np.clip(u, 0.0, 1.0)
        raise ValueError(f"unknown cost_mode {self.cost_mode!r}")

    def _draw_points(self, rng: np.random.Generator, n: int) -> np.ndarray:
        u = rng.random((n, self._dim))
        return self._low + u * (self._high - self._low)

    def get_candidates(self) -> np.ndarray:
        self._require_reset()
        assert self._candidates is not None
        return self._candidates.copy()

    def get_costs(self) -> np.ndarray:
        self._require_reset()
        assert self._costs is not None
        return self._costs.copy()

    def perform_experiment(self, index: int) -> ExperimentOutcome:
        self._require_reset()
        assert self._candidates is not None and self._noise is not None
        assert self._costs is not None
        index = int(index)
        if index < 0 or index >= self.n_candidates:
            raise IndexError(f"candidate index {index} out of range")
        x = self._candidates[index]
        y = float(self._true_fn(x.reshape(1, -1))[0] + self._noise[index])
        self._queried.add(index)
        return ExperimentOutcome(index=index, x=x.copy(), y=y, cost=float(self._costs[index]))

    def get_observation(self, candidate: np.ndarray) -> float:
        self._require_reset()
        assert self._candidates is not None and self._noise is not None
        candidate = np.asarray(candidate, dtype=float).reshape(-1)
        match = np.where(np.all(np.isclose(self._candidates, candidate, atol=1e-12), axis=1))[0]
        if len(match):
            idx = int(match[0])
            return float(self._true_fn(candidate.reshape(1, -1))[0] + self._noise[idx])
        # Off-grid observation: deterministic noise from seed and location.
        key = np.abs(np.round(candidate * 1e6)).astype(np.int64)
        loc_seed = int((int(self._seed) + 17 * int(np.sum(key))) % (2**31 - 1))
        loc_rng = np.random.default_rng(loc_seed)
        return float(self._true_fn(candidate.reshape(1, -1))[0] + loc_rng.normal(0.0, self.noise_std))

    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        self._require_reset()
        assert self._X_test is not None and self._f_test is not None
        return {
            "X_test": self._X_test.copy(),
            "f_test": self._f_test.copy(),
            "theta": self._theta.copy(),
            "feature_names": list(self._feature_names),
            "formula": self._formula,
            "noise_std": self.noise_std,
            "feature_fn": self._feature_fn,
        }

    def get_hidden_state_for_evaluation(self) -> Dict[str, Any]:
        self._require_reset()
        assert self._candidates is not None and self._noise is not None
        return {
            "seed": self._seed,
            "name": self.name,
            "formula": self._formula,
            "theta": self._theta.copy(),
            "candidates": self._candidates.copy(),
            "true_f_candidates": self._true_fn(self._candidates),
            "noise": self._noise.copy(),
            "queried_indices": sorted(self._queried),
        }

    def _require_reset(self) -> None:
        if self._candidates is None:
            raise RuntimeError("environment.reset(seed) must be called first")
