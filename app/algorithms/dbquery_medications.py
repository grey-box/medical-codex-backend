"""
Database Query Medications Module.

This module provides functions for querying medications from the database
using different fuzzy matching algorithms. It supports Levenshtein distance
and Daitch-Mokotoff soundex algorithms for finding approximate matches.
"""

import logging
from typing import List, Literal

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import LOGGER_NAME
from schemas import FuzzyResult

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)

# Define the supported algorithm types
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

    This function executes SQL queries that use either Levenshtein distance or
    Daitch-Mokotoff soundex algorithm to find medications that approximately
    match the query string.

    Args:
        db (Session): SQLAlchemy database session.
        language (str): The language code of the medications to search.
        query (str): The search query string.
        algorithm (AlgorithmType): The algorithm to use for matching.
            Options are "Levenshtein" or "DaitchMokotoff". Default is "Levenshtein".
        max_distance (int): Maximum distance allowed for matches.
            For Levenshtein, this is the edit distance.
            For Daitch-Mokotoff, this is the phonetic difference.
            Default is 5.
        max_results (int): Maximum number of results to return. Default is 5.

    Returns:
        List[FuzzyResult]: A list of FuzzyResult objects matching the query,
            sorted by relevance (closest match first).

    Raises:
        HTTPException: If an unsupported algorithm is specified.
    """
    try:
        # Select the appropriate SQL query based on the algorithm
        if algorithm == "Levenshtein":
            sql = text(
                """
                SELECT 
                id AS matching_uid,
                source_text AS matching_name, 
                source_table_name AS matching_source,
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
                WITH matched_rows AS (SELECT id,
                                             source_text,
                                             source_table_name,
                                             array_dms_diff(
                                                     my_daitch_mokotoff(source_text),
                                                     my_daitch_mokotoff(:query)) AS distance
                                      FROM unique_translation_table
                                      WHERE source_language = :language
                                        AND my_daitch_mokotoff(source_text) && my_daitch_mokotoff(:query))
                SELECT id                                    AS matching_uid,
                       source_text                           AS matching_name,
                       source_table_name                            AS matching_source,
                       ROW_NUMBER() OVER (ORDER BY distance) AS row_number,
                       distance
                FROM matched_rows
                WHERE distance <= :max_distance
                ORDER BY distance
                LIMIT :max_results
                """
            )
        else:
            error_message = f"Unsupported algorithm: {algorithm}"
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )

        # Prepare query parameters
        params = {
            "language": language,
            "query": query,
            "max_results": max_results,
            "max_distance": max_distance,
        }

        # Execute the SQL query
        result = db.execute(sql, params)

        # Convert database results to FuzzyResult objects
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

        # Log the results
        logger.info(
            f"Found {len(medications)} medications for query '{query}' "
            f"in language '{language}' using {algorithm} algorithm"
        )
        return medications

    except HTTPException:
        # Re-raise HTTP exceptions to preserve their status codes
        raise
    except Exception as e:
        # Log the error and return an empty list
        error_message = f"Error querying medications using {algorithm} algorithm: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )


def dbquery_medications_with_levenstein(
    db: Session,
    language: str,
    query: str,
    max_distance: int = 10,
    max_results: int = 10,
) -> List[FuzzyResult]:
    """
    Query medications using the Levenshtein distance algorithm.

    This is a convenience wrapper around dbquery_medications that
    specifically uses the Levenshtein algorithm.

    Args:
        db (Session): SQLAlchemy database session.
        language (str): The language code of the medications to search.
        query (str): The search query string.
        max_distance (int): Maximum Levenshtein distance allowed. Default is 10.
        max_results (int): Maximum number of results to return. Default is 10.

    Returns:
        List[FuzzyResult]: A list of FuzzyResult objects matching the query,
            sorted by Levenshtein distance (closest match first).
    """
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
    """
    Query medications using the Daitch-Mokotoff soundex algorithm.

    This is a convenience wrapper around dbquery_medications that
    specifically uses the Daitch-Mokotoff algorithm.

    Args:
        db (Session): SQLAlchemy database session.
        language (str): The language code of the medications to search.
        query (str): The search query string.
        max_distance (int): Maximum phonetic difference allowed. Default is 10.
        max_results (int): Maximum number of results to return. Default is 10.

    Returns:
        List[FuzzyResult]: A list of FuzzyResult objects matching the query,
            sorted by phonetic similarity (closest match first).
    """
    return dbquery_medications(
        db=db,
        language=language,
        query=query,
        algorithm="DaitchMokotoff",
        max_distance=max_distance,
        max_results=max_results,
    )
