import os
import pathlib
import pandas as pd

# %% Define path to raw data
raw_data_path = (pathlib.Path(os.getcwd()) / "raw_data" / "drugbank" / "drugbank_vocabulary.csv")

# %% Read raw data
raw_data = pd.read_csv(raw_data_path)

# %% Split accession number on different rows using explode and | as separator
raw_data2 = (raw_data.assign(accession_number=raw_data['Accession Numbers']
                             .str.split('|'))
             .explode('accession_number')
             .reset_index(drop=True)
             )
# %% trim accession number
raw_data2['accession_number'] = raw_data2['accession_number'].str.strip()

# %% Drop Accession Numbers column
raw_data2 = raw_data2.drop('Accession Numbers', axis=1)

# %% Split Synonyms on different rows using explode and | as separator
raw_data3 = (raw_data2.assign(synonyms=raw_data2['Synonyms']
                              .str.split('|'))
             .explode('synonyms')
             .reset_index(drop=True)
             )

# %% trim synonyms
raw_data3['synonyms'] = raw_data3['synonyms'].str.strip()

# %% Drop Synonyms column
raw_data3 = raw_data3.drop('Synonyms', axis=1)

# %% Change all other columns names to lower case and replace spaces with underscores
raw_data4 = raw_data3.rename(columns=lambda x: x.lower().replace(' ', '_'))

# %% replace all values in dataframe with empty string if NA
raw_data5 = raw_data4.fillna('')

# %% Save data to csv file
raw_data5.to_csv(pathlib.Path(os.getcwd()) / "prepared_data" / "drugbank_vocabulary.csv",
                 quoting=2,
                 index=False)

# %% Save data to json file
raw_data5.to_json(pathlib.Path(os.getcwd()) / "prepared_data" / "drugbank_vocabulary.json",
                  orient='records')
