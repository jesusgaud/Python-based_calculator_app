import os
import sys
import logging
import logging.config
import pkgutil
import importlib
from dotenv import load_dotenv  # Third-party package
from app.commands import CommandHandler, Command  # Import the CommandHandler class from the commands module
from .calculation import Calculation
from .calculations import Calculations
from .operations import add, subtract, multiply, divide

class App:
    """Main application class that loads environment variables, plugins, and executes commands."""

    def __init__(self):
        """Initialize the application, configure logging, and load settings."""
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()

        self.settings = dict(os.environ.items())  # Load environment variables into a dictionary
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')

        self.ENVIRONMENT = self.settings.get("ENVIRONMENT", "PRODUCTION")
        self.command_handler = CommandHandler()

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
                    logging.info("Loaded plugin: %s", plugin_name)
                except ImportError as e:
                    logging.error("Failed to load plugin %s: %s", plugin_name, e)

    def register_plugin_commands(self, plugin_module, plugin_name):
        """Register commands from dynamically loaded plugins."""
        registered = False
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                self.command_handler.register_command(plugin_name, item())
                logging.info("Registered command from plugin: %s", plugin_name)
                registered = True

        if not registered:
            logging.warning("No valid commands found in plugin: %s", plugin_name)

    def start(self):
        """Start the interactive command loop (REPL mode)."""
        self.load_plugins()
        logging.info("Application started. Type 'exit' to quit.")

        try:
            while True:
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    logging.info("Application exit.")
                    sys.exit(0)

                try:
                    self.command_handler.execute_command(cmd_input)
                except KeyError:
                    logging.error("Unknown command: %s", cmd_input)
        except KeyboardInterrupt:
            logging.info("Application interrupted. Exiting gracefully.")
            sys.exit(0)
        finally:
            logging.info("Application shutdown.")

if __name__ == "__main__":
    app = App()
    app.start()
