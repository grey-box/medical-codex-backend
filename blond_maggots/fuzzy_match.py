import sqlite3
from fuzzywuzzy import process

def fuzzy_match(source_language, input_string):
    # Connect to the SQLite database
    conn = sqlite3.connect('medicines.db')
    cursor = conn.cursor()
    
    # Retrieve all relevant labels based on the source language
    if source_language == 'uk':
        cursor.execute("SELECT label_uk FROM medicines")
    elif source_language == 'ru':
        cursor.execute("SELECT label_ru FROM medicines")
    elif source_language == 'gr':
        cursor.execute("SELECT label_gr FROM medicines")
    elif source_language == 'en':
        cursor.execute("SELECT label_en FROM medicines")
    else:
        raise ValueError("Unsupported source language. Use 'uk', 'ru', 'gr', or 'en'.")

    # Fetch all the labels
    labels = [row[0] for row in cursor.fetchall()]

    # Perform fuzzy matching
    results = process.extract(input_string, labels, limit=10)

    # Close the database connection
    conn.close()

    # Return the matched results (labels with their scores)
    return results

# Example usage
if __name__ == "__main__":
    source_lang = 'en'  # Change this to 'uk', 'ru', or 'gr' as needed
    input_str = 'Aspirin'  # Change this to the string you want to match
    matches = fuzzy_match(source_lang, input_str)
    
    for match in matches:
        print(f"Matched Label: {match[0]} with Score: {match[1]}")
