from decimal import Decimal
import os
import pytest

from app.core.calculation import Calculation
from app.calculations_global import Calculations

HISTORY_FILE = "history.csv"

@pytest.fixture(autouse=True)
def clear_history():
    """Ensure history is cleared before and after tests."""
    history_manager = Calculations()
    history_manager.clear_history()
    yield
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

def test_create_calculation():
    """Test creation of Calculation instance."""
    calculation = Calculation(Decimal("10"), Decimal("5"), "add", Decimal("15"))
    assert calculation.a == Decimal("10")
    assert calculation.b == Decimal("5")
    assert calculation.operation_name == "add"
    assert calculation.result == Decimal("15")

def test_perform_calculation():
    """Test the perform() method for calculations."""
    calculation = Calculation(Decimal("10"), Decimal("5"), "add", Decimal("15"))
    assert calculation.perform() == Decimal("15")

def test_add_calculation():
    """Ensure calculations are added to history."""
    history_manager = Calculations()
    calculation = Calculation(Decimal("15"), Decimal("7"), "add", Decimal("22"))
    history_manager.add_calculation(calculation)
    history = history_manager.get_history()
    assert len(history) == 1
    assert history[0].result == Decimal("22")

def test_clear_history():
    """Ensure clearing history removes all stored calculations."""
    history_manager = Calculations()
    history_manager.add_calculation(Calculation(Decimal("5"), Decimal("2"), "multiply", Decimal("10")))
    history_manager.clear_history()
    assert len(history_manager.get_history()) == 0
    assert not os.path.exists(HISTORY_FILE)

def test_save_and_load_history():
    """Ensure history is saved and loaded correctly from CSV."""
    history_manager = Calculations()
    history_manager.add_calculation(Calculation(Decimal("8"), Decimal("4"), "subtract", Decimal("4")))
    # Reload history
    reloaded_manager = Calculations()
    history = reloaded_manager.get_history()
    assert len(history) == 1
    assert history[0].result == Decimal("4")
