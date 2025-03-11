import os

class App:
    """Application class for managing environment settings."""

    @staticmethod
    def get_environment_variable(key: str):
        """Fetches an environment variable value."""
        return os.getenv(key, "DEFAULT_VALUE")
