"""Interactive Calculator Using the Command Pattern with Multiprocessing and Logging"""

import os
import sys
import multiprocessing
import logging
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
from app.calculation import Calculation
from app.operations import operations  # Import dynamically loaded operations

# Load environment variables from .env file
load_dotenv()

# Access environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # Default to "production"
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "default_user")

# Configure Logging
LOGGING_CONFIG = "logging.conf"

if os.path.exists(LOGGING_CONFIG):
    logging.config.fileConfig(LOGGING_CONFIG)
else:
    logging.basicConfig(
        level=logging.DEBUG if ENVIRONMENT == "development" else logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        handlers=[logging.StreamHandler()]  # Log to console
    )

logging.info(f"Running in {ENVIRONMENT} mode")
logging.info(f"Database Username: {DATABASE_USERNAME}")

def load_commands():
    """Dynamically loads available commands, including plugins."""
    if not operations:
        logging.error("No operations found. Ensure plugins are properly loaded.")
    return operations  # Return the entire operations dictionary

def calculate_and_print(a, b, operation):
    """Performs calculation in a separate process and logs the result."""
    commands = load_commands()

    if operation not in commands:
        logging.error(f"Unknown operation: {operation}")
        print(f"Unknown operation: {operation}")
        return

    try:
        a = Decimal(a)
        b = Decimal(b)
        calc = Calculation(a, b, commands[operation])
        result = calc.perform()
        logging.info(f"Calculated: {a} {operation} {b} = {result}")
        print(f"The result of {a} {operation} {b} is equal to {result}")
    except ZeroDivisionError:
        logging.error("Error: Cannot divide by zero")
        print("An error occurred: Cannot divide by zero")
    except InvalidOperation:
        logging.error(f"Invalid number input: {a} or {b} is not a valid number.")
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except Exception as e:
        logging.exception(f"Unexpected error: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")

def execute_command(a, b, operation):
    """Executes a mathematical operation using multiprocessing."""
    process = multiprocessing.Process(target=calculate_and_print, args=(a, b, operation))
    process.start()
    process.join()  # Ensure the process completes before proceeding

def interactive_mode():
    """Runs the calculator in interactive REPL mode."""
    print("Welcome to the Interactive Calculator (type 'exit' to quit, 'menu' for available commands)")

    commands = load_commands()
    while True:
        user_input = input("\nEnter calculation (e.g., '5 3 add'): ").strip().lower()
        if user_input == "exit":
            print("Exiting calculator. Goodbye!")
            break
        elif user_input == "menu":
            print("\nAvailable commands:", ", ".join(commands.keys()))  # Shows dynamically loaded plugins
            continue

        parts = user_input.split()
        if len(parts) != 3:
            print("Invalid input. Use format: <number1> <number2> <operation>")
            continue

        a, b, operation = parts
        execute_command(a, b, operation)

def main():
    """Runs either interactive mode or command-line mode based on user input."""
    if len(sys.argv) == 1:
        interactive_mode()
    elif len(sys.argv) == 4:
        _, a, b, operation = sys.argv
        execute_command(a, b, operation)
    else:
        print("Usage: python main.py OR python main.py <number1> <number2> <operation>")
        sys.exit(1)

if __name__ == '__main__':
    if sys.platform == "win32":
        multiprocessing.set_start_method("spawn", force=True)  # Ensure compatibility on Windows
    else:
        multiprocessing.set_start_method("fork", force=True)  # Use 'fork' for Unix-like systems

    main()