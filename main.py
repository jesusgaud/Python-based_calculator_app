"""Interactive Calculator with History Management & Logging"""
import os
import sys
import logging
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
from app.calculations_global import Calculations, Calculation
from app.operations import operations
import multiprocessing

# Load environment variables and configure logging
load_dotenv()
LOGGING_CONFIG = "logging.conf"
if os.path.exists(LOGGING_CONFIG):
    logging.config.fileConfig(LOGGING_CONFIG)
else:
    logging.basicConfig(
        level=logging.DEBUG if os.getenv("ENVIRONMENT", "production") == "development" else logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        handlers=[logging.StreamHandler()]
    )
logging.info("Application started.")

# Initialize history manager and load past history
history_manager = Calculations()
history_manager.load_history()

def load_commands():
    """Dynamically load available operation commands, including plugins."""
    if not operations:
        logging.error("No operations found. Ensure plugins are properly loaded.")
    return operations

def calculate_and_print(a, b, operation, history_manager):
    """Perform the calculation and output the result (with logging)."""
    cmds = load_commands()
    if operation not in cmds:
        logging.error(f"Unknown operation: {operation}")
        print(f"Unknown operation: {operation}")
        return
    try:
        a_val, b_val = Decimal(a), Decimal(b)
        result = cmds[operation](a_val, b_val)
        history_manager.add_calculation(Calculation(a_val, b_val, operation, result))
        history_manager.save_history()
        logging.info(f"Calculated: {a} {operation} {b} = {result}")
        print(f"The result of {a} {operation} {b} is equal to {result}")
    except ZeroDivisionError:
        logging.error("Error: Cannot divide by zero")
        print("An error occurred: Cannot divide by zero")
    except InvalidOperation:
        logging.error(f"Invalid number input: {a} or {b} is not a valid number.")
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")

def execute_command(a, b, operation, history_manager, test_mode=False):
    """Execute a math operation in a separate process (unless test_mode)."""
    if test_mode:
        # Synchronous execution for testing
        calculate_and_print(a, b, operation, history_manager)
    else:
        proc = multiprocessing.Process(target=calculate_and_print, args=(a, b, operation, history_manager))
        proc.start()
        proc.join()

def interactive_mode():
    """Run the calculator in interactive REPL mode."""
    print("Welcome to the Interactive Calculator (type 'exit' to quit, 'menu' for commands)")
    while True:
        user_input = input("\nEnter calculation (e.g., '5 3 add'): ").strip().lower()
        if user_input == "exit":
            print("Exiting calculator. Goodbye!")
            break
        elif user_input == "menu":
            print("\nAvailable commands:", ", ".join(load_commands().keys()))
            continue
        parts = user_input.split()
        non_math_commands = {"greet", "menu", "history", "clear_history"}
        if not parts:
            continue
        if parts[0] in non_math_commands:
            handle_non_math_commands(parts[0])
            continue
        if len(parts) != 3:
            print("Invalid input. Use format: <number1> <number2> <operation>")
            continue
        execute_command(parts[0], parts[1], parts[2], history_manager)

def handle_non_math_commands(command):
    """Handle non-arithmetic commands in interactive mode."""
    if command == "greet":
        name = input("Enter your name: ").strip() or "Stranger"
        print(f"Hello, {name}! Welcome to the calculator.")
    elif command == "menu":
        print("\nAvailable commands:", ", ".join(load_commands().keys()))
    elif command == "history":
        display_history()
    elif command == "clear_history":
        history_manager.clear_history()
        print("History cleared.")

def display_history():
    """Display all records in the calculation history."""
    history = history_manager.get_history()
    if not history:
        print("No calculation history available.")
    else:
        print("\nCalculation History:")
        for record in history:
            print(record)

def main():
    """Run the calculator in interactive mode or execute a single calculation from command-line arguments."""
    if len(sys.argv) == 1:
        interactive_mode()
    elif len(sys.argv) == 4:
        execute_command(sys.argv[1], sys.argv[2], sys.argv[3], history_manager)
    else:
        print("Usage: python main.py OR python main.py <number1> <number2> <operation>")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure proper start method for multiprocessing on Windows
    if sys.platform == "win32":
        multiprocessing.set_start_method("spawn", force=True)
    else:
        multiprocessing.set_start_method("fork", force=True)
    main()
