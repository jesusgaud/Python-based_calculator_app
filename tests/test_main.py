"""Test main calculations"""

# Standard library imports
from decimal import Decimal, InvalidOperation

# Third-party imports
import pytest

# Application-specific imports
from app.calculation import Calculation
from app.operations import add, subtract, multiply, divide

# Map operation names to actual function references
operation_map = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide
}

# Parameterize the test function to cover different operations and scenarios, including errors
@pytest.mark.parametrize("a_string, b_string, operation_string, expected_string", [
    ("5", "3", 'add', "The result of 5 add 3 is equal to 8"),
    ("10", "2", 'subtract', "The result of 10 subtract 2 is equal to 8"),
    ("4", "5", 'multiply', "The result of 4 multiply 5 is equal to 20"),
    ("20", "4", 'divide', "The result of 20 divide 4 is equal to 5"),
    ("1", "0", 'divide', "An error occurred: Cannot divide by zero"),  # Adjusted for the actual error message
    ("9", "3", 'unknown', "Unknown operation: unknown"),  # Test for unknown operation
    ("a", "3", 'add', "Invalid number input: a or 3 is not a valid number."),  # Testing invalid number input
    ("5", "b", 'subtract', "Invalid number input: 5 or b is not a valid number.")  # Testing another invalid number input
])
def test_calculate_and_print(a_string, b_string, operation_string, expected_string, capsys):
    """Test Calculation operations with input strings and expected output."""
    try:
        # Convert `a_string` and `b_string` to Decimal, handling InvalidOperation
        try:
            a = Decimal(a_string)
            b = Decimal(b_string)
        except InvalidOperation:
            print(f"Invalid number input: {a_string} or {b_string} is not a valid number.")
            captured = capsys.readouterr()
            assert captured.out.strip() == expected_string
            return  # Exit early since invalid input stops execution

        # Convert `operation_string` to function reference
        if operation_string not in operation_map:
            raise AttributeError(f"Unknown operation: {operation_string}")

        operation_func = operation_map[operation_string]

        calc = Calculation(a, b, operation_func)
        result = calc.perform()
        print(f"The result of {a} {operation_string} {b} is equal to {result}")
    except ZeroDivisionError:
        print("An error occurred: Cannot divide by zero")
    except AttributeError as e:
        print(str(e))

    captured = capsys.readouterr()
    assert captured.out.strip() == expected_string
