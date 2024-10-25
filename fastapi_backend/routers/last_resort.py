import logging

from fastapi import APIRouter, HTTPException
import schemas
from func.ai_translation import last_resort_translation
from config import LOGGER_NAME

router = APIRouter(prefix="/last-resort", tags=["last_resort"])
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.LastResortResponse)
def get_last_resort_translation(query: schemas.LastResortQuery):
    logger.info(f"Received query: {query}")
    try:
        translated_name = last_resort_translation(query.medicine, query.target_language)
        logger.info(f"Translated name: {translated_name}")
        return {
            "translated_medicine": translated_name  # Return the translated medicine
        }
    except Exception as e:
        logger.error(f"Error during last resort translation: {e}")
        raise HTTPException(status_code=500, detail="AI translation failed")

