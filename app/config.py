"""
Configuration module for the Medical Codex Backend.

This module defines application settings, logging configuration, and provides
utility functions for setting up the application environment. It handles:
1. Loading environment variables
2. Configuring application settings
3. Setting up logging with both console and file handlers
"""

import logging
import os
from logging import config as logging_config
from typing import Dict, Any, Optional

from dotenv import find_dotenv
from fastapi import status, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# Define logger names as constants
LOGGER_NAME = "codex_backend_logger"
LOGGER_NAME_FILE = "codex_file_logger"

# Initialize logger - note this is configured properly later
logger = logging.getLogger(LOGGER_NAME)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class defines all configurable settings for the application with sensible
    defaults. Values can be overridden by environment variables or a .env file.
    
    Attributes:
        logging_format: Format string for log messages
        logging_level: Minimum log level to record (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        db_type: Database type (postgresql, sqlite, mysql, etc.)
        db_host: Database server hostname
        db_port: Database server port
        db_name: Database name
        db_user: Database username
        db_password: Database password
        fallback_translation_method: Method to use for fallback translations
        google_api_key: API key for Google services (if used)
    """

    # Logging settings
    logging_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    logging_level: str = "INFO"
    
    # Database settings
    db_type: str = "postgresql"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str = "postgres"
    db_password: Optional[str] = None
    
    # Application settings
    fallback_translation_method: str = "gemini"
    google_api_key: Optional[str] = None

    class Config:
        """Configuration for environment variable loading."""
        env_file = find_dotenv()
        env_file_encoding = "utf-8"
        case_sensitive = False  # Allow case-insensitive env vars


# Create a singleton instance of settings
settings = Settings()


class LogConfig(BaseModel):
    """
    Logging configuration for the application.
    
    This class defines the structure and settings for application logging,
    including formatters, handlers, and logger configurations.
    
    Attributes:
        logger_name: Name of the main application logger
        logger_name_file: Name of the file logger
        log_format: Format string for log messages
        log_level: Minimum log level to record
        version: Logging config schema version (always 1)
        disable_existing_loggers: Whether to disable existing loggers
    """

    # Logger names and basic settings
    logger_name: str = LOGGER_NAME
    logger_name_file: str = LOGGER_NAME_FILE
    log_format: str = settings.logging_format
    log_level: str = settings.logging_level
    version: int = 1
    disable_existing_loggers: bool = False

    # Create logs directory if it doesn't exist
    @property
    def log_dir(self) -> str:
        """Get the log directory path, creating it if it doesn't exist."""
        directory = os.path.join(os.getcwd(), "logs")
        os.makedirs(directory, exist_ok=True)
        return directory
    
    @property
    def log_file_path(self) -> str:
        """Get the full path to the log file."""
        return os.path.join(self.log_dir, f"{LOGGER_NAME}.log")

    # Log formatters configuration
    @property
    def formatters(self) -> Dict[str, Dict[str, Any]]:
        """Get the log formatters configuration."""
        return {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": self.log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": self.log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "file_formatter": {
                "()": "logging.Formatter",
                "fmt": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S %z",
            }
        }
    
    # Log handlers configuration
    @property
    def handlers(self) -> Dict[str, Dict[str, Any]]:
        """Get the log handlers configuration."""
        return {
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
                "filename": self.log_file_path,
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
            }
        }
    
    # Loggers configuration
    @property
    def loggers(self) -> Dict[str, Dict[str, Any]]:
        """Get the loggers configuration."""
        return {
            self.logger_name: {"handlers": ["console"], "level": self.log_level, "propagate": False},
            self.logger_name_file: {"handlers": ["console", "file"], "level": self.log_level, "propagate": False},
            "uvicorn.error": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        }

    def model_dump(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary suitable for logging configuration.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the logging configuration
        """
        # Create a dictionary with all the configuration
        return {
            "version": self.version,
            "disable_existing_loggers": self.disable_existing_loggers,
            "formatters": self.formatters,
            "handlers": self.handlers,
            "loggers": self.loggers,
        }


def setup_logging() -> None:
    """
    Configure logging for the application.
    
    This function applies the logging configuration defined in LogConfig.
    It should be called early in the application startup process.
    
    Raises:
        RuntimeError: If logging configuration fails
    """
    try:
        # Apply logging configuration
        config_dict = LogConfig().model_dump()
        logging_config.dictConfig(config_dict)
        
        # Log successful configuration
        logger.info(f"Logging configured successfully")
    except Exception as error:
        # Since logging might not be configured yet, print to stderr as well
        error_msg = f"Failed to configure logging: {str(error)}"
        print(f"ERROR: {error_msg}")
        
        # Try to log the error, but this might not work if logging setup failed
        try:
            logger.error(f"Error during logging setup: {error_msg}")
        except Exception as e:
            pass
        
        # In a web context, you might want to raise an HTTPException
        # But for module initialization, a RuntimeError is more appropriate
        raise RuntimeError(f"Logging configuration failed: {error_msg}") from error


# Initialize logging when this module is imported
setup_logging()