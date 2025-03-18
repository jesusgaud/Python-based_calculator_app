import pytest
import os
import sys
import logging
import pandas as pd
from unittest.mock import patch, MagicMock
from decimal import Decimal
from app import App
from app.calculations_global import Calculations, Calculation
from app.commands import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand, HistoryCommand

HISTORY_FILE = "history.csv"

@pytest.fixture(scope="session", autouse=True)
def import_app():
    """Return an instance of the App class."""
    return App()

@pytest.fixture
def clean_calculations():
    """Fixture to clear history before each test."""
    calc_instance = Calculations()
    calc_instance.clear_history()
    return calc_instance

# ✅ TEST APP INITIALIZATION
def test_app_initialization(import_app):
    """Test if the application initializes correctly."""
    app_instance = import_app
    assert isinstance(app_instance.settings, dict)
    assert app_instance.ENVIRONMENT in ["PRODUCTION", "DEVELOPMENT", "TESTING"]

# ✅ TEST LOGGING CONFIGURATION
def test_configure_logging_file_exists(import_app):
    """Test logging configuration when logging.conf exists."""
    app_instance = import_app
    with patch("os.path.exists", return_value=True), patch("logging.config.fileConfig") as mock_file_config:
        app_instance.configure_logging()
        mock_file_config.assert_called_once()

def test_configure_logging_file_not_exists(import_app):
    """Test logging configuration when logging.conf does not exist."""
    app_instance = import_app
    with patch("os.path.exists", return_value=False), patch("logging.basicConfig") as mock_basic_config:
        app_instance.configure_logging()
        mock_basic_config.assert_called_once()

# ✅ TEST COMMAND REGISTRATION
def test_register_commands(import_app):
    """Test that commands are registered correctly."""
    app_instance = import_app
    expected_commands = {"add", "subtract", "multiply", "divide", "history"}
    assert set(app_instance.command_handler.commands.keys()) >= expected_commands

# ✅ TEST ADD COMMAND
def test_add_command_valid_input(capsys):
    """Test the AddCommand with valid input."""
    add_command = AddCommand()
    add_command.execute("5", "3")
    captured = capsys.readouterr()
    assert "5 + 3 = 8" in captured.out

def test_add_command_missing_arguments(capsys):
    """Test AddCommand prints usage instructions when arguments are missing."""
    add_command = AddCommand()

    # Case 1: No arguments provided
    add_command.execute()
    captured = capsys.readouterr()
    assert "Usage: add <num1> <num2>" in captured.out

    # Case 2: Only one argument provided
    add_command.execute("5")
    captured = capsys.readouterr()
    assert "Usage: add <num1> <num2>" in captured.out

def test_add_command_invalid_number(capsys):
    """Test the AddCommand with non-numeric input."""
    add_command = AddCommand()
    add_command.execute("five", "three")
    captured = capsys.readouterr()
    assert "Invalid number input. Use numeric values." in captured.out

# ✅ TEST SUBTRACT COMMAND
def test_subtract_command_valid_input(capsys):
    """Test the SubtractCommand with valid input."""
    subtract_command = SubtractCommand()
    subtract_command.execute("8", "2")
    captured = capsys.readouterr()
    assert "8 - 2 = 6" in captured.out

# ✅ TEST MULTIPLY COMMAND
def test_multiply_command_valid_input(capsys):
    """Test the MultiplyCommand with valid input."""
    multiply_command = MultiplyCommand()
    multiply_command.execute("4", "3")
    captured = capsys.readouterr()
    assert "4 x 3 = 12" in captured.out

# ✅ TEST DIVIDE COMMAND
def test_divide_command_valid_input(capsys):
    """Test the DivideCommand with valid input."""
    divide_command = DivideCommand()
    divide_command.execute("10", "2")
    captured = capsys.readouterr()
    assert "10 / 2 = 5" in captured.out

def test_divide_command_zero_division(capsys):
    """Test DivideCommand for division by zero."""
    divide_command = DivideCommand()
    divide_command.execute("10", "0")
    captured = capsys.readouterr()
    assert "Error: Cannot divide by zero." in captured.out

# ✅ TEST HISTORY COMMAND
def test_history_command_no_history(capsys):
    """Test the HistoryCommand when there is no history."""
    history_command = HistoryCommand()
    history_command.execute()
    captured = capsys.readouterr()
    assert "No calculation history available." in captured.out

def test_history_command_with_entries(clean_calculations, capsys):
    """Test the HistoryCommand when there are history entries."""
    calc_instance = Calculations()
    calc_instance.add_calculation(Calculation(Decimal(10), Decimal(5), "add", Decimal(15)))
    history_command = HistoryCommand()
    history_command.execute()
    captured = capsys.readouterr()
    assert "10 + 5 = 15" in captured.out or "Calculation(10, 5, add, 15)" in captured.out

# ✅ TEST MENU COMMAND
def test_menu_command(capsys, import_app):
    """Test that the 'menu' command lists all available commands."""
    app_instance = import_app
    app_instance.command_handler.execute_command("menu")
    captured = capsys.readouterr()
    assert "Available Commands:" in captured.out
    assert "- add" in captured.out
    assert "- subtract" in captured.out
    assert "- multiply" in captured.out
    assert "- divide" in captured.out
    assert "- history" in captured.out
    assert "- menu" in captured.out  # Menu should be listed itself

# ✅ TEST REPL COMMAND EXECUTION
@pytest.mark.skip(reason="sys.exit() terminates the test")
def test_start_method_exit(monkeypatch, import_app):
    """Test that 'exit' command stops the REPL loop."""
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    with pytest.raises(SystemExit):
        app_instance = import_app
        app_instance.start()

def test_start_method_unknown_command(monkeypatch, import_app):
    """Test handling of unknown commands in the REPL."""
    inputs = iter(["unknown_command", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(SystemExit):
        app_instance = import_app
        app_instance.start()

# ✅ TEST BASIC OPERATIONS IN REPL
def test_basic_operations(monkeypatch, capsys, import_app):
    """Test that basic operations (add, subtract, multiply, divide) work in the REPL."""
    app_instance = import_app
    inputs = iter(["add 5 3", "subtract 8 2", "multiply 4 3", "divide 10 2", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(SystemExit):
        app_instance.start()
    captured = capsys.readouterr()
    assert "5 + 3 = 8" in captured.out
    assert "8 - 2 = 6" in captured.out
    assert "4 x 3 = 12" in captured.out
    assert "10 / 2 = 5" in captured.out

# ✅ TEST HISTORY PERSISTENCE
def test_history_persistence(clean_calculations):
    """Ensure history persists across app instances."""
    calc_instance = Calculations()
    calc_instance.add_calculation(Calculation(Decimal(10), Decimal(5), "add", Decimal(15)))
    new_instance = Calculations()
    assert len(new_instance.get_history()) == 1
    df = pd.read_csv(HISTORY_FILE)
    assert "add" in df["operation"].values
