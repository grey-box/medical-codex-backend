from dotenv import find_dotenv
from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator
from pydantic_settings import BaseSettings
from typing import Optional

LOGGER_NAME = "codex_backend_logger"


class Settings(BaseSettings):
    LOGGING_FORMAT: str = '%(asctime)s - %(levelname)s - %(message)s'
    LOGGING_LEVEL: str = 'INFO'
    DB_TYPE: str = "postgresql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    class Config:
        env_file = find_dotenv()
        env_file_encoding = 'utf-8'

    @field_validator('DB_PASSWORD')
    def check_db_password(cls, v, values):
        if values['DB_TYPE'] != "sqlite" and not v:
            raise ValueError("Database password is required for non-sqlite databases")
        return v


settings = Settings()


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "codex_backend_logger"
    LOG_FORMAT: str = settings.LOGGING_FORMAT
    LOG_LEVEL: str = settings.LOGGING_LEVEL
    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
