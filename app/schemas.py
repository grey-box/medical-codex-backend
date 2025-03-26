from datetime import datetime, timezone
from typing import List, Optional, Callable

from pydantic import BaseModel, Field, field_validator


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


class UniqueTranslationsPYD(BaseModel):
    """
    The TranslationPydantic schema is used to validate data from the
    translation database table
    """

    source_language: str
    target_language: str
    source_text: str
    target_text: str
    table_name: str
    source_comment: Optional[str] = None
    weight: int

    class Config:
        # If needed, you can configure ORM mode so Pydantic can serialize SQLAlchemy models directly.
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls.model_validate(obj)


class FallbackQuery(BaseModel):
    medicine: FuzzyResult
    target_language: str


class FallbackResponse(BaseModel):
    translated_medicine: str


class FuzzyAlgorithm(BaseModel):
    function: Callable
    local: bool


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

    @field_validator('error_level')
    @classmethod
    def validate_error_level(cls, value):
        if value not in {0, 10, 20, 30, 40, 50}:
            raise ValueError("Invalid log level. Must be one of {0, 10, 20, 30, 40, 50}")
        return value
    