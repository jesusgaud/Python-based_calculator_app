from decimal import Decimal
from .calculation import Calculation
from .calculations import Calculations
from .operations import add, subtract, multiply, divide

class Calculator:
    """A calculator that performs arithmetic operations and stores a history of calculations."""

    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        """
        Performs addition and stores the calculation.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: The sum of a and b.
        """
        calculation = Calculation.create(a, b, add)
        Calculations.add_calculation(calculation)
        return calculation.perform()

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        """
        Performs subtraction and stores the calculation.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: The result of a - b.
        """
        calculation = Calculation.create(a, b, subtract)
        Calculations.add_calculation(calculation)
        return calculation.perform()

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        """
        Performs multiplication and stores the calculation.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: The result of a * b.
        """
        calculation = Calculation.create(a, b, multiply)
        Calculations.add_calculation(calculation)
        return calculation.perform()

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        """
        Performs division and stores the calculation. Handles divide-by-zero errors.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: The result of a / b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        calculation = Calculation.create(a, b, divide)
        Calculations.add_calculation(calculation)
        return calculation.perform()
