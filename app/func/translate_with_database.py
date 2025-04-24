"""
Database Translation Module.

This module provides functionality for translating medical terms using the local database
as the primary source, with fallback to external translation services when needed.

The translation process follows these steps:
1. Query the database for translations of the requested term
2. If translations are found, return them
3. If no translations are found, use the configured fallback translation method
4. If any errors occur, log them and return an empty result set
"""

import logging
from typing import List

from sqlalchemy import select, distinct, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config import LOGGER_NAME, settings
from func.translate_using_fallback import translate_using_fallback
from models import UniqueTranslations
from schemas import Translation, TranslationQuery, TranslationResult

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


def translate_with_database(
    db: Session, query: TranslationQuery
) -> Translation:
    """
    Translate a medical term using the database or fallback to external services.
    
    This function implements a two-tier translation strategy:
    1. First, it attempts to find translations in the local database
    2. If no translations are found, it falls back to an external translation method
       as specified in the application settings
    
    Args:
        db (Session): Database session for querying translations.
        query (TranslationQuery): Object containing the term to translate and target language.
        
    Returns:
        Translation: Object containing the translation results. If no translations
                    are found or an error occurs, returns an object with an empty
                    results list.
    """
    try:
        # Extract term and language information from the query
        term = query.translation_query.matching_name
        term_uid = query.translation_query.matching_uid
        target_language = query.target_language
        
        logger.info(
            f"Attempting to translate '{term}' (UID: {term_uid}) "
            f"to {target_language}"
        )
        
        # Try to find translations in the database
        translated_terms = _query_database_translations(db, term, target_language)
        
        # If translations were found in the database, return them
        if translated_terms:
            return _create_database_translation_response(translated_terms, term_uid)
        
        # If no translations were found, use fallback method
        return _translate_using_fallback_method(query)
        
    except Exception as e:
        # Log the error and return an empty result set
        error_message = f"Error translating term '{query.translation_query.matching_name}': {str(e)}"
        logger.error(error_message)
        return Translation(results=[])


def _query_database_translations(
    db: Session, term: str, target_language: str
) -> List[str] | None:
    """
    Query the database for translations of a term.
    
    Args:
        db (Session): Database session for querying translations.
        term (str): The term to translate.
        target_language (str): The target language code.
        
    Returns:
        List[str]: List of translated terms found in the database.
        
    Raises:
        SQLAlchemyError: If there's an error executing the database query.
    """
    try:
        logger.debug(f"Querying database for translations of '{term}' to {target_language}")
        
        # Build the database query
        db_query = select(distinct(UniqueTranslations.target_text)).where(
            and_(
                UniqueTranslations.target_language == target_language,
                UniqueTranslations.source_text == term,
            )
        )
        
        # Execute the query
        result = db.execute(db_query).scalars().all()
        
        # Convert query results to strings
        translated_terms = [str(value) for value in result]
        
        # Log the results
        if translated_terms:
            logger.info(f"Found {len(translated_terms)} translations in database for '{term}'")
            logger.debug(f"Translations found: {', '.join(translated_terms)}")
        else:
            logger.info(f"No translations found in database for '{term}'")
            
        return translated_terms
        
    except SQLAlchemyError as e:
        logger.error(f"Database error while querying translations: {str(e)}")
        raise
    finally:
        # Don't close the session here - it should be managed by the caller
        return None


def _create_database_translation_response(
    translated_terms: List[str], term_uid: int
) -> Translation:
    """
    Create a Translation response object from database translation results.
    
    Args:
        translated_terms (List[str]): List of translated terms found in the database.
        term_uid (int): The UID of the original term.
        
    Returns:
        Translation: Object containing the translation results.
    """
    # Create a list of TranslationResult objects
    translation_results: List[TranslationResult] = [
        TranslationResult(
            translated_name=translated_term,
            translated_source="local_db",
            translated_uid=term_uid,
        )
        for translated_term in translated_terms
    ]
    
    logger.debug(f"Created {len(translation_results)} TranslationResult objects")
    return Translation(results=translation_results)


def _translate_using_fallback_method(query: TranslationQuery) -> Translation:
    """
    Translate a term using the configured fallback translation method.
    
    Args:
        query (TranslationQuery): Object containing the term to translate
                                 and language information.
        
    Returns:
        Translation: Object containing the translation results.
    """
    term = query.translation_query.matching_name
    fallback_method = settings.fallback_translation_method
    
    logger.info(f"Using fallback method '{fallback_method}' for term '{term}'")
    
    try:
        # Call the fallback translation function
        fallback_result = translate_using_fallback(query, fallback_method)
        
        logger.info(f"Successfully translated '{term}' using fallback method {fallback_method}: '{fallback_result.results[0].translated_name}'")
        return fallback_result
        
    except Exception as e:
        logger.error(f"Fallback translation failed for '{term}': {str(e)}")
        return Translation(results=[])
