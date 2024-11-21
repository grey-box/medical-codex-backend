import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.database as database
import app.models as models
import app.schemas as schemas
from app.config import LOGGER_NAME

router = APIRouter(prefix="/languages", tags=["languages"])
logger = logging.getLogger(LOGGER_NAME)


@router.get("/", response_model=schemas.AvailableLanguages)
def get_languages(db: Session = Depends(database.get_db)):
    '''
        Gets the languages currently available to translate works to
        and from using the translate endpoint
    '''
    # Query to get the langauge pairs from a View in the DB
    language_pairs = db.query(
            models.LanguagePairs
        ).order_by(
            models.LanguagePairs.source_language.asc()
        ).all()
    
    # Covert to pydantic models
    avialable_languages = [
        schemas.AvailableLanguageResult(
            source_language=language.source_language,
            target_language=language.target_language,
        )
        for language in language_pairs
        ]

    # Log the pairs we are returning
    logger.info(f'\nLanguage pairs:\n{language_pairs}')
    
    # Translate to a list based on the pydantic schemas
    return schemas.AvailableLanguages(translations=avialable_languages)

    
