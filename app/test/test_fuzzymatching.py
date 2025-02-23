from app.algorithms.search_medications_by_levenshtein import (
    search_medications_by_levenshtein,
)
from app.algorithms.search_medications_by_soundex import search_medications_by_soundex
from app.database import get_database_session
from app.func.get_unique_source_texts import get_unique_source_texts
from schemas import FuzzyQuery

db = next(get_database_session())

source_uk = get_unique_source_texts(
    db, FuzzyQuery(source_language="uk", query="астмито", max_distance=5, max_results=5)
)
source_ru = get_unique_source_texts(
    db,
    FuzzyQuery(
        source_language="ru", query="изотретиноїн", max_distance=2, max_results=5
    ),
)


def test_levenshtein():
    assert (
        search_medications_by_levenshtein(
            language="uk",
            query="астмито",
            medications=source_uk,
            max_distance=5,
            max_results=5,
        )[0]
        == "астматол"
    )


def test_fonetika_soundex():
    assert (
        search_medications_by_soundex(
            language="ru",
            query="изотретиноїн",
            medications=source_ru,
            max_distance=2,
            max_results=5,
        )[0]
        == "ізотретиноїн"
    )
