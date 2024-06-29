from pydantic import BaseModel
import Levenshtein
import pandas as pd
import numpy as np

#def fuzzy_matching(db, query):
 #   return None

uk_med = pd.read_csv("prepared_data/wikidata_names.csv", usecols = ["label_uk"])
ru_med = pd.read_csv("prepared_data/wikidata_names.csv", usecols = ["label_ru"])
en_med = pd.read_csv("prepared_data/wikidata_names.csv", usecols = ["label_en"])

def fuzzy(language, input_string):
    threshold = 10
    if language == "English":
        medication_list = en_med
    elif language == "Ukranian":
        medication_list = uk_med
    elif language == "Russian":
        medication_list = ru_med
    a = len(medication_list.index)
    #print(a)
    distance_values = []
    medicine = []
    for x in range(a):
        try:
            dist = Levenshtein.distance(input_string,medication_list.iloc[x, 0])
        except:
            dist = threshold +1
        distance_values.append(dist)
        if dist <= threshold:
            medicine.append(medication_list.iloc[x,0])
    print(medicine)
    return medicine
fuzzy("Ukranian","МЕБЕНДАЗО")