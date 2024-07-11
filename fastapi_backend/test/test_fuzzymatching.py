from func.base_levenshtein import fuzzy_levenshtein
from func.fonetika_soundex import fonetika_soundex


def test_levenshtein():
    assert fuzzy_levenshtein(language="Ukrainian",
                             input_string="астмито",
                             source="wikidata",
                             threshold=5,
                             nb_max_results=5)[0] == "астматол"


def test_fonetika_soundex():
    assert fonetika_soundex(language="Russian",
                            input_string="изотретиноїн",
                            source="wikidata",
                            threshold=2,
                            nb_max_results=5)[0] == "ізотретиноїн"
