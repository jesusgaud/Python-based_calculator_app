from app.commands import Command

class GreetCommand(Command):
    """Command to greet users in the interactive calculator."""

    def execute(self, *args):
        """Prints a greeting message."""
        if not args:
            message = "Hello, Stranger! Welcome to the interactive calculator!"
        else:
            name = " ".join(args)
            message = f"Hello, {name}! Welcome to the interactive calculator!"

        print(message)
        return message
