from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import numpy as np

from echo.environments import make_environment
from echo.evaluation.failure import describe_failure, should_record_failure
from echo.evaluation.figures import plot_discovery_curves, plot_final_bars
from echo.evaluation.statistics import pairwise_final, summarize_matrix
from echo.experiments.runner import run_sequential
from echo.policies import make_policy
from echo.utils.io import ExperimentConfig, save_json


METRIC_KEYS = [
    "function_recovery_rmse",
    "prediction_error",
    "parameter_recovery_rmse",
    "probe_entropy",
    "mean_predictive_std",
]


def _env_kwargs(config: ExperimentConfig) -> dict:
    return {
        "n_candidates": config.n_candidates,
        "n_test": config.n_test,
        "noise_std": config.noise,
        "low": config.domain_low,
        "high": config.domain_high,
    }


def run_one(config: ExperimentConfig, algorithm: str, seed: int):
    env = make_environment(config.environment, **_env_kwargs(config))
    policy = make_policy(algorithm)
    return run_sequential(env, policy, config, seed)


def compare(config: ExperimentConfig, run_dir: Path | None = None) -> dict:
    run_dir = Path(run_dir) if run_dir is not None else Path(config.output_dir) / config.name
    runs_dir = run_dir / "runs"
    fail_dir = run_dir / "failures"
    runs_dir.mkdir(parents=True, exist_ok=True)
    fail_dir.mkdir(parents=True, exist_ok=True)

    seeds = config.seed_list()
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

    total = len(seeds) * len(config.algorithms)
    done = 0
    for s_i, seed in enumerate(seeds):
        for algo in config.algorithms:
            result = run_one(config, algo, seed)
            save_json(runs_dir / f"{result.run_id}.json", result.to_dict())
            for metric in METRIC_KEYS:
                values = [m[metric] for m in result.metrics]
                series[metric][algo][s_i, :] = np.asarray(values, dtype=float)
                finals[metric][algo].append(result.final_metrics[metric])
            if algo == "echo_v0":
                echo_runs[seed] = result
            else:
                other_runs[seed][algo] = result
            done += 1
            print(
                f"[{done}/{total}] {algo} seed={seed} "
                f"function_rmse={result.final_metrics['function_recovery_rmse']:.4f}",
                flush=True,
            )

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
    if "echo_v0" in config.algorithms:
        for other in config.algorithms:
            if other == "echo_v0":
                continue
            pairwise[f"echo_v0_vs_{other}"] = {}
            for metric in METRIC_KEYS:
                a = np.asarray(finals[metric]["echo_v0"], dtype=float)
                b = np.asarray(finals[metric][other], dtype=float)
                stats = pairwise_final(a, b)
                stats["interpretation"] = (
                    "mean_diff = echo_v0 - "
                    f"{other}; negative means ECHO V0 is better if lower-is-better."
                )
                pairwise[f"echo_v0_vs_{other}"][metric] = stats

    failures = []
    comparator = "uncertainty" if "uncertainty" in config.algorithms else (
        config.algorithms[0] if config.algorithms[0] != "echo_v0" else None
    )
    if echo_runs and comparator:
        for seed, echo_result in echo_runs.items():
            other = other_runs.get(seed, {}).get(comparator)
            if other is None:
                continue
            if should_record_failure(echo_result.final_metrics, other.final_metrics):
                env = make_environment(config.environment, **_env_kwargs(config))
                env.reset(seed)
                hidden = env.get_hidden_state_for_evaluation()
                record = {
                    "seed": seed,
                    "environment": config.environment,
                    "comparator": comparator,
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
    }
    save_json(run_dir / "summary.json", summary)
    _write_csv(run_dir / "metrics.csv", summary)
    _write_latex(run_dir / "table.tex", summary)
    fig_dir = Path("figures") / config.name
    plot_discovery_curves(
        summary,
        [
            "function_recovery_rmse",
            "parameter_recovery_rmse",
            "probe_entropy",
            "mean_predictive_std",
        ],
        fig_dir / "discovery_curves.png",
    )
    plot_final_bars(summary, "function_recovery_rmse", fig_dir / "final_function_rmse.png")
    plot_final_bars(summary, "parameter_recovery_rmse", fig_dir / "final_parameter_rmse.png")
    return summary


def _write_csv(path: Path, summary: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["metric,algorithm,mean,median,std,ci_low,ci_high"]
    for metric, algos in summary["final"].items():
        for algo, stats in algos.items():
            lines.append(
                f"{metric},{algo},{stats['mean']},{stats['median']},"
                f"{stats['std']},{stats['ci_low']},{stats['ci_high']}"
            )
    path.write_text("\n".join(lines) + "\n")


def _write_latex(path: Path, summary: dict) -> None:
    metric = "function_recovery_rmse"
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\hline",
        r"Algorithm & Mean RMSE & Median & Std & 95\% CI \\",
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


def analyze_run(run_dir: Path) -> dict:
    from echo.utils.io import load_json

    summary = load_json(Path(run_dir) / "summary.json")
    print(f"Run: {summary['name']}  hash={summary['config_hash']}")
    print(f"Environment: {summary['environment']}  seeds={summary['n_seeds']}")
    print()
    print(f"{'algorithm':<24} {'fn RMSE':>10} {'param RMSE':>12} {'entropy':>10}")
    for algo in summary["algorithms"]:
        fn = summary["final"]["function_recovery_rmse"][algo]
        pr = summary["final"]["parameter_recovery_rmse"][algo]
        ent = summary["final"]["probe_entropy"][algo]
        print(
            f"{algo:<24} {fn['mean']:10.4f} {pr['mean']:12.4f} {ent['mean']:10.3f}"
        )
    if summary.get("pairwise"):
        print("\nPairwise vs ECHO V0 (function RMSE; negative mean_diff favors ECHO):")
        for key, block in summary["pairwise"].items():
            s = block["function_recovery_rmse"]
            print(
                f"  {key}: mean_diff={s['mean_diff']:.4f}  d={s['cohens_d']:.3f}  "
                f"wilcoxon_p={s['wilcoxon_p']:.4g}  "
                f"ECHO wins {s['a_wins']}/{s['n']}"
            )
    print(f"\nFailure reports vs {summary.get('comparator')}: {summary.get('n_failures_vs_comparator')}")
    fig_dir = Path("figures") / summary["name"]
    plot_discovery_curves(
        summary,
        [
            "function_recovery_rmse",
            "parameter_recovery_rmse",
            "probe_entropy",
            "mean_predictive_std",
        ],
        fig_dir / "discovery_curves.png",
    )
    plot_final_bars(summary, "function_recovery_rmse", fig_dir / "final_function_rmse.png")
    return summary
