import os
import pathlib
import pandas as pd

# %% Define path to raw data
raw_data_path = (pathlib.Path(os.getcwd()) / "raw_data" / "wikidata" / "wikidata_names_2024-05-08.csv")

# %% Read raw data
raw_data = pd.read_csv(raw_data_path, sep=',', encoding="UTF-8", dtype={'rxnorm': str, 'chebi_id': str})

# %% Parse json data for Ukrainian names
raw_data['alias_list_uk'] = raw_data['alias_list_uk'].apply(lambda x: eval(x))
# %% Parse json data for Russian names
raw_data['alias_list_ru'] = raw_data['alias_list_ru'].apply(lambda x: eval(x))
# %% Parse json data for English names
raw_data['alias_list_en'] = raw_data['alias_list_en'].apply(lambda x: eval(x))
# %% Parse json data for French names
raw_data['alias_list_fr'] = raw_data['alias_list_fr'].apply(lambda x: eval(x))

# %% save data to csv file
raw_data.to_csv(pathlib.Path(os.getcwd()) / "prepared_data" / "wikidata-names.csv",
                quoting=2,
                index=False)

# %% save data to json file
raw_data.to_json(pathlib.Path(os.getcwd()) / "prepared_data" / "wikidata-names.json",
                  orient='records')