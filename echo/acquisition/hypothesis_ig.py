"""Hypothesis-discrimination acquisition (Box–Hill 1967 style).

Score(x) = sum_{i<j} P_i P_j [ KL(p_i || p_j) + KL(p_j || p_i) ]

where p_i = p(y | x, H_i, D) is Gaussian. An experiment that merely
confirms an already-dominant hypothesis scores low if the other models
make the same prediction there.
"""

from __future__ import annotations

import numpy as np

from echo.policies.state import DecisionState


def _kl_gaussian(m1: np.ndarray, v1: np.ndarray, m2: np.ndarray, v2: np.ndarray) -> np.ndarray:
    return 0.5 * (np.log(v2 / v1) + (v1 + (m1 - m2) ** 2) / v2 - 1.0)


def hypothesis_discrimination(state: DecisionState) -> np.ndarray:
    belief = state.hypothesis_belief
    if belief is None:
        from echo.acquisition.information_gain import global_information_gain

        return global_information_gain(state)
    post = belief.posterior()
    means, vars_ = belief.predict_each(state.candidates)
    n_h, n_x = means.shape
    scores = np.zeros(n_x, dtype=float)
    for i in range(n_h):
        for j in range(i + 1, n_h):
            w = post[i] * post[j]
            if w <= 0:
                continue
            kl = _kl_gaussian(means[i], vars_[i], means[j], vars_[j])
            kl_rev = _kl_gaussian(means[j], vars_[j], means[i], vars_[i])
            scores += w * (kl + kl_rev)
    return scores
