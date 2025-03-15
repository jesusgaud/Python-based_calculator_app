from app.commands import Command

class GreetCommand(Command):
    """A simple greeting plugin command."""
    def execute(self, *args):
        print("Hello from the Greet plugin!")
