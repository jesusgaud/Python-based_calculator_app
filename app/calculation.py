from decimal import Decimal
from typing import Callable

class Calculation:
    """Represents a single mathematical calculation between two operands."""

    def __repr__(self):
        """Returns a string representation of the calculation"""
        return f"Calculation({self.a}, {self.b}, {self.operation.__name__})"

    def __init__(self, a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """
        Initializes a Calculation instance.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.
            operation (Callable): A function that performs an arithmetic operation on two Decimals.
        """
        self.a = a
        self.b = b
        self.operation = operation

    @staticmethod
    def create(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> "Calculation":
        """
        Creates a new Calculation instance.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.
            operation (Callable): A function that performs an arithmetic operation on two Decimals.

        Returns:
            Calculation: A new Calculation instance.
        """
        return Calculation(a, b, operation)

    def perform(self) -> Decimal:
        """
        Executes the stored calculation and returns the result.

        Returns:
            Decimal: The result of the arithmetic operation.
        """
        return self.operation(self.a, self.b)  # Ensure the operation is executed properly
