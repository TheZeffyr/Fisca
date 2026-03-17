import logging

from app.core.logger import setup_logging, get_logger
from app.core.config import Config

from dotenv import load_dotenv


def main():
    setup_logging(logging.DEBUG)
    logger = get_logger(__name__)

    try:
        load_dotenv()
        config = Config()
    except ValueError as e:
        logger.critical(f"Error configuration: {e}")
        raise SystemExit(1)
    
    

if __name__ == "__main__":
    main()
