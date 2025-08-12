"""
Test Fixtures and Mock Data Module.

This module provides reusable test fixtures, mock data, and utilities
for the non-regression test suite. It includes database fixtures,
mock responses, and test data generators.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, List, Any
from sqlalchemy.orm import Session

from schemas import FuzzyQuery, FuzzyResult, TranslationQuery, TranslationResult, Translation


class MockDatabase:
    """Mock database class for testing purposes."""
    
    def __init__(self):
        self.fuzzy_results = [
            {
                "matching_name": "ibuprofen",
                "matching_source": "medications_en",
                "matching_algorithm": "Levenshtein",
                "matching_uid": 1,
                "matching_row_number": 1,
                "distance": 1
            },
            {
                "matching_name": "paracétamol",
                "matching_source": "medications_fr",
                "matching_algorithm": "Levenshtein",
                "matching_uid": 2,
                "matching_row_number": 2,
                "distance": 2
            },
            {
                "matching_name": "астмито",
                "matching_source": "medications_uk",
                "matching_algorithm": "Soundex",
                "matching_uid": 3,
                "matching_row_number": 3,
                "distance": 1
            },
            {
                "matching_name": "изотретиноїн",
                "matching_source": "medications_ru",
                "matching_algorithm": "Soundex",
                "matching_uid": 4,
                "matching_row_number": 4,
                "distance": 1
            }
        ]
        
        self.translation_results = [
            {
                "translated_name": "ibuprofène",
                "translated_source": "local_db",
                "translated_uid": 1,
                "source_term": "ibuprofen",
                "source_language": "en",
                "target_language": "fr",
                "confidence": 0.95,
                "alternatives": [
                    {"text": "ibuprofenum", "confidence": 0.85, "meaning": "alternative spelling"},
                    {"text": "ibuprofenum", "confidence": 0.80, "meaning": "latin form"}
                ],
                "additionalDetails": {
                    "domain": "medicine",
                    "formality": "neutral",
                    "examples_in_context": [
                        "L'ibuprofène est un anti-inflammatoire.",
                        "Prendre de l'ibuprofène pour la douleur."
                    ]
                }
            },
            {
                "translated_name": "paracetamol",
                "translated_source": "local_db",
                "translated_uid": 2,
                "source_term": "paracétamol",
                "source_language": "fr",
                "target_language": "en",
                "confidence": 0.90,
                "alternatives": [
                    {"text": "acetaminophen", "confidence": 0.88, "meaning": "US equivalent"},
                    {"text": "panadol", "confidence": 0.75, "meaning": "brand name"}
                ],
                "additionalDetails": {
                    "domain": "medicine",
                    "formality": "neutral",
                    "examples_in_context": [
                        "Paracetamol is commonly used for pain relief.",
                        "Take paracetamol every 6 hours as needed."
                    ]
                }
            }
        ]
        
        self.language_pairs = [
            {"source_language": "en", "target_languages": ["fr", "uk", "ru"]},
            {"source_language": "fr", "target_languages": ["en", "uk", "ru"]},
            {"source_language": "uk", "target_languages": ["en", "fr", "ru"]},
            {"source_language": "ru", "target_languages": ["en", "fr", "uk"]}
        ]
    
    def get_fuzzy_matches(self, query: FuzzyQuery) -> List[FuzzyResult]:
        """Mock fuzzy matching function."""
        results = []
        for i, result in enumerate(self.fuzzy_results):
            if result["matching_name"].lower().startswith(query.query.lower()[:3]):
                results.append(FuzzyResult(**result))
                if len(results) >= query.max_results:
                    break
        return results
    
    def get_translations(self, query: TranslationQuery) -> Translation:
        """Mock translation function."""
        results = []
        for result in self.translation_results:
            if result["source_term"] == query.translation_query.matching_name:
                results.append(TranslationResult(**result))
                break
        return Translation(results=results)
    
    def get_language_pairs(self) -> List[Dict[str, Any]]:
        """Mock language pairs function."""
        return self.language_pairs


@pytest.fixture
def mock_database():
    """Fixture providing a mock database."""
    return MockDatabase()


@pytest.fixture
def sample_fuzzy_queries():
    """Fixture providing sample fuzzy matching queries."""
    return [
        FuzzyQuery(
            source_language="en",
            query="ibuprofen",
            target_language="fr",
            max_distance=5,
            max_results=3
        ),
        FuzzyQuery(
            source_language="fr",
            query="paracétamol",
            target_language="en",
            max_distance=5,
            max_results=3
        ),
        FuzzyQuery(
            source_language="uk",
            query="астмито",
            target_language="en",
            max_distance=5,
            max_results=3
        ),
        FuzzyQuery(
            source_language="ru",
            query="изотретиноїн",
            target_language="en",
            max_distance=5,
            max_results=3
        ),
        FuzzyQuery(
            source_language="en",
            query="test",
            target_language="fr",
            max_distance=10,
            max_results=5
        )
    ]


@pytest.fixture
def sample_translation_queries():
    """Fixture providing sample translation queries."""
    fuzzy_result = FuzzyResult(
        matching_name="ibuprofen",
        matching_source="medications_en",
        matching_algorithm="Levenshtein",
        matching_uid=1,
        matching_row_number=1,
        distance=1
    )
    
    return [
        TranslationQuery(
            translation_query=fuzzy_result,
            target_language="fr"
        ),
        TranslationQuery(
            translation_query=fuzzy_result,
            target_language="uk"
        ),
        TranslationQuery(
            translation_query=fuzzy_result,
            target_language="ru"
        )
    ]


@pytest.fixture
def sample_language_data():
    """Fixture providing sample language data."""
    return {
        "available_languages": [
            {
                "source_language": "en",
                "target_languages": ["fr", "uk", "ru"]
            },
            {
                "source_language": "fr",
                "target_languages": ["en", "uk", "ru"]
            },
            {
                "source_language": "uk",
                "target_languages": ["en", "fr", "ru"]
            },
            {
                "source_language": "ru",
                "target_languages": ["en", "fr", "uk"]
            }
        ]
    }


@pytest.fixture
def sample_fuzzy_results():
    """Fixture providing sample fuzzy matching results."""
    return [
        FuzzyResult(
            matching_name="ibuprofen",
            matching_source="medications_en",
            matching_algorithm="Levenshtein",
            matching_uid=1,
            matching_row_number=1,
            distance=1
        ),
        FuzzyResult(
            matching_name="paracétamol",
            matching_source="medications_fr",
            matching_algorithm="Levenshtein",
            matching_uid=2,
            matching_row_number=2,
            distance=2
        ),
        FuzzyResult(
            matching_name="астмито",
            matching_source="medications_uk",
            matching_algorithm="Soundex",
            matching_uid=3,
            matching_row_number=3,
            distance=1
        )
    ]


@pytest.fixture
def sample_translation_results():
    """Fixture providing sample translation results."""
    return [
        TranslationResult(
            translated_name="ibuprofène",
            translated_source="local_db",
            translated_uid=1,
            source_term="ibuprofen",
            source_language="en",
            target_language="fr",
            confidence=0.95,
            alternatives=[
                {"text": "ibuprofenum", "confidence": 0.85, "meaning": "alternative spelling"},
                {"text": "ibuprofenum", "confidence": 0.80, "meaning": "latin form"}
            ],
            additionalDetails={
                "domain": "medicine",
                "formality": "neutral",
                "examples_in_context": [
                    "L'ibuprofène est un anti-inflammatoire.",
                    "Prendre de l'ibuprofène pour la douleur."
                ]
            }
        ),
        TranslationResult(
            translated_name="paracetamol",
            translated_source="local_db",
            translated_uid=2,
            source_term="paracétamol",
            source_language="fr",
            target_language="en",
            confidence=0.90,
            alternatives=[
                {"text": "acetaminophen", "confidence": 0.88, "meaning": "US equivalent"},
                {"text": "panadol", "confidence": 0.75, "meaning": "brand name"}
            ],
            additionalDetails={
                "domain": "medicine",
                "formality": "neutral",
                "examples_in_context": [
                    "Paracetamol is commonly used for pain relief.",
                    "Take paracetamol every 6 hours as needed."
                ]
            }
        )
    ]


@pytest.fixture
def edge_case_queries():
    """Fixture providing edge case queries for testing."""
    return [
        # Empty query
        FuzzyQuery(
            source_language="en",
            query="",
            target_language="fr",
            max_distance=5,
            max_results=5
        ),
        # Very long query
        FuzzyQuery(
            source_language="en",
            query="a" * 1000,
            target_language="fr",
            max_distance=5,
            max_results=5
        ),
        # Special characters
        FuzzyQuery(
            source_language="en",
            query="test@#$%^&*()",
            target_language="fr",
            max_distance=5,
            max_results=5
        ),
        # Unicode characters
        FuzzyQuery(
            source_language="en",
            query="café",
            target_language="fr",
            max_distance=5,
            max_results=5
        ),
        # Numeric query
        FuzzyQuery(
            source_language="en",
            query="12345",
            target_language="fr",
            max_distance=5,
            max_results=5
        )
    ]


@pytest.fixture
def invalid_queries():
    """Fixture providing invalid queries for error testing."""
    return [
        # Missing required fields
        {
            "source_language": "en"
            # Missing 'query' field
        },
        # Invalid field types
        {
            "source_language": 123,  # Should be string
            "query": "test",
            "target_language": "fr",
            "max_distance": "ten",  # Should be integer
            "max_results": "five"   # Should be integer
        },
        # Negative values
        {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": -1,
            "max_results": -5
        },
        # SQL injection attempt
        {
            "source_language": "en'; DROP TABLE users; --",
            "query": "test",
            "target_language": "fr"
        },
        # XSS attempt
        {
            "source_language": "<script>alert('xss')</script>",
            "query": "test",
            "target_language": "fr"
        }
    ]


@pytest.fixture
def performance_test_data():
    """Fixture providing data for performance testing."""
    return {
        "concurrent_requests": 10,
        "test_iterations": 5,
        "simple_query": {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 3
        },
        "complex_query": {
            "source_language": "en",
            "query": "ibuprofen",
            "target_language": "fr",
            "max_distance": 10,
            "max_results": 10
        }
    }


@pytest.fixture
def mock_database_session():
    """Fixture providing a mock database session."""
    mock_session = Mock(spec=Session)
    mock_session.info = {"mock": True}
    return mock_session


@pytest.fixture
def mock_fastapi_app():
    """Fixture providing a mock FastAPI app for testing."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    
    app = FastAPI()
    client = TestClient(app)
    return app, client


