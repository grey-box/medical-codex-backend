import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dependancies
import schemas
import translation
from config import LOGGER_NAME

router = APIRouter(prefix='/translate', tags=['levels'])
logger = logging.getLogger(LOGGER_NAME)


@router.get("/", response_model=List[schemas.Translation])
def get_fuzzymatching( query: schemas.TranslationQuery, db: Session = Depends(dependancies.get_db)):
    results = translation.translate(db, query)
    return results
