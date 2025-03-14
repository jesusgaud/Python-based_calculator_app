# pylint: disable=redefined-outer-name
import pytest
from app.plugins.greet.greet import GreetCommand

@pytest.fixture
def greet_command():
    """Fixture for creating a GreetCommand instance."""
    return GreetCommand()

def test_greet_command_execute(greet_command):
    """Test that the GreetCommand execute method returns the correct greeting message."""
    result = greet_command.execute()
    assert result == "Hello, welcome to the interactive calculator!"
