from datetime import datetime, timezone
from typing import List, Optional, Callable
import logging
from config import fuzzySettings

from pydantic import BaseModel, Field


# 2 in the diagram
class FuzzyQuery(BaseModel):
    source_language: str
    query: str
    target_language: Optional[str] = None
    max_distance: int = fuzzySettings.fuzzy_max_distance
    max_results: int = fuzzySettings.fuzzy_max_results


class FuzzyResult(BaseModel):
    matching_name: str
    matching_source: str
    matching_algorithm: str
    matching_uid: int
    matching_row_number: int
    distance: Optional[int] = None


# 3 in the diagram
class FuzzyMatching(BaseModel):
    results: List[FuzzyResult]


# 5 in the diagram
class TranslationQuery(BaseModel):
    translation_query: FuzzyResult
    target_language: str


class Alternative(BaseModel):
    text: str
    confidence: float
    meaning: str

class AdditionalDetails(BaseModel):
    domain: Optional[str] = None
    formality: Optional[str] = None
    examples_in_context: List[str] = []

class TranslationResult(BaseModel):
    translated_name: str
    translated_source: str
    translated_uid: int
    source_term: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    confidence: Optional[float] = 0
    alternatives: List[Alternative] = []
    additionalDetails: Optional[AdditionalDetails] = None


# 6 in the diagram
class Translation(BaseModel):
    results: List[TranslationResult]


class AvailableLanguageResult(BaseModel):
    source_language: str
    target_languages: list[str]

    class Config:
        from_attributes = True


class AvailableLanguages(BaseModel):
    available_languages: List[AvailableLanguageResult]


class FallbackQuery(BaseModel):
    medicine: FuzzyResult
    target_language: str


class FallbackResponse(BaseModel):
    translated_medicine: Translation
    fallback_method: str


class FuzzyAlgorithm(BaseModel):
    function: Callable
    local: bool
    name: str


class ManualTranslationQuery(BaseModel):
    term: str
    proposed_translation: str
    source_language: str
    target_language: str
    description: Optional[str] = None

class ServiceLogEntry(BaseModel):
    """Pydantic model for validating logs to write to the db"""
    log_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error_level: int = Field(..., description="Log level", ge=0, le=50)
    source: str = Field(..., max_length=50, description="Source of the log")
    message: str = Field(..., description="Log message")

    @classmethod
    def validate_error_level(cls, value):
        if value not in {logging.NOTSET, logging.INFO, logging.WARNING, logging.ERROR, logging.DEBUG, logging.CRITICAL}:
            raise ValueError("Invalid log level.")
        return value
    