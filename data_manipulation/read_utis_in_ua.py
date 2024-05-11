import os
import pathlib
from urllib.parse import unquote

import pandas as pd
from transliterate import translit

# %% Define path to raw data
raw_data_path = (pathlib.Path(os.getcwd()) / "raw_data" / "utis.in.ua" / "utis.in.ua.json")

# %% Read raw data
raw_data = pd.read_json(raw_data_path)

# %% Extract page name from URL
raw_data = raw_data.assign(page_name=raw_data['url']
                           .apply(lambda x: x.split('/')[-2]))
# %% Decode URL characters
raw_data = raw_data.assign(page_name_decoded=raw_data['page_name']
                           .apply(lambda x: translit(unquote(x), reversed=True, language_code='ru')))

# %% Delete page_name column
del raw_data['page_name']

# %% save data to csv file
raw_data.to_csv(pathlib.Path(os.getcwd()) / "prepared_data" / "utis_in_ua.csv",
                quoting=2,
                index=False)

# %% save data to json file
raw_data.to_json(pathlib.Path(os.getcwd()) / "prepared_data" / "utis_in_ua.json",
                 orient='records')
