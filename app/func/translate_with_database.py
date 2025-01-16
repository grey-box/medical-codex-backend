import logging
from typing import Dict, List, Any

from sqlalchemy import select, distinct, and_
from sqlalchemy.orm import Session

import app.schemas as schemas
from app.config import LOGGER_NAME
from app.func.translate_using_fallback import translate_using_fallback
from app.models import UniqueTranslations
from config import settings

logger = logging.getLogger(LOGGER_NAME)


def translate_with_database(
    db: Session, query: schemas.TranslationQuery
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get translation for a term using local database or fallback to external API.

    Args:
        db (Session): Database session.
        query (schemas.TranslationQuery): Translation query parameters.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Translation results.
    """
    try:
        term = query.translation_query.matching_name
        target_language = query.target_language

        db_query = select(distinct(UniqueTranslations.target_text)).where(
            and_(
                UniqueTranslations.target_language == target_language,
                UniqueTranslations.source_text == term,
            )
        )
        result = db.execute(db_query).scalars().all()
        db.close()
        translated_terms = [str(value) for value in result]

        if translated_terms:
            return {
                "results": [
                    {
                        "translated_name": translated_term,
                        "translated_source": "local_db",
                        "translated_uid": query.translation_query.matching_uid,
                    }
                    for translated_term in translated_terms
                ]
            }
        else:
            return translate_using_fallback(query, settings.fallback_translation_method)

    except Exception as e:
        logger.error(f"Error in get_translation: {str(e)}")
        return {"results": []}
