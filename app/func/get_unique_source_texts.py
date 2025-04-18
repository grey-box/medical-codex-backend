"""
Unique Source Texts Module.

This module provides functionality for retrieving unique source text values
from the database for a specific language. These texts are used in fuzzy matching
operations to find the closest matches to user queries.
"""

import logging
from typing import List

from sqlalchemy import select, distinct
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import UniqueTranslations
from config import LOGGER_NAME
from schemas import FuzzyQuery

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


def get_unique_source_texts(db: Session, query: FuzzyQuery) -> List[str]:
    """
    Retrieve unique source text values for a given language from the database.
    
    This function queries the database to find all unique source texts in the
    specified language. These texts can be used as a corpus for fuzzy matching
    operations to find the closest matches to user queries.
    
    Args:
        db (Session): The database session for executing queries.
        query (FuzzyQuery): The fuzzy matching query containing the source language.
        
    Returns:
        List[str]: A list of unique source text values in the specified language.
        
    Raises:
        SQLAlchemyError: If there's an issue with the database query.
        Exception: For any other unexpected errors.
    """
    source_language = query.source_language
    logger.info(f"Retrieving unique source texts for language: {source_language}")
    
    try:
        # Create a query to select distinct source texts for the specified language
        db_query = select(distinct(UniqueTranslations.source_text)).where(
            UniqueTranslations.source_language == source_language
        )
        
        # Execute the query and get all results
        result = db.execute(db_query).scalars().all()
        
        # Convert results to strings
        unique_texts = [str(value) for value in result]
        
        # Log the number of unique texts found
        logger.info(f"Found {len(unique_texts)} unique source texts for language: {source_language}")
        
        return unique_texts
        
    except SQLAlchemyError as e:
        # Handle database-specific errors
        error_message = f"Database error retrieving unique source texts for {source_language}: {str(e)}"
        logger.error(error_message)
        # Re-raise as SQLAlchemyError to maintain the original error type
        raise SQLAlchemyError(error_message) from e
        
    except Exception as e:
        # Handle any other unexpected errors
        error_message = f"Unexpected error retrieving unique source texts for {source_language}: {str(e)}"
        logger.error(error_message)
        # Re-raise the exception to be handled by the caller
        raise Exception(error_message) from e
