"""ECHO: sequential experiment selection for scientific discovery.

Research laboratory. No language model is required.
"""

from echo.lab import (
    FunctionWorld,
    TabularWorld,
    compare_policies,
    register_acquisition,
    register_environment,
    register_function,
    register_policy,
    tabular_from_csv,
)

__version__ = "0.2.0"

__all__ = [
    "FunctionWorld",
    "TabularWorld",
    "compare_policies",
    "register_acquisition",
    "register_environment",
    "register_function",
    "register_policy",
    "tabular_from_csv",
    "__version__",
]
