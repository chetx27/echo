from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from echo.environments import make_environment
from echo.evaluation.failure import describe_failure, should_record_failure
from echo.evaluation.figures import plot_discovery_curves, plot_final_bars
from echo.evaluation.statistics import pairwise_final, summarize_matrix
from echo.experiments.runner import RunResult, run_sequential
from echo.policies import make_policy
from echo.utils.io import ExperimentConfig, load_json, save_json


METRIC_KEYS = [
    "function_recovery_rmse",
    "prediction_error",
    "parameter_recovery_rmse",
    "probe_entropy",
    "mean_predictive_std",
    "hypothesis_entropy",
    "correct_hypothesis_prob",
    "hypothesis_identified",
    "leading_hypothesis_correct",
    "structural_hamming_distance",
    "parent_set_f1",
    "region_coverage",
    "mean_region_rmse",
    "anomaly_hit_rate",
    "anomaly_recall",
    "total_cost",
    "cost_efficiency_rmse",
    "discovery_efficiency_rmse",
]


def _env_kwargs(config: ExperimentConfig) -> dict:
    return {
        "n_candidates": config.n_candidates,
        "n_test": config.n_test,
        "noise_std": config.noise,
        "low": config.domain_low,
        "high": config.domain_high,
        "cost_mode": config.cost_mode,
    }


def run_one(config: ExperimentConfig, algorithm: str, seed: int) -> RunResult:
    env = make_environment(config.environment, **_env_kwargs(config))
    policy = make_policy(algorithm)
    return run_sequential(env, policy, config, seed)


def _run_job(item: dict) -> dict:
    """Picklable worker for --jobs > 1."""
    raw = dict(item["config"])
    known = {k: v for k, v in raw.items() if k in ExperimentConfig.__dataclass_fields__}
    cfg = ExperimentConfig(**known)
    if cfg.plugin:
        from echo.plugins import load_plugin

        load_plugin(cfg.plugin)
    result = run_one(cfg, item["algorithm"], int(item["seed"]))
    return result.to_dict()


def _cached_run(runs_dir: Path, algorithm: str, seed: int, config_hash: str) -> Optional[RunResult]:
    matches = sorted(runs_dir.glob(f"*_{algorithm}_seed{seed}_{config_hash}.json"))
    if not matches:
        return None
    return RunResult.from_dict(load_json(matches[0]))


def _figure_dir(config: ExperimentConfig, run_dir: Path) -> Path:
    if Path(config.output_dir) == Path("results"):
        return Path("figures") / config.name
    return Path(run_dir) / "figures"


def _finite_metric_keys(summary_final: dict) -> List[str]:
    keys = []
    for metric in METRIC_KEYS:
        block = summary_final.get(metric) or {}
        if any(
            v is not None and v == v
            for stats in block.values()
            for v in (stats.get("values") or [stats.get("mean")])
        ):
            keys.append(metric)
    return keys


