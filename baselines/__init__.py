"""Baselines live in echo.acquisition; this package is a stable import path."""

from echo.acquisition.expected_improvement import expected_improvement
from echo.acquisition.information_gain import local_information_gain
from echo.acquisition.uncertainty import predictive_uncertainty

__all__ = [
    "expected_improvement",
    "local_information_gain",
    "predictive_uncertainty",
]
