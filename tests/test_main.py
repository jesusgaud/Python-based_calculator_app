from decimal import Decimal, InvalidOperation
import pytest
from app.operations import execute_operation
from app.calculations_global import Calculations

@pytest.fixture
def history_manager():
    """Fixture to provide a fresh history manager instance."""
    history = Calculations()
    history.clear_history()
    return history

@pytest.mark.parametrize("a, b, operation, expected", [
    ("5", "3", "add", "The result of 5 add 3 is equal to 8"),
    ("10", "2", "subtract", "The result of 10 subtract 2 is equal to 8"),
    ("4", "5", "multiply", "The result of 4 multiply 5 is equal to 20"),
    ("20", "4", "divide", "The result of 20 divide 4 is equal to 5"),
])
# pylint: disable=too-many-arguments
def test_calculate_and_print(a, b, operation, expected, capsys, history_manager):
    """Test Calculation operations with input strings and expected output, including history tracking."""
    try:
        a, b = Decimal(a), Decimal(b)
    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
        captured = capsys.readouterr()
        assert captured.out.strip() == expected
        return

    result = execute_operation(a, b, operation, history_manager)
    print(f"The result of {a} {operation} {b} is equal to {result}")

    captured = capsys.readouterr()
    assert expected in captured.out.strip()

def test_history_persistence(history_manager):
    """Ensure calculations persist by verifying history loads correctly from CSV."""
    execute_operation(Decimal("15"), Decimal("7"), "add", history_manager)
    execute_operation(Decimal("9"), Decimal("3"), "divide", history_manager)

    reloaded_manager = Calculations()
    history = reloaded_manager.get_history()

    # Calculate unique entries based on a, b, operation_name, and result.
    unique_entries = { (calc.a, calc.b, calc.operation_name, calc.result) for calc in history }
    assert len(unique_entries) == 2, f"Expected 2 unique entries, got {len(unique_entries)}"
    # Additionally, verify the operations are as expected.
    unique_ops = { calc.operation_name for calc in history }
    assert unique_ops == {"add", "divide"}
