"""Example: a finite experimental table plus a cost-aware acquisition.

`examples/yield_table.csv` is synthetic. It is not a published dataset.
Hotter rows cost more. `yield_noiseless` is evaluator-only.

Run:

    python examples/tabular.py
"""

from __future__ import annotations

from pathlib import Path

from echo.lab import compare_policies, register_acquisition, register_environment, tabular_from_csv

TABLE = Path(__file__).resolve().with_name("yield_table.csv")


def make_yield_table(**kwargs):
    return tabular_from_csv(
        TABLE,
        x_columns=["temp", "pressure"],
        y_column="yield",
        f_column="yield_noiseless",
        cost_column="cost",
        name="yield_table",
        formula="synthetic lookup: yield vs temp, pressure (not a published dataset)",
        **kwargs,
    )


register_environment("yield_table", make_yield_table)


def prefer_cheap(state):
    """Prefer remaining rows with lower experimental cost."""
    return -state.costs


register_acquisition("cheap", prefer_cheap)


if __name__ == "__main__":
    summary = compare_policies(
        "yield_table",
        algorithms=["random", "uncertainty", "cheap"],
        name="example_yield_table",
        budget=10,
        n_candidates=42,
        n_seeds=5,
        n_init=3,
        n_test=8,
        n_probe=16,
        n_restarts=0,
        primary_algorithm="cheap",
        comparator="uncertainty",
        plot_metrics=["function_recovery_rmse"],
    )
    print("wrote results/example_yield_table/")
    print(
        "final RMSE:",
        {k: v["mean"] for k, v in summary["final"]["function_recovery_rmse"].items()},
    )
