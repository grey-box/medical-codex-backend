import logging

from langcodes import Language

from app.config import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_full_language_name(language_code: str) -> str:
    """
    Convert an ISO 639 language code to its full language name.

    Args:
        language_code (str): ISO 639 language code (e.g., 'en', 'uk', 'ru').

    Returns:
        str: Full language name in English or the original code if conversion fails.
    """
    try:
        language = Language.get(language_code)
        full_name = language.display_name("en")
        logger.info(f"Successfully converted '{language_code}' to '{full_name}'")
        return full_name
    except Exception as error:
        logger.error(f"Failed to convert language code '{language_code}': {str(error)}")
        return language_code
