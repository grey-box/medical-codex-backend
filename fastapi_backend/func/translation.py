import logging
import sqlite3
from fastapi import HTTPException

logger = logging.getLogger("translation")


def translate(query) -> dict:
    try:
        term = query.translation_query.matching_name.lower()

        logger.info(f"Searching for translation of '{term}'")

        conn = sqlite3.connect("fastapi_backend/database/medicines.db")
        cursor = conn.cursor()

        sql_query = """
            SELECT label_uk, label_ru, label_gr, label_en
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

        if result:
            translated_term = next((col for col in result if col), None)
            logger.info(f"Translation found: {translated_term}")

            return {
                "results": [
                    {
                        "translated_name": translated_term,
                        "translated_source": "local_db",
                        "translated_uid": 1,
                    }
                ]
            }
        else:
            logger.info(f"No translation found for term '{term}'.")
            return {"results": []}

    except Exception as e:
        logger.error(f"Error during translation: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")