"""
Language Name Conversion Module.

This module provides functionality for converting ISO 639 language codes
to their full language names in English. It uses the langcodes library
to perform the conversion.
"""

import logging

from langcodes import Language, tag_parser

from config import LOGGER_NAME

# Set up logger for this module
logger = logging.getLogger(LOGGER_NAME)


def get_full_language_name(language_code: str) -> str:
    """
    Convert an ISO 639 language code to its full language name in English.

    This function takes a language code (e.g., 'en', 'fr', 'de') and attempts
    to convert it to its full language name in English (e.g., 'English', 'French', 'German').
    If the conversion fails, it returns the original language code.

    Examples:
        >>> get_full_language_name('en')
        'English'
        >>> get_full_language_name('fr')
        'French'
        >>> get_full_language_name('invalid_code')
        'invalid_code'

    Args:
        language_code (str): ISO 639 language code (e.g., 'en', 'uk', 'ru').

    Returns:
        str: Full language name in English if conversion succeeds,
             or the original language code if conversion fails.
    """
    if not language_code:
        logger.warning("Empty language code provided")
        return ""

    try:
        # Attempt to get the Language object for the given code
        language = Language.get(language_code)

        # Get the display name in English
        full_name = language.display_name("en")

        # Log successful conversion
        logger.info(f"Successfully converted '{language_code}' to '{full_name}'")

        # Log successful conversion
        logger.info(f"Successfully converted '{language_code}' to '{full_name}'")

        return full_name

    except tag_parser.LanguageTagError as e:
        # Handle specific language tag parsing errors
        error_message = f"Invalid language code format '{language_code}': {str(e)}"
        logger.warning(error_message)
        return language_code

    except ValueError as e:
        # Handle value errors (e.g., unknown language code)
        error_message = f"Unknown language code '{language_code}': {str(e)}"
        logger.warning(error_message)
        return language_code

    except Exception as e:
        # Handle any other unexpected errors
        error_message = f"Failed to convert language code '{language_code}': {str(e)}"
        logger.error(error_message)
        return language_code
