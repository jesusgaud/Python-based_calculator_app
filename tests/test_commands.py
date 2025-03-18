from unittest.mock import MagicMock, patch
import pytest
from app.commands import (
    CommandHandler, Command, MenuCommand, AddCommand,
    SubtractCommand, MultiplyCommand, DivideCommand, HistoryCommand
)

# ✅ Mock command for testing
class MockCommand(Command):
    """Mock command implementing the execute method."""
    def execute(self, *args, **kwargs):
        _ = kwargs
        return "Mock Execution"

# ✅ Test CommandHandler registers core commands upon initialization
def test_command_handler_initialization():
    """Test that CommandHandler registers default commands upon initialization."""
    handler = CommandHandler()
    expected_commands = {"menu", "add", "subtract", "multiply", "divide", "history"}

    assert expected_commands.issubset(handler.commands.keys())

# ✅ Test MenuCommand Execution
def test_menu_command_execution(capsys):
    """Test MenuCommand prints available commands."""
    handler = CommandHandler()
    menu_command = MenuCommand(handler)

    menu_command.execute()
    captured = capsys.readouterr()

    assert "Available Commands:" in captured.out
    assert "- add" in captured.out
    assert "- subtract" in captured.out
    assert "- multiply" in captured.out
    assert "- divide" in captured.out
    assert "- history" in captured.out

# ✅ Test CommandHandler register_command method
def test_command_handler_register():
    """Test registering commands."""
    handler = CommandHandler()
    command = MockCommand()

    handler.register_command("mock_command", command)

    assert "mock_command" in handler.commands
    assert handler.commands["mock_command"] is command

# ✅ Test CommandHandler execute_command method
def test_command_handler_execute():
    """Test executing registered command."""
    handler = CommandHandler()
    command = MagicMock(spec=MockCommand)

    handler.register_command("mock_command", command)
    handler.execute_command("mock_command")

    command.execute.assert_called_once()

# ✅ Test CommandHandler execute unknown command
def test_command_handler_execute_unknown(capsys):
    """Test execution of an unknown command."""
    handler = CommandHandler()

    handler.execute_command("unknown_command")
    captured = capsys.readouterr()

    assert "Unknown command. Type 'menu' for a list of commands." in captured.out

# ✅ Ensure Command is Abstract
def test_abstract_command():
    """Ensure `Command` cannot be instantiated directly."""
    assert hasattr(Command, "__abstractmethods__")
    assert "execute" in Command.__abstractmethods__

    class InvalidCommand(Command):
        """A subclass that does not override `execute` properly."""
        def execute(self, *args, **kwargs):
            """Ensure execute is implemented but raises NotImplementedError."""
            raise NotImplementedError("This is an abstract method.")

    with pytest.raises(TypeError):
        Command()

    with pytest.raises(NotImplementedError):
        InvalidCommand().execute()

# ✅ Test AddCommand Execution
@patch("app.commands.add", return_value=15)
@patch("app.commands.Calculations.add_calculation")
def test_add_command_execution(mock_add_calc, mock_add, capsys):
    """Test execution of AddCommand with valid input."""
    add_command = AddCommand()
    add_command.execute("10", "5")

    captured = capsys.readouterr()
    assert "10 + 5 = 15" in captured.out

# ✅ Test SubtractCommand Execution
@patch("app.commands.subtract", return_value=5)
@patch("app.commands.Calculations.add_calculation")
def test_subtract_command_execution(mock_add_calc, mock_subtract, capsys):
    """Test execution of SubtractCommand with valid input."""
    subtract_command = SubtractCommand()
    subtract_command.execute("10", "5")

    captured = capsys.readouterr()
    assert "10 - 5 = 5" in captured.out

# ✅ Test MultiplyCommand Execution
@patch("app.commands.multiply", return_value=50)
@patch("app.commands.Calculations.add_calculation")
def test_multiply_command_execution(mock_add_calc, mock_multiply, capsys):
    """Test execution of MultiplyCommand with valid input."""
    multiply_command = MultiplyCommand()
    multiply_command.execute("10", "5")

    captured = capsys.readouterr()
    assert "10 x 5 = 50" in captured.out

# ✅ Test DivideCommand Execution
@patch("app.commands.divide", return_value=2)
@patch("app.commands.Calculations.add_calculation")
def test_divide_command_execution(mock_add_calc, mock_divide, capsys):
    """Test execution of DivideCommand with valid input."""
    divide_command = DivideCommand()
    divide_command.execute("10", "5")

    captured = capsys.readouterr()
    assert "10 / 5 = 2" in captured.out

# ✅ Test DivideCommand handles divide by zero
def test_divide_command_zero_division(capsys):
    """Test that DivideCommand correctly handles division by zero."""
    divide_command = DivideCommand()
    divide_command.execute("10", "0")

    captured = capsys.readouterr()
    assert "Error: Cannot divide by zero." in captured.out

# ✅ Test HistoryCommand Execution
@patch("app.commands.Calculations.get_history", return_value=["10 + 5 = 15"])
def test_history_command_execution(mock_history, capsys):
    """Test execution of HistoryCommand."""
    history_command = HistoryCommand()
    history_command.execute()

    captured = capsys.readouterr()
    assert "10 + 5 = 15" in captured.out
