import pytest
from decimal import Decimal
from app.plugins.modulus import ModulusCommand
from app.plugins.power import PowerCommand
from app.math_operations import modulus, power

@pytest.fixture
def modulus_command():
    """Fixture to create an instance of ModulusCommand."""
    return ModulusCommand()

@pytest.fixture
def power_command():
    """Fixture to create an instance of PowerCommand."""
    return PowerCommand()

# ✅ Test ModulusCommand execution with valid inputs
def test_modulus_command_valid_input(capsys, modulus_command):
    """Test the ModulusCommand with valid input."""
    modulus_command.execute("10", "3")
    captured = capsys.readouterr()
    assert "10 % 3 = 1" in captured.out  # ✅ Ensure correct modulus calculation

# ✅ Test missing arguments for ModulusCommand
def test_modulus_command_missing_arguments(capsys, modulus_command):
    """Test that ModulusCommand prints usage instructions when arguments are missing."""
    modulus_command.execute("10")  # ✅ Only one argument provided
    captured = capsys.readouterr()
    assert "Usage: modulus <num1> <num2>" in captured.out  # ✅ Ensure usage message is printed

# ✅ Test invalid input for ModulusCommand
def test_modulus_command_invalid_number(capsys, modulus_command):
    """Test the ModulusCommand with non-numeric input."""
    modulus_command.execute("ten", "three")
    captured = capsys.readouterr()
    assert "Invalid input. Use numeric values." in captured.out  # ✅ Ensure error message prints

# ✅ Test modulus operation when divisor is zero
def test_modulus_command_zero_divisor(capsys, modulus_command):
    """Test modulus operation when the divisor is zero (should print error message)."""
    modulus_command.execute("10", "0")  # ✅ Calling modulus with zero divisor
    captured = capsys.readouterr()
    assert "Error: Cannot calculate modulus by zero." in captured.out  # ✅ Ensure correct error message

# ✅ Test standalone `modulus` function from `math_operations.py`
def test_math_operations_modulus():
    """Test the `modulus` function from math_operations.py."""
    assert modulus(Decimal(10), Decimal(3)) == Decimal(1)
    assert modulus(Decimal(20), Decimal(6)) == Decimal(2)
    assert modulus(Decimal(100), Decimal(10)) == Decimal(0)
    assert modulus(Decimal(17), Decimal(4)) == Decimal(1)

# ✅ Test modulus function raises ZeroDivisionError when dividing by zero
def test_math_operations_modulus_zero_division():
    """Ensure modulus operation raises ZeroDivisionError when dividing by zero."""
    with pytest.raises(ZeroDivisionError, match="Cannot calculate modulus by zero"):
        modulus(Decimal(10), Decimal(0))

# ✅ Test PowerCommand with valid input
def test_power_command_valid_input(capsys, power_command):
    """Test PowerCommand with valid input."""
    power_command.execute("2", "3")  # ✅ 2^3 = 8
    captured = capsys.readouterr()
    assert "2.0 ^ 3.0 = 8.0" in captured.out  # ✅ Ensure correct output

# ✅ Test PowerCommand with negative exponent
def test_power_command_negative_exponent(capsys, power_command):
    """Test PowerCommand with a negative exponent."""
    power_command.execute("2", "-3")  # ✅ 2^-3 = 0.125
    captured = capsys.readouterr()
    assert "2.0 ^ -3.0 = 0.125" in captured.out

# ✅ Test PowerCommand with base 0
def test_power_command_zero_base(capsys, power_command):
    """Test PowerCommand with base 0."""
    power_command.execute("0", "5")  # ✅ 0^5 = 0
    captured = capsys.readouterr()
    assert "0.0 ^ 5.0 = 0.0" in captured.out

# ✅ Test PowerCommand with exponent 0
def test_power_command_zero_exponent(capsys, power_command):
    """Test PowerCommand with exponent 0."""
    power_command.execute("5", "0")  # ✅ 5^0 = 1
    captured = capsys.readouterr()
    assert "5.0 ^ 0.0 = 1.0" in captured.out

# ✅ Test PowerCommand with non-numeric input
def test_power_command_invalid_input(capsys, power_command):
    """Test PowerCommand with non-numeric input."""
    power_command.execute("two", "three")  # ✅ Should fail
    captured = capsys.readouterr()
    assert "Invalid input. Use numeric values." in captured.out  # ✅ Ensure error message prints

# ✅ Test PowerCommand with missing arguments
def test_power_command_missing_arguments(capsys, power_command):
    """Test PowerCommand with missing arguments."""
    power_command.execute("2")  # ✅ Should fail (missing exponent)
    captured = capsys.readouterr()
    assert "Usage: power <base> <exponent>" in captured.out  # ✅ Ensure correct usage message prints

# ✅ Test PowerCommand with 0^0 (mathematically defined as 1)
def test_power_command_zero_power_zero(capsys, power_command):
    """Test PowerCommand with 0^0 (should return 1 by convention)."""
    power_command.execute("0", "0")
    captured = capsys.readouterr()
    assert "0.0 ^ 0.0 = 1.0" in captured.out  # ✅ 0^0 = 1 by mathematical convention
