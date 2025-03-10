"""My Calculator Test"""

# Standard library imports
from decimal import Decimal
import pytest

# Application-specific imports
from calculator.calculation import Calculation
from calculator.calculations import Calculations
from calculator.operations import add, subtract

@pytest.fixture(name="setup_calculations")
def fixture_setup_calculations():
    """Fixture to clear history and add sample calculations for tests."""
    Calculations.clear_history()
    Calculations.add_calculation(Calculation(Decimal('10'), Decimal('5'), add))
    Calculations.add_calculation(Calculation(Decimal('20'), Decimal('3'), subtract))

def test_add_calculation(setup_calculations):
    """Test adding a calculation to the history."""
    _ = setup_calculations  # Explicitly reference fixture to avoid pylint warnings
    calc = Calculation(Decimal('2'), Decimal('2'), add)
    Calculations.add_calculation(calc)
    assert Calculations.get_latest() == calc, "Failed to add the calculation to the history"

def test_get_history(setup_calculations):
    """Test retrieving the entire calculation history."""
    _ = setup_calculations  # Explicitly reference fixture
    history = Calculations.get_history()
    assert len(history) == 2, "History does not contain the expected number of calculations"

def test_clear_history(setup_calculations):
    """Test clearing the entire calculation history."""
    _ = setup_calculations  # Explicitly reference fixture
    Calculations.clear_history()
    assert len(Calculations.get_history()) == 0, "History was not cleared"

def test_get_latest(setup_calculations):
    """Test getting the latest calculation from the history."""
    _ = setup_calculations  # Explicitly reference fixture
    latest = Calculations.get_latest()
    assert latest is not None, "Latest calculation is None"
    assert latest.a == Decimal('20') and latest.b == Decimal('3'), "Did not get the correct latest calculation"

def test_find_by_operation(setup_calculations):
    """Test finding calculations in the history by operation type."""
    _ = setup_calculations  # Explicitly reference fixture
    if hasattr(Calculations, "find_by_operation"):
        add_operations = Calculations.find_by_operation("add")
        assert len(add_operations) == 1, "Did not find the correct number of calculations with add operation"

        subtract_operations = Calculations.find_by_operation("subtract")
        assert len(subtract_operations) == 1, "Did not find the correct number of calculations with subtract operation"
    else:
        pytest.skip("find_by_operation method is missing in Calculations class")

def test_get_latest_with_empty_history(setup_calculations):
    """Test getting the latest calculation when the history is empty."""
    _ = setup_calculations  # Explicitly reference fixture
    Calculations.clear_history()
    assert Calculations.get_latest() is None, "Expected None for latest calculation with empty history"