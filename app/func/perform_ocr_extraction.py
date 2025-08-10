"""
OCR Module.

This module provides functionality for performing ocr extractions and
then performing fuzzy matching on medical terms.
"""

import logging

from fastapi import File
from sqlalchemy.orm import Session

from algorithms.search_medication_with_image import search_medication_with_image

from schemas import FuzzyMatching
from config import LOGGER_NAME

# Remove dummy_database import as it's not used in this function

logger = logging.getLogger(LOGGER_NAME)

def perform_ocr_extraction(
        language: str,
        file: File(...),
        db: Session
) -> FuzzyMatching:


    search_results = search_medication_with_image(language, file, db)
    return search_results