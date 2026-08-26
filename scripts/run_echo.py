#!/usr/bin/env python3
"""Run ECHO V0 as part of the first-experiment comparison."""

from echo.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["compare", "--config", "configs/first_experiment.yaml"]))
