import os
import logging

from dotenv import load_dotenv


logger = logging.getLogger(__name__)


class Config:
    @staticmethod
    def _get_required(var_name: str) -> str:
        """Getting a required environment variable"""
        value = os.getenv(var_name)

        if value is None:
            logger.error(f"Required environment variable {var_name} is not set")
            raise ValueError(f"Required environment variable {var_name} is not set")
        return value.strip()
    
    load_dotenv()
    BOT_TOKEN = _get_required(var_name="BOT_TOKEN")
    
