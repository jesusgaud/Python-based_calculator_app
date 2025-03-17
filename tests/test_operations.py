from decimal import Decimal

import pytest

from app.calculations_global import Calculations
from app.operations import execute_operation

@pytest.fixture
def history_manager():
    """Fixture to provide a fresh history manager instance."""
    history = Calculations()
    history.clear_history()
    return history

@pytest.mark.parametrize("a, b, operation, expected", [
    (Decimal("10"), Decimal("5"), "add", Decimal("15")),
    (Decimal("9"), Decimal("3"), "subtract", Decimal("6")),
    (Decimal("4"), Decimal("2"), "multiply", Decimal("8")),
    (Decimal("20"), Decimal("4"), "divide", Decimal("5")),
])
def test_execute_operation(a, b, operation, expected, history_manager):
    """Test execution of operations and storage in history."""
    result = execute_operation(a, b, operation, history_manager)
    assert result == expected
    assert history_manager.get_latest().result == expected

def test_divide_by_zero(history_manager):
    """Ensure division by zero raises an error."""
    with pytest.raises(ZeroDivisionError):
        execute_operation(Decimal("5"), Decimal("0"), "divide", history_manager)
