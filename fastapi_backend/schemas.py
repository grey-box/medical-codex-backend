from typing import List

from pydantic import BaseModel


class FuzzyMatching(BaseModel):
    pass


class FuzzyQuery(BaseModel):
    pass


class TranslationLanguagePair(BaseModel):
    source_language: str
    destination_language: str

    class Config:
        orm_mode = True


class Translation(BaseModel):
    pass


class TranslationQuery(BaseModel):
    pass