def compare(
    config: ExperimentConfig,
    run_dir: Path | None = None,
    *,
    n_jobs: int = 1,
    resume: bool = True,
) -> dict:
    run_dir = Path(run_dir) if run_dir is not None else Path(config.output_dir) / config.name
    runs_dir = run_dir / "runs"
    fail_dir = run_dir / "failures"
    runs_dir.mkdir(parents=True, exist_ok=True)
    fail_dir.mkdir(parents=True, exist_ok=True)

    seeds = config.seed_list()
    cfg_hash = config.config_hash()
    jobs: List[Tuple[str, int]] = [(algo, seed) for seed in seeds for algo in config.algorithms]
    loaded: Dict[Tuple[int, str], RunResult] = {}
    pending: List[Tuple[str, int]] = []

    for algo, seed in jobs:
        cached = _cached_run(runs_dir, algo, seed, cfg_hash) if resume else None
        if cached is not None:
            loaded[(seed, algo)] = cached
            print(f"[cache] {algo} seed={seed}", flush=True)
        else:
            pending.append((algo, seed))

    total = len(jobs)
    done = len(loaded)

    def _store(result: RunResult) -> None:
        save_json(runs_dir / f"{result.run_id}.json", result.to_dict())
        loaded[(result.seed, result.algorithm)] = result

    if pending and n_jobs > 1:
        payloads = [
            {"config": config.to_dict(), "algorithm": algo, "seed": seed}
            for algo, seed in pending
        ]
        with ProcessPoolExecutor(max_workers=int(n_jobs)) as pool:
            futures = {pool.submit(_run_job, item): item for item in payloads}
            for fut in as_completed(futures):
                item = futures[fut]
                result = RunResult.from_dict(fut.result())
                _store(result)
                done += 1
                print(
                    f"[{done}/{total}] {result.algorithm} seed={result.seed} "
                    f"function_rmse={result.final_metrics.get('function_recovery_rmse', float('nan')):.4f} "
                    f"P(H*)={result.final_metrics.get('correct_hypothesis_prob', float('nan')):.3f}",
                    flush=True,
                )
    else:
        for algo, seed in pending:
            result = run_one(config, algo, seed)
            _store(result)
            done += 1
            print(
                f"[{done}/{total}] {algo} seed={seed} "
                f"function_rmse={result.final_metrics.get('function_recovery_rmse', float('nan')):.4f} "
                f"P(H*)={result.final_metrics.get('correct_hypothesis_prob', float('nan')):.3f}",
                flush=True,
            )

    n_steps = config.budget - config.n_init + 1
    series: Dict[str, Dict[str, np.ndarray]] = {
        metric: {algo: np.full((len(seeds), n_steps), np.nan) for algo in config.algorithms}
        for metric in METRIC_KEYS
    }
    finals: Dict[str, Dict[str, List[float]]] = {
        metric: {algo: [] for algo in config.algorithms} for metric in METRIC_KEYS
    }
    echo_runs = {}
    other_runs = defaultdict(dict)

    for s_i, seed in enumerate(seeds):
        for algo in config.algorithms:
            result = loaded[(seed, algo)]
            for metric in METRIC_KEYS:
                values = [m.get(metric, float("nan")) for m in result.metrics]
                if len(values) != n_steps:
                    padded = np.full(n_steps, np.nan)
                    padded[: min(len(values), n_steps)] = values[:n_steps]
                    series[metric][algo][s_i, :] = padded
                else:
                    series[metric][algo][s_i, :] = np.asarray(values, dtype=float)
                finals[metric][algo].append(result.final_metrics.get(metric, float("nan")))
            if algo == config.primary_algorithm:
                echo_runs[seed] = result
            else:
                other_runs[seed][algo] = result

    summary_metrics = {
        metric: {algo: summarize_matrix(series[metric][algo]) for algo in config.algorithms}
        for metric in METRIC_KEYS
    }
    summary_final = {}
    for metric in METRIC_KEYS:
        summary_final[metric] = {}
        for algo in config.algorithms:
            vals = np.asarray(finals[metric][algo], dtype=float)
            finite = vals[np.isfinite(vals)]
            mean = float(np.mean(finite)) if len(finite) else float("nan")
            median = float(np.median(finite)) if len(finite) else float("nan")
            std = float(np.std(finite, ddof=1)) if len(finite) > 1 else 0.0
            sem = std / np.sqrt(len(finite)) if len(finite) else float("nan")
            summary_final[metric][algo] = {
                "mean": mean,
                "median": median,
                "std": std,
                "ci_low": mean - 1.96 * sem if np.isfinite(sem) else float("nan"),
                "ci_high": mean + 1.96 * sem if np.isfinite(sem) else float("nan"),
                "values": [float(v) if np.isfinite(v) else None for v in vals],
            }

    pairwise = {}
    primary = config.primary_algorithm
    if primary in config.algorithms:
        for other in config.algorithms:
            if other == primary:
                continue
            pairwise[f"{primary}_vs_{other}"] = {}
            for metric in METRIC_KEYS:
                a = np.asarray(finals[metric][primary], dtype=float)
                b = np.asarray(finals[metric][other], dtype=float)
                stats = pairwise_final(a, b)
                stats["interpretation"] = (
                    f"mean_diff = {primary} - {other}; "
                    "negative means the primary method is better if lower-is-better."
                )
                pairwise[f"{primary}_vs_{other}"][metric] = stats

    failures = []
    comparator = config.comparator if getattr(config, "comparator", None) else (
        "uncertainty" if "uncertainty" in config.algorithms else None
    )
    if echo_runs and comparator:
        for seed, echo_result in echo_runs.items():
            other = other_runs.get(seed, {}).get(comparator)
            if other is None:
                continue
            if should_record_failure(
                echo_result.final_metrics,
                other.final_metrics,
                metric=config.failure_metric,
                higher_is_better=config.failure_higher_is_better,
            ):
                env = make_environment(config.environment, **_env_kwargs(config))
                env.reset(seed)
                hidden = env.get_hidden_state_for_evaluation()
                record = {
                    "seed": seed,
                    "environment": config.environment,
                    "comparator": comparator,
                    "metric": config.failure_metric,
                    "echo_final": echo_result.final_metrics,
                    "comparator_final": other.final_metrics,
                    "echo_sequence": echo_result.sequence,
                    "note": describe_failure(
                        echo_result.final_metrics,
                        other.final_metrics,
                        comparator,
                        hidden,
                        echo_result.sequence,
                    ),
                }
                save_json(fail_dir / f"seed_{seed}.json", record)
                failures.append(record)

    steps = list(range(config.n_init, config.budget + 1))
    active = _finite_metric_keys(summary_final)
    summary = {
        "name": config.name,
        "config": config.to_dict(),
        "config_hash": config.config_hash(),
        "environment": config.environment,
        "algorithms": config.algorithms,
        "seeds": seeds,
        "n_seeds": len(seeds),
        "budget": config.budget,
        "n_init": config.n_init,
        "steps": steps,
        "metrics": summary_metrics,
        "final": summary_final,
        "pairwise": pairwise,
        "n_failures_vs_comparator": len(failures),
        "failure_seeds": [f["seed"] for f in failures],
        "comparator": comparator,
        "primary_algorithm": config.primary_algorithm,
        "plot_metrics": list(config.plot_metrics),
        "failure_metric": config.failure_metric,
        "failure_higher_is_better": bool(config.failure_higher_is_better),
        "active_metrics": active,
        "question": config.question,
    }
    save_json(run_dir / "summary.json", summary)
    _write_csv(run_dir / "metrics.csv", summary)
    _write_latex(run_dir / "table.tex", summary)
    fig_dir = _figure_dir(config, run_dir)
    plot_metrics = list(config.plot_metrics)
    plot_discovery_curves(summary, plot_metrics, fig_dir / "discovery_curves.png")
    plot_final_bars(summary, plot_metrics[0], fig_dir / "final_primary.png")
    if len(plot_metrics) > 1:
        plot_final_bars(summary, plot_metrics[1], fig_dir / f"final_{plot_metrics[1]}.png")
    from echo.evaluation.report import write_markdown_report

    write_markdown_report(summary, run_dir / "report.md")
    return summary


