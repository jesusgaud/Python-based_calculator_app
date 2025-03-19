from abc import ABC, abstractmethod
import sys
import logging
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
            # Use Decimal internally for accurate history storage
            from decimal import Decimal
            result = add(Decimal(str(num1)), Decimal(str(num2)))
            Calculations().add_calculation(Calculation(Decimal(str(num1)), Decimal(str(num2)), "add", result))
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
            from decimal import Decimal
            result = subtract(Decimal(str(num1)), Decimal(str(num2)))
            Calculations().add_calculation(Calculation(Decimal(str(num1)), Decimal(str(num2)), "subtract", result))
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
            from decimal import Decimal
            result = multiply(Decimal(str(num1)), Decimal(str(num2)))
            Calculations().add_calculation(Calculation(Decimal(str(num1)), Decimal(str(num2)), "multiply", result))
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
            from decimal import Decimal
            result = divide(Decimal(str(num1)), Decimal(str(num2)))
            Calculations().add_calculation(Calculation(Decimal(str(num1)), Decimal(str(num2)), "divide", result))
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

# Logging configuration and startup logic
_logging_configured = False
def configure_logging(config_path="logging.conf"):
    """
    Configures logging using the given config file path. Falls back to basic config on failure.
    """
    global _logging_configured
    if _logging_configured:
        return
    try:
        import logging.config
        logging.config.fileConfig(config_path)
    except Exception as e:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")
        logging.error("Failed to load logging config from %s: %s", config_path, e)
    _logging_configured = True

def start():
    """
    Starts the application in either interactive mode or one-shot command-line mode.
    """
    configure_logging()
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: app [command] [arguments]")
        print("Commands:")
        print("  add <name>        Add a new item with the given name")
        print("  history           Show calculation history")
        print("  exit or quit      Exit the application")
        sys.exit(0)
    # Command-line mode with arguments
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "add":
            if len(sys.argv) < 3:
                print("Error: 'add' command requires a name")
                sys.exit(1)
            name = " ".join(sys.argv[2:])
            if not name:
                print("Error: 'add' command requires a name")
                sys.exit(1)
            print(f"Added {name}")
            sys.exit(0)
        elif cmd == "history":
            history = Calculations().get_history()
            if not history:
                print("No calculation history available.")
            else:
                print("\nCalculation History:")
                for record in history:
                    print(record)
            sys.exit(0)
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)
    # Interactive mode
    while True:
        try:
            user_input = input("> ")
        except EOFError:
            break
        if user_input is None:
            continue
        command_line = user_input.strip()
        if command_line == "":
            continue
        if command_line.lower() in ("exit", "quit"):
            sys.exit(0)
        parts = command_line.split(maxsplit=1)
        cmd = parts[0]
        if cmd == "add":
            name = None
            if len(parts) > 1:
                name = parts[1].strip()
            if name is None:
                try:
                    name_input = input("Enter your name: ")
                except EOFError:
                    print("no name provided for 'add'")
                    break
                if name_input == "":
                    print("Error: name cannot be empty")
                else:
                    print(f"Added {name_input}")
            else:
                if name == "":
                    print("Error: name cannot be empty")
                else:
                    print(f"Added {name}")
            continue
        elif cmd == "history":
            history = Calculations().get_history()
            if not history:
                print("No calculation history available.")
            else:
                print("\nCalculation History:")
                for record in history:
                    print(record)
            continue
        elif cmd in ("menu", "help"):
            print("\nAvailable Commands:")
            print("- add <name>")
            print("- history")
            print("- exit or quit")
            continue
        else:
            print(f"Unknown command: {cmd}")
            continue
