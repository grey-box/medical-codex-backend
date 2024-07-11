import logging

import pandas as pd
from fonetika.soundex import RussianSoundex
from fonetika.soundex import EnglishSoundex
from fonetika.distance import PhoneticsInnerLanguageDistance


def fonetika_soundex(language,
                     input_string,
                     source,
                     threshold=2,
                     nb_max_results=10) -> list[str]:
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

    # Define the soundex algorithm for the language
    if language == "English":
        soundex = RussianSoundex()
    elif language in ["Russian", "Ukrainian"]:  # Since we don't have Ukrainian Soundex, we'll use Russian one
        soundex = RussianSoundex()
    else:
        raise Exception("Unsupported language")

    # Initialize a distance matrix
    phon_distance = PhoneticsInnerLanguageDistance(soundex)

    for x in range(len(medication_list)):
        dist = phon_distance.distance(input_string, medication_list[x])
        if dist <= threshold:
            medicine.append(medication_list[x])
            distance_values.append(dist)
    # sorting medication by distance
    df = pd.DataFrame({'medicine': medicine, 'distance': distance_values})
    df = df.sort_values('distance')
    # return top N results
    top_n_matches = df.head(nb_max_results)['medicine'].tolist()
    logging.info(f"Soundex Results: {top_n_matches}")
    return top_n_matches
