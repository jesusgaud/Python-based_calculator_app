from decimal import Decimal
import pytest
from app.calculator import Calculator
from app.calculations_global import Calculations  # Corrected import

@pytest.fixture
def clear_history_fixture():
    """Fixture to clear calculation history before each test."""
    history_manager = Calculations()
    history_manager.clear_history()
    yield
    history_manager.clear_history()

@pytest.mark.usefixtures("clear_history_fixture")
def test_addition():
    assert Calculator.add(Decimal(2), Decimal(2)) == Decimal(4)
    history_manager = Calculations()
    assert len(history_manager.get_history()) == 1  # ✅ Fixed history reference

@pytest.mark.usefixtures("clear_history_fixture")
def test_subtraction():
    assert Calculator.subtract(Decimal(5), Decimal(3)) == Decimal(2)
    history_manager = Calculations()
    assert len(history_manager.get_history()) == 1  # ✅ Fixed history reference

@pytest.mark.usefixtures("clear_history_fixture")
def test_multiplication():
    assert Calculator.multiply(Decimal(3), Decimal(4)) == Decimal(12)
    history_manager = Calculations()
    assert len(history_manager.get_history()) == 1  # ✅ Fixed history reference

@pytest.mark.usefixtures("clear_history_fixture")
def test_division():
    assert Calculator.divide(Decimal(10), Decimal(2)) == Decimal(5)
    history_manager = Calculations()
    assert len(history_manager.get_history()) == 1  # ✅ Fixed history reference

@pytest.mark.usefixtures("clear_history_fixture")
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        Calculator.divide(Decimal(5), Decimal(0))
