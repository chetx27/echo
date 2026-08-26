from __future__ import annotations

from dataclasses import dataclass, fields

from echo.policies.state import DecisionState


def test_decision_state_has_no_hidden_law_fields() -> None:
    names = {f.name for f in fields(DecisionState)}
    forbidden = {"theta", "true_fn", "formula", "f_test", "hidden", "ground_truth"}
    assert names.isdisjoint(forbidden)
