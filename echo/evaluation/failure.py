from __future__ import annotations

from typing import Any, Dict, List, Optional


def describe_failure(
    echo_metrics: Dict[str, float],
    baseline_metrics: Dict[str, float],
    baseline_name: str,
    hidden: Dict[str, Any],
    sequence: List[dict],
) -> str:
    """Short, non-marketing description of why a run looks like a failure."""
    echo_rmse = echo_metrics.get("function_recovery_rmse", float("nan"))
    base_rmse = baseline_metrics.get("function_recovery_rmse", float("nan"))
    echo_ent = echo_metrics.get("probe_entropy", float("nan"))
    base_ent = baseline_metrics.get("probe_entropy", float("nan"))
    notes = []
    if echo_rmse > base_rmse:
        notes.append(
            f"ECHO V0 ended with higher function RMSE ({echo_rmse:.4f}) than "
            f"{baseline_name} ({base_rmse:.4f})."
        )
    echo_p = echo_metrics.get("correct_hypothesis_prob", float("nan"))
    base_p = baseline_metrics.get("correct_hypothesis_prob", float("nan"))
    if echo_p == echo_p and base_p == base_p and echo_p < base_p:
        notes.append(
            f"Primary method ended with lower P(true H) ({echo_p:.3f}) than "
            f"{baseline_name} ({base_p:.3f})."
        )
    xs = [step["x"] for step in sequence]
    if xs:
        import numpy as np

        X = np.asarray(xs, dtype=float)
        spread = float(np.mean(np.std(X, axis=0)))
        if spread < 0.3:
            notes.append(
                "Selected locations had low coordinate-wise spread; "
                "the policy may have concentrated in one region of the domain."
            )
    if not notes:
        notes.append("ECHO underperformed on the recorded metric without a simple geometric signature.")
    formula = hidden.get("formula", "unknown hidden law")
    notes.append(f"Hidden law for evaluation: {formula}.")
    return " ".join(notes)


def should_record_failure(
    echo_final: Dict[str, float],
    other_final: Dict[str, float],
    metric: str = "function_recovery_rmse",
    higher_is_better: bool = False,
) -> bool:
    a = echo_final.get(metric, float("nan"))
    b = other_final.get(metric, float("nan"))
    if a != a or b != b:  # NaN
        return False
    if higher_is_better:
        return a < b - 1e-12
    return a > b + 1e-12
