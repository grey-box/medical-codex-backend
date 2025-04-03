import logging
from logging import config as logging_config
import os
from typing import Optional, Dict, Any

from dotenv import find_dotenv
from pydantic import BaseModel
from pydantic_settings import Basesettings


LOGGER_NAME = "codex_backend_logger"
LOGGER_NAME_FILE = "codex_file_logger"
logger = logging.getLogger(LOGGER_NAME)


class settings(Basesettings):
    """Define application settings."""

    logging_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    logging_level: str = "INFO"
    db_type: str = "postgresql"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str = "postgres"
    db_password: Optional[str] = None
    fallback_translation_method: str = "gemini"
    google_api_key: Optional[str] = None

    class Config:
        """Configure environment variables."""

        env_file = find_dotenv()
        env_file_encoding = "utf-8"


settings = settings()


class LogConfig(BaseModel):
    """Define logging configuration for the server."""

    logger_name: str = LOGGER_NAME
    logger_name_file: str = LOGGER_NAME_FILE
    log_format: str = settings.logging_format
    log_level: str = settings.logging_level
    version: int = 1
    disable_existing_loggers: bool = False

    # Create Logs dir if it doesn't exist
    log_dir: str = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)    
    log_file_path: str = os.path.join(log_dir, f"{LOGGER_NAME}.log")

    formatters: Dict[str, Dict[str, Any]] = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": log_format,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": log_format,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file_formatter": {
            "()": "logging.Formatter",
            "fmt": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        }
    }
    handlers: Dict[str, Dict[str, Any]] = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "formatter": "file_formatter",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": log_file_path,
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf-8",
        }
    }
    loggers: Dict[str, Dict[str, Any]] = {
        logger_name: {"handlers": ["console"], "level": log_level, "propagate": False},
        logger_name_file: {"handlers": ["console", "file"], "level": log_level, "propagate": False},
        "uvicorn.error": {"handlers": ["default", ], "level": logging.INFO, "propagate": False},     
        "uvicorn.access": {"handlers": ["access", ], "level": logging.INFO, "propagate": False},     
    }


def setup_logging() -> None:
    """
    Configure logging for the application.

    Raises:
        Exception: If logging configuration fails.
    """
    try:
        logging_config.dictConfig(LogConfig().model_dump())
        logger.info("Logging configured successfully.")
    except Exception as error:
        logger.error(f"Failed to configure logging: {str(error)}")
        raise


setup_logging()