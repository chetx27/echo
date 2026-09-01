"""ECHO-Bench: a local registry of sequential-discovery tasks.

This is not a published benchmark and not a claim of community adoption.
It exists so experiment configs, metrics, and questions stay in one place.
Leakage rule: policies still never receive ground-truth fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from echo.utils.io import ExperimentConfig, load_config


@dataclass(frozen=True)
class BenchTask:
    name: str
    environment: str
    question: str
    primary_metric: str
    higher_is_better: bool
    config_path: str
    notes: str


_TASKS: dict[str, BenchTask] = {
    "nonlinear_surface": BenchTask(
        name="nonlinear_surface",
        environment="nonlinear",
        question="Which sequential policy recovers a hidden nonlinear surface under budget 20?",
        primary_metric="function_recovery_rmse",
        higher_is_better=False,
        config_path="configs/first_experiment.yaml",
        notes="Phase 1. GP agent is misspecified.",
    ),
    "competing_hypotheses": BenchTask(
        name="competing_hypotheses",
        environment="competing_hypotheses",
        question="Does hypothesis discrimination beat generic uncertainty on P(H_true|D)?",
        primary_metric="correct_hypothesis_prob",
        higher_is_better=True,
        config_path="configs/experiment2_hypotheses.yaml",
        notes="Phase 2. True class is quadratic; agent vocabulary is linear/quadratic/sin.",
    ),
    "falsification": BenchTask(
        name="falsification",
        environment="competing_hypotheses",
        question="Does scoring disagreement with the leading hypothesis identify the true class faster?",
        primary_metric="correct_hypothesis_prob",
        higher_is_better=True,
        config_path="configs/experiment3_falsification.yaml",
        notes="Phase 3. Same world as experiment 2; primary algorithm is echo_falsify.",
    ),
    "cost_aware": BenchTask(
        name="cost_aware",
        environment="competing_hypotheses",
        question="What happens when the most discriminative experiment is not the cheapest?",
        primary_metric="correct_hypothesis_prob",
        higher_is_better=True,
        config_path="configs/experiment4_cost.yaml",
        notes="Heterogeneous x_right costs. Compare raw vs per-cost vs penalized scores.",
    ),
    "causal_roots": BenchTask(
        name="causal_roots",
        environment="causal",
        question="Do sequential designs recover a hidden four-node SCM better than random?",
        primary_metric="structural_hamming_distance",
        higher_is_better=False,
        config_path="configs/experiment_causal.yaml",
        notes="Hard do(A,B) interventions. Graph recovery is evaluator-only BIC.",
    ),
    "multimodal_regions": BenchTask(
        name="multimodal_regions",
        environment="multimodal",
        question="Does a policy visit and reconstruct three distinct mechanisms?",
        primary_metric="mean_region_rmse",
        higher_is_better=False,
        config_path="configs/experiment6_multimodal.yaml",
        notes="Three piecewise mechanisms in x1. Diversity is an extra baseline.",
    ),
    "anomaly_box": BenchTask(
        name="anomaly_box",
        environment="anomaly",
        question="Does sequential design find a structured local violation of a linear law?",
        primary_metric="anomaly_recall",
        higher_is_better=True,
        config_path="configs/experiment7_anomaly.yaml",
        notes="Compact +4 offset box. Primary metric is recall of queries inside the box.",
    ),
    "unseen_form": BenchTask(
        name="unseen_form",
        environment="unseen",
        question="Do the same hand-designed policies keep their ranking on an unused functional form?",
        primary_metric="function_recovery_rmse",
        higher_is_better=False,
        config_path="configs/experiment5_generalization.yaml",
        notes="Not meta-learning. Policies are not trained on other worlds.",
    ),
}


def available_tasks() -> list[str]:
    return sorted(_TASKS)


def get_task(name: str) -> BenchTask:
    if name not in _TASKS:
        known = ", ".join(available_tasks())
        raise ValueError(f"unknown ECHO-Bench task {name!r}; known: {known}")
    return _TASKS[name]


def load_task_config(name: str) -> ExperimentConfig:
    task = get_task(name)
    return load_config(Path(task.config_path))
