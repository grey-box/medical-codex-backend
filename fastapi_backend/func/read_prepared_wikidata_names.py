import pandas as pd

wikidata_names = pd.read_csv("database/wikidata_names.csv")

def read_prepared_wikidata_names(language) -> pd.Series:
    """
    Read prepared Wikidata names based on the specified language.

    This function reads the prepared Wikidata names from a CSV file and returns a pandas Series containing the names in the specified language.

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
        names = wikidata_names[label].dropna().drop_duplicates()
    except Exception as e:
        raise Exception("Label not found in the Wikidata names DataFrame" + str(e))
    return names
