"""Exact Gaussian process regression with an RBF kernel.

Hyperparameters are fit by maximizing the log marginal likelihood.
Input coordinates are scaled to the unit cube using fixed domain bounds
so that lengthscales are comparable across sequential steps.
"""

from __future__ import annotations

from typing import Optional, Tuple, Union

import numpy as np
from scipy.linalg import cho_solve, solve_triangular
from scipy.optimize import minimize
from scipy.spatial.distance import cdist


def rbf_kernel(X1: np.ndarray, X2: np.ndarray, lengthscale: float, variance: float) -> np.ndarray:
    scale = max(float(lengthscale), 1e-12)
    dist2 = cdist(X1 / scale, X2 / scale, metric="sqeuclidean")
    return float(variance) * np.exp(-0.5 * dist2)


class GaussianProcessModel:
    """Exact GP. Predictive mean/std are in the original units of y."""

    def __init__(
        self,
        x_low: np.ndarray,
        x_high: np.ndarray,
        jitter: float = 1e-8,
    ) -> None:
        self.x_low = np.asarray(x_low, dtype=float)
        self.x_high = np.asarray(x_high, dtype=float)
        span = self.x_high - self.x_low
        self.x_span = np.where(span < 1e-12, 1.0, span)
        self.jitter = float(jitter)
        self.lengthscale = 0.3
        self.signal_variance = 1.0
        self.noise_variance = 0.05  # on standardized y
        self._y_mean = 0.0
        self._y_std = 1.0
        self._scale_frozen = False
        self.X_: Optional[np.ndarray] = None
        self.X_norm_: Optional[np.ndarray] = None
        self.y_: Optional[np.ndarray] = None
        self._L: Optional[np.ndarray] = None
        self._alpha: Optional[np.ndarray] = None

    def normalize_x(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        return (X - self.x_low) / self.x_span

    @property
    def noise_variance_original(self) -> float:
        """Observation noise variance on the original y scale."""
        return float(self.noise_variance * self._y_std**2)

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        optimize: bool = True,
        rng: Optional[np.random.Generator] = None,
        n_restarts: int = 2,
    ) -> None:
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float).ravel()
        if X.ndim != 2 or len(X) != len(y):
            raise ValueError("X must be (n, d) and y length n")
        if len(y) < 1:
            raise ValueError("need at least one observation")

        if not self._scale_frozen:
            self._y_mean = float(y.mean())
            std = float(y.std())
            self._y_std = std if std > 1e-8 else 1.0
            self._scale_frozen = True

        self.X_ = X.copy()
        self.X_norm_ = self.normalize_x(X)
        self.y_ = y.copy()
        y_n = (y - self._y_mean) / self._y_std

        if optimize and len(y) >= 2:
            self._optimize_hyperparameters(self.X_norm_, y_n, rng=rng, n_restarts=n_restarts)
        self._factor(self.X_norm_, y_n)

    def _factor(self, Xn: np.ndarray, yn: np.ndarray) -> None:
        extra = self.jitter
        for _ in range(6):
            K = rbf_kernel(Xn, Xn, self.lengthscale, self.signal_variance)
            K = K + (self.noise_variance + extra) * np.eye(len(Xn))
            try:
                self._L = np.linalg.cholesky(K)
                self._alpha = cho_solve((self._L, True), yn)
                return
            except np.linalg.LinAlgError:
                extra *= 10.0
        raise np.linalg.LinAlgError("GP covariance remained non-PD after jitter increases")

    def _nll(self, params: np.ndarray, Xn: np.ndarray, yn: np.ndarray) -> float:
        lengthscale, signal_variance, noise_variance = np.exp(params)
        K = rbf_kernel(Xn, Xn, lengthscale, signal_variance)
        K = K + (noise_variance + self.jitter) * np.eye(len(Xn))
        try:
            L = np.linalg.cholesky(K)
        except np.linalg.LinAlgError:
            return 1e12
        alpha = cho_solve((L, True), yn)
        logdet = 2.0 * float(np.sum(np.log(np.diag(L))))
        n = len(yn)
        return 0.5 * float(yn @ alpha) + 0.5 * logdet + 0.5 * n * np.log(2.0 * np.pi)

    def _optimize_hyperparameters(
        self,
        Xn: np.ndarray,
        yn: np.ndarray,
        rng: Optional[np.random.Generator],
        n_restarts: int,
    ) -> None:
        rng = rng if rng is not None else np.random.default_rng(0)
        starts = [np.log([self.lengthscale, self.signal_variance, self.noise_variance])]
        for _ in range(max(0, n_restarts)):
            starts.append(
                np.log(
                    [
                        rng.uniform(0.05, 1.5),
                        rng.uniform(0.1, 4.0),
                        rng.uniform(1e-3, 0.5),
                    ]
                )
            )
        bounds = [
            (np.log(0.05), np.log(2.0)),
            (np.log(1e-3), np.log(20.0)),
            (np.log(1e-4), np.log(2.0)),
        ]
        best_fun = np.inf
        best_x = starts[0]
        for x0 in starts:
            result = minimize(
                self._nll,
                x0,
                args=(Xn, yn),
                method="L-BFGS-B",
                bounds=bounds,
            )
            if np.isfinite(result.fun) and result.fun < best_fun:
                best_fun = float(result.fun)
                best_x = result.x
        self.lengthscale, self.signal_variance, self.noise_variance = np.exp(best_x)

    def predict(
        self,
        X: np.ndarray,
        return_std: bool = True,
        return_cov: bool = False,
    ) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        self._check_fitted()
        assert self.X_norm_ is not None and self._L is not None and self._alpha is not None
        Xn = self.normalize_x(np.asarray(X, dtype=float))
        K_s = rbf_kernel(Xn, self.X_norm_, self.lengthscale, self.signal_variance)
        mean_n = K_s @ self._alpha
        mean = mean_n * self._y_std + self._y_mean
        if not return_std and not return_cov:
            return mean
        v = solve_triangular(self._L, K_s.T, lower=True)
        if return_cov:
            K_ss = rbf_kernel(Xn, Xn, self.lengthscale, self.signal_variance)
            cov_n = K_ss - v.T @ v
            cov_n = 0.5 * (cov_n + cov_n.T)
            cov = cov_n * self._y_std**2
            if return_std:
                std = np.sqrt(np.clip(np.diag(cov), 0.0, None))
                return mean, std, cov
            return mean, cov
        var_n = self.signal_variance - np.sum(v**2, axis=0)
        std = np.sqrt(np.clip(var_n, 0.0, None)) * self._y_std
        return mean, std

    def posterior_cross_covariance(self, X_a: np.ndarray, X_b: np.ndarray) -> np.ndarray:
        """cov(f(X_a), f(X_b) | D) on the original y scale."""
        self._check_fitted()
        assert self.X_norm_ is not None and self._L is not None
        An = self.normalize_x(np.asarray(X_a, dtype=float))
        Bn = self.normalize_x(np.asarray(X_b, dtype=float))
        K_prior = rbf_kernel(An, Bn, self.lengthscale, self.signal_variance)
        K_a = rbf_kernel(An, self.X_norm_, self.lengthscale, self.signal_variance)
        K_b = rbf_kernel(Bn, self.X_norm_, self.lengthscale, self.signal_variance)
        v_a = solve_triangular(self._L, K_a.T, lower=True)
        v_b = solve_triangular(self._L, K_b.T, lower=True)
        return (K_prior - v_a.T @ v_b) * self._y_std**2

    def probe_entropy(self, X_probe: np.ndarray) -> float:
        """Differential entropy of a Gaussian posterior over f at probe points."""
        _, cov = self.predict(X_probe, return_std=False, return_cov=True)
        n = cov.shape[0]
        cov = cov + self.jitter * np.eye(n)
        sign, logdet = np.linalg.slogdet(cov)
        if sign <= 0:
            return float("nan")
        return 0.5 * n * np.log(2.0 * np.pi * np.e) + 0.5 * float(logdet)

    def hyperparameters(self) -> dict:
        return {
            "lengthscale": float(self.lengthscale),
            "signal_variance": float(self.signal_variance),
            "noise_variance_standardized": float(self.noise_variance),
            "noise_variance_original": self.noise_variance_original,
            "y_mean": float(self._y_mean),
            "y_std": float(self._y_std),
        }

    def _check_fitted(self) -> None:
        if self._L is None:
            raise RuntimeError("model.fit must be called before predict")
