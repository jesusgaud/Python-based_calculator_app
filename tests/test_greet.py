# pylint: disable=redefined-outer-name, unused-argument, wrong-import-order
import logging
import pytest
from app.plugins.greet import GreetCommand

@pytest.fixture
def greet_command():
    """Fixture for creating a GreetCommand instance."""
    return GreetCommand()

def test_greet_command_execution(greet_command, capsys, caplog):
    """Test that the GreetCommand prints the correct greeting message."""
    with caplog.at_level(logging.INFO):
        greet_command.execute("World")

        # Capture printed output
        captured = capsys.readouterr()
        assert "Hello, World! Welcome to the interactive calculator!" in captured.out
