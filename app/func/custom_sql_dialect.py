"""
Custom SQL Dialect Module.

This module provides custom SQL dialect implementations with Unicode support
for various database systems. These dialects ensure proper handling of
Unicode characters across different database backends.
"""

from typing import Any
import logging
from fastapi import HTTPException, status
from sqlalchemy.dialects import postgresql, sqlite, mysql, mssql
from sqlalchemy.types import Unicode

from config import LOGGER_NAME

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


class UnicodeDialectMixin:
    """
    Mixin class to handle Unicode type for different SQL dialects.
    
    This mixin provides a common implementation for converting string types
    to Unicode types, which can be used across different SQL dialects to
    ensure consistent Unicode handling.
    """

    def type_descriptor(self, typeobj: Any) -> Any:
        """
        Convert string type to Unicode type.

        Args:
            typeobj (Any): The type object to be converted.

        Returns:
            Any: Unicode type if input is string, otherwise original type.
            
        Raises:
            HTTPException: If an error occurs during type conversion.
        """
        try:
            if isinstance(typeobj, str):
                return Unicode()
            return super().type_descriptor(typeobj)
        except Exception as e:
            error_message = f"Error in type_descriptor: {str(e)}"
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )


class PostgresqlUnicodeDialect(UnicodeDialectMixin, postgresql.dialect):
    """
    PostgreSQL dialect with Unicode support.
    
    This dialect extends the standard PostgreSQL dialect with the
    UnicodeDialectMixin to ensure proper handling of Unicode characters.
    """
    pass


class SqliteUnicodeDialect(UnicodeDialectMixin, sqlite.dialect):
    """
    SQLite dialect with Unicode support.
    
    This dialect extends the standard SQLite dialect with the
    UnicodeDialectMixin to ensure proper handling of Unicode characters.
    """
    pass


class MySQLUnicodeDialect(UnicodeDialectMixin, mysql.dialect):
    """
    MySQL dialect with Unicode support.
    
    This dialect extends the standard MySQL dialect with the
    UnicodeDialectMixin to ensure proper handling of Unicode characters.
    """
    pass


class MSSQLUnicodeDialect(UnicodeDialectMixin, mssql.dialect):
    """
    Microsoft SQL Server dialect with Unicode support.
    
    This dialect extends the standard Microsoft SQL Server dialect with the
    UnicodeDialectMixin to ensure proper handling of Unicode characters.
    """
    pass
