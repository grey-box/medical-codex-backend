from typing import List
import logging
from app.config import LOGGER_NAME
from fastapi import status

logger = logging.getLogger(LOGGER_NAME)

def normalize_and_filter_strings(source_strings: List[str], query: str) -> List[str]:
    """
    Normalize and filter a list of strings based on a query.

    Args:
        source_strings (List[str]): A list of strings to process.
        query (str): The query string used for validation.

    Returns:
        List[str]: A list of lowercase, non-None strings from the source.

    Raises:
        ValueError: If the query is None.
    """
    try:
        if query is None:
            raise ValueError("Query string cannot be None")

        normalized_strings = [str(item).lower() for item in source_strings if item is not None]
        logger.info(status.HTTP_200_OK + f" Processed {len(normalized_strings)} strings")
        return normalized_strings
    except Exception as e:
        logger.error(status.HTTP_400_BAD_REQUEST + f" Error in normalize_and_filter_strings: {str(e)}")
        raise
