import logging
import logging.config
import os
import colorlog


# Custom formatter that assigns a unique color to both the level name and message based on the log level.
class LevelBasedColoredFormatter(colorlog.ColoredFormatter):
    # Define unique colors for each log level.
    level_colors = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[91m",  # Bright Red
    }

    def format(self, record):
        # Look up the color based on the record's levelname.
        color = self.level_colors.get(record.levelname, "\033[0m")
        # Set both the level and message colors to this value.
        record.level_color = color
        record.message_color = color
        record.reset = "\033[0m"  # Reset code
        return super().format(record)


# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Logging configuration dictionary
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom_colored": {
            # Ensure the formatter class path matches where LevelBasedColoredFormatter is defined.
            "()": "logging_config.LevelBasedColoredFormatter",
            "format": (
                "[%(asctime)s] [%(level_color)s%(levelname)s%(reset)s] [%(name)s]: "
                "%(message_color)s%(message)s%(reset)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "custom_colored",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "level": "DEBUG",
            "filename": os.path.join(LOG_DIR, "app.log"),
            "mode": "a",
            "encoding": "utf-8"
        },
        "null": {  # Used to ignore unwanted logs (e.g., pymongo debug messages)
            "class": "logging.NullHandler",
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
    "loggers": {
        "pymongo": {  # Ignore pymongo DEBUG logs by only logging WARNING and above.
            "handlers": ["null"],
            "level": "WARNING",
            "propagate": False,
        }
    }
}


# Example logger usage
logger = logging.getLogger(__name__)
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")


def setup_logging():
    logging.config.dictConfig(LOG_CONFIG)
