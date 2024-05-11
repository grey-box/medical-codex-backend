import os
import pathlib
import pandas as pd
import difflib

# %% Define path to prepared data
prepared_data_path = (pathlib.Path(os.getcwd()) / "prepared_data")

# %% Read prepared data
prepared_data = {
    "compendium_ru": pd.read_csv(prepared_data_path / "compendium_ru.csv"),
    "compendium_uk": pd.read_csv(prepared_data_path / "compendium_uk.csv"),
    "drugbank_vocabulary": pd.read_csv(prepared_data_path / "drugbank_vocabulary.csv"),
    "fda_product_code_classification": pd.read_csv(prepared_data_path / "fda_product_code_classification.csv"),
    "fip_equiv": pd.read_csv(prepared_data_path / "fip_equiv.csv"),
    "rxterms_ing": pd.read_csv(prepared_data_path / "rxterms_ing.csv"),
    "rxterms_terms": pd.read_csv(prepared_data_path / "rxterms_terms.csv"),
    "utis_in_ua": pd.read_csv(prepared_data_path / "utis_in_ua.csv"),
    "who_essential": pd.read_csv(prepared_data_path / "who_essential.csv"),
    "wikidata_names": pd.read_csv(prepared_data_path / "wikidata_names.csv")
}

# %% Assemble both languages translation for Compendium data

translation_data_compendium = (
    prepared_data["compendium_uk"][['title_latin_name', 'title_uk_name']]
    .drop_duplicates()
    .merge(prepared_data["compendium_ru"][['title_latin_name', 'title_ru_name']]
           .drop_duplicates(),
           how="outer",
           on="title_latin_name",
           suffixes=("_uk", "_ru")).assign(source='compendium.com.ua')
    .reset_index(drop=True)
    .rename(columns={'title_latin_name': 'medicine_name'})
)


# %%
def close_match_substring(my_str, compare_list, cutoff=0.8):
    """
    This function finds the closest match from the given 'compare_list' to the input 'my_str'.
    It uses the difflib library to find the closest matches and then checks the longest common substring.
    If the longest common substring is more than 4 characters and it starts from the beginning of both strings,
    it returns the closest match. If no match is found, it returns the original input string.

    Parameters:
    my_str (str): The input string for which we want to find the closest match.
    compare_list (list): A list of strings to compare with the input string.
    cutoff (float, optional): The minimum similarity score for a match to be considered. Defaults to 0.8.

    Returns:
    str: The closest match to the input string from the 'compare_list' or the original input string if no match is found.
    """
    possible_matches = difflib.get_close_matches(my_str, compare_list, cutoff=cutoff, n=3)
    for possible_match in possible_matches:
        # get longest common substring
        current_match = difflib.SequenceMatcher(None, str(my_str), str(possible_match)).find_longest_match()
        if current_match.size > 4 and current_match.a == 0:
            return possible_match
    return my_str


# %% WHO Essential
translation_data_compendium['medicine_name_who_matches'] = translation_data_compendium['medicine_name'].apply(
    lambda x: close_match_substring(x, list(prepared_data["who_essential"]['medicine_name']), cutoff=0.6))

# %%
translation_data_who = translation_data_compendium.merge(
    prepared_data["who_essential"][['medicine_name', 'atc_classification', 'source']]
    .drop_duplicates(),
    how="outer",
    left_on="medicine_name_who_matches",
    right_on="medicine_name",
    suffixes=("_compendium", "_who")
)

# %% Wikidata Names

