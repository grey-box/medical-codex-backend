import os
import pathlib
import pandas as pd

# %% Define path to raw data
raw_data_path = (pathlib.Path(os.getcwd()) / "raw_data" / "who_essential" / "2024-04-27-who-eml.csv")

# %% Read raw data
raw_data = pd.read_csv(raw_data_path, sep=';', encoding="UTF-8")

# %% Split ATC codes into a list of codes
raw_data = raw_data.assign(atc_classification=raw_data['ATC codes']
                           .apply(lambda x: [x.strip() for x in str(x).split(",") if len(x) > 0])
                           ).explode('atc_classification', ignore_index=True)
# %% Delete ATC codes column
del raw_data['ATC codes']

# %% save data to csv file
raw_data.to_csv(pathlib.Path(os.getcwd()) / "prepared_data" / "who-essential.csv",
                quoting=2,
                index=False)

# %% save data to json file
raw_data.to_json(pathlib.Path(os.getcwd()) / "prepared_data" / "who-essential.json",
                  orient='records')
