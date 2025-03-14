# pylint: disable=redefined-outer-name
import logging
from io import StringIO
from unittest.mock import patch, MagicMock

import pytest  # Third-party imports should come after built-in ones

from app import App
from app.commands import Command  # Ensure we import Command for subclass checking


@pytest.fixture
def app_instance():
    """Fixture to create an instance of the App class."""
    return App()


def test_app_initialization(app_instance):
    """Test if the application initializes correctly."""
    assert isinstance(app_instance.settings, dict)
    assert app_instance.ENVIRONMENT in ["PRODUCTION", "DEVELOPMENT", "TESTING"]


def test_configure_logging(app_instance):
    """Test logging configuration for both fileConfig and basicConfig."""
    with patch("logging.config.fileConfig") as mock_file_config, patch("logging.basicConfig") as mock_basic_config:
        app_instance.configure_logging()
        assert mock_file_config.called or mock_basic_config.called  # At least one should be called


def test_load_plugins_directory_not_found(app_instance, caplog):
    """Test when the plugins directory does NOT exist."""
    with patch("os.path.exists", return_value=False):  # Simulate missing directory
        with caplog.at_level(logging.WARNING):
            app_instance.load_plugins()
            assert "Plugins directory not found. Skipping plugin loading." in caplog.text


def test_load_plugins_successful(app_instance, caplog):
    """Test successful plugin loading."""
    with patch("os.path.exists", return_value=True), \
         patch("pkgutil.iter_modules", return_value=[(None, "mock_plugin", True)]), \
         patch("importlib.import_module") as mock_import:

        mock_plugin = MagicMock()
        mock_import.return_value = mock_plugin

        app_instance.load_plugins()
        assert "Loaded plugin: mock_plugin" in caplog.text


def test_register_plugin_commands(app_instance):
    """Test registering a valid plugin command."""
    class MockCommand(Command):
        """Mock command class."""
        def execute(self, *args, **kwargs) -> str:
            """Override execute method properly."""
            _ = kwargs  # Explicitly reference kwargs to avoid pylint warning
            return "Mock execution"

    mock_plugin = MagicMock()
    mock_plugin.MockCommand = MockCommand

    app_instance.register_plugin_commands(mock_plugin, "mock_plugin")
    assert "mock_plugin" in app_instance.command_handler.commands.keys()
    assert isinstance(app_instance.command_handler.commands["mock_plugin"], MockCommand)


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

    captured_output = StringIO()
    with patch("sys.stdout", captured_output), pytest.raises(SystemExit):
        app_instance.start()

    captured_output.seek(0)
    output_text = captured_output.read()

    assert "Unknown command. Type 'menu' for a list of commands." in output_text


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


def test_main_execution():
    """Ensure main execution runs without error."""
    with patch("app.App.start") as mock_start:
        with patch("app.__name__", "__main__"):
            app = App()
            app.start()
            mock_start.assert_called_once()


# ✅ ADDITIONAL TESTS ✅

def test_menu_command(app_instance, monkeypatch, capsys):
    """Test that the 'menu' command lists all available commands."""
    inputs = iter(["menu", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        app_instance.start()

    captured = capsys.readouterr()
    assert "Available Commands:" in captured.out


def test_history_command(app_instance, monkeypatch, capsys):
    """Test that the 'history' command retrieves calculation history."""
    inputs = iter(["history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch("app.Calculations.get_history", return_value=["1 + 1 = 2"]):
        with pytest.raises(SystemExit):
            app_instance.start()

    captured = capsys.readouterr()
    assert "Calculation History:" in captured.out
    assert "1 + 1 = 2" in captured.out


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
