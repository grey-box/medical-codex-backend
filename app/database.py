import logging
import os
from typing import Generator

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import LOGGER_NAME
from app.custom_dialect import (
    PostgresqlUnicodeDialect,
    SqliteUnicodeDialect,
    MySQLUnicodeDialect,
    MSSQLUnicodeDialect,
)

logger = logging.getLogger(LOGGER_NAME)

dotenv.load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "codex.db")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def create_database_url() -> str:
    """
    Create the database URL based on the environment variables.

    Returns:
        str: The constructed database URL.
    """
    if DB_TYPE == "postgresql":
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif DB_TYPE == "sqlite":
        return f"sqlite:///{DB_NAME}"
    elif DB_TYPE in ["sqlserver", "mssql"]:
        return f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
    elif DB_TYPE == "mysql":
        return f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        raise ValueError(f"Unsupported database type: {DB_TYPE}")


def create_database_engine() -> Engine:
    """
    Create and return a database engine based on the database type.

    Returns:
        Engine: SQLAlchemy engine object.

    Raises:
        ValueError: If an unsupported database type is specified.
    """
    try:
        database_url = create_database_url()
        if DB_TYPE == "postgresql":
            return create_engine(
                database_url, pool_pre_ping=True, dialect=PostgresqlUnicodeDialect()
            )
        elif DB_TYPE == "sqlite":
            return create_engine(database_url, dialect=SqliteUnicodeDialect())
        elif DB_TYPE in ["sqlserver", "mssql"]:
            return create_engine(
                database_url, pool_pre_ping=True, dialect=MSSQLUnicodeDialect()
            )
        elif DB_TYPE == "mysql":
            return create_engine(
                database_url, pool_pre_ping=True, dialect=MySQLUnicodeDialect()
            )
        else:
            raise ValueError(f"Unsupported database type: {DB_TYPE}")
    except Exception as e:
        logger.error(f"Failed to create database engine: {str(e)}")
        raise


engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_database_session() -> Generator[Session, None, None]:
    """
    Create a database session and yield it.

    Yields:
        Session: SQLAlchemy session object.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
