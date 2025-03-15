from decimal import Decimal
from app.commands import Command
from app.operations import modulus

class ModulusCommand(Command):
    """Command to calculate modulus (remainder)."""

    def execute(self, *args):
        if len(args) != 2:
            print("Usage: modulus <num1> <num2>")
            return
        try:
            num1, num2 = map(int, args)
            print(f"{num1} % {num2} = {modulus(num1, num2)}")  # ✅ Uses the function
        except ValueError:
            print("Invalid input. Use numeric values.")

def operation(a: Decimal, b: Decimal) -> Decimal:
    """Perform modulus operation."""
    return a % b  # Ensures compatibility with tests
