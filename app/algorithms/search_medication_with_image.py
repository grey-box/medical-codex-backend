import logging
import string

from app.algorithms.search_medications_by_levenshtein import search_medications_by_levenshtein
from rapidfuzz.distance import Levenshtein
from app.config import LOGGER_NAME
from app.func.perform_ocr_extraction import perform_ocr_extraction
from typing import List

from app.schemas import FuzzyResult

logger = logging.getLogger(LOGGER_NAME)


def search_medication_with_image(
        language: str,
        medications : List[str],
        confidence_threshold: float = 0,
        max_results_per_word: int =10,
        max_distance: int = 5,
        max_results: int = 5,

) -> List[FuzzyResult]:
    """
        Search for medications extracted with PaddleOCR using Levenshtein distance.

        Filters out extracted text under a specified threshold then reduces remaining text blocks into
        individual tokens. Each token is passed through a fuzzy search for medication names using the Levenshtein distance algorithm.

        Args:
            language (str): Language of the input and medication names ('en', 'uk', or 'ru').
            medications (List[str]): List of medication names to search through.
            confidence_threshold (float, optional): A cutoff value between 0 and 1 which filters OCR extracted text by quality.
                The closer this number is to 1 the more strict it is. setting this to 0 will skip the filtering process. (quality control)
                Defaults to 0.

            max_results_per_word (int, optional): Maximum number of results for each word passed through the Levenshtein distance algorithm. Defaults to 10
            max_distance (int, optional): Maximum Levenshtein distance allowed. Defaults to 5.
            max_results (int, optional): Maximum number of results to return. Defaults to 5.

        Returns:
            List[FuzzyResult]: List of FuzzyResult objects matching the query within the specified max_distance.

        Raises:
            ValueError: If the language is invalid.
        """

    try:
        if language not in ['en', 'ru', 'uk']:
            raise ValueError(f"Invalid language: {language}")

        #For testing purposes please insert path string into the function bellow
        extracted_text = perform_ocr_extraction('')

        if extracted_text is None:
            logger.error(f"Invalid File Format or Image")
            return []


        #Discard all extracted text under a certain confidence score
        filtered_text = []
        if confidence_threshold > 0:
            for text in extracted_text:
                if float(text['rec_scores'][0]) > confidence_threshold:
                    filtered_text.append(text)
        else: filtered_text = extracted_text


        #break down filtered text blocks into individual words and clean them by removing punctuation and numbers
        tokens = []

        for text in filtered_text:
            for word in text['rec_texts']:
                no_digit_word = ''.join(char for char in word if not char.isdigit())
                cleaned_word = no_digit_word.translate(str.maketrans('', '', string.punctuation)).lower().split()

                tokens.extend(cleaned_word)


        #perform fuzzy matching for each token. Record results in a list
        result_list: List[FuzzyResult] = []

        for token in tokens:
            fuzzy_results = search_medications_by_levenshtein(
                language=language,
                query = token,
                medications = medications,
                max_distance = max_distance,
                max_results = max_results_per_word,
            )
            print(token + ": ")
            for result in fuzzy_results:
                result_list.append(result)
                print("     " + result.matching_name + str(result.distance))


        # Sort by distance.
        sorted_results = sorted(
            result_list,
            key=lambda res: res.distance if res.distance is not None else float('inf')
        )

        # Limit to top N with no duplicate answers
        top_results: List[FuzzyResult] = []
        seen_names: set[str] = set()

        for result in sorted_results:
            if len(top_results) >= max_results:
                break

            if result.matching_name not in seen_names:
                top_results.append(result)
                seen_names.add(result.matching_name)

        return top_results



    except Exception as e:
        logger.error(f"Error in OCR search: {str(e)}")
        raise