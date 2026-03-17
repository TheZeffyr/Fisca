import os


class Config:
    """Configuration manager for the application."""
    @staticmethod
    def _get_required(var_name: str) -> str:
        """Get required environment variable

        Args:
            var_name (str): Name of the environment variable.

        Raises:
            ValueError: If variable is not set.

        Returns:
            str: Value of the environment variable.
        """
        value = os.getenv(var_name)

        if value is None:
            raise ValueError(
                f"Required environment variable {var_name} is not set"
            )
        return value.strip()


    DB_URL = _get_required("DB_URL")
    DEBUG = _get_required("DEBUG")
