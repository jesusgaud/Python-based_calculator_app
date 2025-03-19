from decimal import Decimal, InvalidOperation
import pytest
from app.operations import execute_operation
from app.calculations_global import Calculations
from main import calculate_and_print, execute_command, load_commands

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
    def test_calculate_and_print(a, b, operation, expected, capsys, history_manager):
        """Test Calculation operations with input strings and expected output, including history tracking."""
        calculate_and_print(a, b, operation, history_manager)
        captured = capsys.readouterr()
        assert expected in captured.out.strip()

    def test_calculate_and_print_invalid_operation(capsys, history_manager):
        """Test calculate_and_print with an invalid operation."""
        calculate_and_print("5", "3", "invalid_op", history_manager)
        captured = capsys.readouterr()
        assert "Unknown operation: invalid_op" in captured.out.strip()

    def test_calculate_and_print_invalid_number(capsys, history_manager):
        """Test calculate_and_print with invalid number input."""
        calculate_and_print("invalid", "3", "add", history_manager)
        captured = capsys.readouterr()
        assert "Invalid number input: invalid or 3 is not a valid number." in captured.out.strip()

    def test_calculate_and_print_zero_division(capsys, history_manager):
        """Test calculate_and_print with division by zero."""
        calculate_and_print("5", "0", "divide", history_manager)
        captured = capsys.readouterr()
        assert "An error occurred: Cannot divide by zero" in captured.out.strip()

    def test_execute_command_sync(history_manager, capsys):
        """Test execute_command in synchronous mode."""
        execute_command("5", "3", "add", history_manager, test_mode=True)
        captured = capsys.readouterr()
        assert "The result of 5 add 3 is equal to 8" in captured.out.strip()

    def test_load_commands():
        """Test load_commands to ensure operations are loaded."""
        commands = load_commands()
        assert "add" in commands
        assert "subtract" in commands
        assert "multiply" in commands
        assert "divide" in commands

    def test_history_persistence(history_manager):
        """Ensure calculations persist by verifying history loads correctly from CSV."""
        calculate_and_print("15", "7", "add", history_manager)
        calculate_and_print("9", "3", "divide", history_manager)

        reloaded_manager = Calculations()
        history = reloaded_manager.get_history()

        unique_entries = { (calc.a, calc.b, calc.operation_name, calc.result) for calc in history }
        assert len(unique_entries) == 2, f"Expected 2 unique entries, got {len(unique_entries)}"
        unique_ops = { calc.operation_name for calc in history }
        assert unique_ops == {"add", "divide"}
