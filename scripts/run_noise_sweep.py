#!/usr/bin/env python3
"""Noise sweep over the nonlinear world.

The YAML default is a cheap check (5 seeds). Override --noise and --name
for each σ. Do not treat a 5-seed sweep as a paper result.
"""

from __future__ import annotations

import sys

from echo.cli import main

NOISE_LEVELS = (0.05, 0.1, 0.3, 1.0)


def run() -> int:
    argv = sys.argv[1:]
    if argv:
        return main(["compare", "--config", "configs/noise_sweep.yaml", *argv])
    status = 0
    for noise in NOISE_LEVELS:
        name = f"noise_sweep_sigma{noise}"
        code = main(
            [
                "compare",
                "--config",
                "configs/noise_sweep.yaml",
                "--noise",
                str(noise),
                "--name",
                name,
            ]
        )
        if code:
            status = code
    return status


if __name__ == "__main__":
    raise SystemExit(run())
