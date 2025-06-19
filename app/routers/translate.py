"""
Translation Router Module.

This module provides API endpoints for translating medical terms from one language
to another. It includes both production and test endpoints for translation services.
"""

import logging
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from config import LOGGER_NAME
from database import get_database_session
from func.translate_with_database import translate_with_database
from schemas import TranslationResult

# Initialize router with prefix and tags for API documentation
router = APIRouter(prefix="/translate", tags=["translation"])
# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.Translation, status_code=status.HTTP_201_CREATED)
async def get_translation(
    query: schemas.TranslationQuery, 
    db: Session = Depends(get_database_session)
) -> schemas.Translation:
    """
    Translate a medical term from one language to another.
    
    This endpoint receives a translation query containing a medical term and target language,
    then attempts to find the appropriate translation in the database.
    
    Args:
        query (schemas.TranslationQuery): The query containing the term to translate
                                         and the target language.
        db (Session): Database session for querying translations.
        
    Returns:
        schemas.Translation: The translation results.
        
    Raises:
        HTTPException 500: If an error occurs during the translation process.
    """
    try:
        logger.info(f"Received translation query: {query}")
        results = translate_with_database(db, query)
        len_results = len(results.results) or 0
        logger.info(f"Successfully translated term with {len_results} results")
        return results
    except Exception as e:
        error_message = f"Error translating term: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )


@router.post("/test", response_model=schemas.Translation, status_code=status.HTTP_201_CREATED)
async def get_translation_test(
    query: schemas.TranslationQuery, 
    db: Session = Depends(get_database_session)
) -> schemas.Translation:
    """
    Generate test translation results for development and testing purposes.
    
    This endpoint creates mock translation results without accessing the database.
    It's useful for testing the API without requiring actual translations.
    
    Args:
        query (schemas.TranslationQuery): The query containing the term to translate
                                         and the target language (not used for actual translation).
        db (Session): Database session (not used for actual translation).
        
    Returns:
        schemas.Translation: Mock translation results.
        
    Raises:
        HTTPException 500: If an error occurs during the test generation process.
    """
    try:
        logger.info(f"Received test translation query: {query}")
        logger.debug(f"Database info: {db.info}")
        
        def create_mock_result(number: int) -> TranslationResult:
            """
            Create a mock translation result.
            
            Args:
                number (int): Index number to use in the mock result.
                
            Returns:
                Dict[str, Any]: A mock translation result dictionary.
            """
            return schemas.TranslationResult(
                translated_name=f"translated_name{number}",
                translated_source=f"translated_source{number}",
                translated_uid=number
            )
        
        # Generate 5 mock translation results
        results = schemas.Translation(results=[create_mock_result(i) for i in range(5)])
        logger.info(f"Generated {len(results.results)} test translation results")
        return results
    except Exception as e:
        error_message = f"Error generating test translations: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )
