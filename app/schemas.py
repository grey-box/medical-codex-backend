from typing import List, Optional

from pydantic import BaseModel


# 2 in the diagram
class FuzzyQuery(BaseModel):
    source_language: str
    query: str
    threshold: int = 10
    nb_max_results: int = 10
class FuzzyResult(BaseModel):
    matching_name: str
    matching_source: str
    matching_uid: int

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
