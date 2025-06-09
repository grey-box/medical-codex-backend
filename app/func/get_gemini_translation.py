import json
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
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Get the full language name for better translation results
        target_language = get_full_language_name(query.target_language)
        source_term = query.translation_query.matching_name
        
        # Create the translation prompt
        prompt = f"""
            Translate "{source_term}" to "{target_language}" as a drug name. 
            Insert the results in a JSON format with the following structure:
            {{
                "source_term": "{source_term}",
                "source_language": ,
                "translated_name": ,
                "target_language": ,
                "confidence": float,
                "alternatives": [
                    {{
                        "text": ,
                        "confidence": float,
                        "meaning": 
                    }}
                ],
                "additional_details": {{
                    "domain",
                    "formality",
                    "examples_in_context": [],
                }}
            }}
            Keep the names of the variables the same for consistency.
            Convert any brand name to the actual drug name.
        """
        
        logger.info(f"Sending translation request to Gemini API: '{source_term}' to '{target_language}'")
        
        # Configure safety settings to allow medical content
        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        response = model.generate_content(prompt, safety_settings=safety_settings)
        
        
        # Process the response
        if not response:
            logger.warning("Gemini API unable to provide a response")
            translated_text = "Translation unavailable"
        else:
            translated_text = response.text.strip()
            logger.info(f"Received translation from Gemini API: '{translated_text}'")
        
        
        # Remove json file characters (e.g., ```json ... ```)
        cleaned_output = re.sub(r"^```(?:json)?\s*|```$", "", translated_text, flags=re.IGNORECASE | re.MULTILINE).strip()
        
        # Parse the JSON
        try:
            parsed_result = json.loads(cleaned_output)
            
            # Pop the alternatives from the data
            raw_alternatives = parsed_result.pop("alternatives", [])

            # Build the alternatives list
            alternatives = [schemas.Alternative(**alt) for alt in raw_alternatives]
            
            # Pop the additional_details from the data
            raw_details = parsed_result.pop("additional_details", None)
            
            # Build the additional_details
            additional_details = schemas.AdditionalDetails(**raw_details) if raw_details else None
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode Gemini JSON: {e}")
            raise ValueError("Gemini output is not valid JSON")

        # Create and return the translation result
        translation_result = schemas.TranslationResult(
            **parsed_result,
            translated_source="gemini_api",
            translated_uid=query.translation_query.matching_uid,
            alternatives=alternatives,
            additionalDetails=additional_details
        )
        
        return schemas.Translation(results=[translation_result])
        
    except genai.types.generation_types.StopCandidateException as e:
        # Handle specific Gemini API errors
        error_message = f"Gemini API content filtered: {str(e)}"
        logger.warning(error_message)
        
        # Create a result indicating the content was filtered
        translation_result = schemas.TranslationResult(
            translated_name="Translation filtered by content policy",
            translated_source="gemini_api_filtered",
            translated_uid=query.translation_query.matching_uid,
        )

        translated_text = response.text.strip()
        logger.info(f"Received translation from Gemini API: '{translated_text}'")
        
        
        # Remove json file characters (e.g., ```json ... ```)
        cleaned_output = re.sub(r"^```(?:json)?\s*|```$", "", translated_text, flags=re.IGNORECASE | re.MULTILINE).strip()
        
        # Parse the JSON
        try:
            parsed_result = json.loads(cleaned_output)
            
            # Pop the alternatives from the data
            raw_alternatives = parsed_result.pop("alternatives", [])

            # Build the alternatives list
            alternatives = [schemas.Alternative(**alt) for alt in raw_alternatives]
            
            # Pop the additional_details from the data
            raw_details = parsed_result.pop("additional_details", None)
            
            # Build the additional_details
            additional_details = schemas.AdditionalDetails(**raw_details) if raw_details else None
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode Gemini JSON: {e}")
            raise ValueError("Gemini output is not valid JSON")

        # Create and return the translation result
        translation_result = schemas.TranslationResult(
            **parsed_result,
            translated_source="gemini_api",
            translated_uid=query.translation_query.matching_uid,
            alternatives=alternatives,
            additionalDetails=additional_details
        )
        
        return schemas.Translation(results=[translation_result])
        
    except genai.types.generation_types.StopCandidateException as e:
        # Handle specific Gemini API errors
        error_message = f"Gemini API content filtered: {str(e)}"
        logger.warning(error_message)
        
        # Create a result indicating the content was filtered
        translation_result = schemas.TranslationResult(
            translated_name="Translation filtered by content policy",
            translated_source="gemini_api_filtered",
            translated_uid=query.translation_query.matching_uid,
        )
        
        return schemas.Translation(results=[translation_result])
        
    except Exception as e:
        logger.error(f"Error in get_gemini_translation: {str(e)}")
        return {"results": []}
