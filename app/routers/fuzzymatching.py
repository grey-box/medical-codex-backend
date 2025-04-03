import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import database
import schemas
from config import LOGGER_NAME
from func import perform_fuzzy_matching

router = APIRouter(prefix="/fuzzymatching", tags=["fuzzymatching"])
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.FuzzyMatching, status_code=status.HTTP_201_CREATED)
def get_fuzzymatching(
    query: schemas.FuzzyQuery, db: Session = Depends(database.get_database_session)
):
    results = perform_fuzzy_matching.perform_fuzzy_matching(db, query)
    logging.info(status.HTTP_201_CREATED + results)
    return results


@router.post("/test", response_model=schemas.FuzzyMatching, status_code=status.HTTP_201_CREATED)
def get_fuzzymatching_test(
    query: schemas.FuzzyQuery, db: Session = Depends(database.get_database_session)
):
    logging.info(status.HTTP_201_CREATED + query)
    logging.info(db.info)

    def result(number):
        return {
            "matching_name": f"matching_name{number}",
            "matching_source": f"matching_source{number}",
            "matching_uid": number,
            "matching_algorithm": "test",
            "matching_row_number": number + 1,  # This is just for testing purposes.
        }

    results = {"results": [result(i) for i in range(5)]}
    return results
