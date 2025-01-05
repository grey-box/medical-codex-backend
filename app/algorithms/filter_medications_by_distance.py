import logging
from typing import List, Callable, Tuple

from app.config import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def filter_medications_by_distance(
    medications: List[str], query: str, distance_function: Callable, max_distance: float
) -> Tuple[List[str], List[float]]:
    """
    Filter medications based on their distance to a query string.

    Compute the distance between the query and each medication using the specified
    distance function. Return medications and their distances within the given threshold.

    Args:
        medications (List[str]): List of medication names to compare against.
        query (str): The query string to compare with each medication.
        distance_function (Callable[[str, str], float]): Function to calculate the distance between two strings.
        max_distance (float): Maximum allowed distance for a medication to be included in the result.

    Returns:
        Tuple[List[str], List[float]]: A tuple containing two lists:
            - List of medications within the threshold distance.
            - Corresponding distances for the medications.

    Raises:
        ValueError: If the medications list is empty or if the query string is empty.
    """
    try:
        if not medications:
            raise ValueError("The medication list is empty.")
        if not query:
            raise ValueError("The query string is empty.")

        filtered_medications = []
        distances = []

        for medication in medications:
            try:
                distance = distance_function(query, medication)
                if distance <= max_distance:
                    filtered_medications.append(medication)
                    distances.append(distance)
            except Exception as e:
                logger.warning(
                    f"Error calculating distance for medication '{medication}': {str(e)}"
                )

        logger.info(
            f"Filtered {len(filtered_medications)} medications within the distance threshold."
        )
        return filtered_medications, distances

    except Exception as e:
        logger.error(f"Error in filter_medications_by_distance: {str(e)}")
        raise
