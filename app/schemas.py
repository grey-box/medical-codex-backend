from datetime import datetime, timezone
from typing import List, Optional, Callable
import logging

from pydantic import BaseModel, Field


# 2 in the diagram
class FuzzyQuery(BaseModel):
    source_language: str
    query: str
    target_language: str = None
    max_distance: int = 10
    max_results: int = 10


class FuzzyResult(BaseModel):
    matching_name: str
    matching_source: str
    matching_algorithm: str
    matching_uid: int
    matching_row_number: int


# 3 in the diagram
class FuzzyMatching(BaseModel):
    results: List[FuzzyResult]


# 5 in the diagram
class TranslationQuery(BaseModel):
    translation_query: FuzzyResult
    target_language: str


class TranslationResult(BaseModel):
    translated_name: str
    translated_source: str
    translated_uid: int


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
    translated_medicine: str
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
    