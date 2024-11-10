import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.custom_dialect import (
    PostgresqlUnicodeDialect,
    SqliteUnicodeDialect,
    MySQLUnicodeDialect,
    MSSQLUnicodeDialect,
)

dotenv.load_dotenv()  # Load environment variables from .env file

# Get database connection details from environment variables
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "codex.db")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Construct the database URL
if DB_TYPE == "postgresql":
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(
        DATABASE_URL, pool_pre_ping=True, dialect=PostgresqlUnicodeDialect()
    )
elif DB_TYPE == "sqlite":
    DATABASE_URL = f"sqlite:///{DB_NAME}"
    engine = create_engine(DATABASE_URL, dialect=SqliteUnicodeDialect())
elif DB_TYPE in ["sqlserver", "mssql"]:
    DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(
        DATABASE_URL, pool_pre_ping=True, dialect=MSSQLUnicodeDialect()
    )
elif DB_TYPE == "mysql":
    DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(
        DATABASE_URL, pool_pre_ping=True, dialect=MySQLUnicodeDialect()
    )
else:
    raise ValueError(f"Unsupported database type: {DB_TYPE}")

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
