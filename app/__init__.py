import os
import sys
import logging
import logging.config
import pkgutil
import importlib
from dotenv import load_dotenv  # Third-party package
from app.commands import CommandHandler, Command  # Import CommandHandler
from app.plugins import load_plugins  # Import load_plugins
from app.plugins.modulus import ModulusCommand
from app.plugins.power import PowerCommand
from app.plugins.greet import GreetCommand
from .calculations import Calculations
from .operations import add, subtract, multiply, divide

class AddCommand(Command):
    """Command to handle addition."""
    def execute(self, *args):
        if len(args) != 2:
            print("Usage: add <num1> <num2>")
            return
        try:
            num1, num2 = map(float, args)
            result = add(num1, num2)
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
            print(f"{num1:g} / {num2:g} = {result:g}")
        except ValueError:
            print("Invalid number input. Use numeric values.")

class HistoryCommand(Command):
    """Command to display calculation history."""
    def execute(self):
        try:
            history = Calculations.get_history()
            if not history:
                print("No calculation history available.")
                return
            print("\nCalculation History:")
            for record in history:
                print(record)
        except Exception as e:
            logging.error("Error retrieving history: %s", str(e))

class GreetCommand(Command):
    """Command for greeting a user."""
    def execute(self, *args):
        if not args:
            print("Usage: greet <name>")
            return
        name = " ".join(args)  # Allow multiple words as name
        print(f"Hello, {name}! Welcome to the calculator.")

class App:
    """Main application class that loads environment variables, plugins, and executes commands."""

    command_handler = CommandHandler()  # ✅ Global Command Handler

    def __init__(self):
        """Initialize the application, configure logging, and load settings."""
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()

        self.settings = dict(os.environ.items())  # Load environment variables into a dictionary
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')

        self.ENVIRONMENT = self.settings.get("ENVIRONMENT", "PRODUCTION")

        load_plugins(App.command_handler)

        App.command_handler.register_command("add", AddCommand())
        App.command_handler.register_command("subtract", SubtractCommand())
        App.command_handler.register_command("multiply", MultiplyCommand())
        App.command_handler.register_command("divide", DivideCommand())
        App.command_handler.register_command("history", HistoryCommand())
        App.command_handler.register_command("menu", MenuCommand(App.command_handler))

        if "modulus" in App.command_handler.commands:
            App.command_handler.register_command("modulus", ModulusCommand())

        if "power" in App.command_handler.commands:
            App.command_handler.register_command("power", PowerCommand())

        if "greet" in App.command_handler.commands:
            App.command_handler.register_command("greet", GreetCommand())

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

    def load_plugins(self):
        """Dynamically discover and load plugins from the plugins directory."""
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning("Plugins directory not found. Skipping plugin loading.")
            return

        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                    logging.info(f"Loaded plugin: {plugin_name}")
                except ImportError as e:
                    logging.error(f"Failed to load plugin {plugin_name}: {e}")
        print("Registered Commands:", list(self.command_handler.commands.keys()))

    def register_plugin_commands(self, plugin_module, plugin_name):
        """Register commands from dynamically loaded plugins."""
        registered = False
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                self.command_handler.register_command(plugin_name, item())
                logging.info(f"Registered command from plugin: {plugin_name}")
                print(f"Registered Plugin: {plugin_name}")
                registered = True

        if not registered:
            logging.warning(f"No valid commands found in plugin: {plugin_name}")
            if plugin_name in self.command_handler.commands:
                del self.command_handler.commands[plugin_name]  # Remove invalid plugin command

    def start(self):
        """Start the interactive command loop (REPL mode)."""
        self.load_plugins()
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

class MenuCommand(Command):
    """Command to display all available commands."""

    def __init__(self, command_handler):
        """Receives a reference to the command handler to list available commands."""
        self.command_handler = command_handler

    def execute(self, *args):
        """Displays all registered commands."""
        print("\nAvailable Commands:")
        for command in self.command_handler.commands.keys():
            print(f"- {command}")
        print("Type 'exit' to quit.")

if __name__ == "__main__":
    app = App()
    app.start()
