from __future__ import annotations

from echo.policies.base import Policy


def available_algorithms() -> list[str]:
    return sorted(
        [
            "random",
            "greedy",
            "uncertainty",
            "diversity",
            "expected_improvement",
            "ucb",
            "thompson",
            "information_gain",
            "echo_v0",
            "echo_hypothesis",
            "echo_falsify",
            "echo_hypothesis_cost",
            "echo_hypothesis_penalty",
            "echo_no_hypothesis",
            "echo_information_only",
            "echo_no_sequential",
        ]
    )


def make_policy(name: str) -> Policy:
    from echo.acquisition.cost_aware import minus_lambda_cost, per_cost
    from echo.acquisition.diversity import diversity_score
    from echo.acquisition.echo_v0 import echo_v0_score
    from echo.acquisition.expected_improvement import expected_improvement
    from echo.acquisition.falsification import falsification_score
    from echo.acquisition.greedy import greedy_mean
    from echo.acquisition.hypothesis_ig import hypothesis_discrimination
    from echo.acquisition.information_gain import local_information_gain
    from echo.acquisition.thompson import thompson_meanfield
    from echo.acquisition.ucb import gp_ucb
    from echo.acquisition.uncertainty import predictive_uncertainty
    from echo.policies.acquisition_policy import AcquisitionPolicy
    from echo.policies.batch import OpenLoopPolicy
    from echo.policies.random_policy import RandomPolicy

    policies = {
        "random": lambda: RandomPolicy(),
        "greedy": lambda: AcquisitionPolicy("greedy", greedy_mean),
        "uncertainty": lambda: AcquisitionPolicy("uncertainty", predictive_uncertainty),
        "diversity": lambda: AcquisitionPolicy("diversity", diversity_score),
        "expected_improvement": lambda: AcquisitionPolicy(
            "expected_improvement", expected_improvement
        ),
        "ucb": lambda: AcquisitionPolicy("ucb", gp_ucb),
        "thompson": lambda: AcquisitionPolicy("thompson", thompson_meanfield),
        "information_gain": lambda: AcquisitionPolicy(
            "information_gain", local_information_gain
        ),
        "echo_v0": lambda: AcquisitionPolicy("echo_v0", echo_v0_score),
        "echo_no_hypothesis": lambda: AcquisitionPolicy("echo_no_hypothesis", echo_v0_score),
        "echo_information_only": lambda: AcquisitionPolicy(
            "echo_information_only", local_information_gain
        ),
        "echo_hypothesis": lambda: AcquisitionPolicy(
            "echo_hypothesis", hypothesis_discrimination
        ),
        "echo_falsify": lambda: AcquisitionPolicy("echo_falsify", falsification_score),
        "echo_hypothesis_cost": lambda: AcquisitionPolicy(
            "echo_hypothesis_cost", per_cost(hypothesis_discrimination)
        ),
        "echo_hypothesis_penalty": lambda: AcquisitionPolicy(
            "echo_hypothesis_penalty", minus_lambda_cost(hypothesis_discrimination)
        ),
        "echo_no_sequential": lambda: OpenLoopPolicy("echo_no_sequential", echo_v0_score),
    }
    if name not in policies:
        known = ", ".join(available_algorithms())
        raise ValueError(f"unknown algorithm {name!r}; known: {known}")
    return policies[name]()
