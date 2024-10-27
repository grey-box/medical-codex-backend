
import sqlite3

class MedicineTranslator:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def translate(self, term, target_language):
        language_columns = {
            'uk': ['label_uk', 'alias_list_uk'],
            'ru': ['label_ru', 'alias_list_ru'],
            'gr': ['label_gr', 'alias_list_gr'],
            'en': ['label_en', 'alias_list_en']
        }

        # Validate the target language
        if target_language not in language_columns:
            raise ValueError(f"Invalid target language: {target_language}. Choose from 'uk', 'ru', 'gr', 'en'.")

        # Search for the term in all language columns and alias lists
        query = f"""
            SELECT label_uk, label_ru, label_gr, label_en
            FROM medicines
            WHERE label_uk = ? OR label_ru = ? OR label_gr = ? OR label_en = ?
            OR alias_list_uk LIKE ? OR alias_list_ru LIKE ? OR alias_list_gr LIKE ? OR alias_list_en LIKE ?
        """
        self.cursor.execute(query, (term, term, term, term, f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'))
        result = self.cursor.fetchone()

        if result:
            # Map the result to the appropriate target language
            translated_term = result[list(language_columns.keys()).index(target_language)]
            return translated_term
        else:
            return f"Term '{term}' not found in the database."

# Usage example
if __name__ == "__main__":
    db_path = "medicines.db"  # Update to the correct path if needed
    translator = MedicineTranslator(db_path)
    
    term = input("Enter the term to translate: ")
    target_language = input("Enter the target language (uk, ru, gr, en): ")
    
    translation = translator.translate(term, target_language)
    print(f"Translation: {translation}")
