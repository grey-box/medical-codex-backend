"""
Fuzzy Matching Router Module.

This module provides API endpoints for fuzzy matching operations, which allow
finding approximate matches for medical terms in the database.
"""

import logging
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import schemas
from config import LOGGER_NAME
from func import perform_fuzzy_matching
from schemas import FuzzyMatching, FuzzyResult

# Initialize router with prefix and tags for API documentation
router = APIRouter(prefix="/fuzzymatching", tags=["fuzzymatching"])
# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


@router.post("/", response_model=schemas.FuzzyMatching, status_code=status.HTTP_201_CREATED)
async def get_fuzzymatching(
    query: schemas.FuzzyQuery, 
    db: Session = Depends(database.get_database_session)
) -> schemas.FuzzyMatching:
    """
    Perform fuzzy matching on the provided query.
    
    This endpoint searches the database for terms that approximately match the query
    using fuzzy matching algorithms.
    
    Args:
        query (schemas.FuzzyQuery): The query parameters for fuzzy matching.
        db (Session): Database session dependency.
        
    Returns:
        schemas.FuzzyMatching: The fuzzy matching results.
        
    Raises:
        HTTPException: If an error occurs during the fuzzy matching process.
    """
    try:
        results = perform_fuzzy_matching.perform_fuzzy_matching(db, query)
        logger.info(f"Successfully performed fuzzy matching for query: {query}")
        return results
    except Exception as e:
        error_message = f"Error performing fuzzy matching: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )


@router.post("/test", response_model=schemas.FuzzyMatching, status_code=status.HTTP_201_CREATED)
async def get_fuzzymatching_test(
    query: schemas.FuzzyQuery, 
    db: Session = Depends(database.get_database_session)
) -> schemas.FuzzyMatching:
    """
    Test endpoint for fuzzy matching that returns mock data.
    
    This endpoint is used for testing purposes and returns predefined mock data
    instead of performing actual fuzzy matching. It generates a fixed set of 5 mock
    results with predictable values to facilitate testing of the API and client
    applications without requiring actual database matching operations.
    
    Args:
        query (schemas.FuzzyQuery): The query parameters for fuzzy matching. These
            parameters are logged but not used for actual matching in this test endpoint.
        db (Session): Database session dependency. The session is not used for actual
            database operations but its information is logged for debugging purposes.
        
    Returns:
        schemas.FuzzyMatching: A FuzzyMatching object containing a list of 5 mock
            FuzzyResult objects with predictable test values.
            
    Raises:
        HTTPException: If an error occurs during the test fuzzy matching process,
            returns a 500 Internal Server Error with details about the exception.
    """
    try:
        logger.info(f"Received test fuzzy matching query: {query}")
        logger.debug(f"Database info: {db.info}")
        
        # Helper function to generate a mock result
        def create_mock_result(number: int) -> FuzzyResult:
            """
            Create a mock fuzzy matching result.
            
            Args:
                number (int): Index number to use in the mock result.
                
            Returns:
                Dict[str, Any]: A mock result dictionary.
            """
            return schemas.FuzzyResult(
                matching_name=f"matching_name{number}",
                matching_source=f"matching_source{number}",
                matching_uid=number,
                matching_algorithm="test",
                matching_row_number=number + 1,  # This is just for testing purposes.
            )
        
        # Generate 5 mock results
        results = FuzzyMatching(results = [create_mock_result(i) for i in range(5)])
        logger.info("Successfully generated test fuzzy matching results")
        return results
    except Exception as e:
        error_message = f"Error in test fuzzy matching: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )
