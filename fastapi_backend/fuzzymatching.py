from pydantic import BaseModel
import Levenshtein
import pandas as pd
import numpy as np
from fonetika.soundex import RussianSoundex
from fonetika.soundex import EnglishSoundex
from fonetika.distance import PhoneticsInnerLanguageDistance

#def fuzzy_matching(db, query):
 #   return None


uk_med = pd.read_csv("prepared_data/compendium_uk.csv", usecols = ["title_uk_name"])
ru_med = pd.read_csv("prepared_data/compendium_ru.csv", usecols = ["title_ru_name"])
en_med = pd.read_csv("prepared_data/who_essential.csv", usecols = ["medicine_name"])



def fonetikasoundex(language, input_string):
    threshold = 2
    medicine = []
    if language == "English":
        medication_list = en_med
    elif language == "Russian":
        medication_list = ru_med
    a = len(medication_list.index)
    print(a)

    if language == "English":
        soundex = RussianSoundex()
    elif language == "Russian":
        soundex = RussianSoundex()
    phon_distance = PhoneticsInnerLanguageDistance(soundex)
    for x in range(a):
        b = phon_distance.distance(input_string, medication_list.iloc[x, 0])
        if b < threshold:
            medicine.append(medication_list.iloc[x,0])
    print(medicine)
#fonetikasoundex("English", "amphotericin b")


def fuzzyLevenshtein(language, input_string):
    threshold = 1
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

fuzzyLevenshtein("Russian","ізотретиноїн")
