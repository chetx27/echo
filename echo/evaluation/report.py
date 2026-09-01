"""Write a markdown report from a run ``summary.json``.

Numbers are copied from the summary. If this file disagrees with the JSON,
the JSON is the record.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional


HIGHER_IS_BETTER = {
    "correct_hypothesis_prob",
    "hypothesis_identified",
    "leading_hypothesis_correct",
    "parent_set_f1",
    "region_coverage",
    "anomaly_hit_rate",
    "anomaly_recall",
}


def _fmt(value: Any, digits: int = 3) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return "—"
    if x != x:
        return "—"
    if abs(x) >= 0.01 or x == 0.0:
        return f"{x:.{digits}f}"
    return f"{x:.2e}"


def _p(value: Any) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return "—"
    if x != x:
        return "—"
    if x < 1e-4:
        return f"{x:.1e}"
    return f"{x:.3g}"


def _question_for(summary: dict) -> str:
    if summary.get("question"):
        return str(summary["question"])
    try:
        from echo.bench import available_tasks, get_task

        name = summary.get("name")
        for task_name in available_tasks():
            task = get_task(task_name)
            stem = Path(task.config_path).stem
            if stem == name:
                return task.question
    except Exception:
        pass
    env = summary.get("environment", "the environment")
    return f"Which sequential policy is more efficient on {env} under the configured budget?"


def write_markdown_report(summary: dict, path: Path, extra: Optional[Dict[str, str]] = None) -> Path:
    extra = extra or {}
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    metric = summary.get("failure_metric") or (summary.get("plot_metrics") or ["function_recovery_rmse"])[0]
    higher = bool(summary.get("failure_higher_is_better")) or metric in HIGHER_IS_BETTER
    primary = summary.get("primary_algorithm", "echo_v0")
    comparator = summary.get("comparator")
    final = summary.get("final") or {}
    algorithms = summary.get("algorithms") or []
    n_seeds = summary.get("n_seeds")
    budget = summary.get("budget")
    question = extra.get("question") or _question_for(summary)

    lines = [
        f"# {summary.get('name', 'experiment')}",
        "",
        f"**Status:** generated from `results/{summary.get('name', '')}/summary.json`.",
        f"**Date:** {date.today().isoformat()}",
        f"**Environment:** `{summary.get('environment')}`",
        f"**Config hash:** `{summary.get('config_hash')}`",
        f"**Seeds:** {n_seeds}  |  **Budget:** {budget}  |  **Init:** {summary.get('n_init')}",
        "",
        "If these numbers disagree with the JSON, the JSON is the record. "
        "Do not treat this file as a claim of superiority.",
        "",
        "## Question",
        "",
        question,
        "",
        f"Primary algorithm: `{primary}`. "
        + (f"Comparator: `{comparator}`." if comparator else ""),
        f"Primary metric: `{metric}` ({'higher' if higher else 'lower'} is better).",
        "",
        "## Final results",
        "",
        f"| Algorithm | Mean | Median | Std | 95% CI |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    block = final.get(metric) or {}
    for algo in algorithms:
        stats = block.get(algo) or {}
        ci = f"[{_fmt(stats.get('ci_low'))}, {_fmt(stats.get('ci_high'))}]"
        lines.append(
            f"| {algo} | {_fmt(stats.get('mean'))} | {_fmt(stats.get('median'))} | "
            f"{_fmt(stats.get('std'))} | {ci} |"
        )

    extra_metrics = [m for m in (summary.get("plot_metrics") or []) if m != metric and m in final]
    for other in extra_metrics[:3]:
        lines.extend(["", f"### `{other}`", "", "| Algorithm | Mean | Median |", "| --- | ---: | ---: |"])
        for algo in algorithms:
            stats = (final.get(other) or {}).get(algo) or {}
            lines.append(f"| {algo} | {_fmt(stats.get('mean'))} | {_fmt(stats.get('median'))} |")

    pairwise = summary.get("pairwise") or {}
    if pairwise:
        lines.extend(
            [
                "",
                "## Pairwise vs primary",
                "",
                f"mean_diff = `{primary}` − other. "
                + (
                    "Positive favors the primary method on this metric."
                    if higher
                    else "Negative favors the primary method on this metric."
                ),
                "",
                "| Contrast | Mean diff | Cohen's d | Wilcoxon p | Primary wins |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for key, metrics in pairwise.items():
            stats = (metrics or {}).get(metric) or {}
            if higher:
                wins = stats.get("b_wins")
            else:
                wins = stats.get("a_wins")
            n = stats.get("n")
            lines.append(
                f"| {key} | {_fmt(stats.get('mean_diff'), 4)} | {_fmt(stats.get('cohens_d'), 2)} | "
                f"{_p(stats.get('wilcoxon_p'))} | {wins} / {n} |"
            )

    n_fail = summary.get("n_failures_vs_comparator", 0)
    fail_seeds = summary.get("failure_seeds") or []
    lines.extend(
        [
            "",
            "## Failures",
            "",
            f"The primary method was worse than `{comparator}` on `{metric}` "
            f"for **{n_fail} / {n_seeds}** seeds.",
        ]
    )
    if fail_seeds:
        shown = ", ".join(str(s) for s in fail_seeds[:20])
        more = "" if len(fail_seeds) <= 20 else f" (+{len(fail_seeds) - 20} more)"
        lines.append(f"Seeds: {shown}{more}.")
        lines.append("Records: `results/" + str(summary.get("name", "")) + "/failures/`.")
    lines.extend(
        [
            "",
            "## What this does not support",
            "",
            "- A claim that ECHO is a general scientific agent.",
            "- Transfer to real laboratory data unless a tabular/CSV world was used.",
            "- Any LLM or autonomy result. This repository does not use a language model.",
            "",
            "## How to reproduce",
            "",
            "```bash",
            f"python -m echo compare --config configs/{summary.get('name', 'experiment')}.yaml",
            f"python -m echo analyze --run results/{summary.get('name', 'experiment')}",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines))
    return path
