from decimal import Decimal
from app.commands import Command
from app.math_operations import modulus

class ModulusCommand(Command):
    """Command to calculate the modulus (remainder of division)."""
    def execute(self, *args):
        if len(args) != 2:
            print("Usage: modulus <num1> <num2>")
            return
        try:
            num1, num2 = map(int, args)
            result = modulus(num1, num2)
            print(f"{num1} % {num2} = {result}")
        except ValueError:
            print("Invalid input. Use numeric values.")
        except ZeroDivisionError:
            print("Error: Cannot calculate modulus by zero.")
