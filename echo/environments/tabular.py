"""Finite lookup-table / CSV scientific environment.

Use this when the experimental domain is a table of candidate rows and
measured (or simulated) responses rather than a closed-form function.
A seed-dependent held-out slice is reserved for evaluation; the rest
are queryable candidates. Policies still never see the held-out rows.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, Optional, Sequence, Union

import numpy as np

from echo.environments.base import ExperimentOutcome, ScientificEnvironment

ArrayFn = Callable[[np.ndarray], np.ndarray]


class TabularScientificSystem(ScientificEnvironment):
    name = "tabular"

    def __init__(
        self,
        X: np.ndarray,
        y: np.ndarray,
        f: Optional[np.ndarray] = None,
        costs: Optional[np.ndarray] = None,
        feature_fn: Optional[ArrayFn] = None,
        theta: Optional[np.ndarray] = None,
        feature_names: Optional[Sequence[str]] = None,
        formula: str = "tabular lookup",
        n_test: Optional[int] = None,
        test_fraction: float = 0.2,
        extra_noise_std: float = 0.0,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        kwargs.pop("n_candidates", None)
        kwargs.pop("noise_std", None)
        kwargs.pop("low", None)
        kwargs.pop("high", None)
        kwargs.pop("cost_mode", None)
        if kwargs:
            raise TypeError(f"unexpected tabular kwargs: {sorted(kwargs)}")
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float).ravel()
        if X.ndim != 2:
            raise ValueError("X must have shape (n, d)")
        if len(y) != len(X):
            raise ValueError("y must have one entry per row of X")
        self._X_all = X
        self._y_all = y
        self._f_all = None if f is None else np.asarray(f, dtype=float).ravel()
        if self._f_all is not None and len(self._f_all) != len(X):
            raise ValueError("f must have one entry per row of X")
        self._costs_all = np.ones(len(X), dtype=float) if costs is None else np.asarray(costs, dtype=float).ravel()
        if len(self._costs_all) != len(X):
            raise ValueError("costs must have one entry per row of X")
        self._feature_fn = feature_fn if feature_fn is not None else (lambda Z: np.asarray(Z, dtype=float))
        self._theta = np.zeros(X.shape[1], dtype=float) if theta is None else np.asarray(theta, dtype=float)
        self._feature_names = list(feature_names) if feature_names is not None else [f"x{i + 1}" for i in range(X.shape[1])]
        self._formula = str(formula)
        self._n_test = None if n_test is None else int(n_test)
        self._test_fraction = float(test_fraction)
        self.extra_noise_std = float(extra_noise_std)
        if name:
            self.name = str(name)
        self._seed: int | None = None
        self._cand_idx: np.ndarray | None = None
        self._test_idx: np.ndarray | None = None
        self._noise: np.ndarray | None = None
        self._queried: set[int] = set()

    @property
    def bounds(self) -> tuple[np.ndarray, np.ndarray]:
        return self._X_all.min(axis=0), self._X_all.max(axis=0)

    @property
    def dim(self) -> int:
        return int(self._X_all.shape[1])

    @property
    def n_candidates(self) -> int:
        return 0 if self._cand_idx is None else int(len(self._cand_idx))

    def reset(self, seed: int) -> None:
        self._seed = int(seed)
        rng = np.random.default_rng(self._seed)
        n = len(self._X_all)
        n_test = self._n_test if self._n_test is not None else max(1, int(round(self._test_fraction * n)))
        n_test = min(n_test, n - 2)
        if n_test < 1:
            raise ValueError("need at least one test row and two candidate rows")
        perm = rng.permutation(n)
        self._test_idx = perm[:n_test]
        self._cand_idx = perm[n_test:]
        self._noise = rng.normal(0.0, self.extra_noise_std, size=len(self._cand_idx))
        self._queried = set()

    def get_candidates(self) -> np.ndarray:
        self._require_reset()
        assert self._cand_idx is not None
        return self._X_all[self._cand_idx].copy()

    def get_costs(self) -> np.ndarray:
        self._require_reset()
        assert self._cand_idx is not None
        return self._costs_all[self._cand_idx].copy()

    def perform_experiment(self, index: int) -> ExperimentOutcome:
        self._require_reset()
        assert self._cand_idx is not None and self._noise is not None
        index = int(index)
        if index < 0 or index >= len(self._cand_idx):
            raise IndexError(f"candidate index {index} out of range")
        row = int(self._cand_idx[index])
        x = self._X_all[row]
        y = float(self._y_all[row] + self._noise[index])
        self._queried.add(index)
        return ExperimentOutcome(index=index, x=x.copy(), y=y, cost=float(self._costs_all[row]))

    def get_observation(self, candidate: np.ndarray) -> float:
        self._require_reset()
        assert self._cand_idx is not None and self._noise is not None
        candidate = np.asarray(candidate, dtype=float).reshape(-1)
        table = self._X_all[self._cand_idx]
        match = np.where(np.all(np.isclose(table, candidate, atol=1e-12), axis=1))[0]
        if not len(match):
            raise ValueError("candidate is not a row of the tabular environment")
        idx = int(match[0])
        row = int(self._cand_idx[idx])
        return float(self._y_all[row] + self._noise[idx])

    def get_ground_truth_for_evaluation(self) -> Dict[str, Any]:
        self._require_reset()
        assert self._test_idx is not None
        X_test = self._X_all[self._test_idx]
        if self._f_all is not None:
            f_test = self._f_all[self._test_idx]
        else:
            f_test = self._y_all[self._test_idx]
        return {
            "X_test": X_test.copy(),
            "f_test": f_test.copy(),
            "theta": self._theta.copy(),
            "feature_names": list(self._feature_names),
            "formula": self._formula,
            "noise_std": self.extra_noise_std,
            "feature_fn": self._feature_fn,
            "kind": "tabular",
        }

    def get_hidden_state_for_evaluation(self) -> Dict[str, Any]:
        self._require_reset()
        assert self._cand_idx is not None
        return {
            "seed": self._seed,
            "name": self.name,
            "formula": self._formula,
            "theta": self._theta.copy(),
            "candidates": self._X_all[self._cand_idx].copy(),
            "true_f_candidates": (
                self._f_all[self._cand_idx].copy()
                if self._f_all is not None
                else self._y_all[self._cand_idx].copy()
            ),
            "queried_indices": sorted(self._queried),
            "kind": "tabular",
        }

    def _require_reset(self) -> None:
        if self._cand_idx is None:
            raise RuntimeError("environment.reset(seed) must be called first")


def tabular_from_csv(
    path: Union[str, Path],
    x_columns: Sequence[str],
    y_column: str,
    f_column: Optional[str] = None,
    cost_column: Optional[str] = None,
    **kwargs: Any,
) -> TabularScientificSystem:
    """Load a CSV with a header row. Requires the csv module only."""
    import csv

    path = Path(path)
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not rows:
        raise ValueError(f"no rows in {path}")
    missing = [c for c in list(x_columns) + [y_column] if c not in rows[0]]
    if missing:
        raise ValueError(f"CSV missing columns {missing}; have {list(rows[0])}")
    X = np.asarray([[float(row[c]) for c in x_columns] for row in rows], dtype=float)
    y = np.asarray([float(row[y_column]) for row in rows], dtype=float)
    f = None if f_column is None else np.asarray([float(row[f_column]) for row in rows], dtype=float)
    costs = None if cost_column is None else np.asarray([float(row[cost_column]) for row in rows], dtype=float)
    kwargs.setdefault("formula", f"csv:{path.name}")
    return TabularScientificSystem(X, y, f=f, costs=costs, **kwargs)
