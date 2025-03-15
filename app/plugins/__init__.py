import os
import pkgutil
import importlib
import logging
from app.commands import CommandHandler, Command

def load_plugins(command_handler: CommandHandler):
    """Dynamically discovers and loads all plugins in the `app/plugins` directory."""
    plugins_package = "app.plugins"
    plugins_path = os.path.dirname(__file__)

    for _, module_name, is_pkg in pkgutil.iter_modules([plugins_path]):
        if not is_pkg:  # Only load Python files, not subdirectories
            try:
                plugin_module = importlib.import_module(f"{plugins_package}.{module_name}")
                register_plugin_commands(plugin_module, command_handler)
                logging.info(f"Loaded plugin: {module_name}")
            except ImportError as e:
                logging.error(f"Failed to load plugin {module_name}: {e}")

def register_plugin_commands(plugin_module, command_handler: CommandHandler):
    """Registers commands found in the plugin module."""
    registered = False
    for attr_name in dir(plugin_module):
        attr = getattr(plugin_module, attr_name)
        if isinstance(attr, type) and issubclass(attr, Command) and attr is not Command:
            command_name = plugin_module.__name__.split('.')[-1]
            command_handler.register_command(attr_name.lower(), attr())
            logging.info(f"Registered plugin command: {attr_name.lower()}")
            registered = True

    if not registered:
        logging.warning(f"No valid commands found in plugin: {plugin_module.__name__}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ch = CommandHandler()
    load_plugins(ch)
    print("Registered Commands:", list(ch.commands.keys()))
