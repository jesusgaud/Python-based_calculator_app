# pylint: disable=redefined-outer-name, unused-argument, wrong-import-order
import pytest  # Third-party imports should come after built-in ones
from unittest.mock import MagicMock, patch
from app import App
from app.commands import Command


@pytest.fixture
def app_instance():
    """Fixture to create an instance of the App class."""
    return App()


def test_app_initialization(app_instance):
    """Test if the application initializes correctly."""
    assert isinstance(app_instance.settings, dict)
    assert app_instance.ENVIRONMENT in ["PRODUCTION", "DEVELOPMENT", "TESTING"]


def test_register_plugin_commands(app_instance):
    """Test registering a valid plugin command."""

    class MockCommand(Command):
        """Mock command class."""
        def execute(self, *args, **kwargs):
            """Override execute method properly."""
            _ = args, kwargs  # Avoid Pylint warning
            return "Mock execution"

    mock_plugin = MagicMock()
    mock_plugin.MockCommand = MockCommand

    # ✅ Register the command properly
    app_instance.register_plugin_commands(mock_plugin, "mock_command")

    # ✅ Verify the mock command was registered
    assert "mock_command" in app_instance.command_handler.commands.keys()


def test_register_plugin_commands_no_valid_commands(app_instance, caplog):
    """Test registering plugin commands when there are NO valid commands."""
    mock_plugin = MagicMock()
    app_instance.register_plugin_commands(mock_plugin, "mock_plugin")

    assert "mock_plugin" not in app_instance.command_handler.commands.keys()
    assert "No valid commands found in plugin: mock_plugin" in caplog.text


def test_start_method_exit(app_instance, monkeypatch):
    """Test that 'exit' command stops the REPL loop."""
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    with pytest.raises(SystemExit):
        app_instance.start()


def test_start_method_unknown_command(app_instance, monkeypatch):
    """Test handling of unknown commands in the REPL."""
    inputs = iter(["unknown_command", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        app_instance.start()


def test_start_keyboard_interrupt(app_instance, monkeypatch, caplog):
    """Test handling of KeyboardInterrupt in the REPL."""
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(KeyboardInterrupt))

    with pytest.raises(SystemExit):
        app_instance.start()

    assert "Application interrupted. Exiting gracefully." in caplog.text


def test_start_application_shutdown_logging(app_instance, monkeypatch, caplog):
    """Test final shutdown logging in the REPL."""
    monkeypatch.setattr("builtins.input", lambda _: "exit")

    with pytest.raises(SystemExit):
        app_instance.start()

    assert "Application shutdown." in caplog.text


def test_menu_command(app_instance, capsys):
    """Test that the 'menu' command lists all available commands."""

    # Execute the menu command
    app_instance.command_handler.execute_command("menu")

    # Capture the printed output
    captured = capsys.readouterr()

    # ✅ Verify the expected command list appears
    assert "Available Commands:" in captured.out
    assert "- add" in captured.out
    assert "- subtract" in captured.out
    assert "- multiply" in captured.out
    assert "- divide" in captured.out
    assert "- history" in captured.out
    assert "- menu" in captured.out  # Menu should be listed itself


def test_history_command(app_instance, monkeypatch, capsys):
    """Test that the 'history' command retrieves calculation history."""
    inputs = iter(["history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # ✅ Mock `Calculations.get_history()` to return valid data
    with patch("app.Calculations.get_history", return_value=["5 + 3 = 8"]):
        with pytest.raises(SystemExit):
            app_instance.start()

    captured = capsys.readouterr()
    assert "Calculation History:" in captured.out
    assert "5 + 3 = 8" in captured.out  # ✅ Verify correct history output


def test_basic_operations(app_instance, monkeypatch, capsys):
    """Test that basic operations (add, subtract, multiply, divide) work in the REPL."""
    inputs = iter(["add 5 3", "subtract 8 2", "multiply 4 3", "divide 10 2", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("app.Calculations.get_history", return_value=["5 + 3 = 8", "8 - 2 = 6", "4 * 3 = 12", "10 / 2 = 5"]):
        with pytest.raises(SystemExit):
            app_instance.start()

    captured = capsys.readouterr()
    assert "5 + 3 = 8" in captured.out
    assert "8 - 2 = 6" in captured.out
    assert "4 x 3 = 12" in captured.out
    assert "10 / 2 = 5" in captured.out
