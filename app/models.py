import logging

from sqlalchemy import Column
from sqlalchemy.types import String, Integer

from app.database import Base, engine
from config import LOGGER_NAME

# Create all tables
Base.metadata.create_all(engine)

# Assuming LOGGER_NAME is imported from config
logger = logging.getLogger(LOGGER_NAME)


class UniqueTranslations(Base):
    """
    Represent a single translation entry in the unique translation table.

    This model is used to build a single translation table that serves as the
    primary source for querying translation results.
    """

    __tablename__ = "unique_translation_table"

    id = Column(Integer, primary_key=True)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    source_text = Column(String, nullable=False)
    target_text = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    source_comment = Column(String, nullable=True)
    weight = Column(Integer, nullable=False)

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
            f"weight={self.weight}"
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
            f"<Language(\n"
            f"    source_language={self.source_language},\n"
            f"    target_language={self.target_language}\n"
            f")>"
        )


try:
    Base.metadata.create_all(engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"Error creating database tables: {str(e)}")
    raise
