import os
import pathlib
import pandas as pd
import re
from transliterate import translit
from conn import conn

# %% Define path to raw data
raw_data_path = (pathlib.Path(os.getcwd()) / "raw_data" / "fip" / "fip-equiv.csv")

# %% Read raw data
raw_data = pd.read_csv(raw_data_path, sep=',', dtype={'activeingredient': str})

# %% Fix atc_classification
raw_data['atc_classification'] = (
    raw_data['atc_classification'].str.replace(' ', '').apply(lambda x: str(x).strip())
)
# %% Fix activeingredient
raw_data['activeingredient'] = (raw_data['activeingredient']
                                .apply(lambda x: re.sub(r'\\+n', ' ', string=repr(x)))
                                .apply(lambda x: re.sub(r'\'', '', string=x))
                                .apply(lambda x: [x.strip() for x in x.split("/") if len(x) > 0])
                                )
# %% Fix activeingredient_cy
raw_data['activeingredient_cy'] = (raw_data['activeingredient_cy']
                                   .apply(lambda x: re.sub(r'\\+n', ' ', string=repr(x)))
                                   .apply(lambda x: re.sub(r'\'', '', string=x))
                                   .apply(lambda x: [x.strip() for x in x.split("/") if len(x) > 0])
                                   )
# %% Fix activeingredient_lat
raw_data['brandname_uk_cy'] = (raw_data['brandname_uk_cy']
                               .apply(lambda x: re.sub(r'\\+n', ' ', string=repr(x)))
                               .apply(lambda x: re.sub(r'\'', '', string=x))
                               )
# %% Fix activeingredient_lat
raw_data['brandname_uk_lat'] = (raw_data['brandname_uk_lat']
                                .apply(lambda x: re.sub(r'\\+n', ' ', string=repr(x)))
                                .apply(lambda x: re.sub(r'\'', '', string=x))
                                .apply(lambda x: x.strip() if len(x) > 1 else None)
                                )
# %% Fix manufacturer
raw_data['manufacturer'] = (raw_data['manufacturer']
                            .apply(lambda x: re.sub(r'\\+n', ' ', string=repr(x)))
                            .apply(lambda x: re.sub(r'\'', '', string=x))
                            )
# %% Fix dosage_cy
raw_data['dosage_cy'] = (raw_data['dosage_cy']
                         .apply(lambda x: re.sub(r'\\+n', ' ', string=repr(x)))
                         .apply(lambda x: re.sub(r'\'', '', string=x))
                         .apply(lambda x: [x.replace(';', '').strip() for x in x.split("\u2010") if len(x) > 1])
                         )
# %% Fix dosage
raw_data['dosage'] = (raw_data['dosage']
                      .apply(lambda x: re.sub(r'\\+n', ' ', string=repr(x)))
                      .apply(lambda x: re.sub(r'\'', '', string=x))
                      .apply(lambda x: [x.replace(';', '').strip() for x in x.split("\u2010") if len(x) > 1])
                      )
# %% Replace missing urls going forward
raw_data['info_uk'] = (raw_data['info_uk'].ffill())

# %% Remove all rows with missing atc_classification
raw_data2 = raw_data[~raw_data['atc_classification'].isna()].copy()

# %% Transliterate brandname_uk_cy from cyrillic to latin if brandname_uk_lat is missing
raw_data2 = raw_data2.assign(brandname_uk_lat_translit=raw_data2['brandname_uk_cy']
                             .apply(lambda x: translit(str(x), 'ru', reversed=True)))
# %% Coalesce brandname_uk_lat and brandname_uk_lat_translit
raw_data2 = raw_data2.assign(brandname_uk_lat_merge=raw_data2['brandname_uk_lat']
                             .combine_first(raw_data2['brandname_uk_lat_translit']))

# %% Save data to csv file
raw_data2.to_csv(pathlib.Path(os.getcwd()) / "prepared_data" / "fip_equiv.csv",
                 quoting=2,
                 index=False)

# %% Save data to json file
raw_data2.to_json(pathlib.Path(os.getcwd()) / "prepared_data" / "fip_equiv.json",
                  orient='records')

# %% Convert all list columns to string type
raw_data3 = raw_data2.copy()
for col in raw_data3.select_dtypes(include=['object']).columns:
    raw_data3[col] = raw_data3[col].apply(lambda x: '^'.join(x) if isinstance(x, list) else x)

# %% Add table to SQLite database
raw_data3.to_sql('fip_equiv', conn, if_exists='replace', index=False)

conn.close()

