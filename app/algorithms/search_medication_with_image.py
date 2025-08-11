import logging

from fastapi import UploadFile

from algorithms.search_medications_by_levenshtein import search_medications_by_levenshtein
from config import LOGGER_NAME, fuzzySettings
from func.extract_text_with_ocr import extract_text_with_ocr
from typing import List

from schemas import FuzzyResult, FuzzyMatching
from sqlalchemy.orm import Session

from func.get_unique_source_texts import get_unique_source_texts
from func.run_matching_algorithm import run_matching_algorithm
from schemas import FuzzyQuery, FuzzyAlgorithm

from func.normalize_and_filter_extracted_text import normalize_and_filter_extracted_text

logger = logging.getLogger(LOGGER_NAME)


def search_medication_with_image(
        language: str,
        file: UploadFile,
        db: Session,
        confidence_threshold: float = fuzzySettings.ocr_confidence_threshold,
        max_results_per_word: int = fuzzySettings.ocr_max_results_per_word,
        max_distance: int = fuzzySettings.ocr_max_distance,
        max_results: int = fuzzySettings.ocr_max_results,

) -> FuzzyMatching:
    """
        Search for medications extracted with PaddleOCR using Levenshtein distance.

        Filters out extracted text under a specified threshold then reduces remaining text blocks into
        individual tokens. Each token is passed through a fuzzy search for medication names using the Levenshtein distance algorithm.

        Args:
            language (str): Language of the input and medication names ('en', 'uk', or 'ru').
            file (UploadFile): A file uploaded by the frontend through fastAPI
            db (Session): Database of medication names to search through.
            confidence_threshold (float, optional): A cutoff value between 0 and 1 which filters OCR extracted text by quality.
                The closer this number is to 1 the more strict it is. setting this to 0 will skip the filtering process. (quality control)

            max_results_per_word (int, optional): Maximum number of results for each word passed through the Levenshtein distance algorithm.
            max_distance (int, optional): Maximum Levenshtein distance allowed.
            max_results (int, optional): Maximum number of results to return.

        Returns:
            FuzzyMatching: List of FuzzyResult objects matching the query within the specified max_distance.

        Raises:
            ValueError: If the language is invalid.
        """

    try:
        if language not in ['en', 'ru', 'uk']:
            raise ValueError(f"Invalid language: {language}")

        #For testing purposes please insert path string into the function bellow
        extracted_text = extract_text_with_ocr(file)

        if extracted_text is None:
            logger.error(f"Invalid File Format or Image")
            return FuzzyMatching(results=[])


        #Discard all extracted text under a certain confidence score
        filtered_text = [
            text for text in extracted_text
            if confidence_threshold == 0 or float(text['rec_score']) > confidence_threshold
        ]


        #Normalize and clean text, breaking them down into individual tokens
        tokens = normalize_and_filter_extracted_text(filtered_text)

        #Cahce list of medications for improved efficiency
        initial_query = FuzzyQuery(
            query="",
            source_language=language,
            max_distance=max_distance,
            max_results=max_results,
        )
        medications = get_unique_source_texts(db, initial_query)

        #Setup algorithm
        algorithm = FuzzyAlgorithm(
            function=search_medications_by_levenshtein,
            name="levenshtein",
            local=True
        )

        #perform fuzzy matching for each token. Record results in a list
        result_list: List[FuzzyResult] = []

        for token in tokens:
            query_params = FuzzyQuery(
                query=token,
                source_language=language,
                max_distance=max_distance,
                max_results=max_results_per_word,
            )

            token_results = run_matching_algorithm(
                algorithm=algorithm,
                db=db,
                query_params=query_params,
                medications=medications
            )

            #Discard an unrelated results to avoid clutter later on
            cleaned_list: List[FuzzyResult] = []
            for result in token_results:
                if token.__len__() >= result.distance:
                    cleaned_list.append(result)

            result_list.extend(cleaned_list)


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

        return FuzzyMatching(results = top_results)



    except Exception as e:
        logger.error(f"Error in OCR search: {str(e)}")
        raise