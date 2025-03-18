import pytest
from abc import ABC, abstractmethod
from typing import List, Optional
from unittest.mock import MagicMock, patch
from app.core.history_interface import HistoryInterface

# ✅ Ensure HistoryInterface cannot be instantiated directly
def test_cannot_instantiate_history_interface():
    """Test that HistoryInterface cannot be instantiated."""
    with pytest.raises(TypeError, match="Can't instantiate abstract class HistoryInterface"):
        HistoryInterface()

# ✅ Concrete class for testing abstract implementation
class ConcreteHistory(HistoryInterface):
    """Concrete implementation of HistoryInterface for testing."""

    def __init__(self):
        self.history = []

    def add_calculation(self, calculation) -> None:
        self.history.append(calculation)

    def get_latest(self) -> Optional:
        return self.history[-1] if self.history else None

    def get_history(self) -> List:
        return self.history

    def clear_history(self) -> None:
        self.history.clear()

    def find_by_operation(self, operation: str) -> List:
        return [calc for calc in self.history if getattr(calc, "operation", None) == operation]

    def save_history(self) -> None:
        pass  # Simulate saving logic

    def load_history(self) -> None:
        pass  # Simulate loading logic

@pytest.fixture
def history_instance():
    """Fixture to create an instance of the concrete history class."""
    return ConcreteHistory()

# ✅ Ensure concrete implementation can be instantiated
def test_concrete_history_instantiation(history_instance):
    """Test instantiation of a concrete HistoryInterface subclass."""
    assert isinstance(history_instance, HistoryInterface)

# ✅ Test add_calculation method
def test_add_calculation(history_instance):
    """Test adding a calculation."""
    mock_calc = MagicMock(operation="add", value=10)
    history_instance.add_calculation(mock_calc)
    assert len(history_instance.get_history()) == 1
    assert history_instance.get_latest() == mock_calc

# ✅ Test get_latest method when history is empty
def test_get_latest_empty(history_instance):
    """Test get_latest when history is empty."""
    assert history_instance.get_latest() is None

# ✅ Test get_history method
def test_get_history(history_instance):
    """Test retrieving the full history."""
    mock_calc1 = MagicMock(operation="add", value=10)
    mock_calc2 = MagicMock(operation="subtract", value=5)
    history_instance.add_calculation(mock_calc1)
    history_instance.add_calculation(mock_calc2)
    assert history_instance.get_history() == [mock_calc1, mock_calc2]

# ✅ Test clear_history method
def test_clear_history(history_instance):
    """Test clearing history."""
    mock_calc = MagicMock(operation="add", value=10)
    history_instance.add_calculation(mock_calc)
    history_instance.clear_history()
    assert len(history_instance.get_history()) == 0

# ✅ Test find_by_operation method (valid match)
def test_find_by_operation(history_instance):
    """Test finding calculations by operation."""
    mock_calc1 = MagicMock(operation="add", value=10)
    mock_calc2 = MagicMock(operation="subtract", value=5)
    history_instance.add_calculation(mock_calc1)
    history_instance.add_calculation(mock_calc2)
    result = history_instance.find_by_operation("add")
    assert len(result) == 1
    assert result[0] == mock_calc1

# ✅ Test find_by_operation method (no match)
def test_find_by_operation_no_match(history_instance):
    """Test finding calculations by operation when no matches exist."""
    mock_calc1 = MagicMock(operation="multiply", value=10)
    history_instance.add_calculation(mock_calc1)
    result = history_instance.find_by_operation("add")
    assert len(result) == 0  # No "add" operations exist

# ✅ Test save_history method (mocked)
@patch.object(ConcreteHistory, "save_history", return_value=None)
def test_save_history(mock_save, history_instance):
    """Test save_history is callable."""
    history_instance.save_history()
    mock_save.assert_called_once()  # Ensure the method was called

# ✅ Test load_history method (mocked)
@patch.object(ConcreteHistory, "load_history", return_value=None)
def test_load_history(mock_load, history_instance):
    """Test load_history is callable."""
    history_instance.load_history()
    mock_load.assert_called_once()  # Ensure the method was called
