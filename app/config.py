import logging
from logging import config as logging_config
from typing import Optional, Dict, Any

from dotenv import find_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

LOGGER_NAME = "codex_backend_logger"
logger = logging.getLogger(LOGGER_NAME)


class Settings(BaseSettings):
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


settings = Settings()


class LogConfig(BaseModel):
    """Define logging configuration for the server."""

    logger_name: str = LOGGER_NAME
    log_format: str = settings.logging_format
    log_level: str = settings.logging_level
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: Dict[str, Dict[str, Any]] = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": log_format,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: Dict[str, Dict[str, Any]] = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: Dict[str, Dict[str, Any]] = {
        logger_name: {"handlers": ["default"], "level": log_level},
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