from abc import ABC, abstractmethod

class Command(ABC):
    """Abstract base class for all command implementations."""

    @abstractmethod
    def execute(self, *args):
        """Abstract method that must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the execute method.")

class CommandHandler:
    """Handles command registration and execution."""

    def __init__(self):
        """Initializes an empty dictionary to store commands."""
        self.commands = {}
        self.register_command("menu", MenuCommand(self))

    def register_command(self, command_name: str, command: Command):
        """Registers a command with a given name."""
        self.commands[command_name] = command

    def execute_command(self, command_name: str, *args):
        """
        Executes a registered command with optional arguments.

        - **LBYL (Look Before You Leap)**: Checks existence before executing.
        - **EAFP (Easier to Ask for Forgiveness than Permission)**: Uses exception handling.

        Example:
        ```python
        command_handler.execute_command("greet")
        command_handler.execute_command("add", "5", "3")  # Example with arguments
        ```
        """
        try:
            command = self.commands[command_name]
            command.execute(*args)  # Pass arguments properly
        except KeyError:
            print("Unknown command. Type 'menu' for a list of commands.")

class MenuCommand(Command):
    """Command that lists all available commands."""

    def __init__(self, command_handler: CommandHandler):
        """Receives a reference to the command handler to list available commands."""
        self.command_handler = command_handler

    def execute(self, *args):
        """Displays all registered commands."""
        print("\nAvailable Commands:")
        for command in self.command_handler.commands.keys():
            print(f"- {command}")
        print("Type 'exit' to quit.")
