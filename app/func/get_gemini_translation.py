import logging
import os
from typing import Dict, List, Any

from dotenv import load_dotenv
from google import generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from app import schemas as schemas
from app.func.get_full_language_name import get_full_language_name
from config import LOGGER_NAME

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
        
        # Select the model to use
        # Malcolm Gauthier (4 jun 2025): switched from gemini 1.5 flash to 2.5 flash
        # at the time of writing this, gemini 2.5 flash doesn't have a standalone version, it's still only previews
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
        
        # Get the full language name for better translation results
        target_language = get_full_language_name(query.target_language)
        prompt = f'Translate "{query.translation_query.matching_name}" to "{target_language}" as a drug name. Convert any brand name to the actual drug name.'

        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        response = model.generate_content(prompt, safety_settings=safety_settings)

        if not response:
            logger.warning("Gemini API unable to provide a response")
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
        logger.error(f"Error in get_gemini_translation: {str(e)}")
        return {"results": []}
