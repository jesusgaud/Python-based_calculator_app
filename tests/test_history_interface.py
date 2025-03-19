import pytest
from unittest.mock import MagicMock
from typing import Optional, List
from app.core.history_interface import HistoryInterface

# ✅ TEST: Ensure `HistoryInterface` cannot be instantiated directly
def test_cannot_instantiate_history_interface():
    """Ensure `HistoryInterface` cannot be instantiated directly."""
    with pytest.raises(TypeError, match="Can't instantiate abstract class HistoryInterface"):
        HistoryInterface()

# ✅ Create a concrete class to test abstract methods
class ConcreteHistory(HistoryInterface):
    """Concrete implementation of HistoryInterface for testing."""

    def __init__(self):
        self.history = []

    def add_calculation(self, calculation) -> None:
        self.history.append(calculation)

    def get_latest(self) -> Optional[str]:
        return self.history[-1] if self.history else None

    def get_history(self) -> List[str]:
        return self.history

    def clear_history(self) -> None:
        self.history.clear()

    def find_by_operation(self, operation: str) -> List[str]:
        return [calc for calc in self.history if getattr(calc, "operation", None) == operation]

    def save_history(self) -> None:
        pass  # Simulate saving logic

    def load_history(self) -> None:
        pass  # Simulate loading logic

# ✅ TEST: Ensure all abstract methods are implemented in `ConcreteHistory`
@pytest.fixture
def history_instance():
    """Fixture to create an instance of the concrete history class."""
    return ConcreteHistory()

def test_add_calculation(history_instance):
    """Test adding a calculation."""
    mock_calc = MagicMock(operation="add", value=10)
    history_instance.add_calculation(mock_calc)
    assert len(history_instance.get_history()) == 1
    assert history_instance.get_latest() == mock_calc

def test_get_latest_empty(history_instance):
    """Test get_latest when history is empty."""
    assert history_instance.get_latest() is None

def test_get_history(history_instance):
    """Test retrieving the full history."""
    mock_calc1 = MagicMock(operation="add", value=10)
    mock_calc2 = MagicMock(operation="subtract", value=5)
    history_instance.add_calculation(mock_calc1)
    history_instance.add_calculation(mock_calc2)
    assert history_instance.get_history() == [mock_calc1, mock_calc2]

def test_clear_history(history_instance):
    """Test clearing history."""
    mock_calc = MagicMock(operation="add", value=10)
    history_instance.add_calculation(mock_calc)
    history_instance.clear_history()
    assert len(history_instance.get_history()) == 0

def test_find_by_operation(history_instance):
    """Test finding calculations by operation."""
    mock_calc1 = MagicMock(operation="add", value=10)
    mock_calc2 = MagicMock(operation="subtract", value=5)
    history_instance.add_calculation(mock_calc1)
    history_instance.add_calculation(mock_calc2)
    result = history_instance.find_by_operation("add")
    assert len(result) == 1
    assert result[0] == mock_calc1

def test_save_history(history_instance):
    """Test save_history is callable."""
    assert history_instance.save_history() is None  # Should not raise an error

def test_load_history(history_instance):
    """Test load_history is callable."""
    assert history_instance.load_history() is None  # Should not raise an error
