import logging
from typing import Dict, List, Any

import schemas
from app.config import LOGGER_NAME, settings
from app.func.get_gemini_translation import get_gemini_translation
from fastapi import status

logger = logging.getLogger(LOGGER_NAME)


def translate_using_fallback(
    query: schemas.TranslationQuery,
    fallback_method: str = settings.fallback_translation_method,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Translate using a fallback method when primary translation fails.

    Args:
        query (schemas.TranslationQuery): Translation query parameters.
        fallback_method (str): Fallback translation method to use.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Translation results.
    """
    try:
        if fallback_method == "gemini":
            return get_gemini_translation(query)
        else:
            logger.warning(status.HTTP_400_BAD_REQUEST + 
                f" Unsupported fallback translation method: {fallback_method}"
            )
            return {"results": []}
    except Exception as e:
        logger.error(status.HTTP_500_INTERNAL_SERVER_ERROR + f" Error in fallback translation using {fallback_method}: {str(e)}")
        return {"results": []}
