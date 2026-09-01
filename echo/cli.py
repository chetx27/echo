"""Command-line interface: python -m echo <run|compare|analyze|bench|list|report>.

The Unix command `echo` is a shell builtin. Use `python -m echo` or `echolab`.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from echo.environments import available_environments
from echo.experiments.compare import analyze_run, compare, run_one
from echo.policies import available_algorithms
from echo.utils.io import ExperimentConfig, load_config, save_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m echo",
        description="ECHO: sequential experiment selection (research laboratory).",
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
    p_cmp.add_argument("--jobs", type=int, default=1, help="Parallel workers (1 = in-process).")
    p_cmp.add_argument(
        "--no-resume",
        action="store_true",
        help="Re-run even if a matching trajectory already exists.",
    )

    p_an = sub.add_parser("analyze", help="Summarize a completed run directory.")
    p_an.add_argument("--run", required=True, help="Path to results/<name>/")

    p_rep = sub.add_parser("report", help="Write markdown from a run summary.json.")
    p_rep.add_argument("--run", required=True, help="Path to results/<name>/")
    p_rep.add_argument("--out", default=None, help="Output .md path (default: <run>/report.md).")

    sub.add_parser("bench", help="List local ECHO-Bench tasks (not a published benchmark).")

    p_list = sub.add_parser("list", help="List environments, algorithms, or tasks.")
    p_list.add_argument(
        "what",
        nargs="?",
        default="all",
        choices=["all", "environments", "algorithms", "tasks"],
    )
    p_list.add_argument("--plugin", default=None, help="Optional plugin file to import first.")

    args = parser.parse_args(argv)

    if args.command == "analyze":
        analyze_run(Path(args.run))
        return 0

    if args.command == "report":
        from echo.evaluation.report import write_markdown_report
        from echo.utils.io import load_json

        run_dir = Path(args.run)
        summary = load_json(run_dir / "summary.json")
        out = Path(args.out) if args.out else run_dir / "report.md"
        write_markdown_report(summary, out)
        print(f"wrote {out}")
        return 0

    if args.command == "bench":
        _print_tasks()
        return 0

    if args.command == "list":
        if args.plugin:
            from echo.plugins import load_plugin

            load_plugin(args.plugin)
        _print_list(args.what)
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
        compare(config, n_jobs=int(args.jobs), resume=not args.no_resume)
        analyze_run(Path(config.output_dir) / config.name)
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


def _print_tasks() -> None:
    from echo.bench import available_tasks, get_task

    print(f"{'task':<24}{'environment':<24}{'metric':<32}config")
    for name in available_tasks():
        task = get_task(name)
        print(
            f"{task.name:<24}{task.environment:<24}"
            f"{task.primary_metric:<32}{task.config_path}"
        )


def _print_list(what: str) -> None:
    if what in ("all", "environments"):
        print("environments:")
        for name in available_environments():
            print(f"  {name}")
    if what in ("all", "algorithms"):
        print("algorithms:")
        for name in available_algorithms():
            print(f"  {name}")
    if what in ("all", "tasks"):
        print("tasks:")
        _print_tasks()


def _add_shared(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", default=None, help="YAML config path.")
    parser.add_argument("--environment", default=None, help="Environment name (built-in or plugin).")
    parser.add_argument("--budget", type=int, default=None)
    parser.add_argument("--seeds", type=int, default=None, help="Number of seeds.")
    parser.add_argument("--n-candidates", type=int, default=None)
    parser.add_argument("--noise", type=float, default=None)
    parser.add_argument("--name", default=None, help="Result directory name.")
    parser.add_argument("--plugin", default=None, help="Python file that registers custom worlds/policies.")


def _config_from_args(args: argparse.Namespace) -> ExperimentConfig:
    config = load_config(args.config) if args.config else ExperimentConfig()
    if getattr(args, "plugin", None):
        from echo.plugins import load_plugin

        load_plugin(args.plugin)
        config.plugin = args.plugin
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
