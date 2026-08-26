#!/usr/bin/env python3
"""Regenerate figures and print the statistical summary for a run directory."""

import argparse

from echo.experiments.compare import analyze_run


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", default="results/first_experiment")
    args = parser.parse_args()
    analyze_run(args.run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
