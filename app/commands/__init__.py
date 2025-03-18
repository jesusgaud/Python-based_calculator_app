from abc import ABC, abstractmethod
from app.math_operations import add, subtract, multiply, divide
from app.calculations_global import Calculations, Calculation

class Command(ABC):
    """Abstract base class for all command implementations."""

    @abstractmethod
    def execute(self, *args):
        """Abstract method that must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the execute method.")

class CommandHandler:
    """Handles command registration and execution."""

    def __init__(self):
        """Initializes an empty dictionary to store commands."""
        self.commands = {}
        self.register_command("menu", MenuCommand(self))
        self.register_command("add", AddCommand())
        self.register_command("subtract", SubtractCommand())
        self.register_command("multiply", MultiplyCommand())
        self.register_command("divide", DivideCommand())
        self.register_command("history", HistoryCommand())

    def register_command(self, command_name: str, command: Command):
        """Registers a command with a given name."""
        self.commands[command_name] = command

    def execute_command(self, command_name: str, *args):
        """
        Executes a registered command with optional arguments.
        """
        try:
            command = self.commands[command_name]
            command.execute(*args)
        except KeyError:
            print("Unknown command. Type 'menu' for a list of commands.")

class MenuCommand(Command):
    """Command that lists all available commands."""

    def __init__(self, command_handler: CommandHandler):
        """Receives a reference to the command handler to list available commands."""
        self.command_handler = command_handler

    def execute(self, *args):
        """Displays all registered commands."""
        print("\nAvailable Commands:")
        for command in self.command_handler.commands.keys():
            print(f"- {command}")
        print("Type 'exit' to quit.")

class AddCommand(Command):
    """Command to handle addition."""

    def execute(self, *args):
        """Executes the add command with two numbers."""
        if len(args) != 2:
            print("Usage: add <num1> <num2>")
            return
        try:
            num1, num2 = map(float, args)
            result = add(num1, num2)
            Calculations().add_calculation(Calculation(num1, num2, add, "add"))
            print(f"{num1:g} + {num2:g} = {result:g}")
        except ValueError:
            print("Invalid number input. Use numeric values.")

class SubtractCommand(Command):
    """Command to handle subtraction."""

    def execute(self, *args):
        if len(args) != 2:
            print("Usage: subtract <num1> <num2>")
            return
        try:
            num1, num2 = map(float, args)
            result = subtract(num1, num2)
            Calculations().add_calculation(Calculation(num1, num2, subtract, "subtract"))
            print(f"{num1:g} - {num2:g} = {result:g}")
        except ValueError:
            print("Invalid number input. Use numeric values.")

class MultiplyCommand(Command):
    """Command to handle multiplication."""

    def execute(self, *args):
        if len(args) != 2:
            print("Usage: multiply <num1> <num2>")
            return
        try:
            num1, num2 = map(float, args)
            result = multiply(num1, num2)
            Calculations().add_calculation(Calculation(num1, num2, multiply, "multiply"))
            print(f"{num1:g} x {num2:g} = {result:g}")
        except ValueError:
            print("Invalid number input. Use numeric values.")

class DivideCommand(Command):
    """Command to handle division."""

    def execute(self, *args):
        if len(args) != 2:
            print("Usage: divide <num1> <num2>")
            return
        try:
            num1, num2 = map(float, args)
            if num2 == 0:
                print("Error: Cannot divide by zero.")
                return
            result = divide(num1, num2)
            Calculations().add_calculation(Calculation(num1, num2, divide, "divide"))
            print(f"{num1:g} / {num2:g} = {result:g}")
        except ValueError:
            print("Invalid number input. Use numeric values.")

class HistoryCommand(Command):
    """Command to display calculation history."""

    def execute(self):
        history = Calculations().get_history()
        if not history:
            print("No calculation history available.")
            return
        print("\nCalculation History:")
        for record in history:
            print(record)
