from func.fuzzymatching import fuzzy


def test_fuzzy_matching():
    assert fuzzy(language="Ukrainian",
                 input_string="астмито",
                 source="wikidata",
                 threshold=5,
                 nb_max_results=5)[0] == "астматол"
