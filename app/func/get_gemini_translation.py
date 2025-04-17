import logging
import os
from typing import Dict, List, Any

from dotenv import load_dotenv
from google import generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

import schemas
from func.get_full_language_name import get_full_language_name
from config import LOGGER_NAME
from fastapi import status

logger = logging.getLogger(LOGGER_NAME)


def get_gemini_translation(
    query: schemas.TranslationQuery,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get translation using Google's Gemini API.

    Args:
        query (schemas.TranslationQuery): Translation query parameters.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Translation results.
    """
    try:
        load_dotenv("env.local")
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        target_language = get_full_language_name(query.target_language)
        prompt = f'Translate "{query.translation_query.matching_name}" to "{target_language}" as a drug name. Convert any brand name to the actual drug name.'

        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        response = model.generate_content(prompt, safety_settings=safety_settings)

        if not response:
            logger.warning(status.HTTP_503_SERVICE_UNAVAILABLE + " Gemini API unable to provide a response")
            translated_text = "Translation unavailable"
        else:
            translated_text = response.text

        return {
            "results": [
                {
                    "translated_name": translated_text,
                    "translated_source": "gemini_api",
                    "translated_uid": query.translation_query.matching_uid,
                }
            ]
        }
    except Exception as e:
        logger.error(status.HTTP_500_INTERNAL_SERVER_ERROR + f" Error in get_gemini_translation: {str(e)}")
        return {"results": []}
