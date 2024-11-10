from app.database import get_db

from app.func.algorithms import fonetika_soundex
from app.func.algorithms import fuzzy_levenshtein
from app.func.fuzzy_matching import get_unique_source_values

db = get_db()

source_uk = get_unique_source_values(db, "uk")
source_ru = get_unique_source_values(db, "ru")


def test_levenshtein():
    assert (
        fuzzy_levenshtein(
            source_language="uk",
            input_string="астмито",
            source_data=source_uk,
            threshold=5,
            nb_max_results=5,
        )[0]
        == "астматол"
    )


def test_fonetika_soundex():
    assert (
        fonetika_soundex(
            source_language="ru",
            input_string="изотретиноїн",
            source_data=source_ru,
            threshold=2,
            nb_max_results=5,
        )[0]
        == "ізотретиноїн"
    )
