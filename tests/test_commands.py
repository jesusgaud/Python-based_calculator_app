import pytest
from unittest.mock import MagicMock
from app.commands import CommandHandler, Command

class MockCommand(Command):
    """Mock command implementing the execute method."""
    def execute(self):
        return "Mock Execution"

def test_command_handler_register():
    """Test registering commands."""
    handler = CommandHandler()
    command = MockCommand()

    handler.register_command("mock_command", command)

    assert "mock_command" in handler.commands
    assert handler.commands["mock_command"] is command

def test_command_handler_execute():
    """Test executing registered command."""
    handler = CommandHandler()
    command = MagicMock(spec=MockCommand)

    handler.register_command("mock_command", command)
    handler.execute_command("mock_command")

    command.execute.assert_called_once()

def test_command_handler_execute_unknown(capsys):
    """Test execution of an unknown command."""
    handler = CommandHandler()

    handler.execute_command("unknown_command")
    captured = capsys.readouterr()

    assert "Unknown command. Type 'menu' for a list of commands." in captured.out

def test_abstract_command():
    """Ensure `Command` cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Command()
