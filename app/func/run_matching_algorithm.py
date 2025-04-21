"""
Matching Algorithm Runner Module.

This module provides functions for executing fuzzy matching algorithms with
consistent error handling and parameter preparation. It supports both local
(in-memory) and database-based matching algorithms.
"""

import logging
from typing import List, Callable, Dict, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from config import LOGGER_NAME
from func.get_unique_source_texts import get_unique_source_texts
from schemas import FuzzyQuery, FuzzyAlgorithm, FuzzyResult

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


def execute_algorithm(func: Callable, **kwargs) -> List[FuzzyResult]:
    """
    Execute a fuzzy matching algorithm with the provided parameters.
    
    This function serves as a wrapper for algorithm execution, providing
    consistent error handling and logging across all algorithms.
    
    Args:
        func (Callable): The algorithm function to execute.
        **kwargs: Keyword arguments to pass to the algorithm function.
        
    Returns:
        List[FuzzyResult]: A list of matching results. Returns an empty list
                          if an error occurs during execution.
    """
    query = kwargs.get('query', 'unknown')
    
    try:
        # Execute the algorithm function with the provided parameters
        logger.debug(f"Executing algorithm {func.__name__} with query: {query}")
        matches = func(**kwargs)
        
        # Log the results
        match_count = len(matches)
        logger.info(f"Found {match_count} matches for query: {query}")
        
        return matches
        
    except Exception as error:
        # Log the error and return an empty list
        error_message = f"Error during {func.__name__} algorithm execution: {str(error)}"
        logger.error(error_message)
        return []


def run_matching_algorithm(
    algorithm: FuzzyAlgorithm,
    db: Session,
    query_params: FuzzyQuery,
) -> List[FuzzyResult]:
    """
    Run the specified matching algorithm with given parameters.
    
    This function prepares the appropriate parameters for the algorithm based on
    whether it's a local (in-memory) or database-based algorithm, then executes it.
    
    For local algorithms, it first retrieves all unique source texts from the database
    to use as the corpus for matching. For database algorithms, it passes the database
    session directly to the algorithm.
    
    Args:
        algorithm (FuzzyAlgorithm): The matching algorithm to execute, containing
                                   the function, name, and locality information.
        db (Session): The database session for executing queries or retrieving source texts.
        query_params (FuzzyQuery): The fuzzy matching query parameters containing the
                                  query string, source language, and matching thresholds.
        
    Returns:
        List[FuzzyResult]: A list of matching results sorted by relevance.
        
    Raises:
        Exception: Propagates any exceptions from the underlying algorithm execution.
                  These are caught and handled by the execute_algorithm function.
    """
    # Log the algorithm execution
    algorithm_name = algorithm.function.__name__
    query_string = query_params.query_string
    source_language = query_params.source_language
    
    logger.info(f"Running {algorithm_name} algorithm for query: '{query_string}' in language: {source_language}")
    
    # Prepare common parameters for all algorithms
    common_params: Dict[str, Any] = {
        "language": source_language,
        "query": query_string.lower(),  # Normalize query to lowercase
        "max_distance": query_params.max_distance,
        "max_results": query_params.max_results,
    }
    
    # Add algorithm-specific parameters based on locality
    if algorithm.local:
        # For local algorithms, retrieve all source texts to use as the corpus
        logger.debug(f"Retrieving source texts for local algorithm: {algorithm_name}")
        try:
            source_texts = get_unique_source_texts(db, query_params)
            common_params["medications"] = source_texts
            logger.debug(f"Retrieved {len(source_texts)} source texts for matching")
        except Exception as e:
            error_message = f"Failed to retrieve source texts: {str(e)}"
            logger.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_message
            )
    else:
        # For database algorithms, pass the database session
        logger.debug(f"Using database for algorithm: {algorithm_name}")
        common_params["db"] = db
    
    # Execute the algorithm with the prepared parameters
    return execute_algorithm(algorithm.function, **common_params)