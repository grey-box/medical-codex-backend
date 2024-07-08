import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from func import fuzzymatching
import schemas
import dependancies
from config import LOGGER_NAME

router = APIRouter(prefix='/fuzzymatching', tags=['fuzzymatching'])
logger = logging.getLogger(LOGGER_NAME)


@router.get('/', response_model=schemas.FuzzyMatching)
def get_fuzzymatching(query: schemas.FuzzyQuery, db: Session = Depends(dependancies.get_db)):
    results = fuzzymatching.fuzzy_matching(db, query)
    logging.info(results)
    return results


@router.get('/test', response_model=schemas.FuzzyMatching)
def get_fuzzymatching_test(query: schemas.FuzzyQuery, db: Session = Depends(dependancies.get_db)):
    logging.info(query)
    logging.info(db.info)

    def result(number):
        return {
            "matching_name": f"matching_name{number}",
            "matching_source": f"matching_source{number}",
            "matching_uid": number
        }

    results = {"results": [
        result(i) for i in range(5)
    ]}
    return results
