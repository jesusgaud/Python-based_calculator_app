from decimal import Decimal
from app.commands import Command
from app.operations import power

class PowerCommand(Command):
    """Command to calculate exponentiation."""

    def execute(self, *args):
        if len(args) != 2:
            print("Usage: power <base> <exponent>")
            return
        try:
            base, exponent = map(float, args)
            print(f"{base} ^ {exponent} = {base ** exponent}")
        except ValueError:
            print("Invalid input. Use numeric values.")

def operation(a: Decimal, b: Decimal) -> Decimal:
    """Perform exponentiation."""
    return a ** b  # Ensures compatibility with tests
