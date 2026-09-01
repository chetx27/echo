"""Public laboratory API.

Plug in a hidden function, a CSV of candidate experiments, or a custom
acquisition score, then compare sequential policies under a budget.

Example:

    from echo.lab import compare_policies

    def f(X):
        return X[:, 0] ** 2 + 0.3 * X[:, 1]

    summary = compare_policies(
        f,
        dim=2,
        algorithms=["random", "uncertainty", "echo_v0"],
        budget=15,
        n_candidates=400,
        n_seeds=5,
        name="my_system",
    )
"""

from __future__ import annotations

from typing import Callable, Optional, Sequence, Union

import numpy as np

from echo.environments import (
    FunctionScientificSystem,
    TabularScientificSystem,
    available_environments,
    make_environment,
    register_environment,
    register_function,
    tabular_from_csv,
)
from echo.experiments.compare import analyze_run, compare, run_one
from echo.policies import (
    available_algorithms,
    make_policy,
    register_acquisition,
    register_policy,
)
from echo.utils.io import ExperimentConfig

FunctionWorld = FunctionScientificSystem
TabularWorld = TabularScientificSystem
ArrayFn = Callable[[np.ndarray], np.ndarray]


def compare_policies(
    environment: Union[str, ArrayFn],
    algorithms: Optional[Sequence[str]] = None,
    *,
    name: str = "adhoc",
    dim: int = 1,
    budget: int = 20,
    n_candidates: int = 500,
    n_seeds: int = 8,
    n_init: int = 3,
    noise: float = 0.1,
    n_test: int = 200,
    n_probe: int = 64,
    n_jobs: int = 1,
    resume: bool = True,
    formula: str = "user-supplied f",
    **config_kwargs,
) -> dict:
    """Compare sequential policies on a named world or a Python function.

    ``environment`` is either a registered environment name or a callable
    ``f(X) -> y`` with ``X.shape == (n, dim)``.
    """
    if callable(environment) and not isinstance(environment, str):
        env_name = name if name not in available_environments() else f"{name}_fn"
        register_function(env_name, environment, dim=dim, formula=formula)
    elif isinstance(environment, str):
        env_name = environment
    else:
        raise TypeError("environment must be a registered name or a callable f(X)")

    known = {k: v for k, v in config_kwargs.items() if k in ExperimentConfig.__dataclass_fields__}
    config = ExperimentConfig(
        name=name,
        environment=env_name,
        algorithms=list(algorithms or ["random", "uncertainty", "echo_v0"]),
        budget=int(budget),
        n_candidates=int(n_candidates),
        n_seeds=int(n_seeds),
        n_init=int(n_init),
        noise=float(noise),
        n_test=int(n_test),
        n_probe=int(n_probe),
        **known,
    )
    return compare(config, n_jobs=int(n_jobs), resume=bool(resume))


__all__ = [
    "ArrayFn",
    "ExperimentConfig",
    "FunctionWorld",
    "TabularWorld",
    "analyze_run",
    "available_algorithms",
    "available_environments",
    "compare",
    "compare_policies",
    "make_environment",
    "make_policy",
    "register_acquisition",
    "register_environment",
    "register_function",
    "register_policy",
    "run_one",
    "tabular_from_csv",
]
