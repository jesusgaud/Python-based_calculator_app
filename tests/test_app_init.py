from decimal import Decimal
import pytest
import pandas as pd
from app import App
from app.calculations_global import Calculations, Calculation

HISTORY_FILE = "history.csv"

@pytest.fixture(scope="session", autouse=True)
def import_app():
    # Return the App class (imported at the top-level)
    return App

@pytest.fixture
def clean_calculations():
    """Fixture to clear history before each test."""
    calc_instance = Calculations()
    calc_instance.clear_history()
    return calc_instance

def test_app_initialization(import_app):
    """Test if the application initializes correctly."""
    app_instance = import_app()
    assert isinstance(app_instance.settings, dict)
    assert app_instance.ENVIRONMENT in ["PRODUCTION", "DEVELOPMENT", "TESTING"]

def test_start_method_exit(monkeypatch, import_app):
    """Test that 'exit' command stops the REPL loop."""
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    with pytest.raises(SystemExit):
        app_instance = import_app()
        app_instance.start()

def test_start_method_unknown_command(monkeypatch, import_app):
    """Test handling of unknown commands in the REPL."""
    inputs = iter(["unknown_command", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(SystemExit):
        app_instance = import_app()
        app_instance.start()

def test_menu_command(capsys, import_app):
    """Test that the 'menu' command lists all available commands."""
    app_instance = import_app()
    app_instance.command_handler.execute_command("menu")  # Force reloading of commands
    captured = capsys.readouterr()
    assert "Available Commands:" in captured.out
    assert "- add" in captured.out
    assert "- subtract" in captured.out
    assert "- multiply" in captured.out
    assert "- divide" in captured.out
    assert "- history" in captured.out
    assert "- menu" in captured.out  # Menu should be listed itself

def test_basic_operations(monkeypatch, capsys, import_app):
    """Test that basic operations (add, subtract, multiply, divide) work in the REPL."""
    app_instance = import_app()
    app_instance.command_handler.execute_command("menu")  # Force reload of commands
    inputs = iter(["add 5 3", "subtract 8 2", "multiply 4 3", "divide 10 2", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(SystemExit):
        app_instance.start()
    captured = capsys.readouterr()
    assert "5 + 3 = 8" in captured.out
    assert "8 - 2 = 6" in captured.out
    assert "4 x 3 = 12" in captured.out
    assert "10 / 2 = 5" in captured.out

def test_history_persistence(clean_calculations):
    """Ensure history persists across app instances."""
    calc_instance = Calculations()
    calc_instance.add_calculation(Calculation(Decimal(10), Decimal(5), "add", Decimal(15)))
    new_instance = Calculations()
    assert len(new_instance.get_history()) == 1, "History should persist across instances"
    df = pd.read_csv(HISTORY_FILE)
    assert "add" in df["operation"].values, "CSV should contain the 'add' operation"
