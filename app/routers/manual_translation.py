import logging

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

import schemas
from config import LOGGER_NAME, settings
from database import get_database_session
from func.store_manual_translation import store_manual_translation

# Initialize router with prefix and tags for API documentation
router = APIRouter(prefix="/manual_translation", tags=["manual_translation"])
# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.FallbackResponse, status_code=status.HTTP_201_CREATED)
async def manual_translation(
    query: schemas.ManualTranslationQuery, 
    db: Session = Depends(get_database_session)
) -> schemas.FallbackResponse:
    """
    Store a medical term for manual translation by human translators.
    
    This endpoint receives a medical term and language information, then stores
    the request in the database for later processing by human translators.
    This is typically used when automated translation methods are insufficient
    or unavailable.
    
    Args:
        query (schemas.ManualTranslationQuery): Query containing the medical term,
                                               the target language, and the source language.
        db (Session): Database session for storing the translation request.
        
    Returns:
        schemas.FallbackResponse: Response confirming the term has been stored
                                 for manual translation.
        
    Raises:
        HTTPException 500: If there's an error storing the request in the database.
    """
    # Log the incoming request
    logger.info(f"Received manual translation query: {query}")
    
    try:
        # Store the translation request in the database
        store_manual_translation(db, query)
        
        # Log successful storage
        logger.info(f"Successfully stored term '{query.term}' for manual translation")
        
        # Create and return the response
        response_message = f"Term '{query.term}' has been submitted for manual translation"
        return schemas.FallbackResponse(translated_medicine=response_message,
                                        fallback_method=settings.fallback_translation_method
                                        )
        
    except Exception as error:
        # Handle any errors that occur during storage
        error_message = f"Manual translation request failed for '{query.term}': {str(error)}"
        logger.error(error_message)
        
        # Raise an HTTP exception with appropriate status code and detail
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )
