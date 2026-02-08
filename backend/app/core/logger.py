from logging.config import dictConfig


def setup_logging(debug: bool = False) -> None:
    """
    Configures the logging system for the application.
    
    Creates a logger configuration with output to the console (stdout).
    The output format includes a timestamp and a logging level.,
    the name of the logger and the message.
    
    Args:
        debug (bool): Debugging flag.
    """
    level = "DEBUG" if debug else "INFO"
    dictConfig({
        "version":1,
        "disable_existing_loggers": False,

        "formatters": {
            "default": {
                "format": (
                    "%(asctime)s | %(levelname)s | "
                    "%(name)s | %(message)s"
                )
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default"
            }
        },

        "root": {
            "level": level,
            "handlers": ["console"]
        }
    })