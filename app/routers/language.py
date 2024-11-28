import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import test

from app.database import get_db
import app.models as models
import app.schemas as schemas
from app.config import LOGGER_NAME

router = APIRouter(prefix="/languages", tags=["languages"])
logger = logging.getLogger(LOGGER_NAME)


@router.get("/", response_model=schemas.AvailableLanguages)
def get_languages(db: Session = Depends(get_db)):
    '''
        Gets the languages currently available to translate works to
        and from using the translate endpoint
    '''
    # Query to get the langauge pairs from a View in the DB
    language_pairs = db.query(
            models.LanguagePairs
        ).order_by(
            models.LanguagePairs.source_language.asc(),
            models.LanguagePairs.target_language.asc()
        ).all()
    
    # Group Languages with list of languages they can be translated to
    grouped_languages = {}
    for language in language_pairs:
        if language.source_language not in grouped_languages:
            grouped_languages[language.source_language] = []
        grouped_languages[language.source_language].append(language.target_language)

    # Covert to pydantic models
    avialable_languages_list = [
        schemas.AvailableLanguageResult(
            source_language=source,
            target_languages=targets,
        )
        for source, targets in grouped_languages.items()
    ]

    # Log the pairs we are returning
    logger.info(f'\nLanguage pairs:\n{language_pairs}')
    
    # Translate to a list based on the pydantic schemas
    return schemas.AvailableLanguages(available_languages=avialable_languages_list)

@router.get("/test", response_model=schemas.AvailableLanguages)
def get_translation_test(
    db: Session = Depends(get_db)
):
    logging.info(db.info)

    def result(num_range):
        
        test_result = []

        for num in range(1, num_range + 1):
            
            source_language = f'lang{num}'
            target_languages = [f'lang{i}' for i in range(1, num_range + 1) if i != num]

            test_result.append({
                'source_language': source_language,
                'target_languages': target_languages, 

            })

        return test_result

    results = {"available_languages": result(3)}
    return results
