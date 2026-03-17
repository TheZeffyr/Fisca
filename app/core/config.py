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
    
    @staticmethod
    def _str_to_bool(value: str) -> bool:
        """Converts the string to a boolean value.
        
        Args:
            value: str: Value of the convert to string
        
        Returns:
            bool: Boolean variable value
        """
        return value.lower() in ('true', '1', 't', 'yes', 'y', 'on')
    
    @property
    def DB_URL(self):
       return self._get_required("DB_URL")
        
    @property
    def DEBUG(self):
        return self._str_to_bool(self._get_required("DEBUG"))
