import logging
from typing import List

from fonetika.distance import PhoneticsInnerLanguageDistance
from fonetika.soundex import EnglishSoundex, RussianSoundex

from algorithms.filter_medications_by_distance import filter_medications_by_distance
from algorithms.get_top_matches_by_distance import get_top_matches_by_distance
from config import LOGGER_NAME
from func.normalize_and_filter_strings import normalize_and_filter_strings
from schemas import FuzzyResult

logger = logging.getLogger(LOGGER_NAME)


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
    based on the specified language.

    Args:
        language (str): Language of the input and medication names ('en', 'ru', or 'uk').
        medications (List[str]): List of medication names to search through.
        query (str): Input string to search for.
        max_distance (float, optional): Maximum phonetic distance allowed. Defaults to 2.
        max_results (int, optional): Maximum number of results to return. Defaults to 10.

    Returns:
        List[FuzzyResult]: List of FuzzyResult objects matching the query within the specified max_distance.

    Raises:
        ValueError: If the input is invalid or the language is unsupported.
    """
    try:
        processed_medications = normalize_and_filter_strings(medications, query)

        if language in ["en", "fr"]:
            soundex = EnglishSoundex()
            soundex_version_name = "English Soundex"
        elif language in ["ru", "uk"]:
            soundex = RussianSoundex()
            soundex_version_name = "Russian Soundex"
        else:
            raise ValueError(f"Unsupported language: {language}")

        phonetic_distance = PhoneticsInnerLanguageDistance(soundex)
        filtered_medications, distances = filter_medications_by_distance(
            processed_medications, query, phonetic_distance.distance, max_distance
        )
        top_matches = get_top_matches_by_distance(
            filtered_medications, distances, max_results
        )

        # Create FuzzyResult objects for each matched medication
        fuzzy_results = [
            FuzzyResult(
                matching_name=medication,
                matching_source="Soundex",
                matching_algorithm=f"{soundex_version_name} (Local)",
                matching_uid=0,  # You may need to adjust this if you have a way to get the UID
                matching_row_number=index + 1,
            )
            for index, medication in enumerate(top_matches)
        ]

        logger.info(f"Soundex search results: {fuzzy_results}")
        return fuzzy_results

    except Exception as e:
        logger.error(f"Error in Soundex search: {str(e)}")
        raise
