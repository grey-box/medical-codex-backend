import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dependancies
import schemas
from func import translation
from config import LOGGER_NAME

router = APIRouter(prefix='/translate', tags=['levels'])
logger = logging.getLogger(LOGGER_NAME)


@router.get("/", response_model=schemas.TranslationResult)
def get_translation(query: schemas.TranslationQuery, db: Session = Depends(dependancies.get_db)):
    results = translation.translate(db, query)
    return results


@router.get("/test", response_model=schemas.Translation)
def get_translation_test(query: schemas.TranslationQuery, db: Session = Depends(dependancies.get_db)):
    logging.info(query)
    logging.info(db.info)

    def result(number):
        return {
            "translated_name": f"translated_name{number}",
            "translated_source": f"translated_source{number}",
            "translated_uid": number
        }

    results = {"results": [
        result(i) for i in range(5)
    ]}
    return results
