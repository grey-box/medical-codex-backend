"""
Database connection module.

This module handles database connection setup and session management for the application.
It supports multiple database types including PostgreSQL, SQLite, MS SQL Server, and MySQL.
"""

import logging
import os
from typing import Generator, Dict, Any

import dotenv
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config import LOGGER_NAME
from func.custom_sql_dialect import (
    PostgresqlUnicodeDialect,
    SqliteUnicodeDialect,
    MySQLUnicodeDialect,
    MSSQLUnicodeDialect,
)

# Initialize logger
logger = logging.getLogger(LOGGER_NAME)

# Load environment variables
dotenv.load_dotenv()

# Database configuration from environment variables
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "codex.db")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Database dialect configuration
DB_DIALECTS = {
    "postgresql": PostgresqlUnicodeDialect,
    "sqlite": SqliteUnicodeDialect,
    "mysql": MySQLUnicodeDialect,
    "mssql": MSSQLUnicodeDialect,
    "sqlserver": MSSQLUnicodeDialect,
}

# Engine configuration options for different database types
ENGINE_OPTIONS: Dict[str, Dict[str, Any]] = {
    "postgresql": {"pool_pre_ping": True},
    "sqlite": {},
    "mysql": {"pool_pre_ping": True},
    "mssql": {"pool_pre_ping": True},
    "sqlserver": {"pool_pre_ping": True},
}


def create_database_url() -> str:
    """
    Create the database URL based on the environment variables.

    Returns:
        str: The constructed database URL for the configured database type.

    Raises:
        HTTPException: If an unsupported database type is specified.
    """
    if DB_TYPE == "postgresql":
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif DB_TYPE == "sqlite":
        return f"sqlite:///{DB_NAME}"
    elif DB_TYPE in ["sqlserver", "mssql"]:
        return (
            f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
        )
    elif DB_TYPE == "mysql":
        return f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported database type: {DB_TYPE}",
        )


def create_database_engine() -> Engine:
    """
    Create and return a database engine based on the database type.

    The function configures the appropriate dialect and engine options
    for the selected database type.

    Returns:
        Engine: SQLAlchemy engine object configured for the selected database.

    Raises:
        HTTPException: If database engine creation fails or if an unsupported 
                      database type is specified.
    """
    try:
        database_url = create_database_url()
        
        # Check if the database type is supported
        if DB_TYPE not in DB_DIALECTS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported database type: {DB_TYPE}",
            )
        
        # Get the appropriate dialect class and engine options
        dialect_class = DB_DIALECTS[DB_TYPE]
        engine_options = ENGINE_OPTIONS.get(DB_TYPE, {})
        
        # Create and return the engine with the appropriate configuration
        return create_engine(
            database_url, 
            dialect=dialect_class(),
            **engine_options
        )
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        # Log the error and convert other exceptions to HTTPException
        error_message = f"Failed to create database engine: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )


# Initialize database components
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_database_session() -> Generator[Session, None, None]:
    """
    Create a database session and yield it.
    
    This function is intended to be used as a FastAPI dependency.
    It ensures that the database session is properly closed after use,
    even if an exception occurs.

    Yields:
        Session: SQLAlchemy session object connected to the configured database.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
