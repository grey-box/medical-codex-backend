"""
OCR Module.

This module provides functionality for performing ocr extractions and
then performing fuzzy matching on medical terms.
"""

import logging

from fastapi import File
from sqlalchemy.orm import Session

from algorithms import search_medication_with_image

from schemas import FuzzyMatching
from config import LOGGER_NAME

from dummy_database import dummy_database

logger = logging.getLogger(LOGGER_NAME)

def perform_ocr_extraction(
        language: str,
        file: File(...),
        db: Session
) -> FuzzyMatching:

    # Get medication names from Test DB
    medications = dummy_database()

    search_results = search_medication_with_image.search_medication_with_image(language, file,medications)
    return search_results