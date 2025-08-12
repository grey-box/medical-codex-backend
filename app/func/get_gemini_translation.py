"""
Gemini Translation Module.

This module provides functionality for translating medical terms using Google's
Gemini AI API. It serves as a fallback translation method when database translations
are not available.
"""

import json
import logging
import os
import re

from dotenv import load_dotenv
from google import generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

import schemas
from config import LOGGER_NAME, settings
from func.get_full_language_name import get_full_language_name

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


def get_gemini_translation(
    query: schemas.TranslationQuery,
) -> schemas.Translation:
    """
    Translate a medical term using Google's Gemini AI API.
    
    This function takes a translation query containing a medical term and target language,
    then uses Google's Gemini AI to generate a translation. It specifically instructs
    the AI to translate drug names and convert brand names to generic drug names.
    
    Args:
        query (schemas.TranslationQuery): Object containing the term to translate
                                         and the target language.
        
    Returns:
        schemas.Translation: Object containing the translation results.
        If successful, contains the translated term with source "gemini_api".
        If unsuccessful, returns an empty result set.
    """
    # Initialize variables
    translated_text = "Translation unavailable"
    
    try:
        # Check if we're in test mode and return mock translation
        if os.getenv("TEST_MODE") == "true":
            logger.info("Using mock translation for test mode")
            source_term = query.translation_query.matching_name
            target_language = get_full_language_name(query.target_language)
            
            # Create a mock translation result
            translation_result = schemas.TranslationResult(
                source_term=source_term,
                source_language="en",
                translated_name=f"Mock translation of {source_term}",
                target_language=target_language,
                confidence=0.9,
                alternatives=[],
                additional_details=None,
                translated_source="mock_gemini",
                translated_uid=query.translation_query.matching_uid
            )
            return schemas.Translation(results=[translation_result])
        
        # Load API key from environment variables
        env_file = settings.env_file if hasattr(settings, 'env_file') else ".env"
        load_dotenv(env_file)
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not gemini_api_key:
            logger.error("Google API key not found in environment variables")
            return schemas.Translation(results=[])
        
        # Configure Gemini API
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
        
        # Generate the translation
        response = model.generate_content(prompt, safety_settings=safety_settings)
        
        
        # Process the response
        
        
        # Process the response
        if not response:
            logger.warning("Gemini API unable to provide a response")
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
        # Handle any other errors
        error_message = f"Error in Gemini translation for '{query.translation_query.matching_name}': {str(e)}"
        logger.error(error_message)
        
        # Return an empty result set
        return schemas.Translation(results=[])
