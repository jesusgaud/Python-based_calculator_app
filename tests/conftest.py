# conftest.py
import os
import pytest
from decimal import Decimal
from faker import Faker
from app import start, configure_logging  # ✅ Import start() and configure_logging() instead of App
from app.math_operations import add, subtract, multiply, divide
from app.calculations_global import Calculations

# ✅ Faker for generating test data
fake = Faker()
HISTORY_FILE = "history.csv"

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Ensures logging is configured before any test runs."""
    configure_logging()  # ✅ Call configure_logging() once at the start of the test session

@pytest.fixture(autouse=True)
def clean_history():
    """Ensures test isolation by clearing calculation history before each test."""
    calc_instance = Calculations()
    calc_instance.clear_history()
    yield calc_instance  # ✅ Return instance for test use
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

@pytest.fixture(params=range(10))  # ✅ Generates test data 10 times
def generate_test_data(request):
    """Fixture to generate test data for Calculator tests."""
    operation_mappings = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    a = Decimal(fake.random_number(digits=2))
    b = Decimal(fake.random_number(digits=2)) if request.param % 4 != 3 else Decimal(1)
    operation_name = fake.random_element(elements=list(operation_mappings.keys()))
    operation_func = operation_mappings[operation_name]

    if callable(operation_func) and operation_func is divide and b == Decimal(0):
        b = Decimal(1)

    try:
        expected = operation_func(a, b)
    except ZeroDivisionError:
        expected = "ZeroDivisionError"

    return a, b, operation_name, operation_func, expected
