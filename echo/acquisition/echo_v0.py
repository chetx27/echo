"""ECHO V0 acquisition: expected knowledge change about the scientific function.

For each candidate x the score is the expected reduction in posterior
entropy of f over a fixed probe set in the experimental domain.

Scientific interpretation
-------------------------
The current scientific belief is the GP posterior over the unknown
response surface. An experiment is valuable insofar as its outcome is
expected to change that belief globally, not merely to have large local
predictive variance or to improve an optimum.

This is not a weighted combination of unrelated terms. It is one
quantity: expected global knowledge change.

Relation to prior work
----------------------
The mathematics is closely related to mutual-information / maximum-entropy
experimental design for GPs (MacKay 1992; Krause, Singh & Guestrin 2008).
ECHO V0 uses that acquisition inside a discovery-evaluation protocol
(mechanism recovery, parameter recovery, multi-metric curves) rather
than treating entropy reduction as the definition of scientific success.
"""

from __future__ import annotations

from echo.acquisition.information_gain import global_information_gain
from echo.policies.state import DecisionState


def echo_v0_score(state: DecisionState):
    return global_information_gain(state)
