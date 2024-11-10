import logging
from typing import List, Callable

import Levenshtein
import pandas as pd
from fonetika.distance import PhoneticsInnerLanguageDistance
from fonetika.soundex import EnglishSoundex, RussianSoundex

def process_input(source_data: List[str], input_string: str) -> List[str]:
    if input_string is None:
        raise ValueError("Invalid input")
    return [str(item).lower() for item in source_data if item is not None]

def calculate_distances(medication_list: List[str], input_string: str, distance_func: Callable, threshold: float) -> tuple:
    """
    Calculate distances between an input string and a list of medications.

    This function computes the distance between the input string and each medication
    in the provided list using the specified distance function. It returns medications
    and their corresponding distances that are within the given threshold.

    Parameters:
    - medication_list (List[str]): A list of medication names to compare against.
    - input_string (str): The input string to compare with each medication.
    - distance_func (Callable): A function that calculates the distance between two strings.
    - threshold (float): The maximum distance allowed for a medication to be included in the result.

    Returns:
    tuple: A tuple containing two lists:
        - List[str]: Medications that are within the threshold distance.
        - List[float]: Corresponding distances for the medications.
    """
    medicine = []
    distance_values = []
    for med in medication_list:
        dist = distance_func(input_string, med)
        if dist <= threshold:
            medicine.append(med)
            distance_values.append(dist)
    return medicine, distance_values

def get_top_matches(medicine: List[str], distance_values: List[float], nb_max_results: int) -> List[str]:
    """
    Get the top matching medicines based on their distance values.

    This function takes lists of medicines and their corresponding distance values,
    sorts them by distance, and returns the top matches.

    Parameters:
    - medicine (List[str]): A list of medicine names.
    - distance_values (List[float]): A list of distance values corresponding to each medicine.
    - nb_max_results (int): The maximum number of top matches to return.

    Returns:
    - List[str]: A list of medicine names, sorted by their distance values,
                 containing at most nb_max_results elements.
    """
    df = pd.DataFrame({"medicine": medicine, "distance": distance_values})
    df = df.sort_values("distance")
    return df.head(nb_max_results)["medicine"].tolist()

def fuzzy_levenshtein(
    source_language: str, source_data: List[str], input_string: str, threshold: int = 10, nb_max_results: int = 10
) -> List[str]:
    """
    Fuzzy search function for medication names using Levenshtein distance.

    Parameters:
    - source_language (str): The language of the input string and medication names.
    - source_data (List[str]): The list of medication names to search through.
    - input_string (str): The input string to search for.
    - threshold (int, optional): The maximum Levenshtein distance allowed. Default is 10.
    - nb_max_results (int, optional): The maximum number of results to return. Default is 10.

    Returns:
    - List[str]: A list of medication names that match the input string within the specified threshold.

    Raises:
    - ValueError: If the input or language is invalid.
    """
    if source_language not in ["en", "uk", "ru"]:
        raise ValueError("Invalid language")
    
    medication_list = process_input(source_data, input_string)
    medicine, distance_values = calculate_distances(medication_list, input_string, Levenshtein.distance, threshold)
    top_n_matches = get_top_matches(medicine, distance_values, nb_max_results)
    
    logging.info(f"Levenshtein results: {top_n_matches}")
    return top_n_matches

def fonetika_soundex(
    source_language: str, source_data: List[str], input_string: str, threshold: float = 2, nb_max_results: int = 10
) -> List[str]:
    """
    Fuzzy search function for medication names using Soundex algorithm.

    Parameters:
    - source_language (str): The language of the input string and medication names.
    - source_data (List[str]): The list of medication names to search through.
    - input_string (str): The input string to search for.
    - threshold (float, optional): The maximum phonetic distance allowed. Default is 2.
    - nb_max_results (int, optional): The maximum number of results to return. Default is 10.

    Returns:
    - List[str]: A list of medication names that match the input string within the specified threshold.

    Raises:
    - ValueError: If the input or language is invalid.
    """
    medication_list = process_input(source_data, input_string)

    if source_language == "en":
        soundex = EnglishSoundex()
    elif source_language in ["ru", "uk"]:
        soundex = RussianSoundex()
    else:
        raise ValueError("Unsupported language")

    phon_distance = PhoneticsInnerLanguageDistance(soundex)
    medicine, distance_values = calculate_distances(medication_list, input_string, phon_distance.distance, threshold)
    top_n_matches = get_top_matches(medicine, distance_values, nb_max_results)

    logging.info(f"Soundex Results: {top_n_matches}")
    return top_n_matches