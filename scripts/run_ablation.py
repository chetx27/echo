#!/usr/bin/env python3
from echo.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["compare", "--config", "configs/ablation_hypotheses.yaml"]))
