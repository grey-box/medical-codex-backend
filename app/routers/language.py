import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.database as database
import app.models as models
import app.schemas as schemas
from app.config import LOGGER_NAME

router = APIRouter(prefix="/languages", tags=["languages"])
logger = logging.getLogger(LOGGER_NAME)


@router.get("/", response_model=schemas.TranslationLanguageResult)
def get_languages(db: Session = Depends(database.get_db)):
    return db.query(models.LanguagePairs).all()
