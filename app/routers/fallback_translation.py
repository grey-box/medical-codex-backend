"""
Fallback Translation Router Module.

This module provides API endpoints for fallback translation services when
standard translation methods fail. It uses AI-based translation as a last resort.
"""

import logging

from fastapi import APIRouter, HTTPException, status

import schemas
from config import LOGGER_NAME, settings
from func.translate_using_fallback import translate_using_fallback

# Initialize router with prefix and tags for API documentation
router = APIRouter(prefix="/fallback_translation", tags=["fallback_translation"])
# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.FallbackResponse, status_code=status.HTTP_201_CREATED)
async def fallback_translation(
    query: schemas.FallbackQuery,
) -> schemas.FallbackResponse:
    """
    Translate medicine name using AI as a last resort.

    This endpoint is called when standard translation methods have failed.
    It attempts to translate the medicine name using the configured fallback method
    (typically an AI-based translation service).

    Args:
        query (schemas.FallbackQuery): Query containing medicine name and target language.

    Returns:
        schemas.FallbackResponse: Response containing the translation and the fallback method.
        
    Raises:
        HTTPException 400: If there's a validation error with the input.
        HTTPException 500: If the AI translation service fails or any other error occurs.
    """
    # Log the incoming request
    logger.info(f"Received last resort translation query: {query}")
    
    try:
        # Create a translation query from the input and call the fallback translation function
        translation_query = schemas.TranslationQuery(
            translation_query=query.medicine,
            target_language=query.target_language,
        )
        
        translated_medicine = translate_using_fallback(
            translation_query,
            fallback_method=settings.fallback_translation_method,
        )
        
        # Log successful translation
        logger.info(
            f"Successfully translated '{query.medicine}' to '{str(translated_medicine.results)}'"
        )
        
        # Return the translated medicine name
        return schemas.FallbackResponse(translated_medicine=translated_medicine,
                                        fallback_method=settings.fallback_translation_method)
    
    except ValueError as e:
        # Handle validation errors with 400 Bad Request
        error_message = f"Value error in fallback translation: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=error_message
        )
    
    except Exception as e:
        # Handle all other errors with 500 Internal Server Error
        error_message = f"Error in fallback translation: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=error_message
        )
