import logging

from sqlalchemy import insert
from sqlalchemy.orm import Session

import schemas
from config import LOGGER_NAME
from models import ManualTranslations

logger = logging.getLogger(LOGGER_NAME)


def store_manual_translation(
    db: Session, query: schemas.ManualTranslationQuery
) -> bool:
    """
    Store a term to be manually translated for later.

    Args:
        db (Session): Database session.
        query (schemas.ManualTranslationQuery): manual translation query parameters.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Manual translation results.
    """
    try:
        term = query.term
        source_language = query.source_language
        target_language = query.target_language
        description = query.description if query.description else None

        db_query = insert(ManualTranslations).values(
            term=term,
            proposed_translation=query.proposed_translation,
            language_to=target_language,
            language_from=source_language,
            description=description,
        )
        db.execute(db_query).scalars().all()
        db.close()

        return True

    except Exception as e:
        logger.error(f"Error in store_translation: {str(e)}")
        raise
