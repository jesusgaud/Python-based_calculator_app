# pylint: disable=redefined-outer-name
import pytest
from app.plugins.greet import GreetCommand

@pytest.fixture
def greet_command():
    """Fixture for creating a GreetCommand instance."""
    return GreetCommand()

def test_greet_command_execute(greet_command):
    """Test that the GreetCommand execute method returns the correct greeting message."""
    result = greet_command.execute("Jesus")
    assert result == "Hello, Jesus! Welcome to the interactive calculator!"

    # Test default case (no name provided)
    result_default = greet_command.execute()
    assert result_default == "Hello, Stranger! Welcome to the interactive calculator!"
