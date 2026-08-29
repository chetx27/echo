#!/usr/bin/env python3
"""Budget sweep over the nonlinear world.

The YAML default is a cheap check. Override --budget and --name for each B.
Do not treat a 5-seed sweep as a paper result.
"""

from __future__ import annotations

import sys

from echo.cli import main

BUDGETS = (8, 12, 20, 40)


def run() -> int:
    argv = sys.argv[1:]
    if argv:
        return main(["compare", "--config", "configs/budget_sweep.yaml", *argv])
    status = 0
    for budget in BUDGETS:
        name = f"budget_sweep_B{budget}"
        code = main(
            [
                "compare",
                "--config",
                "configs/budget_sweep.yaml",
                "--budget",
                str(budget),
                "--name",
                name,
            ]
        )
        if code:
            status = code
    return status


if __name__ == "__main__":
    raise SystemExit(run())
