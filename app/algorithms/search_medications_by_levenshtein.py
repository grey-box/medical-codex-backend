import logging
from typing import List

import Levenshtein

from app.algorithms.filter_medications_by_distance import filter_medications_by_distance
from app.algorithms.get_top_matches_by_distance import get_top_matches_by_distance
from app.config import LOGGER_NAME
from app.func.normalize_and_filter_strings import normalize_and_filter_strings

logger = logging.getLogger(LOGGER_NAME)


def search_medications_by_levenshtein(
    language: str,
    medications: List[str],
    query: str,
    max_distance: int = 10,
    max_results: int = 10,
) -> List[str]:
    """
    Search for medications using Levenshtein distance.

    Perform a fuzzy search for medication names using the Levenshtein distance algorithm.

    Args:
        language (str): Language of the input and medication names ('en', 'uk', or 'ru').
        medications (List[str]): List of medication names to search through.
        query (str): Input string to search for.
        max_distance (int, optional): Maximum Levenshtein distance allowed. Defaults to 10.
        max_results (int, optional): Maximum number of results to return. Defaults to 10.

    Returns:
        List[str]: List of medication names matching the query within the specified threshold.

    Raises:
        ValueError: If the language is invalid.
    """
    try:
        if language not in ["en", "uk", "ru"]:
            raise ValueError(f"Invalid language: {language}")

        processed_medications = normalize_and_filter_strings(medications, query)
        filtered_medications, distances = filter_medications_by_distance(
            processed_medications, query, Levenshtein.distance, max_distance
        )
        top_matches = get_top_matches_by_distance(filtered_medications, distances, max_results)

        logger.info(f"Levenshtein search results: {top_matches}")
        return top_matches

    except Exception as e:
        logger.error(f"Error in Levenshtein search: {str(e)}")
        raise
