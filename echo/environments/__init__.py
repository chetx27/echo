from echo.environments.base import ScientificEnvironment
from echo.environments.competing import CompetingHypothesesSystem
from echo.environments.interaction import InteractionScientificSystem
from echo.environments.linear import LinearScientificSystem
from echo.environments.nonlinear import NonlinearScientificSystem

_ENVIRONMENTS = {
    "linear": LinearScientificSystem,
    "nonlinear": NonlinearScientificSystem,
    "interaction": InteractionScientificSystem,
    "competing_hypotheses": CompetingHypothesesSystem,
}


def available_environments() -> list[str]:
    return sorted(_ENVIRONMENTS)


def make_environment(name: str, **kwargs) -> ScientificEnvironment:
    if name not in _ENVIRONMENTS:
        known = ", ".join(available_environments())
        raise ValueError(f"unknown environment {name!r}; known: {known}")
    return _ENVIRONMENTS[name](**kwargs)