# Utility functions for test data generation
def generate_test_fuzzy_result(index: int, language: str = "en") -> FuzzyResult:
    """Generate a test fuzzy matching result."""
    return FuzzyResult(
        matching_name=f"test_medication_{index}",
        matching_source=f"medications_{language}",
        matching_algorithm="test",
        matching_uid=index,
        matching_row_number=index + 1,
        distance=1
    )


def generate_test_translation_result(index: int, language: str = "fr") -> TranslationResult:
    """Generate a test translation result."""
    return TranslationResult(
        translated_name=f"translated_medication_{index}",
        translated_source="test_source",
        translated_uid=index,
        source_term=f"test_medication_{index}",
        source_language="en",
        target_language=language,
        confidence=0.9,
        alternatives=[
            {"text": f"alternative_{index}_1", "confidence": 0.8, "meaning": "alternative 1"},
            {"text": f"alternative_{index}_2", "confidence": 0.7, "meaning": "alternative 2"}
        ],
        additionalDetails={
            "domain": "medicine",
            "formality": "neutral",
            "examples_in_context": [
                f"Example usage for medication {index}.",
                f"Another example for medication {index}."
            ]
        }
    )


def generate_test_language_pairs(num_languages: int = 4) -> List[Dict[str, Any]]:
    """Generate test language pairs."""
    languages = ["en", "fr", "uk", "ru"]
    pairs = []
    
    for i, source_lang in enumerate(languages[:num_languages]):
        target_languages = [lang for j, lang in enumerate(languages[:num_languages]) if j != i]
        pairs.append({
            "source_language": source_lang,
            "target_languages": target_languages
        })
    
    return pairs


