"""

OCR Matching Router Module.

This module provides API endpoints for OCR operations, which allows extracting text from image files
then finding approximate matches for most medical terms in the database from extracted text.
"""

import logging
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

import database
import schemas
from config import LOGGER_NAME
from algorithms import search_medication_with_image
from schemas import FuzzyMatching, FuzzyResult

from app.func.perform_ocr_extraction import perform_ocr_extraction

#Initialize router with prefix and tags for API documentation
router= APIRouter(prefix="/ocrmatching", tags=["ocrmatching"])

#Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)

@router.post("/", response_model=schemas.FuzzyMatching, status_code=status.HTTP_201_CREATED)
async def ocr_matching_endpoint(
        file:UploadFile = File(...),
        source_language: str = Form(...),
        db: Session = Depends(database.get_database_session),
        ) -> schemas.FuzzyMatching:
    try:
        results = perform_ocr_extraction(source_language, file, db)
        logger.info(f"Successfully performed OCR text extraction for file: {file.filename}")
        return results
    except Exception as e:
        error_message = f"Error performing OCR extraction: {str(e)}"
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )

