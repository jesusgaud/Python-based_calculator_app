from decimal import Decimal
from typing import Optional
from app.math_operations import operations

class Calculation:
    """Represents a single calculation between two operands."""
    def __init__(self, a: Decimal, b: Decimal, operation_name: str, result: Optional[Decimal] = None):
        """Initialize operands, operation name, and result."""
        self.a = a
        self.b = b
        self.operation_name = operation_name
        self.operation = operations.get(operation_name)
        self.result = result if result is not None else self.perform()
    def __repr__(self):
        """String representation for debugging."""
        return f"Calculation({self.a}, {self.b}, {self.operation_name}, {self.result})"
    def perform(self) -> Decimal:
        """Execute the stored operation and return the result."""
        if not callable(self.operation):
            raise TypeError(f"Invalid operation: {self.operation_name} is not a valid function.")
        return self.operation(self.a, self.b)
    @staticmethod
    def from_history(num1: str, num2: str, operation_name: str, result: str) -> "Calculation":
        """Reconstruct a Calculation instance from stored history strings."""
        return Calculation(Decimal(num1), Decimal(num2), operation_name, Decimal(result))
