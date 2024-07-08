import logging

import Levenshtein
import pandas as pd

import schemas

wikidata_names = pd.read_csv("database/wikidata_names.csv")


def fuzzy_matching(db: object, query: schemas.FuzzyQuery) -> dict[str, list[dict[str, str | int]]]:
    try:
        list_medicine = fuzzy(language=str(query.source_language),
                              input_string=str(query.query).lower(),  # Convert the query to lowercase
                              source="wikidata",
                              threshold=int(query.threshold),
                              nb_max_results=int(query.nb_max_results)
                              )
    except Exception as e:
        logging.error(f"Error during fuzzy matching: {e}")
        return {"results": []}
    logging.info(f"List of medications: {list_medicine}")
    # Generate a FuzzyResult for each medication
    results = {"results": [{
        "matching_name": medicine,
        "matching_source": "wikidata",  # Replace with the actual source
        "matching_uid": 0  # We'll get this from the database
    } for medicine in list_medicine]}

    logging.info(f"Results: {results}")

    return results


def read_prepared_wikidata_names(language) -> pd.Series:
    """
    Read prepared Wikidata names based on the specified language.

    This function reads the prepared Wikidata names from a CSV file and returns a pandas Series containing the names in the specified language.

    Parameters:
    - language (str): The language of the Wikidata names to read. It can be either "English", "Ukrainian", or "Russian".

    Returns:
    - pd.Series: A pandas Series containing the Wikidata names in the specified language. If the language is not supported, it returns a pandas Series with None values.

    Raises:
    - Exception: If the specified language is not supported.
    """
    if language == "English":
        label = "label_en"
    elif language == "Ukrainian":
        label = "label_uk"
    elif language == "Russian":
        label = "label_ru"
    else:
        raise Exception("Unsupported language")
    try:
        names = wikidata_names[label].dropna().drop_duplicates()
    except Exception as e:
        raise Exception("Label not found in the Wikidata names DataFrame" + str(e))
    return names


def fuzzy(language,
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
    logging.info(f"Fuzzy search results: {top_n_matches}")
    return top_n_matches
