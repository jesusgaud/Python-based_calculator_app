from decimal import Decimal
import pytest
from app.calculation import Calculation
from app.operations import add, subtract, multiply, divide
from app.plugins import modulus, power  # Import modulus and power modules

@pytest.mark.parametrize(
    "x, y, op, expected_result",
    [
        (Decimal("10"), Decimal("5"), add, Decimal("15")),
        (Decimal("10"), Decimal("5"), subtract, Decimal("5")),
        (Decimal("3"), Decimal("4"), multiply, Decimal("12")),
        (Decimal("20"), Decimal("5"), divide, Decimal("4")),
        (Decimal("10"), Decimal("3"), modulus.operation, Decimal("1")),  # Modulus test
        (Decimal("20"), Decimal("4"), modulus.operation, Decimal("0")),  # Modulus test
        (Decimal("7"), Decimal("5"), modulus.operation, Decimal("2")),  # Modulus test
        (Decimal("15"), Decimal("7"), modulus.operation, Decimal("1")),  # Modulus test
        (Decimal("2"), Decimal("3"), power.operation, Decimal("8")),  # Power test (2^3)
        (Decimal("5"), Decimal("2"), power.operation, Decimal("25")),  # Power test (5^2)
        (Decimal("10"), Decimal("0"), power.operation, Decimal("1")),  # Power test (10^0)
        (Decimal("4"), Decimal("0.5"), power.operation, Decimal("2")),  # Power test (sqrt 4)
    ],
)
def test_operation(x, y, op, expected_result):
    """Testing various operations, including modulus and power"""
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
