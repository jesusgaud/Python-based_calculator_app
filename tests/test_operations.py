from decimal import Decimal
import pytest
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide

@pytest.mark.parametrize(
    "x, y, op, expected_result",
    [
        (Decimal("10"), Decimal("5"), add, Decimal("15")),
        (Decimal("10"), Decimal("5"), subtract, Decimal("5")),
        (Decimal("3"), Decimal("4"), multiply, Decimal("12")),
        (Decimal("20"), Decimal("5"), divide, Decimal("4")),
    ],
)
def test_operation(x, y, op, expected_result):
    """Testing various operations"""
    # Ensure `Calculation.create()` exists; if not, use Calculation(x, y, op)
    if hasattr(Calculation, "create"):
        calculation = Calculation.create(x, y, op)
    else:
        calculation = Calculation(x, y, op)
    assert calculation.perform() == expected_result, f"{op.__name__} operation failed"


# Keeping the divide by zero test as is since it tests a specific case
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(Decimal(5), Decimal(0))