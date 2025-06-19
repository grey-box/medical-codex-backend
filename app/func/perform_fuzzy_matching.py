"""
Fuzzy Matching Module.

This module provides functionality for performing fuzzy matching on medical terms
using various algorithms. It supports both local (in-memory) and database-based
matching algorithms to find the closest matches to user queries.
"""

import logging

from sqlalchemy.orm import Session

from algorithms.dbquery_medications import (
    dbquery_medications_with_daitch_mokotoff,
    dbquery_medications_with_levenstein,
)
from algorithms.search_medications_by_levenshtein import (
    search_medications_by_levenshtein,
)
from algorithms.search_medications_by_soundex import search_medications_by_soundex
from config import LOGGER_NAME
from func.run_matching_algorithm import run_matching_algorithm
from schemas import FuzzyAlgorithm, FuzzyMatching, FuzzyQuery

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)

# Define available fuzzy matching algorithms
AVAILABLE_ALGORITHMS = {
    "LevenshteinLocal": FuzzyAlgorithm(
        function=search_medications_by_levenshtein,
        local=True,
        name="Levenshtein (Local)",
    ),
    "SoundexLocal": FuzzyAlgorithm(
        function=search_medications_by_soundex, 
        local=True, 
        name="Soundex (Local)"
    ),
    "LevenshteinDB": FuzzyAlgorithm(
        function=dbquery_medications_with_levenstein,
        local=False,
        name="Levenshtein (Database)",
    ),
    "DaitchMokotoffDB": FuzzyAlgorithm(
        function=dbquery_medications_with_daitch_mokotoff,
        local=False,
        name="Daitch-Mokotoff (Database)",
    ),
}


def perform_fuzzy_matching(
    db: Session,
    query: FuzzyQuery,
    matching_algorithm: str = "DaitchMokotoffDB",
) -> FuzzyMatching:
    """
    Perform fuzzy matching on the given query using the specified algorithm.
    
    This function takes a query and attempts to find the closest matches using
    the specified fuzzy matching algorithm. It supports both local (in-memory)
    and database-based matching algorithms.
    
    Available algorithms:
    - LevenshteinLocal: Uses Levenshtein distance for in-memory matching
    - SoundexLocal: Uses Soundex phonetic algorithm for in-memory matching
    - LevenshteinDB: Uses Levenshtein distance for database-based matching
    - DaitchMokotoffDB: Uses Daitch-Mokotoff phonetic algorithm for database-based matching
    
    Args:
        db (Session): The database session for executing queries.
        query (FuzzyQuery): The query parameters containing the term to match
                           and source language.
        matching_algorithm (str, optional): The name of the matching algorithm to use.
                                          Defaults to "DaitchMokotoffDB".
        
    Returns:
        FuzzyMatching: Object containing the matching results. If no matches are found
                      or an error occurs, returns an object with an empty results list.
    """
    logger.info(f"Performing fuzzy matching with algorithm: {matching_algorithm}")
    logger.info(f"Query: {query.model_dump()}")
    
    try:
        # Get the specified algorithm from the available algorithms
        algorithm = AVAILABLE_ALGORITHMS.get(matching_algorithm)
        
        # Check if the algorithm exists
        if not algorithm:
            error_message = f"Unsupported matching algorithm: {matching_algorithm}"
            logger.error(error_message)
            logger.info(f"Available algorithms: {list(AVAILABLE_ALGORITHMS.keys())}")
            return FuzzyMatching(results=[])
        
        # Run the matching algorithm
        logger.info(f"Running matching algorithm: {algorithm.name}")
        matched_medications = run_matching_algorithm(algorithm, db, query)
        
        # Log the number of matches found
        match_count = len(matched_medications)
        logger.info(f"Found {match_count} matches using {algorithm.name}")
        
        if match_count > 0:
            logger.debug(f"Matched medications: {matched_medications}")
        else:
            logger.warning(f"No matches found for query: {query.query}")
        
        # Return the results
        return FuzzyMatching(results=matched_medications)
        
    except Exception as e:
        # Log the error and return an empty result set
        error_message = f"Error in fuzzy matching: {str(e)}"
        logger.error(error_message)
        return FuzzyMatching(results=[])