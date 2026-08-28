"""Bayesian linear-in-parameter hypothesis beliefs.

Each hypothesis H has features Φ_H(x) and θ ~ N(0, σ0² I),
y | θ ~ N(Φθ, σn² I). Posteriors P(H | D) come from the Gaussian
marginal likelihood with a uniform prior over hypotheses.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy.linalg import cho_solve

from echo.hypotheses.models import ParametricHypothesis


def _entropy(p: np.ndarray) -> float:
    q = np.clip(p, 1e-15, 1.0)
    return float(-np.sum(q * np.log(q)))


class HypothesisBelief:
    def __init__(
        self,
        hypotheses: Sequence[ParametricHypothesis],
        noise_std: float = 0.1,
        prior_scale: float = 2.0,
    ) -> None:
        self.hypotheses = list(hypotheses)
        self.noise_std = float(noise_std)
        self.prior_scale = float(prior_scale)
        self.log_prior = np.log(np.ones(len(self.hypotheses)) / len(self.hypotheses))
        self.X = np.zeros((0, 1))
        self.y = np.zeros((0,))

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        self.X = X
        self.y = np.asarray(y, dtype=float).ravel()

    def log_marginals(self) -> np.ndarray:
        logs = []
        for h in self.hypotheses:
            logs.append(self._log_marginal(h.features(self.X), self.y))
        return np.asarray(logs, dtype=float)

    def posterior(self) -> np.ndarray:
        logp = self.log_marginals() + self.log_prior
        logp = logp - np.max(logp)
        p = np.exp(logp)
        return p / np.sum(p)

    def entropy(self) -> float:
        return _entropy(self.posterior())

    def leading_index(self) -> int:
        return int(np.argmax(self.posterior()))

    def _log_marginal(self, Phi: np.ndarray, y: np.ndarray) -> float:
        n = len(y)
        if n == 0:
            return 0.0
        sn2 = self.noise_std**2
        s02 = self.prior_scale**2
        V = sn2 * np.eye(n) + s02 * (Phi @ Phi.T)
        V = V + 1e-8 * np.eye(n)
        try:
            L = np.linalg.cholesky(V)
        except np.linalg.LinAlgError:
            return -1e12
        alpha = cho_solve((L, True), y)
        logdet = 2.0 * float(np.sum(np.log(np.diag(L))))
        return -0.5 * n * np.log(2.0 * np.pi) - 0.5 * logdet - 0.5 * float(y @ alpha)

    def predict_each(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return (means, vars) of shape (n_hypotheses, n_points) for p(y|x,H,D)."""
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        n_h = len(self.hypotheses)
        n_x = len(X)
        means = np.zeros((n_h, n_x))
        vars_ = np.zeros((n_h, n_x))
        sn2 = self.noise_std**2
        s02 = self.prior_scale**2
        for i, h in enumerate(self.hypotheses):
            if len(self.y) == 0:
                phi = h.features(X)
                means[i] = 0.0
                vars_[i] = sn2 + s02 * np.sum(phi**2, axis=1)
                continue
            Phi = h.features(self.X)
            phi = h.features(X)
            p = Phi.shape[1]
            A = (Phi.T @ Phi) / sn2 + np.eye(p) / s02
            A = A + 1e-8 * np.eye(p)
            L = np.linalg.cholesky(A)
            mu = cho_solve((L, True), Phi.T @ self.y / sn2)
            means[i] = phi @ mu
            v = np.linalg.solve(L, phi.T)
            vars_[i] = np.sum(v**2, axis=0) + sn2
        return means, np.clip(vars_, 1e-12, None)
