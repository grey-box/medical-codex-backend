"""
OCR Module.

This module provides functionality for performing ocr extractions and
then performing fuzzy matching on medical terms.
"""

import logging

from fastapi import File
from sqlalchemy.orm import Session

from app.algorithms import search_medication_with_image

from app.schemas import FuzzyMatching


def perform_ocr_extraction(
        language: str,
        file: File(...),
        db: Session
) -> FuzzyMatching:

    search_results = search_medication_with_image.search_medication_with_image(language, file,db,0.85)
    return search_results