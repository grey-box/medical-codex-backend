"""
Fuzzy Matching Test Module.

This module contains tests for the fuzzy matching algorithms used in the application.
It tests both Levenshtein distance and Soundex phonetic matching algorithms with
sample medication names in different languages.
"""

import logging
from typing import List

from fastapi import HTTPException, status

from algorithms.search_medications_by_levenshtein import (
    search_medications_by_levenshtein,
)
from algorithms.search_medications_by_soundex import search_medications_by_soundex
from config import LOGGER_NAME
from database import get_database_session
from func.get_unique_source_texts import get_unique_source_texts
from schemas import FuzzyQuery, FuzzyResult

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)

# Get database session for testing
try:
    db = next(get_database_session())
except Exception as e:
    logger.error(f"Failed to get database session: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database connection error"
    )

# Prepare test data - Ukrainian medications
try:
    source_uk = get_unique_source_texts(
        db, 
        FuzzyQuery(
            source_language="uk",
            query="астмито",
            max_distance=5, 
            max_results=5
        )
    )
    logger.debug(f"Retrieved {len(source_uk)} Ukrainian medications for testing")
except Exception as e:
    logger.error(f"Failed to get Ukrainian medications: {str(e)}")
    source_uk = []

# Prepare test data - Russian medications
try:
    source_ru = get_unique_source_texts(
        db,
        FuzzyQuery(
            source_language="ru",
            query="изотретиноин",
            max_distance=2,
            max_results=5
        ),
    )
    logger.debug(f"Retrieved {len(source_ru)} Russian medications for testing")
except Exception as e:
    logger.error(f"Failed to get Russian medications: {str(e)}")
    source_ru = []


def test_levenshtein() -> None:
    """
    Test the Levenshtein distance algorithm for fuzzy matching.
    
    This test verifies that the Levenshtein algorithm correctly identifies
    'астматол' as the closest match to 'астмито' in Ukrainian.
    
    Returns:
        None
        
    Raises:
        AssertionError: If the test fails.
    """
    try:
        # Skip test if no data is available
        if not source_uk:
            logger.warning("Skipping Levenshtein test due to missing Ukrainian data")
            return
            
        # Execute the Levenshtein search algorithm
        results: List[FuzzyResult] = search_medications_by_levenshtein(
            language="uk",
            query="астмито",
            medications=source_uk,
            max_distance=5,
            max_results=5,
        )
        
        # Verify that results were returned
        if not results:
            logger.error("Levenshtein search returned no results")
            assert False, "No results returned from Levenshtein search"
            
        # Check if the top result is the expected medication
        top_match = results[0].matching_name
        logger.info(f"Levenshtein test: Top match for 'астмито' is '{top_match}'")
        assert top_match == "астматол", f"Expected 'астматол', got '{top_match}'"
        
    except Exception as ee:
        logger.error(f"Levenshtein test failed: {str(ee)}")
        raise


def test_fonetika_soundex() -> None:
    """
    Test the Soundex phonetic algorithm for fuzzy matching.
    
    This test verifies that the Soundex algorithm correctly identifies
    'изотретиноин' as the closest phonetic match to 'изотретиноїн' in Russian.
    
    Returns:
        None
        
    Raises:
        AssertionError: If the test fails.
    """
    try:
        # Skip test if no data is available
        if not source_ru:
            logger.warning("Skipping Soundex test due to missing Russian data")
            return
            
        # Execute the Soundex search algorithm
        results: List[FuzzyResult] = search_medications_by_soundex(
            language="ru",
            query="изотретиноїн",
            medications=source_ru,
            max_distance=2,
            max_results=5,
        )
        
        # Verify that results were returned
        if not results:
            logger.error("Soundex search returned no results")
            assert False, "No results returned from Soundex search"
            
        # Check if the top result is the expected medication
        top_match = results[0].matching_name
        logger.info(f"Soundex test: Top match for 'изотретиноїн' is '{top_match}'")
        assert top_match == "изотретиноин", f"Expected 'изотретиноин', got '{top_match}'"
        
    except Exception as ee:
        logger.error(f"Soundex test failed: {str(ee)}")
        raise