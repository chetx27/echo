from __future__ import annotations

from typing import Dict, List

import numpy as np
from scipy import stats


def _ci95(values: np.ndarray) -> tuple[float, float, float, float, float]:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) == 0:
        return (float("nan"),) * 5
    mean = float(np.mean(v))
    median = float(np.median(v))
    std = float(np.std(v, ddof=1)) if len(v) > 1 else 0.0
    sem = std / np.sqrt(len(v)) if len(v) > 0 else float("nan")
    half = 1.96 * sem if np.isfinite(sem) else float("nan")
    return mean, median, std, mean - half, mean + half


def summarize_matrix(matrix: np.ndarray) -> Dict[str, List[float]]:
    """matrix: (n_seeds, n_steps)."""
    means, medians, stds, lows, highs = [], [], [], [], []
    for t in range(matrix.shape[1]):
        mean, median, std, lo, hi = _ci95(matrix[:, t])
        means.append(mean)
        medians.append(median)
        stds.append(std)
        lows.append(lo)
        highs.append(hi)
    return {
        "mean": means,
        "median": medians,
        "std": stds,
        "ci_low": lows,
        "ci_high": highs,
    }


def pairwise_final(a: np.ndarray, b: np.ndarray) -> dict:
    """Compare two seed-aligned final-metric vectors. Lower is better."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    mask = np.isfinite(a) & np.isfinite(b)
    a, b = a[mask], b[mask]
    if len(a) < 2:
        return {
            "n": int(len(a)),
            "mean_diff": float("nan"),
            "cohens_d": float("nan"),
            "wilcoxon_p": float("nan"),
            "ttest_p": float("nan"),
            "a_wins": 0,
            "b_wins": 0,
            "ties": 0,
        }
    diff = a - b
    mean_diff = float(np.mean(diff))
    std_diff = float(np.std(diff, ddof=1))
    cohens_d = mean_diff / std_diff if std_diff > 1e-15 else 0.0
    try:
        w = stats.wilcoxon(a, b, zero_method="wilcox", alternative="two-sided")
        wilcoxon_p = float(w.pvalue)
    except ValueError:
        wilcoxon_p = float("nan")
    t = stats.ttest_rel(a, b)
    a_wins = int(np.sum(a < b - 1e-12))
    b_wins = int(np.sum(b < a - 1e-12))
    ties = int(len(a) - a_wins - b_wins)
    return {
        "n": int(len(a)),
        "mean_diff": mean_diff,
        "cohens_d": float(cohens_d),
        "wilcoxon_p": wilcoxon_p,
        "ttest_p": float(t.pvalue),
        "a_wins": a_wins,
        "b_wins": b_wins,
        "ties": ties,
    }
