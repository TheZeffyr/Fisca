import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging(
	level: int = logging.INFO,
	LOG_DIR: str = "logs"
) -> None:
	"""Initializes logging in the Fisca API

	Creates 2 handlers: file and console.
	Set uniform login style.
	Creates a file directory and file for the file handler.

	Args:
		level (int, optional): Log output level. Defaults to logging.INFO.
		LOG_DIR (str, optional): Directory where logs are stored. Defaults to "logs".
	"""
	os.makedirs(LOG_DIR, exist_ok=True)
	
	logger = logging.getLogger()

	logger.setLevel(level)

	if logger.hasHandlers():
		logger.handlers.clear()
	
	formatter = logging.Formatter(
		"[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
		datefmt="%H:%M:%S"
	)

	file_handler = RotatingFileHandler(
		filename=os.path.join(LOG_DIR,"fisca.log"),
		maxBytes=5*1024*1024,
		backupCount=5
	)
	file_handler.setFormatter(formatter)

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(formatter)
	
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
	"""Returns logger

	Args:
		name (str): Name of the logger.

	Returns:
		logging.Logger: Configured logger instance.
	"""
	return logging.getLogger(name)