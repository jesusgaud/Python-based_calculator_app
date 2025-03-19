from decimal import Decimal
from typing import Callable, Dict

def add(a: Decimal, b: Decimal) -> Decimal:
    """Return the sum of two numbers."""
    return a + b

def subtract(a: Decimal, b: Decimal) -> Decimal:
    """Return the difference of two numbers (a - b)."""
    return a - b

def multiply(a: Decimal, b: Decimal) -> Decimal:
    """Return the product of two numbers."""
    return a * b

def divide(a: Decimal, b: Decimal) -> Decimal:
    """Return the quotient of a divided by b. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def modulus(a: Decimal, b: Decimal) -> Decimal:
    """Return the remainder of a divided by b. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot calculate modulus by zero")
    return a % b

def power(a: Decimal, b: Decimal) -> Decimal:
    """Return a raised to the power of b."""
    return a ** b

operations: Dict[str, Callable[[Decimal, Decimal], Decimal]] = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "modulus": modulus,
    "power": power
}
