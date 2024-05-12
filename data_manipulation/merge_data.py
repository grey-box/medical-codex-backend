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
    "wikidata_names": pd.read_json(prepared_data_path / "wikidata_names.json")
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

# %% assign first non-empty value to medicine_name column
translation_data_who['medicine_name_merge1_en'] = translation_data_who[['medicine_name_who_matches', 'medicine_name_who']].apply(
    lambda x: x['medicine_name_who_matches'] if pd.isna(x['medicine_name_who']) else x['medicine_name_who'],
    axis=1
)

# %% Wikidata Names
wikidata_labels_aliases = pd.concat([
    ## Labels only
    prepared_data['wikidata_names'][['id', 'label_uk', 'label_ru', 'label_en']].rename(columns={'id': 'wikidata_id'}),
    ## Exploded English alias list
    prepared_data['wikidata_names'][['id', 'label_uk', 'label_ru', 'alias_list_en']]
    .explode('alias_list_en')
    .rename(columns={'alias_list_en': 'label_en', 'id': 'wikidata_id'}),
    ## Exploded Russian alias list
    prepared_data['wikidata_names'][['id', 'label_uk', 'alias_list_ru', 'label_en']]
    .explode('alias_list_ru')
    .rename(columns={'alias_list_ru': 'label_ru', 'id': 'wikidata_id'}),
    ## Exploded Ukrainian alias list
    prepared_data['wikidata_names'][['id', 'alias_list_uk', 'label_ru', 'label_en']]
    .explode('alias_list_uk')
    .rename(columns={'alias_list_uk': 'label_uk', 'id': 'wikidata_id'}),
])
# %% delete records with empty labels
wikidata_labels_aliases = (wikidata_labels_aliases
                           .dropna(subset=['label_uk', 'label_ru', 'label_en'])
                           .reset_index(drop=True)
                           )

# %% merge wikidata names
translation_data_wikidata = wikidata_labels_aliases[['wikidata_id', 'label_uk', 'label_ru', 'label_en']].merge(
    translation_data_who,
    how="outer",
    left_on="label_en",
    right_on="medicine_name_merge1_en",
    suffixes=("_wikidata", "_who")
)

# %% assign first non-empty value to medicine_name column
translation_data_wikidata['medicine_name_merge2_en'] = translation_data_wikidata[['medicine_name_merge1_en', 'label_en']].apply(
    lambda x: x['label_en'] if pd.isna(x['medicine_name_merge1_en']) else x['medicine_name_merge1_en'],
    axis=1
)

translation_data_wikidata['medicine_name_merge2_uk'] = translation_data_wikidata[['title_uk_name', 'label_uk']].apply(
    lambda x: x['label_uk'] if pd.isna(x['title_uk_name']) else x['title_uk_name'],
    axis=1
)

translation_data_wikidata['medicine_name_merge2_ru'] = translation_data_wikidata[['title_ru_name', 'label_ru']].apply(
    lambda x: x['label_ru'] if pd.isna(x['title_ru_name']) else x['title_ru_name'],
    axis=1
)

# %% Export what's done for today
(translation_data_wikidata[(translation_data_wikidata['medicine_name_merge2_en'] != "") |
                           (translation_data_wikidata['medicine_name_merge2_uk'] != "")]
 .to_excel(pathlib.Path(os.getcwd()) / "merged_data" / "translation_data_wikidata_2024-05-11.xlsx", index=False))
