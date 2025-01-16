import logging
from typing import Dict, List

from sqlalchemy.orm import Session

import app.schemas
from app.algorithms.dbquery_medications import (
    dbquery_medications_with_daitch_mokotoff,
    dbquery_medications_with_levenstein,
)
from app.algorithms.search_medications_by_levenshtein import (
    search_medications_by_levenshtein,
)
from app.algorithms.search_medications_by_soundex import search_medications_by_soundex
from app.config import LOGGER_NAME
from app.func.run_matching_algorithm import run_matching_algorithm
from app.schemas import FuzzyAlgorithm
from schemas import FuzzyResult

logger = logging.getLogger(LOGGER_NAME)


def perform_fuzzy_matching(
    db: Session,
    query: app.schemas.FuzzyQuery,
    matching_algorithm: str = "DaitchMokotoffDB",
) -> Dict[str, List[FuzzyResult]]:
    """
    Perform fuzzy matching on the given query using the specified algorithm.

    Args:
        db (Session): The database session.
        query (app.schemas.FuzzyQuery): The query parameters for fuzzy matching.
        matching_algorithm (str): The name of the matching algorithm to use.

    Returns:
        Dict[str, List[FuzzyResult]]: A dictionary containing the matching results.
    """
    algorithms = {
        "LevenshteinLocal": FuzzyAlgorithm(
            function=search_medications_by_levenshtein,
            local=True,
            name="Levenshtein (Local)",
        ),
        "SoundexLocal": FuzzyAlgorithm(
            function=search_medications_by_soundex, local=True, name="Soundex (Local)"
        ),
        "LevenshteinDB": FuzzyAlgorithm(
            function=dbquery_medications_with_levenstein,
            local=False,
            name="Levenshtein (Database)",
        ),
        "DaitchMokotoffDB": FuzzyAlgorithm(
            function=dbquery_medications_with_daitch_mokotoff,
            local=False,
            name="Daitch-Mokotoff (Database)",
        ),
    }

    try:
        algorithm = algorithms.get(matching_algorithm)
        if not algorithm:
            logger.error(f"Unsupported matching algorithm: {matching_algorithm}")
            return {"results": []}

        matched_medications = run_matching_algorithm(algorithm, db, query)

        logger.info(f"Matched medications: {matched_medications}")

        return {"results": matched_medications}

    except Exception as e:
        logger.error(f"Error in fuzzy matching: {str(e)}")
        return {"results": []}
