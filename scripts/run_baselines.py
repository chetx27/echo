#!/usr/bin/env python3
"""Compare standard acquisition baselines on a configured experiment."""

from echo.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["compare", "--config", "configs/first_experiment.yaml"]))
