from datetime import datetime, timezone
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.config import LOGGER_NAME, LOGGER_NAME_FILE
from app.database import get_database_session

router = APIRouter(prefix="/languages", tags=["languages"])
logger = logging.getLogger(LOGGER_NAME)
logger_file = logging.getLogger(LOGGER_NAME_FILE)


@router.get("/", response_model=schemas.AvailableLanguages)
def get_available_languages(
    db: Session = Depends(get_database_session),
) -> schemas.AvailableLanguages:
    """
    Retrieve the languages currently available for translation.

    Args:
        db: Database session.

    Returns:
        AvailableLanguages: Object containing available language pairs.
    """
    try:
        language_pairs = (
            db.query(models.LanguagePairs)
            .order_by(
                models.LanguagePairs.source_language.asc(),
                models.LanguagePairs.target_language.asc(),
            )
            .all()
        )

        grouped_languages = {}
        for pair in language_pairs:
            if pair.source_language not in grouped_languages:
                grouped_languages[pair.source_language] = []
            grouped_languages[pair.source_language].append(pair.target_language)

        available_languages_list = [
            schemas.AvailableLanguageResult(
                source_language=source,
                target_languages=targets,
            )
            for source, targets in grouped_languages.items()
        ]

        logger.info(f"Retrieved language pairs: {language_pairs}")
        logger_file.info(f"Retrieved language pairs: {language_pairs}")
        return schemas.AvailableLanguages(available_languages=available_languages_list)
    except Exception as e:
        logger.error(f"Error retrieving available languages: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/test", response_model=schemas.AvailableLanguages)
def get_test_languages(
    db: Session = Depends(get_database_session),
) -> schemas.AvailableLanguages:
    """
    Generate test language pairs for development purposes.

    Args:
        db: Database session (not used in this function, kept for consistency).

    Returns:
        AvailableLanguages: Object containing test language pairs.
    """
    try:
        logger.info("Generating test language pairs")

        def generate_test_pairs(num_languages: int) -> List[dict]:
            return [
                {
                    "source_language": f"lang{num}",
                    "target_languages": [
                        f"lang{i}" for i in range(1, num_languages + 1) if i != num
                    ],
                }
                for num in range(1, num_languages + 1)
            ]

        test_results = generate_test_pairs(3)
        return schemas.AvailableLanguages(available_languages=test_results)
    except Exception as e:
        logger.error(f"Error generating test language pairs: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
