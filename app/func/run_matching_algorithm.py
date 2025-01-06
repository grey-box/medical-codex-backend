import logging
from typing import List, Callable

from sqlalchemy.orm import Session

from app.config import LOGGER_NAME
from func.get_unique_source_texts import get_unique_source_texts
from schemas import FuzzyQuery, FuzzyAlgorithm, FuzzyResult

logger = logging.getLogger(LOGGER_NAME)


def execute_algorithm(func: Callable, **kwargs) -> List[FuzzyResult]:
    try:
        matches = func(**kwargs)
        logger.info(f"Found {len(matches)} matches for query: {kwargs.get('query')}")
        return matches
    except Exception as error:
        logger.error(f"Error during {func.__name__} algorithm: {str(error)}")
        return []


def run_matching_algorithm(
    algorithm: FuzzyAlgorithm,
    db: Session,
    query_params: FuzzyQuery,
) -> List[FuzzyResult]:
    """
    Run the specified matching algorithm with given parameters.

    Args:
        algorithm: The matching algorithm to execute.
        db: The database session.
        query_params: The fuzzy matching query parameters.

    Returns:
        A list of FuzzyResult objects.
    """
    logger.info(
        f"Running {algorithm.function.__name__} algorithm for query: {query_params.query}"
    )

    common_params = {
        "language": query_params.language,
        "query": query_params.query.lower(),
        "max_distance": query_params.max_distance,
        "max_results": query_params.max_results,
    }

    if algorithm.local:
        source_texts = get_unique_source_texts(db, query_params)
        common_params["medications"] = source_texts
    else:
        common_params["db"] = db

    return execute_algorithm(algorithm.function, **common_params)
