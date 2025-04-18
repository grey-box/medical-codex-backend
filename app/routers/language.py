"""
Language Router Module.

This module provides API endpoints for retrieving available language pairs
for translation in the medical codex system. It includes both production
and test endpoints.
"""

import logging
from typing import Dict, List
from dataclasses import dataclass

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from config import LOGGER_NAME, LOGGER_NAME_FILE
from database import get_database_session

# Initialize router with prefix and tags for API documentation
router = APIRouter(prefix="/languages", tags=["languages"])
# Set up loggers for console and file logging
logger = logging.getLogger(LOGGER_NAME)
logger_file = logging.getLogger(LOGGER_NAME_FILE)


@dataclass
class GroupedLanguage:
    """
    Class to represent a source language and its available target languages.
    
    This class is used to organize language pairs by grouping target languages
    under their respective source language.
    
    Attributes:
        source_language (str): The source language code.
        target_languages (List[str]): List of available target language codes.
    """
    source_language: str
    target_languages: List[str] = None
    
    def __post_init__(self):
        """Initialize target_languages as an empty list if None."""
        if self.target_languages is None:
            self.target_languages = []
    
    def add_target_language(self, target_language: str) -> None:
        """
        Add a target language to this group.
        
        Args:
            target_language (str): The target language code to add.
        """
        self.target_languages.append(target_language)
    
    def to_schema(self) -> schemas.AvailableLanguageResult:
        """
        Convert this GroupedLanguage to an AvailableLanguageResult schema.
        
        Returns:
            schemas.AvailableLanguageResult: Schema representation of this grouped language.
        """
        return schemas.AvailableLanguageResult(
            source_language=self.source_language,
            target_languages=self.target_languages,
        )


@router.get("/", response_model=schemas.AvailableLanguages, status_code=status.HTTP_200_OK)
async def get_available_languages(
    db: Session = Depends(get_database_session),
) -> schemas.AvailableLanguages:
    """
    Retrieve the languages currently available for translation.
    
    This endpoint queries the database for all available language pairs and
    organizes them by source language with their corresponding target languages.
    
    Args:
        db (Session): Database session for querying language pairs.
        
    Returns:
        schemas.AvailableLanguages: Object containing available language pairs
                                   organized by source language.
                                   
    Raises:
        HTTPException: If there's an error retrieving language pairs from the database.
    """
    try:
        # Query all language pairs from the database, ordered by source and target languages
        language_pairs = (
            db.query(models.LanguagePairs)
            .order_by(
                models.LanguagePairs.source_language.asc(),
                models.LanguagePairs.target_language.asc(),
            )
            .all()
        )
        
        # Group language pairs by source language using the GroupedLanguage class
        grouped_languages_dict: Dict[str, GroupedLanguage] = {}
        
        for pair in language_pairs:
            source = str(pair.source_language)
            target = str(pair.target_language)
            
            if source not in grouped_languages_dict:
                grouped_languages_dict[source] = GroupedLanguage(source_language=source)
                
            grouped_languages_dict[source].add_target_language(target)
        
        # Convert GroupedLanguage objects to AvailableLanguageResult schemas
        available_languages_list = [
            grouped_lang.to_schema()
            for grouped_lang in grouped_languages_dict.values()
        ]
        
        # Log successful retrieval
        logger.info(f"Retrieved {len(language_pairs)} language pairs")
        logger_file.debug(f"Retrieved language pairs: {language_pairs}")
        
        # Return the available languages
        return schemas.AvailableLanguages(available_languages=available_languages_list)
    
    except Exception as e:
        # Log the error and raise an HTTP exception
        error_message = f"Error retrieving available languages: {str(e)}"
        logger.error(error_message)
        logger_file.error(error_message, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to retrieve available languages"
        )


@router.get("/test", response_model=schemas.AvailableLanguages, status_code=status.HTTP_200_OK)
async def get_test_languages() -> schemas.AvailableLanguages:
    """
    Generate test language pairs for development and testing purposes.
    
    This endpoint creates mock language pairs without accessing the database.
    It's useful for testing the API without requiring a database connection.
    
    Args:
        
    Returns:
        schemas.AvailableLanguages: Object containing test language pairs.
        
    Raises:
        HTTPException: If there's an error generating the test data.
    """
    try:
        logger.info("Generating test language pairs")
        
        # Generate test language pairs using the GroupedLanguage class
        def generate_test_pairs(num_languages: int) -> List[schemas.AvailableLanguageResult]:
            """
            Generate a list of test language pairs.
            
            For each language, creates a GroupedLanguage with the source language and
            a list of all other languages as target languages.
            
            Args:
                num_languages (int): Number of test languages to generate.
                
            Returns:
                List[schemas.AvailableLanguageResult]: List of language results for testing.
            """
            test_pairs = []
            
            for source_num in range(1, num_languages + 1):
                source_lang = f"lang{source_num}"
                grouped_lang = GroupedLanguage(source_language=source_lang)
                
                # Add all other languages as targets
                for target_num in range(1, num_languages + 1):
                    if target_num != source_num:
                        grouped_lang.add_target_language(f"lang{target_num}")
                
                test_pairs.append(grouped_lang.to_schema())
                
            return test_pairs
        
        # Generate test language pairs with 3 languages
        test_results = generate_test_pairs(3)
        logger.info(f"Generated {len(test_results)} test language pairs")
        
        return schemas.AvailableLanguages(available_languages=test_results)
    
    except Exception as e:
        # Log the error and raise an HTTP exception
        error_message = f"Error generating test language pairs: {str(e)}"
        logger.error(error_message)
        logger_file.error(error_message, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to generate test language pairs"
        )