import logging
from app.core import logger

def main():
    logger.setup_logging(logging.DEBUG)

if __name__ == "__main__":
    main()
