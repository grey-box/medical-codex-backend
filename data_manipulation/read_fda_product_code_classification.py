import os
import pathlib
import pandas as pd

# %% Define path to raw data
raw_data_path = (pathlib.Path(os.getcwd()) / "raw_data" / "fda-product-code-classification" / "2024-04-29.txt")

# %% Read raw data, REGULATIONNUMBER is of type object
raw_data = pd.read_csv(raw_data_path, sep='|', encoding="ISO-8859-1", dtype={'REGULATIONNUMBER': str,
                                                                             'SUBMISSION_TYPE_ID': str,
                                                                             'DEVICECLASS': str})

# %% Replace all values in dataframe with empty string if NA
raw_data2 = raw_data.fillna('')

# %% All columns names to lower case and replace spaces with underscores
raw_data3 = raw_data2.rename(columns=lambda x: x.lower().replace(' ', '_'))

# %% Save data to csv file
raw_data3.to_csv(pathlib.Path(os.getcwd()) / "prepared_data" / "fda-product-code-classification.csv",
                 quoting=2,
                 index=False)

# %% Save data to json file
raw_data3.to_json(pathlib.Path(os.getcwd()) / "prepared_data" / "fda-product-code-classification.json",
                  orient='records')