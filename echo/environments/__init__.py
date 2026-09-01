from __future__ import annotations

from typing import Callable, Type, Union

from echo.environments.anomaly import AnomalyScientificSystem
from echo.environments.base import ScientificEnvironment
from echo.environments.causal import CausalScientificSystem
from echo.environments.competing import CompetingHypothesesSystem
from echo.environments.function import FunctionScientificSystem
from echo.environments.interaction import InteractionScientificSystem
from echo.environments.linear import LinearScientificSystem
from echo.environments.multimodal import MultimodalScientificSystem
from echo.environments.nonlinear import NonlinearScientificSystem
from echo.environments.tabular import TabularScientificSystem, tabular_from_csv
from echo.environments.unseen import UnseenScientificSystem

EnvFactory = Callable[..., ScientificEnvironment]
EnvSpec = Union[Type[ScientificEnvironment], EnvFactory]

_ENVIRONMENTS: dict[str, EnvSpec] = {
    "linear": LinearScientificSystem,
    "nonlinear": NonlinearScientificSystem,
    "interaction": InteractionScientificSystem,
    "competing_hypotheses": CompetingHypothesesSystem,
    "causal": CausalScientificSystem,
    "multimodal": MultimodalScientificSystem,
    "anomaly": AnomalyScientificSystem,
    "unseen": UnseenScientificSystem,
}


def available_environments() -> list[str]:
    return sorted(_ENVIRONMENTS)


def register_environment(name: str, factory: EnvSpec) -> str:
    """Register a custom environment class or factory under ``name``."""
    key = str(name)
    _ENVIRONMENTS[key] = factory
    return key


def register_function(name: str, fn, **defaults) -> str:
    """Register a hidden function as a named environment."""

    def factory(**kwargs):
        merged = {**defaults, **kwargs}
        merged.setdefault("name", name)
        return FunctionScientificSystem(fn, **merged)

    return register_environment(name, factory)


def make_environment(name: str, **kwargs) -> ScientificEnvironment:
    if name not in _ENVIRONMENTS:
        known = ", ".join(available_environments())
        raise ValueError(f"unknown environment {name!r}; known: {known}")
    env = _ENVIRONMENTS[name](**kwargs)
    if not getattr(env, "name", None):
        env.name = name
    return env


__all__ = [
    "AnomalyScientificSystem",
    "CausalScientificSystem",
    "CompetingHypothesesSystem",
    "FunctionScientificSystem",
    "InteractionScientificSystem",
    "LinearScientificSystem",
    "MultimodalScientificSystem",
    "NonlinearScientificSystem",
    "ScientificEnvironment",
    "TabularScientificSystem",
    "UnseenScientificSystem",
    "available_environments",
    "make_environment",
    "register_environment",
    "register_function",
    "tabular_from_csv",
]
