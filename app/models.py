import logging

from sqlalchemy import CheckConstraint, Column, DateTime, Text, func
from sqlalchemy.types import String, Integer

from database import Base, engine
from config import LOGGER_NAME
from fastapi import status, HTTPException

# Create all tables (REMOVE OR COMMENT OUT THIS LINE IF TABLES ARE CREATED EXTERNALLY)
# Base.metadata.create_all(engine) # <-- REMOVE OR COMMENT OUT THIS LINE

# Assuming LOGGER_NAME is imported from config
logger = logging.getLogger(LOGGER_NAME)


class UniqueTranslations(Base):
    """
    Represent a single translation entry in the unique translation table.

    This model is used to build a single translation table that serves as the
    primary source for querying translation results.
    """

    __tablename__ = "unique_translation_table"


    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    source_text = Column(String, nullable=False)
    target_text = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    source_comment = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    description = Column(String, nullable=True)

    def __repr__(self) -> str:
        """
        Return a string representation of the UniqueTranslationsORM instance.

        Returns:
            str: A formatted string containing the instance's attributes.
        """
        return (
            f"<Translation("
            f"source_language={self.source_language}, "
            f"target_language={self.target_language}, "
            f"source_text={self.source_text}, "
            f"target_text={self.target_text}, "
            f"table_name={self.table_name}, "
            f"weight={self.weight},"
            f"description={self.description}\n"
            f")>"
        )


class ManualTranslations(Base):
    """
    Represent a single translation entry in the manual translation table.

    This model is used to build a single translation table that serves as the
    primary source for querying translation results.
    """

    __tablename__ = "manual_translation"

    id = Column(Integer, primary_key=True)
    term = Column(String, nullable=False)
    proposed_translation = Column(String, nullable=True)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    description = Column(String, nullable=True)

    def __repr__(str) -> str:
        """
        Return a string representation of the UniqueTranslationsORM instance.

        Returns:
            str: A formatted string containing the instance's attributes.
        """
        return (
            f"<Manual Translation("
            f"term={str.term}, "
            f"proposed_translation={str.proposed_translation}, "
            f"source_language={str.source_language}, "
            f"target_language={str.target_language}, "
            f"description={str.description}\n"
            f")>"
        )


class LanguagePairs(Base):
    """
    Represent available language pairs from the 'unique_translation_table'.

    This class maps to a view named 'available_languages_view' and excludes
    certain odd language names.
    """

    __tablename__ = "available_languages_view"

    source_language = Column(String, nullable=False, primary_key=True)
    target_language = Column(String, nullable=False, primary_key=True)

    __table_args__ = {"autoload_with": engine}

    def __repr__(self) -> str:
        """
        Return a string representation of the LanguagePairs instance.

        Returns:
            str: A formatted string containing the instance's attributes.
        """
        return (
            f"<Language(source_language={self.source_language},target_language={self.target_language})>"
        )

class ServiceLogs(Base):

    """Model to store log messages in the database."""
    __tablename__ = "_service_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    log_timestamp = Column(DateTime(timezone=True), server_default=func.now())  # Auto timestamp
    error_level = Column(Integer, nullable=False)
    source = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    
    __table_args__ = (
        CheckConstraint("error_level IN (logging.NOTSET, logging.INFO, logging.WARNING, logging.ERROR, logging.DEBUG, logging.CRITICAL)", name="_service_logs_error_level_check"),
    )

    def __repr__(self):
        return f"<LogEntry(id={self.id}, timestamp={self.log_timestamp}, level={self.error_level}, source={self.source}, message={self.message})>"

