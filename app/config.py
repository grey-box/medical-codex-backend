from dotenv import find_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

LOGGER_NAME = "codex_backend_logger"


class Settings(BaseSettings):
    DB_TYPE: str = "postgresql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str
    LOGGING_LEVEL: str
    LOGGING_FORMAT: str
    GOOGLE_API_KEY: str

    class Config:
        env_file = find_dotenv()


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
