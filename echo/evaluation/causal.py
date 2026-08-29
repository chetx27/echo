"""Evaluator-only linear-Gaussian parent recovery and structural Hamming distance.

For each node, every parent set among the other nodes is scored with a
Gaussian BIC. The selected parent sets are compared to the hidden graph.

This is not PC, FCI, or a new causal-discovery algorithm. It is a small
exhaustive score used so that sequential designs can be compared on SHD.
Cycles are possible; SHD is still defined.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Iterable, Mapping, Sequence, Set

import numpy as np

NODES = ("A", "B", "C", "D")


def _gaussian_bic(y: np.ndarray, X: np.ndarray) -> float:
    n = len(y)
    if n < 3:
        return -np.inf
    if X.size == 0:
        resid = y - float(np.mean(y))
        k = 2.0  # mean and variance
    else:
        design = np.column_stack([np.ones(n), X])
        beta, *_ = np.linalg.lstsq(design, y, rcond=None)
        resid = y - design @ beta
        k = float(design.shape[1] + 1)  # coefficients + variance
    sigma2 = float(np.mean(resid**2)) + 1e-12
    ll = -0.5 * n * (np.log(2.0 * np.pi * sigma2) + 1.0)
    return float(ll - 0.5 * k * np.log(n))


def recover_parents_bic(
    observations: Sequence[Mapping[str, float]],
    nodes: Sequence[str] = NODES,
    intervened: Sequence[str] = (),
) -> Dict[str, Set[str]]:
    """Score-based parent search.

    Intervened nodes are given empty parent sets because the evaluator
    knows the experimental protocol (hard do() on those variables).
    """
    if len(observations) < 6:
        return {node: set() for node in nodes}
    data = {node: np.asarray([row[node] for row in observations], dtype=float) for node in nodes}
    parents: Dict[str, Set[str]] = {}
    intervened_set = set(intervened)
    for node in nodes:
        if node in intervened_set:
            parents[node] = set()
            continue
        y = data[node]
        candidates = [o for o in nodes if o != node]
        best_score = -np.inf
        best: Set[str] = set()
        for k in range(0, len(candidates) + 1):
            for subset in combinations(candidates, k):
                if subset:
                    X = np.column_stack([data[p] for p in subset])
                else:
                    X = np.zeros((len(y), 0))
                score = _gaussian_bic(y, X)
                if score > best_score:
                    best_score = score
                    best = set(subset)
        parents[node] = best
    return parents


def structural_hamming_distance(
    predicted: Mapping[str, Iterable[str]],
    truth: Mapping[str, Iterable[str]],
) -> float:
    """Directed SHD: extra + missing + reversed (a reverse counts once)."""
    pred_edges = {(p, c) for c, parents in predicted.items() for p in parents}
    true_edges = {(p, c) for c, parents in truth.items() for p in parents}
    reversed_pairs = set()
    for a, b in pred_edges:
        if (b, a) in true_edges and (a, b) not in true_edges:
            reversed_pairs.add(frozenset((a, b)))
    used_pred = {(a, b) for a, b in pred_edges if frozenset((a, b)) in reversed_pairs}
    used_true = {(b, a) for a, b in used_pred}
    remaining_pred = pred_edges - used_pred
    remaining_true = true_edges - used_true
    extra = len(remaining_pred - remaining_true)
    missing = len(remaining_true - remaining_pred)
    return float(extra + missing + len(reversed_pairs))


def parent_set_f1(
    predicted: Mapping[str, Iterable[str]],
    truth: Mapping[str, Iterable[str]],
) -> float:
    pred = {(p, c) for c, parents in predicted.items() for p in parents}
    true = {(p, c) for c, parents in truth.items() for p in parents}
    if not pred and not true:
        return 1.0
    if not pred or not true:
        return 0.0
    tp = len(pred & true)
    prec = tp / len(pred)
    rec = tp / len(true)
    if prec + rec == 0:
        return 0.0
    return float(2.0 * prec * rec / (prec + rec))
