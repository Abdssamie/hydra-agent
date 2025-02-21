import logging
import logging.config
import os

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
        },
        "simple": {
            "format": "[%(levelname)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "level": "DEBUG",
            "filename": os.path.join(LOG_DIR, "app.log"),
            "mode": "a",
            "encoding": "utf-8"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
    "loggers": {
        "module1": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "module2": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        }
    }
}


def setup_logging():
    logging.config.dictConfig(LOG_CONFIG)
