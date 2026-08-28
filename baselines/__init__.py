"""Baselines live in echo.acquisition; this package is a stable import path."""

from echo.acquisition.diversity import diversity_score
from echo.acquisition.expected_improvement import expected_improvement
from echo.acquisition.greedy import greedy_mean
from echo.acquisition.information_gain import local_information_gain
from echo.acquisition.thompson import thompson_meanfield
from echo.acquisition.ucb import gp_ucb
from echo.acquisition.uncertainty import predictive_uncertainty

__all__ = [
    "diversity_score",
    "expected_improvement",
    "greedy_mean",
    "gp_ucb",
    "local_information_gain",
    "predictive_uncertainty",
    "thompson_meanfield",
]
