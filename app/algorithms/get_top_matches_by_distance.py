"""
Top Matches Retrieval Module.

This module provides functionality for retrieving the top matching items
based on their distance values. It sorts items by their distance scores
and returns the specified number of best matches.
"""

from typing import List
import pandas as pd
import logging
from config import LOGGER_NAME
from fastapi import HTTPException, status

logger = logging.getLogger(LOGGER_NAME)


def get_top_matches_by_distance(
    items: List[str],
    distances: List[float],
    max_results: int
) -> List[str]:
    """
    Return the top matching items based on their distance values.

    This function pairs items with their corresponding distance values,
    sorts them by distance (ascending), and returns the top matches.
    Lower distance values indicate better matches.

    Args:
        items (List[str]): A list of item names.
        distances (List[float]): A list of distance values corresponding to each item.
        max_results (int): The maximum number of top matches to return.

    Returns:
        List[str]: A list of item names, sorted by their distance values,
                  containing at most max_results elements.

    Raises:
        HTTPException: If the lengths of items and distances do not match,
                      or if any other error occurs during processing.
    """
    try:
        # Validate input parameters
        if len(items) != len(distances):
            error_message = "The lengths of items and distances must be equal."
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )

        # Create a DataFrame to easily sort items by their distances
        df = pd.DataFrame({"item": items, "distance": distances})
        
        # Sort by distance (ascending) and take the top matches
        df_sorted = df.sort_values("distance")
        top_matches = df_sorted.head(max_results)["item"].tolist()

        # Log the result
        logger.info(f"Retrieved top {len(top_matches)} matches out of {len(items)} total items.")
        
        return top_matches

    except HTTPException:
        # Re-raise HTTP exceptions to preserve their status codes
        raise
    except Exception as e:
        # Convert other exceptions to HTTPException
        error_message = f"Error in get_top_matches_by_distance: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )
