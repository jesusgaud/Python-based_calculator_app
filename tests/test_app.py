# import pytest
# import os
from app.app import App

def test_get_environment_variable(monkeypatch):
    """Test fetching environment variables with a default fallback."""

    # Set a test environment variable
    monkeypatch.setenv("TEST_KEY", "TEST_VALUE")

    # Ensure the environment variable is correctly fetched
    assert App.get_environment_variable("TEST_KEY") == "TEST_VALUE"

    # Ensure that a missing environment variable returns the default value
    assert App.get_environment_variable("NON_EXISTENT_KEY") == "DEFAULT_VALUE"
