"""
Text Normalization and Filtering Module.

This module provides functionality for normalizing and filtering text extracted by paddle.
This function breaks down text blocks into individual words while removing unwanted characters, numerical digits
and excluding common filler words that may muddy and slow the fuzzysearch.
"""

import string
import unicodedata

STOPWORDS = {
    "and", "or", "the", "a", "an", "of", "to", "in", "on", "for", "with", "is", "at",
    "by", "from", "this", "that", "it", "as", "be", "are", "was", "were", "but", "not",
    "no", "yes", "you", "i", "we", "he", "she", "they", "them", "us", "our", "your",
}

def normalize_and_filter_extracted_text(text_to_filter) -> list[str]:
    tokens = []

    for text_block in text_to_filter:
        for word in text_block['rec_text'].split():
            # Normalize Unicode
            normalized = unicodedata.normalize('NFKC', word)

            # Remove punctuation and digits, lowercase, strip
            cleaned = ''.join(
                char for char in normalized
                if char not in string.punctuation and not char.isdigit()
            ).lower().strip()

            # Skip empty tokens and common stopwords
            if cleaned and cleaned not in STOPWORDS:
                tokens.append(cleaned)

    return tokens