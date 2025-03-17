from abc import ABC, abstractmethod
from typing import List, Optional

class HistoryInterface(ABC):
    """Abstract interface for managing calculation history."""

    @abstractmethod
    def add_calculation(self, calculation) -> None:
        """Adds a calculation to the history."""
        pass

    @abstractmethod
    def get_latest(self) -> Optional:
        """Returns the latest calculation if available."""
        pass

    @abstractmethod
    def get_history(self) -> List:
        """Returns the entire calculation history."""
        pass

    @abstractmethod
    def clear_history(self) -> None:
        """Clears history from memory and removes the storage file."""
        pass

    @abstractmethod
    def find_by_operation(self, operation: str) -> List:
        """Finds calculations based on the operation name."""
        pass

    @abstractmethod
    def save_history(self) -> None:
        """Saves the history to a storage file."""
        pass

    @abstractmethod
    def load_history(self) -> None:
        """Loads the calculation history from storage."""
        pass
