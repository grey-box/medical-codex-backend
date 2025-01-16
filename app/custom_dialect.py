from sqlalchemy.dialects import postgresql, sqlite, mysql, mssql
from sqlalchemy.types import Unicode


class UnicodeDialectMixin:
    def type_descriptor(self, typeobj):
        if isinstance(typeobj, str):
            return Unicode()
        return super().type_descriptor(typeobj)


class PostgresqlUnicodeDialect(UnicodeDialectMixin, postgresql.dialect):
    pass


class SqliteUnicodeDialect(UnicodeDialectMixin, sqlite.dialect):
    pass


class MySQLUnicodeDialect(UnicodeDialectMixin, mysql.dialect):
    pass


class MSSQLUnicodeDialect(UnicodeDialectMixin, mssql.dialect):
    pass
