import logging

import schemas
from func.base_levenshtein import fuzzy_levenshtein
from func.fonetika_soundex import fonetika_soundex


def fuzzy_matching(db: object, query: schemas.FuzzyQuery, matching_algorithm="Levenshtein") -> dict[str, list[dict[str, str | int]]]:
    list_medicine = []
    if matching_algorithm == "Levenshtein":
        try:
            list_medicine = fuzzy_levenshtein(language=str(query.source_language),
                                              input_string=str(query.query).lower(),  # Convert the query to lowercase
                                              source="wikidata",
                                              threshold=int(query.threshold),
                                              nb_max_results=int(query.nb_max_results)
                                              )
        except Exception as e:
            logging.error(f"Error during Levenshtein algorithm: {e}")
            return {"results": []}
    elif matching_algorithm == "Soundex":
        try:
            list_medicine = fonetika_soundex(language=str(query.source_language),
                                             input_string=str(query.query).lower(),  # Convert the query to lowercase
                                             source="wikidata",
                                             threshold=int(query.threshold),
                                             nb_max_results=int(query.nb_max_results)
                                             )
        except Exception as e:
            logging.error(f"Error during Soundex algorithm: {e}")
            return {"results": []}
    logging.info(f"List of medications: {list_medicine}")
    # Generate a FuzzyResult for each medication
    results = {"results": [{
        "matching_name": medicine,
        "matching_source": "wikidata",  # Replace with the actual source
        "matching_algorithm": matching_algorithm,  # Replace with the actual algorithm used
        "matching_uid": 0  # We'll get this from the database
    } for medicine in list_medicine]}

    logging.info(f"Results: {results}")

    return results


