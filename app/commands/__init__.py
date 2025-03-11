from abc import ABC, abstractmethod

class Command(ABC):
    """Abstract base class for all command implementations."""

    @abstractmethod
    def execute(self):
        """Abstract method that must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the execute method.")

class CommandHandler:
    """Handles command registration and execution."""

    def __init__(self):
        """Initializes an empty dictionary to store commands."""
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        """Registers a command with a given name."""
        self.commands[command_name] = command

    def execute_command(self, command_name: str):
        """
        Executes a registered command.

        - **LBYL (Look Before You Leap)**: Checks existence before executing.
        - **EAFP (Easier to Ask for Forgiveness than Permission)**: Uses exception handling.

        Example:
        ```python
        command_handler.execute_command("greet")
        ```
        """
        try:
            self.commands[command_name].execute()
        except KeyError:
            print(f"No such command: {command_name}")
