import logging

import Levenshtein
import pandas as pd

from func.read_prepared_wikidata_names import read_prepared_wikidata_names


def fuzzy_levenshtein(language,
                      input_string,
                      source,
                      threshold=10,
                      nb_max_results=10) -> list[str]:
    """
    Fuzzy search function for medication names.

    This function takes a language, input string, source, threshold, and number of maximum results as parameters.
    It returns a list of medication names that match the input string within the specified threshold.

    Parameters:
    - language (str): The language of the input string and medication names.
    - input_string (str): The input string to search for.
    - source (str): The source of the medication names.
    - threshold (int, optional): The maximum Levenshtein distance allowed between the input string and medication names. Default is 10.
    - nb_max_results (int, optional): The maximum number of results to return. Default is 10.

    Returns:
    - list[str]: A list of medication names that match the input string within the specified threshold.

    Raises:
    - Exception: If the input, source, or language is invalid.
    """
    if not language in ["English", "Ukrainian", "Russian"]:
        # Generate Exception
        raise Exception("Invalid language")
    medication_list = []
    if input_string is not None:
        if "wikidata" in source:
            wikidata_not_none = [str(item).lower() for item in read_prepared_wikidata_names(language).to_list() if
                                 item is not None]
            medication_list = medication_list + wikidata_not_none
        else:
            # Add more sources here if needed
            raise Exception("Invalid source: only wikidata for now")
    else:
        # Generate Exception
        raise Exception("Invalid input")
    distance_values = []
    medicine = []
    for x in range(len(medication_list)):
        dist = Levenshtein.distance(input_string, medication_list[x])
        if dist <= threshold:
            medicine.append(medication_list[x])
            distance_values.append(dist)
    # sorting medication by distance
    df = pd.DataFrame({'medicine': medicine, 'distance': distance_values})
    df = df.sort_values('distance')
    # return top N results
    top_n_matches = df.head(nb_max_results)['medicine'].tolist()
    logging.info(f"Levenshtein results: {top_n_matches}")
    return top_n_matches
