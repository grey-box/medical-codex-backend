import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.database as database
from app import schemas
from app.config import LOGGER_NAME
from func import perform_fuzzy_matching

router = APIRouter(prefix="/fuzzymatching", tags=["fuzzymatching"])
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.FuzzyMatching)
def get_fuzzymatching(
    query: schemas.FuzzyQuery, db: Session = Depends(database.get_database_session)
):
    results = perform_fuzzy_matching.perform_fuzzy_matching(db, query)
    logging.info(results)
    return results


@router.post("/test", response_model=schemas.FuzzyMatching)
def get_fuzzymatching_test(
    query: schemas.FuzzyQuery, db: Session = Depends(database.get_database_session)
):
    logging.info(query)
    logging.info(db.info)

    def result(number):
        return {
            "matching_name": f"matching_name{number}",
            "matching_source": f"matching_source{number}",
            "matching_uid": number,
        }

    results = {"results": [result(i) for i in range(5)]}
    return results
