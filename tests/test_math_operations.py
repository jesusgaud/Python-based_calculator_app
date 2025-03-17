"""
Unit tests for math_operations.py.
"""

from decimal import Decimal
import pytest
from app.math_operations import add, subtract, divide

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("5"), Decimal("3"), Decimal("8")),
        (Decimal("-5"), Decimal("10"), Decimal("5")),
        (Decimal("0"), Decimal("0"), Decimal("0")),
    ],
)
def test_add(a, b, expected):
    """Test addition operation."""
    assert add(a, b) == expected, f"Failed add({a}, {b})"

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("10"), Decimal("5"), Decimal("5")),
        (Decimal("5"), Decimal("10"), Decimal("-5")),
        (Decimal("0"), Decimal("5"), Decimal("-5")),
    ],
)
def test_subtract(a, b, expected):
    """Test subtraction operation."""
    assert subtract(a, b) == expected, f"Failed subtract({a}, {b})"

def test_divide_by_zero():
    """Ensure division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(Decimal("5"), Decimal("0"))
