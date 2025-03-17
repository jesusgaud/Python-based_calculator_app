import os
import importlib
import sys
import logging
from decimal import Decimal
from typing import Dict, Callable, Union, Optional
from app.math_operations import add, subtract, multiply, divide  # ✅ Fixed imports

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_calculation_class():
    """Avoid circular imports by loading Calculation inside the function."""
    from app.calculations_global import Calculation
    return Calculation

def get_history_manager():
    """Avoid circular imports by loading Calculations inside the function."""
    from app.calculations_global import Calculations
    return Calculations()

class AddOperation:
    """Command for addition."""
    @staticmethod
    def execute(a: Decimal, b: Decimal) -> Decimal:
        result = add(a, b)
        Calculation = get_calculation_class()
        history_manager = get_history_manager()
        history_manager.add_calculation(Calculation(a, b, "add", result))
        return result

class SubtractOperation:
    """Command for subtraction."""
    @staticmethod
    def execute(a: Decimal, b: Decimal) -> Decimal:
        result = subtract(a, b)
        Calculation = get_calculation_class()
        history_manager = get_history_manager()
        history_manager.add_calculation(Calculation(a, b, "subtract", result))
        return result

class MultiplyOperation:
    """Command for multiplication."""
    @staticmethod
    def execute(a: Decimal, b: Decimal) -> Decimal:
        result = multiply(a, b)
        Calculation = get_calculation_class()
        history_manager = get_history_manager()
        history_manager.add_calculation(Calculation(a, b, "multiply", result))
        return result

class DivideOperation:
    """Command for division."""
    @staticmethod
    def execute(a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = divide(a, b)
        Calculation = get_calculation_class()
        history_manager = get_history_manager()
        history_manager.add_calculation(Calculation(a, b, "divide", result))
        return result

# Mapping basic operations to their command execution methods.
operations: Dict[str, Callable[..., Union[Decimal, str]]] = {
    "add": AddOperation.execute,
    "subtract": SubtractOperation.execute,
    "multiply": MultiplyOperation.execute,
    "divide": DivideOperation.execute,
}

def execute_operation(a: Decimal, b: Decimal, operation: str, history_manager: Optional["HistoryInterface"] = None) -> Decimal:
    """Executes an operation and returns the result.

    Note: The command classes already add the calculation to history.
    """
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    result = operations[operation](a, b)
    return result

# Dynamically load operation plugins.
PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "plugins")

def load_plugins():
    """Dynamically loads all operation plugins from the plugins directory."""
    global operations

    if not os.path.exists(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR)

    sys.path.insert(0, PLUGIN_DIR)

    from app.math_operations import modulus, power
    operations["modulus"] = modulus
    operations["power"] = power

    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"app.plugins.{module_name}")
                if hasattr(module, "operation"):
                    operations[module_name] = module.operation
                    logging.info(f"Loaded plugin: {module_name}")
            except ImportError as e:
                logging.error(f"Failed to load plugin {module_name}: {e}")

load_plugins()
