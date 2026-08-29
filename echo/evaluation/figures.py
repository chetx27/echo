from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np


ALGORITHM_STYLE = {
    "random": {"color": "#4d4d4d", "label": "Random"},
    "greedy": {"color": "#999999", "label": "Greedy"},
    "uncertainty": {"color": "#0072B2", "label": "Uncertainty"},
    "diversity": {"color": "#56B4E9", "label": "Diversity"},
    "expected_improvement": {"color": "#E69F00", "label": "Expected Improvement"},
    "ucb": {"color": "#F0E442", "label": "GP-UCB"},
    "thompson": {"color": "#CC79A7", "label": "Thompson (mean-field)"},
    "information_gain": {"color": "#009E73", "label": "Local information gain"},
    "echo_v0": {"color": "#D55E00", "label": "ECHO V0"},
    "echo_no_hypothesis": {"color": "#D55E00", "label": "ECHO no-hypothesis"},
    "echo_information_only": {"color": "#009E73", "label": "ECHO information-only"},
    "echo_hypothesis": {"color": "#882255", "label": "ECHO hypothesis"},
    "echo_falsify": {"color": "#AA4499", "label": "ECHO falsify"},
    "echo_hypothesis_cost": {"color": "#661100", "label": "ECHO hypothesis/cost"},
    "echo_hypothesis_penalty": {"color": "#332288", "label": "ECHO hypothesis−λ cost"},
    "echo_no_sequential": {"color": "#888888", "label": "ECHO open-loop"},
}

METRIC_TITLES = {
    "function_recovery_rmse": "Function recovery RMSE (lower is better)",
    "prediction_error": "Prediction error RMSE (lower is better)",
    "parameter_recovery_rmse": "Oracle parameter RMSE (lower is better)",
    "probe_entropy": "Probe-set posterior entropy (lower is better)",
    "mean_predictive_std": "Mean predictive std",
    "hypothesis_entropy": "Hypothesis posterior entropy (lower is better)",
    "correct_hypothesis_prob": "P(true hypothesis | data) (higher is better)",
    "hypothesis_identified": "Fraction identified (P(true H) ≥ 0.9)",
    "leading_hypothesis_correct": "Leading hypothesis is true",
    "structural_hamming_distance": "Structural Hamming distance (lower is better)",
    "parent_set_f1": "Parent-set F1 (higher is better)",
    "region_coverage": "Fraction of mechanism regions visited",
    "mean_region_rmse": "Mean per-region RMSE (lower is better)",
    "anomaly_hit_rate": "Fraction of queries in the anomaly box",
    "anomaly_recall": "Anomaly-box recall (higher is better)",
    "total_cost": "Cumulative experimental cost",
    "cost_efficiency_rmse": "Function RMSE / cumulative cost",
    "discovery_efficiency_rmse": "Function RMSE / number of experiments",
}


def plot_discovery_curves(
    summary: dict,
    metric_names: List[str],
    output_path: Path,
) -> None:
    n = len(metric_names)
    cols = 2
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(10.5, 3.6 * rows), squeeze=False)
    steps = np.asarray(summary["steps"], dtype=float)
    metrics = summary["metrics"]
    algorithms = summary["algorithms"]

    for i, metric in enumerate(metric_names):
        ax = axes[i // cols][i % cols]
        for algo in algorithms:
            style = ALGORITHM_STYLE.get(algo, {"color": "C0", "label": algo})
            series = metrics[metric][algo]
            mean = np.asarray(series["mean"], dtype=float)
            lo = np.asarray(series["ci_low"], dtype=float)
            hi = np.asarray(series["ci_high"], dtype=float)
            ax.plot(steps, mean, color=style["color"], label=style["label"], lw=2)
            ax.fill_between(steps, lo, hi, color=style["color"], alpha=0.18, linewidth=0)
        ax.set_xlabel("Number of experiments")
        ax.set_ylabel(METRIC_TITLES.get(metric, metric))
        ax.set_title(METRIC_TITLES.get(metric, metric), fontsize=10)
        ax.grid(True, alpha=0.3)
        if i == 0:
            ax.legend(frameon=False, fontsize=8)

    for j in range(n, rows * cols):
        axes[j // cols][j % cols].axis("off")

    fig.suptitle(
        f"{summary.get('environment', '')}  |  "
        f"budget {summary.get('budget', '')}  |  "
        f"{summary.get('n_seeds', '')} seeds",
        fontsize=11,
    )
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    fig.savefig(output_path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def plot_final_bars(summary: dict, metric: str, output_path: Path) -> None:
    algorithms = summary["algorithms"]
    final = summary["final"][metric]
    means = [final[a]["mean"] for a in algorithms]
    lows = [final[a]["ci_low"] for a in algorithms]
    highs = [final[a]["ci_high"] for a in algorithms]
    colors = [ALGORITHM_STYLE.get(a, {}).get("color", "C0") for a in algorithms]
    labels = [ALGORITHM_STYLE.get(a, {}).get("label", a) for a in algorithms]
    yerr = np.vstack([np.asarray(means) - np.asarray(lows), np.asarray(highs) - np.asarray(means)])
    fig, ax = plt.subplots(figsize=(8, 4.2))
    x = np.arange(len(algorithms))
    ax.bar(x, means, yerr=yerr, color=colors, capsize=4, error_kw={"linewidth": 1})
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylabel(METRIC_TITLES.get(metric, metric))
    ax.set_title(f"Final {metric} (mean ± 95% CI)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    fig.savefig(output_path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
