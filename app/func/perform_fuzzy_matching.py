import logging
from typing import Dict, Any, List

from sqlalchemy.orm import Session

import app.schemas
from app.algorithms.search_medications_by_levenshtein import (
    search_medications_by_levenshtein,
)
from app.algorithms.search_medications_by_soundex import search_medications_by_soundex
from app.config import LOGGER_NAME
from app.func.get_unique_source_texts import get_unique_source_texts
from app.func.run_matching_algorithm import run_matching_algorithm

logger = logging.getLogger(LOGGER_NAME)


def perform_fuzzy_matching(
    db: Session,
    query: app.schemas.FuzzyQuery,
    matching_algorithm: str = "Levenshtein",
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Perform fuzzy matching on the given query using the specified algorithm.

    Args:
        db (Session): The database session.
        query (app.schemas.FuzzyQuery): The query parameters for fuzzy matching.
        matching_algorithm (str): The name of the matching algorithm to use.

    Returns:
        Dict[str, List[Dict[str, Any]]]: A dictionary containing the matching results.
    """
    algorithms = {
        "Levenshtein": search_medications_by_levenshtein,
        "Soundex": search_medications_by_soundex,
    }

    try:
        unique_source_texts = get_unique_source_texts(db, query.source_language)

        algorithm = algorithms.get(matching_algorithm)
        if not algorithm:
            logger.error(f"Unsupported matching algorithm: {matching_algorithm}")
            return {"results": []}

        matched_medications = run_matching_algorithm(
            algorithm,
            str(query.source_language),
            unique_source_texts,
            str(query.query),
            int(query.threshold),
            int(query.nb_max_results),
        )

        logger.info(f"Matched medications: {matched_medications}")

        results = {
            "results": [
                {
                    "matching_name": medication,
                    "matching_source": "wikidata",  # Replace with the actual source
                    "matching_algorithm": matching_algorithm,
                    "matching_uid": 0,  # We'll get this from the database
                }
                for medication in matched_medications
            ]
        }

        logger.info(f"Fuzzy matching results: {results}")
        return results

    except Exception as e:
        logger.error(f"Error in fuzzy matching: {str(e)}")
        return {"results": []}
