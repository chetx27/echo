from __future__ import annotations

from abc import ABC, abstractmethod

from echo.policies.state import DecisionState


class Policy(ABC):
    name: str

    @abstractmethod
    def select(self, state: DecisionState) -> int:
        """Return the index of the next candidate experiment."""
