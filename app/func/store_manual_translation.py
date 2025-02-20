import logging
from typing import Dict, List, Any

from sqlalchemy import insert
from sqlalchemy.orm import Session

import app.schemas as schemas
from app.config import LOGGER_NAME
from app.models import ManualTranslations
from config import settings

logger = logging.getLogger(LOGGER_NAME)


def store_manual_translation(
    db: Session, query: schemas.ManualTranslationQuery
) -> str:
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
        target_language = query.language_to
        source_language = query.language_from

        db_query = insert(ManualTranslations).values(term=term, language_to=target_language, language_from=source_language)
        db.execute(db_query).scalars().all()
        db.close()

        return {
                term + " inserted into the database for manual translation"
        }

    except Exception as e:
        logger.error(f"Error in store_translation: {str(e)}")
        return {"Error"}
