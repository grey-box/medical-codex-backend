import logging
from typing import List

from sqlalchemy import select, distinct
from sqlalchemy.orm import Session

from app.models import UniqueTranslations
from config import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_unique_source_texts(db: Session, source_language: str) -> List[str]:
    """
    Retrieve unique source text values for a given language from the database.

    Args:
        db (Session): The database session.
        source_language (str): The language code to filter the source texts.

    Returns:
        List[str]: A list of unique source text values.

    Raises:
        SQLAlchemyError: If there's an issue with the database query.
    """
    try:
        query = select(distinct(UniqueTranslations.source_text)).where(
            UniqueTranslations.source_language == source_language
        )
        result = db.execute(query).scalars().all()
        return [str(value) for value in result]
    except Exception as e:
        logger.error(f"Error retrieving unique source texts: {str(e)}")
        raise
