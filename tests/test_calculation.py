"""
This module contains tests for the calculator operations and Calculation class.

The tests verify arithmetic operations (addition, subtraction, multiplication, division)
implemented in the calculator.operations module, and functionality of the Calculation class.
"""

# Import statements:
# pylint: disable=unnecessary-dunder-call, invalid-name
from decimal import Decimal
import pytest
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide

# Renamed `a, b, operation, expected` to `a1, b1, op1, exp1` to avoid duplicate parameterization conflicts
@pytest.mark.parametrize(
    "a1, b1, op1, exp1",
    [
        (Decimal("10"), Decimal("5"), add, Decimal("15")),
        (Decimal("10"), Decimal("5"), subtract, Decimal("5")),
        (Decimal("3"), Decimal("4"), multiply, Decimal("12")),
        (Decimal("20"), Decimal("5"), divide, Decimal("4")),
    ],
)
def test_calculation_operations(a1, b1, op1, exp1):
    """
    Test calculation operations with various scenarios.

    Ensures that the Calculation class correctly performs
    arithmetic operations and matches the expected outcome.
    """
    calc = Calculation(a1, b1, op1)  # Create Calculation instance
    assert calc.perform() == exp1, f"Failed {op1.__name__} operation with {a1} and {b1}"  # Validate result


def test_calculation_repr():
    """
    Test the string representation (__repr__) of the Calculation class.
    """
    calc = Calculation(Decimal('10'), Decimal('5'), add)  # Create Calculation instance
    expected_repr = "Calculation(10, 5, add)"  # Expected string representation
    assert calc.__repr__() == expected_repr, "The __repr__ method output does not match the expected string."


def test_divide_by_zero():
    """
    Test that division by zero raises the correct ZeroDivisionError.
    """
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(Decimal(5), Decimal(0))