from decimal import Decimal
import pytest
from calculator.calculator import Calculator
from calculator.calculations import Calculations

@pytest.fixture
def clear_history_fixture():
    """Fixture to clear calculation history before each test."""
    Calculations.clear_history()

@pytest.mark.usefixtures("clear_history_fixture")
def test_addition():
    assert Calculator.add(Decimal(2), Decimal(2)) == Decimal(4)
    assert len(Calculations.history) == 1

@pytest.mark.usefixtures("clear_history_fixture")
def test_subtraction():
    assert Calculator.subtract(Decimal(5), Decimal(3)) == Decimal(2)
    assert len(Calculations.history) == 1

@pytest.mark.usefixtures("clear_history_fixture")
def test_multiplication():
    assert Calculator.multiply(Decimal(3), Decimal(4)) == Decimal(12)
    assert len(Calculations.history) == 1

@pytest.mark.usefixtures("clear_history_fixture")
def test_division():
    assert Calculator.divide(Decimal(10), Decimal(2)) == Decimal(5)
    assert len(Calculations.history) == 1

@pytest.mark.usefixtures("clear_history_fixture")
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        Calculator.divide(Decimal(5), Decimal(0))