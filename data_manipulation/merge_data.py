import os
import pathlib
from conn import conn

import pandas as pd

from close_match_substring import close_match_substring

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

# %% WHO Essential
translation_data_compendium['medicine_name_who_matches'] = translation_data_compendium['medicine_name'].apply(
    lambda x: close_match_substring(x, list(prepared_data["who_essential"]['medicine_name']), cutoff=0.6))

# %% Merge compendium and WHO data
translation_data_who = translation_data_compendium.merge(
    prepared_data["who_essential"][['medicine_name', 'atc_classification', 'source']]
    .drop_duplicates(),
    how="outer",
    left_on="medicine_name_who_matches",
    right_on="medicine_name",
    suffixes=("_compendium", "_who")
)

# %% Assign first non-empty value to medicine_name column
translation_data_who['medicine_name_merge1_en'] = translation_data_who[
    ['medicine_name_who_matches', 'medicine_name_who']].apply(
    lambda x: x['medicine_name_who_matches'] if pd.isna(x['medicine_name_who']) else x['medicine_name_who'],
    axis=1
)

# %% Wikidata Names
wikidata_labels_aliases = pd.concat([
    # Labels only
    prepared_data['wikidata_names'][['id', 'label_uk', 'label_ru', 'label_en']].rename(columns={'id': 'wikidata_id'}),
    # Exploded English alias list
    prepared_data['wikidata_names'][['id', 'label_uk', 'label_ru', 'alias_list_en']]
    .explode('alias_list_en')
    .rename(columns={'alias_list_en': 'label_en', 'id': 'wikidata_id'}),
    # Exploded Russian alias list
    prepared_data['wikidata_names'][['id', 'label_uk', 'alias_list_ru', 'label_en']]
    .explode('alias_list_ru')
    .rename(columns={'alias_list_ru': 'label_ru', 'id': 'wikidata_id'}),
    # Exploded Ukrainian alias list
    prepared_data['wikidata_names'][['id', 'alias_list_uk', 'label_ru', 'label_en']]
    .explode('alias_list_uk')
    .rename(columns={'alias_list_uk': 'label_uk', 'id': 'wikidata_id'}),
])
# %% delete records with empty labels
wikidata_labels_aliases = (wikidata_labels_aliases
                           .dropna(subset=['label_uk', 'label_ru', 'label_en'])
                           .reset_index(drop=True)
                           )

# %% merge wikidata names with Compendium and WHO data
translation_data_wikidata = wikidata_labels_aliases[['wikidata_id', 'label_uk', 'label_ru', 'label_en']].merge(
    translation_data_who,
    how="outer",
    left_on="label_en",
    right_on="medicine_name_merge1_en",
    suffixes=("_wikidata", "_who")
)

# %% assign first non-empty value to medicine_name column
translation_data_wikidata['medicine_name_merge2_en'] = (
    translation_data_wikidata[['medicine_name_merge1_en', 'label_en']].apply(
        lambda x: x['label_en'] if pd.isna(x['medicine_name_merge1_en']) else x['medicine_name_merge1_en'],
        axis=1
    ))

translation_data_wikidata['medicine_name_merge2_uk'] = (
    translation_data_wikidata[['title_uk_name', 'label_uk']].apply(
        lambda x: x['label_uk'] if pd.isna(x['title_uk_name']) else x['title_uk_name'],
        axis=1
    ))

translation_data_wikidata['medicine_name_merge2_ru'] = (
    translation_data_wikidata[['title_ru_name', 'label_ru']].apply(
        lambda x: x['label_ru'] if pd.isna(x['title_ru_name']) else x['title_ru_name'],
        axis=1
    ))

# %% Drugbank data

drugbank_data = prepared_data['drugbank_vocabulary'][['common_name']].drop_duplicates().copy()
# %%
drugbank_data['best_match_medicine_name_merge2_en'] = (
    drugbank_data['common_name'].apply(
        lambda x: close_match_substring(str(x), list(translation_data_wikidata['medicine_name_merge2_en']
                                                     .dropna()
                                                     .drop_duplicates()), cutoff=0.6)
    )
)

# %% Drugbank data synonym

drugbank_data_synonyms = prepared_data['drugbank_vocabulary'][['synonyms']].drop_duplicates().copy()
# %%
drugbank_data_synonyms['best_match_synonym_merge2_en'] = (
    drugbank_data_synonyms['synonyms'].apply(
        lambda x: close_match_substring(str(x), list(translation_data_wikidata['medicine_name_merge2_en']
                                                     .dropna()
                                                     .drop_duplicates()), cutoff=0.6)
    )
)

# %% Merge with Drugbank data
translation_data_drugbank = translation_data_wikidata.merge(
    drugbank_data[['common_name', 'best_match_medicine_name_merge2_en']],
    how="outer",
    left_on="medicine_name_merge2_en",
    right_on="best_match_medicine_name_merge2_en",
    suffixes=("", "_drugbank"))
# %%
translation_data_drugbank2 = translation_data_drugbank.merge(
    prepared_data['drugbank_vocabulary'][['common_name', 'drugbank_id']].drop_duplicates(),
    how="outer",
    left_on="common_name",
    right_on="common_name").reset_index()

# %% Best english name
translation_data_drugbank2['medicine_name_merge3_en'] = (
    translation_data_drugbank2[['medicine_name_merge2_en', 'common_name']].apply(
        lambda x: x['common_name'] if pd.isna(x['medicine_name_merge2_en']) else x['medicine_name_merge2_en'],
        axis=1
    ))

# %% Export what's done for today
if not os.path.exists(pathlib.Path(os.getcwd()) / "merged_data"):
    os.mkdir(pathlib.Path(os.getcwd()) / "merged_data")
single_table_data = (translation_data_drugbank2[(translation_data_drugbank2['medicine_name_merge3_en'] != "") |
                                                (translation_data_drugbank2['medicine_name_merge2_uk'] != "")][[
    'medicine_name_merge3_en',
    'medicine_name_merge2_uk',
    'medicine_name_merge2_ru',
    'wikidata_id',
    'source_who',
    'source_compendium',
    'atc_classification']].drop_duplicates()
                     .sort_values(['source_who', 'medicine_name_merge3_en'])
                     .rename(columns={'medicine_name_merge3_en': 'English Name',
                                      'medicine_name_merge2_uk': 'Ukrainian Name',
                                      'medicine_name_merge2_ru': 'Russian Name',
                                      'source_who': 'WHO Source',
                                      'source_compendium': 'Compendium Source',
                                      'atc_classification': 'ATC Classification'}))

# %% Export the merged data to an Excel file
single_table_data.to_excel(pathlib.Path(os.getcwd()) /
                           "merged_data" /
                           "translation_data_wikidata_2024-07-14.xlsx", index=False)

# %% Export the merged data to a SQLite database
single_table_data.to_sql('translation_data', conn, if_exists='replace', index=False)
conn.close()

print("Data exported successfully!")
