from __future__ import annotations

from echo.policies.base import Policy


def available_algorithms() -> list[str]:
    return [
        "random",
        "uncertainty",
        "expected_improvement",
        "information_gain",
        "echo_v0",
    ]


def make_policy(name: str) -> Policy:
    # Imported here to avoid a package-level cycle with echo.acquisition.
    from echo.acquisition.echo_v0 import echo_v0_score
    from echo.acquisition.expected_improvement import expected_improvement
    from echo.acquisition.information_gain import local_information_gain
    from echo.acquisition.uncertainty import predictive_uncertainty
    from echo.policies.acquisition_policy import AcquisitionPolicy
    from echo.policies.random_policy import RandomPolicy

    policies = {
        "random": lambda: RandomPolicy(),
        "uncertainty": lambda: AcquisitionPolicy("uncertainty", predictive_uncertainty),
        "expected_improvement": lambda: AcquisitionPolicy(
            "expected_improvement", expected_improvement
        ),
        "information_gain": lambda: AcquisitionPolicy(
            "information_gain", local_information_gain
        ),
        "echo_v0": lambda: AcquisitionPolicy("echo_v0", echo_v0_score),
    }
    if name not in policies:
        known = ", ".join(available_algorithms())
        raise ValueError(f"unknown algorithm {name!r}; known: {known}")
    return policies[name]()
