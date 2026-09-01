"""Reserved for versioned datasets. Built-in worlds draw synthetically.

Load a finite experimental table with ``echo.environments.tabular_from_csv``.
"""

from echo.environments.tabular import TabularScientificSystem, tabular_from_csv

__all__ = ["TabularScientificSystem", "tabular_from_csv"]
