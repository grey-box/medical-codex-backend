"""
Soundex Search Module.

This module provides functionality for searching medications using the
Soundex algorithm, which is a phonetic algorithm for indexing names by sound,
as pronounced in English. The algorithm provides a way to group similar-sounding
names together, making it useful for fuzzy matching of medication names.
"""

import logging
from typing import List, Dict

from fastapi import HTTPException, status
from fonetika.distance import PhoneticsInnerLanguageDistance
from fonetika.soundex import EnglishSoundex, RussianSoundex

from algorithms.filter_medications_by_distance import filter_medications_by_distance
from algorithms.get_top_matches_by_distance import get_top_matches_by_distance
from config import LOGGER_NAME
from func.normalize_and_filter_strings import normalize_and_filter_strings
from schemas import FuzzyResult

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)

# Define language to soundex mappings
LANGUAGE_SOUNDEX_MAP: Dict[str, tuple] = {
    "en": (EnglishSoundex(), "English Soundex"),
    "fr": (EnglishSoundex(), "English Soundex"),
    "ru": (RussianSoundex(), "Russian Soundex"),
    "uk": (RussianSoundex(), "Russian Soundex"),
}


def search_medications_by_soundex(
    language: str,
    medications: List[str],
    query: str,
    max_distance: float = 2,
    max_results: int = 10,
) -> List[FuzzyResult]:
    """
    Search for medications using Soundex algorithm.

    Perform a fuzzy search for medication names using the Soundex algorithm
    based on the specified language. Soundex is a phonetic algorithm that
    indexes words by their sound when pronounced in English or Russian.

    Args:
        language (str): Language of the input and medication names.
            Supported languages: 'en' (English), 'fr' (French),
            'ru' (Russian), or 'uk' (Ukrainian).
        medications (List[str]): List of medication names to search through.
        query (str): Input string to search for.
        max_distance (float, optional): Maximum phonetic distance allowed.
            Lower values require closer phonetic matches. Defaults to 2.
        max_results (int, optional): Maximum number of results to return.
            Results are sorted by phonetic similarity. Defaults to 10.

    Returns:
        List[FuzzyResult]: List of FuzzyResult objects matching the query
            within the specified max_distance, sorted by phonetic similarity.

    Raises:
        HTTPException: If the language is unsupported or if an error occurs during processing.
    """
    try:
        # Step 1: Normalize and filter medication strings
        logger.debug(f"Normalizing {len(medications)} medications for Soundex search")
        processed_medications = normalize_and_filter_strings(medications, query)

        # Step 2: Select the appropriate Soundex algorithm based on language
        if language not in LANGUAGE_SOUNDEX_MAP:
            error_message = f"Unsupported language: {language}. Supported languages: {', '.join(LANGUAGE_SOUNDEX_MAP.keys())}"
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
            
        soundex, soundex_version_name = LANGUAGE_SOUNDEX_MAP[language]
        logger.debug(f"Using {soundex_version_name} for language '{language}'")

        # Step 3: Create phonetic distance calculator and filter medications
        phonetic_distance = PhoneticsInnerLanguageDistance(soundex)
        logger.debug(f"Filtering medications with max phonetic distance {max_distance}")
        filtered_medications, distances = filter_medications_by_distance(
            processed_medications, query, phonetic_distance.distance, max_distance
        )
        
        # Step 4: Get top matches based on phonetic distance
        logger.debug(f"Getting top {max_results} matches from {len(filtered_medications)} filtered medications")
        top_matches = get_top_matches_by_distance(
            filtered_medications, distances, max_results
        )

        # Step 5: Create FuzzyResult objects for each matched medication
        fuzzy_results = [
            FuzzyResult(
                matching_name=medication,
                matching_source="Soundex",
                matching_algorithm=f"{soundex_version_name} (Local)",
                matching_uid=0,  # Default UID as 0 for local search results
                matching_row_number=index + 1,
            )
            for index, medication in enumerate(top_matches)
        ]

        # Log the results
        logger.info(f"Found {len(fuzzy_results)} medications matching '{query}' using {soundex_version_name}")
        return fuzzy_results

    except HTTPException:
        # Re-raise HTTP exceptions to preserve their status codes
        raise
    except Exception as e:
        # Convert other exceptions to HTTPException
        error_message = f"Error in Soundex search: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )
