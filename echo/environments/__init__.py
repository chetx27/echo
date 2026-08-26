"""Environment registry. Add new worlds here without changing the runner."""

from __future__ import annotations

from echo.environments.base import ScientificEnvironment
from echo.environments.linear import LinearScientificSystem
from echo.environments.nonlinear import NonlinearScientificSystem

_ENVIRONMENTS = {
    "linear": LinearScientificSystem,
    "nonlinear": NonlinearScientificSystem,
}


def available_environments() -> list[str]:
    return sorted(_ENVIRONMENTS)


def make_environment(name: str, **kwargs) -> ScientificEnvironment:
    if name not in _ENVIRONMENTS:
        known = ", ".join(available_environments())
        raise ValueError(f"unknown environment {name!r}; known: {known}")
    return _ENVIRONMENTS[name](**kwargs)
