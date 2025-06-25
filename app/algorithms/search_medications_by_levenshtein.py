"""
Levenshtein Search Module.

This module provides functionality for searching medications using the
Levenshtein distance algorithm, which measures the minimum number of
single-character edits required to change one string into another.
"""

import logging
from typing import List

import Levenshtein
from fastapi import HTTPException, status

from algorithms.filter_medications_by_distance import filter_medications_by_distance
from algorithms.get_top_matches_by_distance import get_top_matches_by_distance
from config import LOGGER_NAME
from func.normalize_and_filter_strings import normalize_and_filter_strings
from schemas import FuzzyResult

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)

# Supported languages for medication search
SUPPORTED_LANGUAGES = ["en", "uk", "ru"]


def search_medications_by_levenshtein(
    language: str,
    medications: List[str],
    query: str,
    max_distance: int = 10,
    max_results: int = 10,
) -> List[FuzzyResult]:
    """
    Search for medications using Levenshtein distance.

    Perform a fuzzy search for medication names using the Levenshtein distance algorithm,
    which measures the minimum number of single-character edits (insertions, deletions,
    or substitutions) required to change one string into another.

    Args:
        language (str): Language of the input and medication names.
            Must be one of: 'en' (English), 'uk' (Ukrainian), or 'ru' (Russian).
        medications (List[str]): List of medication names to search through.
        query (str): Input string to search for.
        max_distance (int, optional): Maximum Levenshtein distance allowed.
            Higher values allow more dissimilar matches. Defaults to 10.
        max_results (int, optional): Maximum number of results to return.
            Results are sorted by distance (closest matches first). Defaults to 10.

    Returns:
        List[FuzzyResult]: List of FuzzyResult objects matching the query
            within the specified max_distance, sorted by relevance.

    Raises:
        HTTPException: If the language is invalid or if an error occurs during processing.
    """
    try:
        # Validate language parameter
        if language not in SUPPORTED_LANGUAGES:
            error_message = f"Invalid language: {language}. Supported languages: {', '.join(SUPPORTED_LANGUAGES)}"
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )

        # Step 1: Normalize and filter medication strings
        logger.debug(f"Normalizing {len(medications)} medications for Levenshtein search")
        processed_medications = normalize_and_filter_strings(medications, query)
        
        # Step 2: Filter medications by Levenshtein distance
        logger.debug(f"Filtering medications with max distance {max_distance}")
        filtered_medications, distances = filter_medications_by_distance(
            processed_medications, query, Levenshtein.distance, max_distance
        )
        
        # Step 3: Get top matches based on distance
        logger.debug(f"Getting top {max_results} matches from {len(filtered_medications)} filtered medications")
        top_matches = get_top_matches_by_distance(
            filtered_medications, distances, max_results
        )

        # Step 4: Create FuzzyResult objects for each matched medication
        fuzzy_results = [
            FuzzyResult(
                matching_name=medication,
                matching_source="Levenshtein",
                matching_algorithm="Levenshtein (Local)",
                matching_uid=0,  # Default UID as 0 for local search results
                matching_row_number=index + 1,
                distance = Levenshtein.distance(medication, query)
            )
            for index, medication in enumerate(top_matches)
        ]

        # Log the results
        logger.info(f"Found {len(fuzzy_results)} medications matching '{query}' using Levenshtein search")
        return fuzzy_results

    except HTTPException:
        # Re-raise HTTP exceptions to preserve their status codes
        raise
    except Exception as e:
        # Convert other exceptions to HTTPException
        error_message = f"Error in Levenshtein search: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )
