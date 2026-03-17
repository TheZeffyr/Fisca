import logging

from dotenv import load_dotenv

from app.core.config import Config
from app.core.database import Database
from app.core.logger import setup_logging, get_logger

def main():
    setup_logging(logging.DEBUG)
    logger = get_logger(__name__)

    try:
        load_dotenv()
        config = Config()
    except ValueError as e:
        logger.critical(f"Error configuration: {e}")
        raise SystemExit(1)
    
    if config.LOG_LEVEL!=10:
        setup_logging(config.LOG_LEVEL)
    
    db = Database(config.DB_URL)
    logger.info("The database is initialized")
    
    

if __name__ == "__main__":
    main()