def assert_fuzzy_result_structure(result: FuzzyResult):
    """Assert that a fuzzy result has the correct structure."""
    assert hasattr(result, 'matching_name')
    assert hasattr(result, 'matching_source')
    assert hasattr(result, 'matching_algorithm')
    assert hasattr(result, 'matching_uid')
    assert hasattr(result, 'matching_row_number')
    assert hasattr(result, 'distance')
    assert isinstance(result.matching_name, str)
    assert isinstance(result.matching_source, str)
    assert isinstance(result.matching_algorithm, str)
    assert isinstance(result.matching_uid, int)
    assert isinstance(result.matching_row_number, int)
    assert result.distance is None or isinstance(result.distance, int)


def assert_translation_result_structure(result: TranslationResult):
    """Assert that a translation result has the correct structure."""
    assert hasattr(result, 'translated_name')
    assert hasattr(result, 'translated_source')
    assert hasattr(result, 'translated_uid')
    assert hasattr(result, 'source_term')
    assert hasattr(result, 'source_language')
    assert hasattr(result, 'target_language')
    assert hasattr(result, 'confidence')
    assert hasattr(result, 'alternatives')
    assert hasattr(result, 'additionalDetails')
    
    assert isinstance(result.translated_name, str)
    assert isinstance(result.translated_source, str)
    assert isinstance(result.translated_uid, int)
    assert isinstance(result.source_term, str)
    assert isinstance(result.source_language, str)
    assert isinstance(result.target_language, str)
    assert result.confidence is None or isinstance(result.confidence, (int, float))
    assert isinstance(result.alternatives, list)
    assert result.additionalDetails is None or isinstance(result.additionalDetails, dict)


def assert_language_result_structure(result: Dict[str, Any]):
    """Assert that a language result has the correct structure."""
    assert "source_language" in result
    assert "target_languages" in result
    assert isinstance(result["source_language"], str)
    assert isinstance(result["target_languages"], list)
    assert all(isinstance(lang, str) for lang in result["target_languages"])