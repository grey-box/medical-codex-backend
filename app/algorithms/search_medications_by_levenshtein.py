import logging
from typing import List

import Levenshtein

from algorithms.filter_medications_by_distance import filter_medications_by_distance
from algorithms.get_top_matches_by_distance import get_top_matches_by_distance
from config import LOGGER_NAME
from func.normalize_and_filter_strings import normalize_and_filter_strings
from schemas import FuzzyResult
from fastapi import status

logger = logging.getLogger(LOGGER_NAME)


def search_medications_by_levenshtein(
    language: str,
    medications: List[str],
    query: str,
    max_distance: int = 10,
    max_results: int = 10,
) -> List[FuzzyResult]:
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
        List[FuzzyResult]: List of FuzzyResult objects matching the query within the specified max_distance.

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
        top_matches = get_top_matches_by_distance(
            filtered_medications, distances, max_results
        )

        # Create FuzzyResult objects for each matched medication
        fuzzy_results = [
            FuzzyResult(
                matching_name=medication,
                matching_source="Levenshtein",
                matching_algorithm="Levenshtein (Local)",
                matching_uid=0,  # You may need to adjust this if you have a way to get the UID
                matching_row_number=index + 1
            )
            for index, medication in enumerate(top_matches)
        ]

        logger.info(status.HTTP_200_OK + f" Levenshtein search results: {fuzzy_results}")
        return fuzzy_results

    except Exception as e:
        logger.error(status.HTTP_400_BAD_REQUEST + f" Error in Levenshtein search: {str(e)}")
        raise