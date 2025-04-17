import logging
from typing import List, Literal

from sqlalchemy import text
from sqlalchemy.orm import Session

from config import LOGGER_NAME
from schemas import FuzzyResult

logger = logging.getLogger(LOGGER_NAME)

AlgorithmType = Literal["Levenshtein", "DaitchMokotoff"]


def dbquery_medications(
    db: Session,
    language: str,
    query: str,
    algorithm: AlgorithmType = "Levenshtein",
    max_distance: int = 5,
    max_results: int = 5,
) -> List[FuzzyResult]:
    """
    Query medications from the database using the specified algorithm.

    Args:
        db (Session): SQLAlchemy database session.
        language (str): The language of the medications to search.
        query (str): The search query.
        algorithm (AlgorithmType): The algorithm to use ("Levenshtein" or "DaitchMokotoff").
        max_distance (int): Maximum distance allowed (for Levenshtein only).
        max_results (int): Maximum number of results to return.

    Returns:
        List[FuzzyResult]: A list of FuzzyResult objects matching the query.
    """
    try:
        if algorithm == "Levenshtein":
            sql = text(
                """
                SELECT 
                0 AS matching_uid,
                source_text AS matching_name, 
                table_name AS matching_source,
                ROW_NUMBER() OVER (ORDER BY levenshtein(lower(source_text), lower(:query))) AS row_number,
                levenshtein(lower(source_text), lower(:query)) AS distance
                FROM unique_translation_table
                WHERE source_language = :language
                  AND levenshtein(lower(source_text), lower(:query)) <= :max_distance
                ORDER BY levenshtein(lower(source_text), lower(:query))
                LIMIT :max_results
                """
            )
        elif algorithm == "DaitchMokotoff":
            sql = text(
                """
                WITH matched_rows AS (SELECT source_text,
                             table_name,
                             array_dms_diff(my_daitch_mokotoff(source_text), my_daitch_mokotoff(:query)) AS distance
                      FROM unique_translation_table
                      WHERE source_language = :language
                        AND (my_daitch_mokotoff(source_text) && my_daitch_mokotoff(:query)))
                SELECT 0                                     AS matching_uid,
                       source_text                           AS matching_name,
                       table_name                            AS matching_source,
                       ROW_NUMBER() OVER (ORDER BY distance) AS row_number,
                       distance
                FROM matched_rows
                WHERE distance <= :max_distance
                ORDER BY distance
                LIMIT :max_results
                """
            )
        else:
            raise ValueError(status.HTTP_400_BAD_REQUEST + f" Unsupported algorithm: {algorithm}")

        params = {
            "language": language,
            "query": query,
            "max_results": max_results,
            "max_distance": max_distance,
        }

        result = db.execute(sql, params)

        medications = [
            FuzzyResult(
                matching_uid=row.matching_uid,
                matching_name=row.matching_name,
                matching_source=row.matching_source,
                matching_algorithm=algorithm,
                matching_row_number=row.row_number,
            )
            for row in result
        ]

        logger.info(
            f"Found {len(medications)} medications for query '{query}' in language '{language}' using {algorithm} algorithm"
        )
        return medications

    except Exception as e:
        logger.error(status.HTTP_400_BAD_REQUEST + 
            f" Error querying medications using {algorithm} algorithm: {str(e)}"
        )
        return []


def dbquery_medications_with_levenstein(
    db: Session,
    language: str,
    query: str,
    max_distance: int = 10,
    max_results: int = 10,
) -> List[FuzzyResult]:
    return dbquery_medications(
        db=db,
        language=language,
        query=query,
        algorithm="Levenshtein",
        max_distance=max_distance,
        max_results=max_results,
    )


def dbquery_medications_with_daitch_mokotoff(
    db: Session,
    language: str,
    query: str,
    max_distance: int = 10,
    max_results: int = 10,
) -> List[FuzzyResult]:
    return dbquery_medications(
        db,
        language,
        query,
        algorithm="DaitchMokotoff",
        max_distance=max_distance,
        max_results=max_results,
    )
