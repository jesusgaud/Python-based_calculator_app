import pytest
import logging
from unittest.mock import patch
from app.plugins.greet import GreetCommand

@pytest.fixture
def greet_command():
    """Fixture for creating a GreetCommand instance."""
    return GreetCommand()

def test_greet_command_execution(greet_command, capsys, caplog):
    """Test that the GreetCommand executes correctly, logs, and prints output."""
    with caplog.at_level(logging.INFO):
        greet_command.execute()

        # Capture printed output
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out  # Ensure print statement executed

        # Verify logging output
        assert "Hello, World!" in caplog.text
