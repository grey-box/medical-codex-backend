import logging
from typing import Callable, List

from app.config import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def run_matching_algorithm(
    algorithm: Callable,
    source_language: str,
    source_texts: List[str],
    query_text: str,
    distance_threshold: int,
    max_results: int,
) -> List[str]:
    """
    Run the specified matching algorithm with given parameters.

    Args:
        algorithm: The matching algorithm to execute.
        source_language: The language of the source texts.
        source_texts: The list of source texts to match against.
        query_text: The input text to match.
        distance_threshold: The maximum distance allowed for a match.
        max_results: The maximum number of results to return.

    Returns:
        A list of matched texts.
    """
    logger.info(f"Running {algorithm.__name__} algorithm for query: {query_text}")
    try:
        matches = algorithm(
            source_language=source_language,
            source_data=source_texts,
            input_string=query_text.lower(),
            threshold=distance_threshold,
            nb_max_results=max_results,
        )
        logger.info(f"Found {len(matches)} matches for query: {query_text}")
        return matches
    except Exception as error:
        logger.error(f"Error during {algorithm.__name__} algorithm: {str(error)}")
        return []
