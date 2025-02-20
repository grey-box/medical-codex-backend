import logging

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.config import LOGGER_NAME, settings
from app.database import get_database_session
from app.func.store_manual_translation import store_manual_translation

router = APIRouter(prefix="/manual_translation", tags=["manual_translation"])
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.FallbackResponse)
async def manual_translation(
    query: schemas.ManualTranslationQuery, db: Session = Depends(get_database_session)
) -> schemas.ManualTranslationResponse:
    """
    Translate medicine name using AI as a last resort.

    Args:
        query (schemas.ManualTranslationQuery): Query containing the medical term, the lanugage to convert to, and the language to convert from.

    Returns:
        schemas.ManualTranslationResponse: Response stating the term has been put into the database for manual translation.

    Raises:
        HTTPException: Database storage fails.
    """
    logger.info(f"Received manual translation query: {query}")
    try:
        stored_medicine = store_manual_translation(
            db, query
        )
        logger.info(
            f"Successfully stored '{stored_medicine}'"
        )
        return schemas.ManualTranslationResponse(storedTranslationResponse=stored_medicine)
    except Exception as error:
        error_message = f"Manual translation store failed for '{query.term}': {str(error)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)