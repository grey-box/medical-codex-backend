"""
Manual Translation Storage Module.

This module provides functionality for storing terms that require manual translation
by human translators. It saves the terms along with their source and target languages,
proposed translations, and optional descriptions to the database.
"""

import logging

from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config import LOGGER_NAME
from models import ManualTranslations
from schemas import ManualTranslationQuery

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


def store_manual_translation(
    db: Session, query: ManualTranslationQuery
):
    """
    Store a term to be manually translated for later processing.
    
    This function saves a term that requires manual translation to the database.
    It records the term, its source and target languages, an optional proposed
    translation, and an optional description to provide context for the translators.
    
    Args:
        db (Session): Database session for executing the insert operation.
        query (ManualTranslationQuery): Object containing the term to translate,
                                       source and target languages, proposed translation,
                                       and optional description.
        
    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        Exception: For any other unexpected errors.
    """
    try:
        # Extract values from the query object
        term = query.term
        source_language = query.source_language
        target_language = query.target_language
        proposed_translation = query.proposed_translation
        description = query.description if query.description else None
        
        logger.info(
            f"Storing manual translation request: '{term}' from {source_language} to {target_language}"
        )
        
        # Create the database insert query
        db_query = insert(ManualTranslations).values(
            term=term,
            proposed_translation=proposed_translation,
            language_to=target_language,
            language_from=source_language,
            description=description,
        )
        
        # Execute the query
        db.execute(db_query)
        
        # Commit the transaction
        db.commit()
        
        logger.info(f"Successfully stored manual translation request for term: '{term}'")
        
    except SQLAlchemyError as e:
        # Handle database-specific errors
        db.rollback()  # Roll back the transaction on error
        error_message = f"Database error storing manual translation for '{query.term}': {str(e)}"
        logger.error(error_message)
        raise SQLAlchemyError(error_message) from e
        
    except Exception as e:
        # Handle any other unexpected errors
        db.rollback()  # Roll back the transaction on error
        error_message = f"Unexpected error storing manual translation for '{query.term}': {str(e)}"
        logger.error(error_message)
        raise Exception(error_message) from e
    finally:
        # Don't close the session here - it should be managed by the caller
        pass