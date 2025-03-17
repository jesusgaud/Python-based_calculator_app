# conftest.py
import os
from decimal import Decimal
import pytest
from faker import Faker
from app.math_operations import add, subtract, multiply, divide  # ✅ Use direct function imports
from app.calculations_global import Calculations

fake = Faker()

HISTORY_FILE = "history.csv"

def generate_test_data(num_records):
    """Generates test data for both Calculator and Calculation tests."""
    # Define operation mappings
    operation_mappings = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2)) if _ % 4 != 3 else Decimal(1)  # Prevent zero in division
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_name]

        if callable(operation_func) and operation_func is divide and b == Decimal(0):
            b = Decimal(1)

        try:
            expected = operation_func(a, b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"

        yield a, b, operation_name, operation_func, expected

@pytest.fixture(autouse=True)
def clean_history():
    """Ensures test isolation by clearing calculation history before each test."""
    calc_instance = Calculations()
    calc_instance.clear_history()
    yield
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
