from collections import deque
from typing import List, Optional
from app.calculation import Calculation

class Calculations:
    """Manages a history of calculations using the Command Pattern."""
    history: deque[Calculation] = deque()

    @classmethod
    def add_calculation(cls, calculation: Calculation) -> None:
        """Adds a calculation to the history."""
        cls.history.append(calculation)

    @classmethod
    def get_latest(cls) -> Optional[Calculation]:
        """Returns the latest calculation if available."""
        return cls.history[-1] if cls.history else None

    @classmethod
    def get_history(cls) -> List[Calculation]:
        """Returns the entire calculation history."""
        return list(cls.history)

    @classmethod
    def clear_history(cls) -> None:
        """Clears the calculation history."""
        cls.history.clear()

    @classmethod
    def find_by_operation(cls, operation: str) -> List[Calculation]:
        """Finds calculations based on the operation name."""
        return [calc for calc in cls.history if calc.operation.__name__ == operation]
