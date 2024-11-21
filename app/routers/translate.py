import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.schemas as schemas
from app.config import LOGGER_NAME
from app.database import get_db
from app.func import translation

router = APIRouter(prefix="/translate", tags=["levels"])
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.Translation)
def get_translation(query: schemas.TranslationQuery, db: Session = Depends(get_db)):
    results = translation.translate(db, query)
    return results


@router.post("/test", response_model=schemas.Translation)
def get_translation_test(
    query: schemas.TranslationQuery, db: Session = Depends(get_db)
):
    logging.info(query)
    logging.info(db.info)

    def result(number):
        return {
            "translated_name": f"translated_name{number}",
            "translated_source": f"translated_source{number}",
            "translated_uid": number,
        }

    results = {"results": [result(i) for i in range(5)]}
    return results

@router.post("/lastresort", response_model=schemas.Translation)
def get_last_resort_translation(query: schemas.TranslationQuery, agnosticModel: str = "gemini"):
    results = translation.lastResortTranslate(query, agnosticModel)
    return results