#!/usr/bin/env python3
"""Run remaining paper configs. Safe to interrupt; compare resumes."""

from __future__ import annotations

import argparse
import os

from echo.cli import main

CONFIGS = [
    "configs/experiment2_hypotheses.yaml",
    "configs/experiment3_falsification.yaml",
    "configs/experiment4_cost.yaml",
    "configs/experiment_causal.yaml",
    "configs/experiment6_multimodal.yaml",
    "configs/experiment7_anomaly.yaml",
    "configs/experiment5_generalization.yaml",
]


def run() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    parser.add_argument("--seeds", type=int, default=None, help="Override n_seeds (pilot).")
    args = parser.parse_args()
    extra = ["--jobs", str(args.jobs)]
    if args.seeds is not None:
        extra.extend(["--seeds", str(args.seeds)])
    for config in CONFIGS:
        print(f"\n=== {config} jobs={args.jobs} ===", flush=True)
        code = main(["compare", "--config", config, *extra])
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
