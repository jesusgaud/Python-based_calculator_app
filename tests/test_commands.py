import pytest
from app.math_operations import add, subtract, multiply, divide
from app.calculations_global import Calculations, Calculation

from app.commands import (
    CommandHandler, MenuCommand, AddCommand, SubtractCommand,
    MultiplyCommand, DivideCommand, HistoryCommand
)

@pytest.fixture
def command_handler():
    return CommandHandler()

def test_menu_command(command_handler, capsys):
    command_handler.execute_command("menu")
    captured = capsys.readouterr()
    assert "Available Commands:" in captured.out
    assert "- menu" in captured.out
    assert "- add" in captured.out
    assert "- subtract" in captured.out
    assert "- multiply" in captured.out
    assert "- divide" in captured.out
    assert "- history" in captured.out

def test_add_command(command_handler, capsys):
    command_handler.execute_command("add", "2", "3")
    captured = capsys.readouterr()
    assert "2 + 3 = 5" in captured.out

def test_add_command_invalid_args(command_handler, capsys):
    command_handler.execute_command("add", "2")
    captured = capsys.readouterr()
    assert "Usage: add <num1> <num2>" in captured.out

def test_subtract_command(command_handler, capsys):
    command_handler.execute_command("subtract", "5", "3")
    captured = capsys.readouterr()
    assert "5 - 3 = 2" in captured.out

def test_subtract_command_invalid_args(command_handler, capsys):
    command_handler.execute_command("subtract", "5")
    captured = capsys.readouterr()
    assert "Usage: subtract <num1> <num2>" in captured.out

def test_multiply_command(command_handler, capsys):
    command_handler.execute_command("multiply", "2", "3")
    captured = capsys.readouterr()
    assert "2 x 3 = 6" in captured.out

def test_multiply_command_invalid_args(command_handler, capsys):
    command_handler.execute_command("multiply", "2")
    captured = capsys.readouterr()
    assert "Usage: multiply <num1> <num2>" in captured.out

def test_divide_command(command_handler, capsys):
    command_handler.execute_command("divide", "6", "3")
    captured = capsys.readouterr()
    assert "6 / 3 = 2" in captured.out

def test_divide_command_invalid_args(command_handler, capsys):
    command_handler.execute_command("divide", "6")
    captured = capsys.readouterr()
    assert "Usage: divide <num1> <num2>" in captured.out

def test_divide_command_divide_by_zero(command_handler, capsys):
    command_handler.execute_command("divide", "6", "0")
    captured = capsys.readouterr()
    assert "Error: Cannot divide by zero." in captured.out

def test_history_command(command_handler, capsys):
    command_handler.execute_command("add", "2", "3")
    command_handler.execute_command("history")
    captured = capsys.readouterr()
    assert "Calculation History:" in captured.out
    assert "2 + 3 = 5" in captured.out

def test_history_command_no_history(command_handler, capsys):
    command_handler.execute_command("history")
    captured = capsys.readouterr()
    assert "No calculation history available." in captured.out

def test_unknown_command(command_handler, capsys):
    command_handler.execute_command("unknown")
    captured = capsys.readouterr()
    assert "Unknown command. Type 'menu' for a list of commands." in captured.out
