from typing import List
import pandas as pd
import logging
from config import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

def get_top_matches_by_distance(
    items: List[str],
    distances: List[float],
    max_results: int
) -> List[str]:
    """
    Return the top matching items based on their distance values.

    Args:
        items (List[str]): A list of item names.
        distances (List[float]): A list of distance values corresponding to each item.
        max_results (int): The maximum number of top matches to return.

    Returns:
        List[str]: A list of item names, sorted by their distance values,
                   containing at most max_results elements.

    Raises:
        ValueError: If the lengths of items and distances do not match.
    """
    try:
        if len(items) != len(distances):
            raise ValueError("The lengths of items and distances must be equal.")

        df = pd.DataFrame({"item": items, "distance": distances})
        df_sorted = df.sort_values("distance")
        top_matches = df_sorted.head(max_results)["item"].tolist()

        logger.info(f"Retrieved top {len(top_matches)} matches.")
        return top_matches

    except Exception as e:
        logger.error(f"Error in get_top_matches_by_distance: {str(e)}")
        raise
