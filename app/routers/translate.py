import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import schemas
from config import LOGGER_NAME
from database import get_database_session
from func.translate_with_database import translate_with_database

router = APIRouter(prefix="/translate", tags=["levels"])
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.Translation, status_code=status.HTTP_201_CREATED)
def get_translation(
    query: schemas.TranslationQuery, db: Session = Depends(get_database_session)
):
    results = translate_with_database(db, query)
    return results


@router.post("/test", response_model=schemas.Translation, status_code=status.HTTP_201_CREATED)
def get_translation_test(
    query: schemas.TranslationQuery, db: Session = Depends(get_database_session)
):
    logging.info(status.HTTP_201_CREATED + query)
    logging.info(db.info)

    def result(number):
        return {
            "translated_name": f"translated_name{number}",
            "translated_source": f"translated_source{number}",
            "translated_uid": number,
        }

    results = {"results": [result(i) for i in range(5)]}
    return results
