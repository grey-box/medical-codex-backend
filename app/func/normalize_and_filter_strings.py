"""
String Normalization and Filtering Module.

This module provides functionality for normalizing and filtering lists of strings,
which is useful for preparing text data for fuzzy matching and other text processing
operations in the medical codex system.
"""

from typing import List
import logging
from fastapi import status
from config import LOGGER_NAME

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


def normalize_and_filter_strings(source_strings: List[str], query: str) -> List[str]:
    """
    Normalize and filter a list of strings based on a query.
    
    This function processes a list of strings by:
    1. Removing None values
    2. Converting all strings to lowercase
    3. Ensuring all items are string type
    
    The query parameter is used for validation but does not affect the normalization process.
    
    Examples:
        >>> normalize_and_filter_strings(["Test", "EXAMPLE", None, 123], "query")
        ['test', 'example', '123']
    
    Args:
        source_strings (List[str]): A list of strings to process. May contain None values
                                   or non-string types that can be converted to strings.
        query (str): The query string used for validation. Must not be None.
        
    Returns:
        List[str]: A list of lowercase, non-None strings from the source.
        
    Raises:
        ValueError: If the query is None.
        TypeError: If source_strings is not a list.
    """
    # Validate inputs
    if query is None:
        error_message = "Query string cannot be None"
        logger.error(error_message)
        raise ValueError(error_message)
    
    if not isinstance(source_strings, list):
        error_message = f"Expected list for source_strings, got {type(source_strings).__name__}"
        logger.error(error_message)
        raise TypeError(error_message)
    
    try:
        # Process the strings: filter out None values and convert to lowercase strings
        normalized_strings = [
            str(item).lower() 
            for item in source_strings 
            if item is not None
        ]
        
        # Log the results
        logger.info(f"{status.HTTP_200_OK} Processed {len(normalized_strings)} strings from {len(source_strings)} source items")
        
        return normalized_strings
        
    except Exception as e:
        # Log and re-raise any unexpected errors
        error_message = f"Error normalizing strings: {str(e)}"
        logger.error(f"{error_message}")
        raise RuntimeError(error_message) from e