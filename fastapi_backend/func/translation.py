import logging
import sqlite3
from fastapi import HTTPException

logger = logging.getLogger("translation")


def translate(query) -> dict:
    try:
        term = query.translation_query.matching_name.lower()
        target_language = query.target_language.lower()

        logger.info(f"Searching for translation of '{term}' in '{target_language}'")

        conn = sqlite3.connect("fastapi_backend/database/medicines.db")
        cursor = conn.cursor()

        language_column = f"label_{target_language}"

        sql_query = f"""
            SELECT {language_column}
            FROM medicines
            WHERE LOWER(label_uk) = ? OR LOWER(label_ru) = ? 
               OR LOWER(label_gr) = ? OR LOWER(label_en) = ?
               OR alias_list_uk LIKE ? OR alias_list_ru LIKE ? 
               OR alias_list_gr LIKE ? OR alias_list_en LIKE ?
            LIMIT 1;
        """

        logger.info(f"Executing SQL query: {sql_query}")

        cursor.execute(
            sql_query,
            (
                term,
                term,
                term,
                term,
                f"%{term}%",
                f"%{term}%",
                f"%{term}%",
                f"%{term}%",
            ),
        )
        result = cursor.fetchone()

        conn.close()

        if result and result[0]:
            translated_term = result[0]
            logger.info(f"Translation found: {translated_term}")

            return {
                "results": [
                    {
                        "translated_name": translated_term,
                        "translated_source": "local_db",
                        "translated_uid": query.translation_query.matching_uid,
                    }
                ]
            }
        else:
            logger.info(f"No translation found for '{term}' in '{target_language}'.")
            return {"results": []}

    except Exception as e:
        logger.error(f"Error during translation: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")
