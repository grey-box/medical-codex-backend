import os
import pathlib
import pandas as pd


# %%
def read_compendium_data(raw_data_path, source, language):
    # Read raw data from json file
    raw_data = pd.read_json(raw_data_path)
    # Add source information column
    raw_data['source'] = source
    # Add language column
    raw_data['language'] = language
    # Extract page name from url
    raw_data['page_name'] = raw_data['url'].apply(lambda x: x.split('/')[-2])
    # Extract latin name from the parenthesis part in the title
    raw_data['title_latin_name'] = raw_data['title'].apply(lambda x: x.split('(')[-1].split(')')[0].strip())
    # Detect is there is an asterisk at the end of the latin name,
    # create a boolean column indicating its presence and remove it
    raw_data['title_latin_name_has_asterisk'] = raw_data['title_latin_name'].apply(
        lambda x: True if x[-1] == '*' else False)
    raw_data['title_latin_name'] = raw_data['title_latin_name'].apply(lambda x: x[:-1] if x[-1] == '*' else x)
    # Get part before parenthesis in title
    raw_data[f'title_{language}_name'] = raw_data['title'].apply(lambda x: x.split('(')[0].strip())
    # Remove asterisk at the end of the uk name
    raw_data[f'title_{language}_name'] = raw_data[f'title_{language}_name'].apply(lambda x: x[:-1] if x[-1] == '*' else x)
    return raw_data


# %% Define path to raw data
raw_data_path_uk = (pathlib.Path(os.getcwd()) /
                    "raw_data" /
                    "compendium.com.ua" /
                    "uk" /
                    "compendium.json")

raw_data_path_ru = (pathlib.Path(os.getcwd()) /
                    "raw_data" /
                    "compendium.com.ua" /
                    "ru" /
                    "compendium.json")

# %% Prepare data
compendium_uk = read_compendium_data(raw_data_path=raw_data_path_uk,
                                     source="compendium.com.ua",
                                     language='uk')

compendium_ru = read_compendium_data(raw_data_path=raw_data_path_ru,
                                     source="compendium.com.ua",
                                     language='ru')

# %% Save data to csv file

compendium_uk.to_csv(pathlib.Path(os.getcwd()) /
                     "prepared_data" /
                     "compendium_uk.csv",
                     quoting=2,
                     index=False)

compendium_ru.to_csv(pathlib.Path(os.getcwd()) /
                     "prepared_data" /
                     "compendium_ru.csv",
                     quoting=2,
                     index=False)

# %% Save data to json file

compendium_uk.to_json(pathlib.Path(os.getcwd()) /
                      "prepared_data" /
                      "compendium_uk.json",
                      orient='records')

compendium_ru.to_json(pathlib.Path(os.getcwd()) /
                      "prepared_data" /
                      "compendium_ru.json",
                      orient='records')
