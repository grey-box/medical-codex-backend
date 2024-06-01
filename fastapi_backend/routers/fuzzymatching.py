import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import fuzzymatching
import schemas
import dependancies
from config import LOGGER_NAME

router = APIRouter(prefix='/fuzzymatching', tags=['fuzzymatching'])
logger = logging.getLogger(LOGGER_NAME)


@router.get("/", response_model=List[schemas.FuzzyMatching])
def get_fuzzymatching(query: schemas.FuzzyQuery, db: Session = Depends(dependancies.get_db)):
    results = fuzzymatching.fuzzy_matching(db, query)
    return results
