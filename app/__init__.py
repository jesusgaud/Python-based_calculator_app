import os
import sys
import logging
import logging.config
from dotenv import load_dotenv

# ✅ Delayed Imports to prevent circular dependency
def lazy_imports():
    global CommandHandler, load_plugins, Calculations, Calculation, add, subtract, multiply, divide
    from app.commands import CommandHandler
    from app.plugins import load_plugins
    from app.calculations_global import Calculations, Calculation
    from app.operations import add, subtract, multiply, divide

class App:
    """Main application class that loads environment variables, plugins, and executes commands."""

    command_handler = None  # ✅ Prevent multiple instances

    def __init__(self):
        """Initialize the application, configure logging, and load settings."""
        lazy_imports()  # ✅ Load dynamically to prevent circular imports

        os.makedirs('logs', exist_ok=True)
        self.configure_logging()  # ✅ Ensure logging is configured
        load_dotenv()

        self.settings = dict(os.environ.items())  # Load environment variables into a dictionary
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')

        self.ENVIRONMENT = self.settings.get("ENVIRONMENT", "PRODUCTION")

        if App.command_handler is None:
            App.command_handler = CommandHandler()  # ✅ Initialize only once

        self.register_commands()  # ✅ Ensure commands are registered

        logging.info("Running in %s mode", self.ENVIRONMENT)

    def configure_logging(self):
        """Configure logging from file or set up basic logging."""
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler()]
            )
        logging.info("Logging configured.")

    def register_commands(self):
        """Register all available commands."""
        from app.operations import add, subtract, multiply, divide
        from app.commands import Command
        from app.calculations_global import Calculations, Calculation

        class AddCommand(Command):
            """Command to handle addition."""
            def execute(self, *args):
                if len(args) != 2:
                    print("Usage: add <num1> <num2>")
                    return
                try:
                    num1, num2 = map(float, args)
                    result = add(num1, num2)
                    Calculations().add_calculation(Calculation(num1, num2, add, "add"))  # ✅ Fix
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
                    Calculations().add_calculation(Calculation(num1, num2, subtract, "subtract"))  # ✅ Fix
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
                    Calculations().add_calculation(Calculation(num1, num2, multiply, "multiply"))  # ✅ Fix
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
                    Calculations().add_calculation(Calculation(num1, num2, divide, "divide"))  # ✅ Fix
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

        # ✅ Register commands dynamically
        commands = {
            "add": AddCommand(),
            "subtract": SubtractCommand(),
            "multiply": MultiplyCommand(),
            "divide": DivideCommand(),
            "history": HistoryCommand(),  # ✅ Fix: Ensure history command is registered
        }
        for cmd, instance in commands.items():
            App.command_handler.register_command(cmd, instance)

    def start(self):
        """Start the interactive command loop (REPL mode)."""
        logging.info("Application started. Type 'exit' to quit.")
        try:
            while True:
                cmd_input = input(">>> ").strip().split()
                if not cmd_input:
                    continue
                command = cmd_input[0]
                args = cmd_input[1:]

                if command.lower() == 'exit':
                    logging.info("Application exit.")
                    sys.exit(0)

                try:
                    App.command_handler.execute_command(command, *args)
                except KeyError:
                    logging.error("Unknown command: %s", command)
                    print("Unknown command. Type 'menu' for a list of commands.")
        except KeyboardInterrupt:
            logging.info("Application interrupted. Exiting gracefully.")
            sys.exit(0)
        finally:
            logging.info("Application shutdown.")

__all__ = ["App"]
