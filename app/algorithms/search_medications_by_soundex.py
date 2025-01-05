import logging
from typing import List

from fonetika.distance import PhoneticsInnerLanguageDistance
from fonetika.soundex import EnglishSoundex, RussianSoundex

from app.algorithms.filter_medications_by_distance import filter_medications_by_distance
from app.algorithms.get_top_matches_by_distance import get_top_matches_by_distance
from app.config import LOGGER_NAME
from app.func.normalize_and_filter_strings import normalize_and_filter_strings

logger = logging.getLogger(LOGGER_NAME)


def search_medications_by_soundex(
    source_language: str,
    medications: List[str],
    query: str,
    max_distance: float = 2,
    max_results: int = 10,
) -> List[str]:
    """
    Search for medications using Soundex algorithm.

    Perform a fuzzy search for medication names using the Soundex algorithm
    based on the specified language.

    Args:
        source_language (str): Language of the input and medication names ('en', 'ru', or 'uk').
        medications (List[str]): List of medication names to search through.
        query (str): Input string to search for.
        max_distance (float, optional): Maximum phonetic distance allowed. Defaults to 2.
        max_results (int, optional): Maximum number of results to return. Defaults to 10.

    Returns:
        List[str]: List of medication names matching the query within the specified threshold.

    Raises:
        ValueError: If the input is invalid or the language is unsupported.
    """
    try:
        processed_medications = normalize_and_filter_strings(medications, query)

        if source_language == ["en", "fr"]:
            soundex = EnglishSoundex()
        elif source_language in ["ru", "uk"]:
            soundex = RussianSoundex()
        else:
            raise ValueError(f"Unsupported language: {source_language}")

        phonetic_distance = PhoneticsInnerLanguageDistance(soundex)
        filtered_medications, distances = filter_medications_by_distance(
            processed_medications, query, phonetic_distance.distance, max_distance
        )
        top_matches = get_top_matches_by_distance(filtered_medications, distances, max_results)

        logger.info(f"Soundex search results: {top_matches}")
        return top_matches

    except Exception as e:
        logger.error(f"Error in Soundex search: {str(e)}")
        raise
