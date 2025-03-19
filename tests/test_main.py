import pytest
import sys
import multiprocessing
from decimal import Decimal
from unittest.mock import patch
from app.calculations_global import Calculations
from main import execute_command, handle_non_math_commands, interactive_mode

@pytest.fixture
def history_manager():
    """Provides a fresh history manager instance for tests."""
    history = Calculations()
    history.clear_history()
    return history

# ✅ Test multiprocessing execution in `execute_command()`
def test_execute_command_multiprocessing(history_manager, capsys):
    """Test execute_command using multiprocessing."""
    with patch("multiprocessing.Process.start") as mock_start, patch("multiprocessing.Process.join") as mock_join:
        execute_command("5", "3", "add", history_manager, test_mode=False)
        mock_start.assert_called_once()
        mock_join.assert_called_once()

# ✅ Test `handle_non_math_commands()` for `greet`
def test_handle_non_math_commands_greet(monkeypatch, capsys):
    """Test greet command handling."""
    monkeypatch.setattr("builtins.input", lambda _: "John")
    handle_non_math_commands("greet")
    captured = capsys.readouterr()
    assert "Hello, John! Welcome to the calculator." in captured.out

# ✅ Test `handle_non_math_commands()` for invalid command
def test_handle_non_math_commands_invalid(capsys):
    """Test handling of an unknown command."""
    handle_non_math_commands("unknown")
    captured = capsys.readouterr()
    assert "Unknown command: unknown" in captured.out  # ✅ Fix: Ensure correct string comparison

# ✅ Test `interactive_mode()` exit scenario
def test_interactive_mode_exit(monkeypatch, capsys):
    """Simulate user typing `exit` to leave interactive mode."""
    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(SystemExit):  # ✅ Fix: Now expects `SystemExit`
        interactive_mode()
    captured = capsys.readouterr()
    assert "Exiting calculator. Goodbye!" in captured.out
