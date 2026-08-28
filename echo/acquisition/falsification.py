"""Falsification-driven acquisition.

Let H* be the current leading hypothesis. Score(x) is the posterior-weighted
squared disagreement between H* and the alternatives, scaled by predictive
variance. Large scores are locations where another remaining hypothesis
would make a different prediction than H*.

This is not assumed to help. Experiment 2 compares it to discrimination
and to generic uncertainty.
"""

from __future__ import annotations

import numpy as np

from echo.policies.state import DecisionState


def falsification_score(state: DecisionState) -> np.ndarray:
    belief = state.hypothesis_belief
    if belief is None:
        from echo.acquisition.information_gain import global_information_gain

        return global_information_gain(state)
    post = belief.posterior()
    star = int(np.argmax(post))
    means, vars_ = belief.predict_each(state.candidates)
    scores = np.zeros(means.shape[1], dtype=float)
    for i, p in enumerate(post):
        if i == star or p <= 0:
            continue
        denom = np.clip(vars_[i] + vars_[star], 1e-12, None)
        scores += p * (means[i] - means[star]) ** 2 / denom
    return scores