def _write_csv(path: Path, summary: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    active = summary.get("active_metrics") or list(summary["final"])
    lines = ["metric,algorithm,mean,median,std,ci_low,ci_high"]
    for metric in active:
        algos = summary["final"].get(metric) or {}
        for algo, stats in algos.items():
            lines.append(
                f"{metric},{algo},{stats['mean']},{stats['median']},"
                f"{stats['std']},{stats['ci_low']},{stats['ci_high']}"
            )
    path.write_text("\n".join(lines) + "\n")


def _write_latex(path: Path, summary: dict) -> None:
    metric = (summary.get("plot_metrics") or ["function_recovery_rmse"])[0]
    if metric not in summary["final"]:
        metric = "function_recovery_rmse"
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\hline",
        r"Algorithm & Mean & Median & Std & 95\% CI \\",
        r"\hline",
    ]
    for algo, stats in summary["final"][metric].items():
        name = algo.replace("_", r"\_")
        lines.append(
            f"{name} & {stats['mean']:.3f} & {stats['median']:.3f} & "
            f"{stats['std']:.3f} & [{stats['ci_low']:.3f}, {stats['ci_high']:.3f}] \\\\"
        )
    lines.extend([r"\hline", r"\end{tabular}", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def analyze_run(run_dir: Path, write_report: bool = True) -> dict:
    summary = load_json(Path(run_dir) / "summary.json")
    print(f"Run: {summary['name']}  hash={summary['config_hash']}")
    print(f"Environment: {summary['environment']}  seeds={summary['n_seeds']}")
    print()
    preferred = list(summary.get("plot_metrics") or [])
    fallback = ["function_recovery_rmse", "correct_hypothesis_prob", "hypothesis_entropy"]
    keys = [k for k in preferred + fallback if k in summary["final"]]
    seen = []
    for k in keys:
        if k not in seen:
            seen.append(k)
    keys = seen[:4] or ["function_recovery_rmse"]
    header = f"{'algorithm':<24}" + "".join(f"{k[:12]:>14}" for k in keys)
    print(header)
    for algo in summary["algorithms"]:
        row = f"{algo:<24}"
        for k in keys:
            row += f"{summary['final'][k][algo]['mean']:14.4f}"
        print(row)
    if summary.get("pairwise"):
        print("\nPairwise vs primary (see interpretation in JSON):")
        metric = summary.get("failure_metric", "function_recovery_rmse")
        higher = bool(summary.get("failure_higher_is_better"))
        for key, block in summary["pairwise"].items():
            if metric not in block:
                metric = "function_recovery_rmse"
            s = block[metric]
            if higher:
                wins = f"primary_higher_wins {s['b_wins']}/{s['n']}"
            else:
                wins = f"primary_lower_wins {s['a_wins']}/{s['n']}"
            print(
                f"  {key} [{metric}]: mean_diff={s['mean_diff']:.4f}  d={s['cohens_d']:.3f}  "
                f"wilcoxon_p={s['wilcoxon_p']:.4g}  {wins}"
            )
    print(f"\nFailure reports vs {summary.get('comparator')}: {summary.get('n_failures_vs_comparator')}")
    cfg = summary.get("config") or {}
    output_dir = cfg.get("output_dir", "results")
    fig_dir = Path("figures") / summary["name"] if Path(output_dir) == Path("results") else Path(run_dir) / "figures"
    plot_metrics = summary.get("plot_metrics") or [
        "function_recovery_rmse",
        "parameter_recovery_rmse",
        "probe_entropy",
        "mean_predictive_std",
    ]
    plot_discovery_curves(summary, plot_metrics, fig_dir / "discovery_curves.png")
    plot_final_bars(summary, plot_metrics[0], fig_dir / "final_primary.png")
    if write_report:
        from echo.evaluation.report import write_markdown_report

        write_markdown_report(summary, Path(run_dir) / "report.md")
    return summary
