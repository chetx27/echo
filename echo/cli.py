"""Command-line interface: python -m echo <run|compare|analyze>.

The Unix command `echo` is a shell builtin. Use `python -m echo` or `echolab`.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from echo.environments import available_environments
from echo.experiments.compare import analyze_run, compare, run_one
from echo.utils.io import ExperimentConfig, load_config, save_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m echo",
        description="ECHO: sequential experiment selection (research prototype).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="Run one algorithm on one environment.")
    _add_shared(p_run)
    p_run.add_argument("--algorithm", default="echo_v0")
    p_run.add_argument("--seed", type=int, default=0)

    p_cmp = sub.add_parser("compare", help="Compare algorithms across seeds.")
    _add_shared(p_cmp)
    p_cmp.add_argument(
        "--algorithms",
        nargs="+",
        default=None,
        help="Override config algorithms.",
    )

    p_an = sub.add_parser("analyze", help="Summarize a completed run directory.")
    p_an.add_argument("--run", required=True, help="Path to results/<name>/")

    args = parser.parse_args(argv)

    if args.command == "analyze":
        analyze_run(Path(args.run))
        return 0

    config = _config_from_args(args)
    if args.command == "run":
        result = run_one(config, args.algorithm, args.seed)
        out = Path(config.output_dir) / config.name / "runs" / f"{result.run_id}.json"
        save_json(out, result.to_dict())
        print(f"wrote {out}")
        print("final:", {k: round(v, 4) if isinstance(v, float) else v for k, v in result.final_metrics.items()})
        return 0

    if args.command == "compare":
        if args.algorithms:
            config.algorithms = list(args.algorithms)
        compare(config)
        analyze_run(Path(config.output_dir) / config.name)
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


def _add_shared(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", default=None, help="YAML config path.")
    parser.add_argument("--environment", default=None, choices=available_environments())
    parser.add_argument("--budget", type=int, default=None)
    parser.add_argument("--seeds", type=int, default=None, help="Number of seeds.")
    parser.add_argument("--n-candidates", type=int, default=None)
    parser.add_argument("--noise", type=float, default=None)
    parser.add_argument("--name", default=None, help="Result directory name.")


def _config_from_args(args: argparse.Namespace) -> ExperimentConfig:
    config = load_config(args.config) if args.config else ExperimentConfig()
    if args.environment is not None:
        config.environment = args.environment
    if args.budget is not None:
        config.budget = args.budget
    if args.seeds is not None:
        config.n_seeds = args.seeds
    if args.n_candidates is not None:
        config.n_candidates = args.n_candidates
    if args.noise is not None:
        config.noise = args.noise
    if args.name is not None:
        config.name = args.name
    elif args.config is None:
        config.name = "adhoc"
    return config
