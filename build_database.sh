# Run this in the root of the project

python data_manipulation/conn.py
python data_manipulation/read_compendium.py
python data_manipulation/read_who_essentials.py
python data_manipulation/read_wikidata.py
python data_manipulation/read_drugbank.py
python data_manipulation/read_fda_product_code_classification.py
python data_manipulation/read_fip.py
python data_manipulation/read_rxterms.py
python data_manipulation/read_utis_in_ua.py

# Database will now be available in fastapi_backend/prepared_data.db