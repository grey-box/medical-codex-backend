"""
Fallback Translation Module.

This module provides functionality for translating text using fallback methods
when primary translation methods fail. It serves as a safety net to ensure
translation services remain available even when the primary methods are unavailable.

Currently supported fallback methods:
- gemini: Uses Google's Gemini AI for translation
"""

import logging

from fastapi import HTTPException, status

from config import LOGGER_NAME, settings
from func.get_gemini_translation import get_gemini_translation
from schemas import TranslationQuery, Translation

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)

# Define supported fallback methods
SUPPORTED_FALLBACK_METHODS = ["gemini"]


def translate_using_fallback(
    query: TranslationQuery,
    fallback_method: str = settings.fallback_translation_method,
) -> Translation:
    """
    Translate text using a fallback method when primary translation fails.
    
    This function attempts to translate text using the specified fallback method.
    It serves as a safety net when database translations or other primary methods
    are unavailable or unsuccessful.
    
    Currently supported fallback methods:
    - gemini: Uses Google's Gemini AI for translation
    
    Args:
        query (TranslationQuery): Translation query containing the text to translate and target language.
        fallback_method (str, optional): The fallback translation method to use.
                                        Defaults to the value specified in settings.
        
    Returns:
        str: The translated text if successful.
        
    Raises:
        HTTPException: With appropriate status code if the translation fails or
                      the fallback method is not supported.
    """
    source_text = query.translation_query.matching_name
    target_lang = query.target_language
    
    logger.info(
        f"Attempting fallback translation using '{fallback_method}' method: "
        f"'{source_text}' to {target_lang}"
    )
    
    # Validate fallback method
    if fallback_method not in SUPPORTED_FALLBACK_METHODS:
        error_message = (
            f"Unsupported fallback translation method: '{fallback_method}'. "
            f"Supported methods: {', '.join(SUPPORTED_FALLBACK_METHODS)}"
        )
        logger.warning(error_message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    # Attempt translation using the specified fallback method
    try:
        if fallback_method == "gemini":
            return _translate_with_gemini(query)
        
        # This should never be reached due to the validation above,
        # but included for future extensibility
        raise ValueError(f"Implementation missing for method: {fallback_method}")
        
    except Exception as e:
        error_message = f"Fallback translation failed: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )


def _translate_with_gemini(query: TranslationQuery) -> Translation:
    """
    Helper function to translate text using Google's Gemini AI.
    
    Args:
        query (TranslationQuery): Translation query containing the text to translate
                                 and language information.
        
    Returns:
        str: The translated text.
        
    Raises:
        ValueError: If the Gemini translation returns empty or invalid results.
    """
    logger.debug(f"Translating with Gemini AI: '{query.translation_query.matching_name}'")
    
    # Call the Gemini translation function
    translation_result = get_gemini_translation(query)

    return translation_result
