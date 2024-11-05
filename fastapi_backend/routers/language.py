import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dependancies
import models
import schemas
from config import LOGGER_NAME

router = APIRouter(prefix='/languages', tags=['languages'])
logger = logging.getLogger(LOGGER_NAME)


@router.get("/", response_model=schemas.TranslationLanguageResult)
def get_languages(db: Session = Depends(dependancies.get_db)):
    return db.query(models.Languages).all()
