import os
import pathlib
import pandas as pd
import sqlite3

# %% Define path to raw data
raw_terms_path = (pathlib.Path(os.getcwd()) / "raw_data" / "rxterms" / "RxTerms202304.txt")
raw_ingredients_path = (pathlib.Path(os.getcwd()) / "raw_data" / "rxterms" / "RxTermsIngredients202304.txt")

# %% Read raw data
raw_terms = pd.read_csv(raw_terms_path,
                        delimiter='|',
                        encoding="UTF-8",
                        dtype={'RXCUI': str, 'GENERIC_RXCUI': str, 'SXDG_RXCUI': str})
raw_ingredients = pd.read_csv(raw_ingredients_path,
                              delimiter='|',
                              encoding="UTF-8",
                              dtype={'RXCUI': str, 'ING_RXCUI': str})

# %% Column names to lowercase
raw_terms.columns = raw_terms.columns.str.lower()
raw_ingredients.columns = raw_ingredients.columns.str.lower()

# %% save data to csv file
raw_terms.to_csv(pathlib.Path(os.getcwd()) / "prepared_data" / "rxterms_terms.csv",
                 quoting=2,
                 index=False)
raw_ingredients.to_csv(pathlib.Path(os.getcwd()) / "prepared_data" / "rxterms_ing.csv",
                       quoting=2,
                       index=False)

# %% save data to json file
raw_terms.to_json(pathlib.Path(os.getcwd()) / "prepared_data" / "rxterms_terms.json",
                  orient='records')
raw_ingredients.to_json(pathlib.Path(os.getcwd()) / "prepared_data" / "rxterms_ing.json",
                        orient='records')

# %% Add table to SQLite database


conn = sqlite3.connect('fastapi_backend/codex.db')

raw_terms.to_sql('rxterms_terms', conn, if_exists='replace', index=False)
raw_ingredients.to_sql('rxterms_ing', conn, if_exists='replace', index=False)

conn.close()
