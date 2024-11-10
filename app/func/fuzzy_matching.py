import logging
from typing import Callable, Dict, Any
from typing import List

from sqlalchemy import select, distinct
from sqlalchemy.orm import Session

import app.schemas
from app.func.algorithms import fuzzy_levenshtein, fonetika_soundex
from app.models import UniqueTranslationsORM


def get_unique_source_values(db: Session, source_language: str) -> List[str]:
    """
    Retrieve unique source text values for a given language from the database.

    This function queries the UniqueTranslationsORM table to get distinct source_text
    values for the specified source_language.

    Args:
        db (Session): The database session.
        source_language (str): The language code to filter the source texts.

    Returns:
        List[str]: A list of unique source text values.

    Note:
        The function uses SQLAlchemy's select and distinct functions for efficient querying.
        The result is converted to a list of strings for consistency and ease of use.
    """
    # Construct and execute the query
    query = select(distinct(UniqueTranslationsORM.source_text)).where(
        UniqueTranslationsORM.source_language == source_language
    )
    result = db.execute(query).scalars().all()

    # Convert the result to a list of strings
    return [str(value) for value in result]


def apply_matching_algorithm(
    algorithm: Callable,
    source_language: str,
    source_data: List[str],
    input_string: str,
    threshold: int,
    nb_max_results: int,
) -> List[str]:
    try:
        return algorithm(
            source_language=source_language,
            source_data=source_data,
            input_string=input_string.lower(),
            threshold=threshold,
            nb_max_results=nb_max_results,
        )
    except Exception as e:
        logging.error(f"Error during {algorithm.__name__} algorithm: {e}")
        return []


def fuzzy_matching(
    db: Session,
    query: app.schemas.FuzzyQuery,
    matching_algorithm: str = "Levenshtein",
) -> Dict[str, List[Dict[str, Any]]]:
    algorithms = {
        "Levenshtein": fuzzy_levenshtein,
        "Soundex": fonetika_soundex,
    }

    unique_source_values = get_unique_source_values(db, query.source_language)

    algorithm = algorithms.get(matching_algorithm)
    if not algorithm:
        logging.error(f"Unsupported matching algorithm: {matching_algorithm}")
        return {"results": []}

    list_medicine = apply_matching_algorithm(
        algorithm,
        str(query.source_language),
        unique_source_values,
        str(query.query),
        int(query.threshold),
        int(query.nb_max_results),
    )

    logging.info(f"List of medications: {list_medicine}")

    results = {
        "results": [
            {
                "matching_name": medicine,
                "matching_source": "wikidata",  # Replace with the actual source
                "matching_algorithm": matching_algorithm,
                "matching_uid": 0,  # We'll get this from the database
            }
            for medicine in list_medicine
        ]
    }

    logging.info(f"Results: {results}")

    return results
