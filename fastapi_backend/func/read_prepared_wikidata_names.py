import sqlite3
import pandas as pd


def read_prepared_wikidata_names(language) -> pd.Series:
    """
    Read prepared Wikidata names based on the specified language.

    This function reads the prepared Wikidata names from an SQLite database
    and returns a pandas Series containing the names in the specified language.

    Parameters:
    - language (str): The language of the Wikidata names to read. It can be either "English", "Ukrainian", or "Russian".

    Returns:
    - pd.Series: A pandas Series containing the Wikidata names in the specified language. If the language is not supported, it returns a pandas Series with None values.

    Raises:
    - Exception: If the specified language is not supported.
    """
    if language == "English":
        label = "label_en"
    elif language == "Ukrainian":
        label = "label_uk"
    elif language == "Russian":
        label = "label_ru"
    else:
        raise Exception("Unsupported language")
    try:
        conn = sqlite3.connect("fastapi_backend/database/medicines.db")
        query = f"SELECT DISTINCT {label} FROM medicines WHERE {label} IS NOT NULL"
        names_df = pd.read_sql_query(query, conn)
        conn.close()

        names = names_df[label].dropna().drop_duplicates()

    except Exception as e:
        raise Exception("Error fetching data from the SQLite database: " + str(e))

    return names
