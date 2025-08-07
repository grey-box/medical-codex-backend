"""
Medication Distance Filter Module.

This module provides functionality for filtering medications based on their
string distance to a query string. It can be used with various distance functions
to implement fuzzy matching algorithms.
"""

import logging
from typing import List, Callable, Tuple, Sequence, Hashable

from fastapi import HTTPException, status

from config import LOGGER_NAME

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


def filter_medications_by_distance(
    medications: List[str], 
    query: str, 
    distance_function: Callable[[Sequence[Hashable], Sequence[Hashable]], float],
    max_distance: float
) -> Tuple[List[str], List[float]]:
    """
    Filter medications based on their distance to a query string.

    Compute the distance between the query and each medication using the specified
    distance function. Return medications and their distances within the given max_distance.

    Args:
        medications (List[str]): List of medication names to compare against.
        query (str): The query string to compare with each medication.
        distance_function (Callable[[str, str], float]): Function to calculate 
            the distance between two strings.
        max_distance (float): Maximum allowed distance for a medication to be 
            included in the result.

    Returns:
        Tuple[List[str], List[float]]: A tuple containing two lists:
            - List of medications within the max_distance.
            - Corresponding distances for the medications.

    Raises:
        HTTPException: If the medications list is empty or if the query string is empty.
    """
    try:
        # Validate input parameters
        if not medications:
            error_message = "The medication list is empty."
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
            
        if not query:
            error_message = "The query string is empty."
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )

        # Initialize result lists
        filtered_medications = []
        distances = []

        # Process each medication
        for medication in medications:
            try:
                # Calculate distance between query and medication
                distance = distance_function(query, medication)
                logger.info(f"Distance of {distance} between {query} and {medication}")
                
                # Include medication if within max_distance
                if distance <= max_distance:
                    filtered_medications.append(medication)
                    distances.append(distance)
            except Exception as e:
                # Log warning but continue processing other medications
                error_message = f"Error calculating distance for medication '{medication}': {str(e)}"
                logger.warning(error_message)

        # Log results
        logger.info(
            f"Filtered {len(filtered_medications)} medications within the distance {max_distance}."
        )
        
        return filtered_medications, distances

    except HTTPException:
        # Re-raise HTTP exceptions to preserve their status codes
        raise
    except Exception as e:
        # Convert other exceptions to HTTPException
        error_message = f"Error in filter_medications_by_distance: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )
