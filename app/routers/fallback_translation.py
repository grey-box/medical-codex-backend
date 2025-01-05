import logging

from fastapi import APIRouter, HTTPException

from app import schemas
from app.config import LOGGER_NAME, settings
from app.func.translate_using_fallback import translate_using_fallback

router = APIRouter(prefix="/fallback_translation", tags=["fallback_translation"])
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.FallbackResponse)
async def fallback_translation(
    query: schemas.FallbackQuery,
) -> schemas.FallbackResponse:
    """
    Translate medicine name using AI as a last resort.

    Args:
        query (schemas.FallbackQuery): Query containing medicine name and target language.

    Returns:
        schemas.FallbackResponse: Response containing the translated medicine name.

    Raises:
        HTTPException: If AI translation fails.
    """
    logger.info(f"Received last resort translation query: {query}")
    try:
        translated_medicine = translate_using_fallback(
            schemas.TranslationQuery(
                translation_query=query.medicine.matching_name,
                target_language=query.target_language,
            ),
            fallback_method=settings.fallback_translation_method,
        )
        logger.info(
            f"Successfully translated '{query.medicine}' to '{translated_medicine}'"
        )
        return schemas.FallbackResponse(translated_medicine=translated_medicine)
    except Exception as error:
        error_message = f"AI translation failed for '{query.medicine}': {str(error)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
