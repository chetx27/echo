#!/usr/bin/env python3
"""Compare policies on the unseen functional form (experiment 5)."""

from echo.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["compare", "--config", "configs/experiment5_generalization.yaml"]))
