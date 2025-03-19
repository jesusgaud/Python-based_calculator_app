import importlib
import logging
import os
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent

def load_plugins():
    """Dynamically load available plugins and return a list of loaded modules."""
    plugins = []
    sys.path.insert(0, str(PLUGIN_DIR))  # Ensure plugin directory is in path

    for plugin_file in PLUGIN_DIR.glob("*.py"):
        if plugin_file.stem == "__init__":
            continue  # Skip __init__.py

        module_name = f"app.plugins.{plugin_file.stem}"

        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "commands") and isinstance(module.commands, dict):
                plugins.append(module)
            else:
                logging.error(f"Plugin {module_name} missing 'commands' dict.")
        except ImportError as e:
            logging.error(f"Failed to load plugin {module_name}: {e}")

    return plugins
