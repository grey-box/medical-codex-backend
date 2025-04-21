from typing import Any
import logging
from sqlalchemy.dialects import postgresql, sqlite, mysql, mssql
from sqlalchemy.types import Unicode
from config import LOGGER_NAME
from fastapi import status

logger = logging.getLogger(LOGGER_NAME)


class UnicodeDialectMixin:
    """Mixin class to handle Unicode type for different SQL dialects."""

    def type_descriptor(self, typeobj: Any) -> Any:
        """
        Convert string type to Unicode type.

        Args:
            typeobj: The type object to be converted.

        Returns:
            Unicode type if input is string, otherwise original type.
        """
        try:
            if isinstance(typeobj, str):
                return Unicode()
            return super().type_descriptor(typeobj)
        except Exception as e:
            logger.error(status.HTTP_400_BAD_REQUEST + f" Error in type_descriptor: {str(e)}")
            raise


class PostgresqlUnicodeDialect(UnicodeDialectMixin, postgresql.dialect):
    """PostgreSQL dialect with Unicode support."""
    pass


class SqliteUnicodeDialect(UnicodeDialectMixin, sqlite.dialect):
    """SQLite dialect with Unicode support."""
    pass


class MySQLUnicodeDialect(UnicodeDialectMixin, mysql.dialect):
    """MySQL dialect with Unicode support."""
    pass


class MSSQLUnicodeDialect(UnicodeDialectMixin, mssql.dialect):
    """Microsoft SQL Server dialect with Unicode support."""
    pass
