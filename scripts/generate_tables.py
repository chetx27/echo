#!/usr/bin/env python3
"""Print the LaTeX table path for a completed run."""

from pathlib import Path


def main() -> None:
    path = Path("results/first_experiment/table.tex")
    if not path.exists():
        raise SystemExit("Run the first experiment before generating tables.")
    print(path.read_text())


if __name__ == "__main__":
    main()
