import importlib
import pkgutil
import logging

# Global registry for plugin commands
PLUGIN_COMMANDS = {}

def load_plugins():
    """Dynamically discovers and imports all modules in the app.plugins package."""
    modules = []
    try:
        import app.plugins  # Ensure the package is recognized
    except ImportError:
        logging.error("app.plugins package not found.")
        return modules  # No plugins will be loaded

    for _, module_name, is_pkg in pkgutil.iter_modules(app.plugins.__path__, app.plugins.__name__ + "."):
        if is_pkg:
            continue  # Ignore subdirectories
        try:
            plugin_module = importlib.import_module(module_name)
            modules.append(plugin_module)
        except Exception as e:
            logging.error(f"Failed to import plugin module {module_name}: {e}")
            continue  # Skip bad plugins, continue loading others

    return modules

def register_plugin_commands():
    """Imports all plugins and registers their commands into PLUGIN_COMMANDS."""
    PLUGIN_COMMANDS.clear()
    modules = load_plugins()
    for module in modules:
        if hasattr(module, "commands") and isinstance(module.commands, dict):
            for cmd_name, cmd_func in module.commands.items():
                PLUGIN_COMMANDS[cmd_name] = cmd_func
        else:
            logging.warning(f"No valid commands found in plugin: {module.__name__}")

    return PLUGIN_COMMANDS
