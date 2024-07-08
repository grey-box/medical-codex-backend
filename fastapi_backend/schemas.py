from typing import List

from pydantic import BaseModel


class FuzzyResult(BaseModel):
    matching_name: str
    matching_source: str
    matching_uid: int


class TranslationResult(BaseModel):
    translated_name: str
    translated_source: str
    translated_uid: int


# 3 in the diagram
class FuzzyMatching(BaseModel):
    results: List[FuzzyResult]


# 2 in the diagram
class FuzzyQuery(BaseModel):
    source_language: str
    query: str
    threshold: int = 10
    nb_max_results: int = 10


class TranslationLanguagePair(BaseModel):
    source_language: str
    target_language: str

    class Config:
        from_attributes = True


class TranslationLanguageResult(BaseModel):
    translations: List[TranslationLanguagePair]


# 6 in the diagram
class Translation(BaseModel):
    results: List[TranslationResult]


# 5 in the diagram
class TranslationQuery(BaseModel):
    translation_query: FuzzyResult
    target_language: str
