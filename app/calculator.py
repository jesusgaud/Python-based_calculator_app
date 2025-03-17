from decimal import Decimal
from app.calculations_global import Calculations, Calculation  # Import both classes
from app.operations import add, subtract, multiply, divide
from app.core.history_interface import HistoryInterface  # Decouple dependency

class Calculator:
    """A calculator that performs arithmetic operations and stores a history of calculations."""

    def __init__(self, history_manager: HistoryInterface = None):
        """
        Initializes the calculator with a history management system.

        Args:
            history_manager (HistoryInterface, optional): The history manager instance.
        """
        self.history_manager = history_manager or Calculations()  # Default to Singleton history manager

    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        """Performs addition and stores the calculation."""
        result = add(a, b)
        history_manager = Calculations()
        calculation = Calculation(a, b, "add", result)  # ✅ Fixed constructor arguments
        history_manager.add_calculation(calculation)
        return result

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        """Performs subtraction and stores the calculation."""
        result = subtract(a, b)
        history_manager = Calculations()
        calculation = Calculation(a, b, "subtract", result)  # ✅ Fixed
        history_manager.add_calculation(calculation)
        return result

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        """Performs multiplication and stores the calculation."""
        result = multiply(a, b)
        history_manager = Calculations()
        calculation = Calculation(a, b, "multiply", result)  # ✅ Fixed
        history_manager.add_calculation(calculation)
        return result

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        """Performs division and stores the calculation. Handles divide-by-zero errors."""
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        result = divide(a, b)
        history_manager = Calculations()
        calculation = Calculation(a, b, "divide", result)  # ✅ Fixed
        history_manager.add_calculation(calculation)
        return result
