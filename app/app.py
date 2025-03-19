import os

class App:
    """Application class for managing environment settings."""
    @staticmethod
    def get_environment_variable(key: str):
        """Fetch an environment variable or return a default if not set."""
        return os.getenv(key, "DEFAULT_VALUE")
