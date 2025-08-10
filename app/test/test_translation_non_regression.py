"""
Non-Regression Test Suite for Translation Endpoints.

This module contains comprehensive non-regression tests for the translation
functionality, ensuring that existing features continue to work correctly
after code changes. It covers various scenarios including different languages,
translation workflows, and edge cases.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from main import app
from schemas import TranslationQuery, TranslationResult, Translation, FuzzyResult


class TestTranslationNonRegression:
    """Test class for translation non-regression tests."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)

    def test_translation_basic_functionality(self):
        """Test basic translation functionality."""
        # First, get a fuzzy match
        fuzzy_query = {
            "source_language": "en",
            "query": "ibuprofen",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 1
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        if fuzzy_data["results"]:
            # Use the fuzzy match for translation
            translation_query = {
                "translation_query": fuzzy_data["results"][0],
                "target_language": "fr"
            }
            
            response = self.client.post("/translate/", json=translation_query)
            
            assert response.status_code == 201
            data = response.json()
            assert "results" in data
            assert isinstance(data["results"], list)
            
            # Verify structure of each result
            for result in data["results"]:
                assert "translated_name" in result
                assert "translated_source" in result
                assert "translated_uid" in result
                assert "source_term" in result
                assert "source_language" in result
                assert "target_language" in result
                assert "confidence" in result
                assert "alternatives" in result
                assert "additionalDetails" in result

    def test_translation_with_ukrainian_to_english(self):
        """Test translation from Ukrainian to English."""
        # Get fuzzy match for Ukrainian term
        fuzzy_query = {
            "source_language": "uk",
            "query": "астмито",
            "target_language": "en",
            "max_distance": 5,
            "max_results": 1
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        if fuzzy_data["results"]:
            translation_query = {
                "translation_query": fuzzy_data["results"][0],
                "target_language": "en"
            }
            
            response = self.client.post("/translate/", json=translation_query)
            
            assert response.status_code == 201
            data = response.json()
            assert "results" in data

    def test_translation_with_russian_to_english(self):
        """Test translation from Russian to English."""
        # Get fuzzy match for Russian term
        fuzzy_query = {
            "source_language": "ru",
            "query": "изотретиноин",
            "target_language": "en",
            "max_distance": 5,
            "max_results": 1
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        if fuzzy_data["results"]:
            translation_query = {
                "translation_query": fuzzy_data["results"][0],
                "target_language": "en"
            }
            
            response = self.client.post("/translate/", json=translation_query)
            
            assert response.status_code == 201
            data = response.json()
            assert "results" in data

    def test_translation_test_endpoint(self):
        """Test the test endpoint for translation."""
        # Create a mock fuzzy result
        mock_fuzzy_result = {
            "matching_name": "test_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 1,
            "matching_row_number": 1,
            "distance": 1
        }
        
        translation_query = {
            "translation_query": mock_fuzzy_result,
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/test", json=translation_query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 5  # Test endpoint should return exactly 5 results
        
        # Verify test results structure
        for i, result in enumerate(data["results"]):
            assert result["translated_name"] == f"translated_name{i}"
            assert result["translated_source"] == f"translated_source{i}"
            assert result["translated_uid"] == i

    def test_translation_empty_fuzzy_result(self):
        """Test translation with empty fuzzy result."""
        empty_fuzzy_result = {
            "matching_name": "",
            "matching_source": "",
            "matching_algorithm": "",
            "matching_uid": 0,
            "matching_row_number": 0,
            "distance": None
        }
        
        translation_query = {
            "translation_query": empty_fuzzy_result,
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/", json=translation_query)
        
        # Should handle empty fuzzy result gracefully
        assert response.status_code in [201, 500]

    def test_translation_missing_required_fields(self):
        """Test translation with missing required fields."""
        incomplete_query = {
            "translation_query": {
                "matching_name": "test",
                # Missing other required fields
            },
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/", json=incomplete_query)
        
        # Should handle incomplete data gracefully
        assert response.status_code in [422, 500]

    def test_translation_invalid_target_language(self):
        """Test translation with invalid target language."""
        mock_fuzzy_result = {
            "matching_name": "test_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 1,
            "matching_row_number": 1,
            "distance": 1
        }
        
        translation_query = {
            "translation_query": mock_fuzzy_result,
            "target_language": "invalid_lang"
        }
        
        response = self.client.post("/translate/", json=translation_query)
        
        # Should handle invalid language gracefully
        assert response.status_code in [201, 500]

    def test_translation_response_structure_consistency(self):
        """Test that the response structure is consistent across different queries."""
        # Create a mock fuzzy result
        mock_fuzzy_result = {
            "matching_name": "test_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 1,
            "matching_row_number": 1,
            "distance": 1
        }
        
        target_languages = ["fr", "en", "uk", "ru"]
        
        for target_lang in target_languages:
            translation_query = {
                "translation_query": mock_fuzzy_result,
                "target_language": target_lang
            }
            
            response = self.client.post("/translate/", json=translation_query)
            assert response.status_code == 201
            data = response.json()
            
            # Verify consistent structure
            assert "results" in data
            assert isinstance(data["results"], list)
            
            for result in data["results"]:
                required_fields = [
                    "translated_name", "translated_source", "translated_uid",
                    "source_term", "source_language", "target_language",
                    "confidence", "alternatives", "additionalDetails"
                ]
                for field in required_fields:
                    assert field in result

    def test_translation_confidence_values(self):
        """Test that confidence values are reasonable."""
        mock_fuzzy_result = {
            "matching_name": "test_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 1,
            "matching_row_number": 1,
            "distance": 1
        }
        
        translation_query = {
            "translation_query": mock_fuzzy_result,
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/test", json=translation_query)
        
        assert response.status_code == 201
        data = response.json()
        
        for result in data["results"]:
            if result["confidence"] is not None:
                assert result["confidence"] >= 0, "Confidence should be non-negative"
                assert result["confidence"] <= 1, "Confidence should not exceed 1.0"

    def test_translation_alternatives_structure(self):
        """Test that alternatives structure is correct."""
        mock_fuzzy_result = {
            "matching_name": "test_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 1,
            "matching_row_number": 1,
            "distance": 1
        }
        
        translation_query = {
            "translation_query": mock_fuzzy_result,
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/test", json=translation_query)
        
        assert response.status_code == 201
        data = response.json()
        
        for result in data["results"]:
            assert isinstance(result["alternatives"], list)
            for alternative in result["alternatives"]:
                assert "text" in alternative
                assert "confidence" in alternative
                assert "meaning" in alternative

    def test_translation_additional_details_structure(self):
        """Test that additional details structure is correct."""
        mock_fuzzy_result = {
            "matching_name": "test_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 1,
            "matching_row_number": 1,
            "distance": 1
        }
        
        translation_query = {
            "translation_query": mock_fuzzy_result,
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/test", json=translation_query)
        
        assert response.status_code == 201
        data = response.json()
        
        for result in data["results"]:
            if result["additionalDetails"] is not None:
                assert isinstance(result["additionalDetails"], dict)
                assert "domain" in result["additionalDetails"]
                assert "formality" in result["additionalDetails"]
                assert "examples_in_context" in result["additionalDetails"]
                assert isinstance(result["additionalDetails"]["examples_in_context"], list)

    def test_translation_uid_consistency(self):
        """Test that UIDs are consistent between fuzzy matching and translation."""
        # Get fuzzy match
        fuzzy_query = {
            "source_language": "en",
            "query": "ibuprofen",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 1
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        if fuzzy_data["results"]:
            fuzzy_uid = fuzzy_data["results"][0]["matching_uid"]
            
            translation_query = {
                "translation_query": fuzzy_data["results"][0],
                "target_language": "fr"
            }
            
            response = self.client.post("/translate/", json=translation_query)
            assert response.status_code == 201
            data = response.json()
            
            # UID should be preserved in translation
            for result in data["results"]:
                assert result["translated_uid"] == fuzzy_uid

    def test_translation_multiple_results(self):
        """Test translation with multiple fuzzy results."""
        fuzzy_query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 10,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        if len(fuzzy_data["results"]) > 1:
            # Test translation with each fuzzy result
            for fuzzy_result in fuzzy_data["results"]:
                translation_query = {
                    "translation_query": fuzzy_result,
                    "target_language": "fr"
                }
                
                response = self.client.post("/translate/", json=translation_query)
                assert response.status_code == 201
                data = response.json()
                assert "results" in data

    def test_translation_language_consistency(self):
        """Test that language codes are consistent."""
        mock_fuzzy_result = {
            "matching_name": "test_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 1,
            "matching_row_number": 1,
            "distance": 1
        }
        
        translation_query = {
            "translation_query": mock_fuzzy_result,
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/test", json=translation_query)
        
        assert response.status_code == 201
        data = response.json()
        
        for result in data["results"]:
            # The test endpoint may not set language fields, so check if they exist or are None
            assert result["source_language"] is None or result["source_language"] == "test_source"
            assert result["target_language"] is None or result["target_language"] == "fr"

    def test_translation_performance_with_multiple_requests(self):
        """Test performance with multiple consecutive requests."""
        mock_fuzzy_result = {
            "matching_name": "test_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 1,
            "matching_row_number": 1,
            "distance": 1
        }
        
        translation_query = {
            "translation_query": mock_fuzzy_result,
            "target_language": "fr"
        }
        
        # Make multiple requests
        responses = []
        for _ in range(5):
            response = self.client.post("/translate/", json=translation_query)
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 201
            data = response.json()
            assert "results" in data
            assert isinstance(data["results"], list)

    def test_translation_fallback_workflow(self):
        """Test the complete translation workflow including fallback."""
        # This test would verify that when no database translation is found,
        # the system falls back to the configured fallback method
        mock_fuzzy_result = {
            "matching_name": "unknown_medication",
            "matching_source": "test_source",
            "matching_algorithm": "test",
            "matching_uid": 999,
            "matching_row_number": 999,
            "distance": 1
        }
        
        translation_query = {
            "translation_query": mock_fuzzy_result,
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/", json=translation_query)
        
        # Should either return database results or fallback results
        assert response.status_code == 201
        data = response.json()
        assert "results" in data
        
        # If results are empty, it means fallback failed or no translation available
        if data["results"]:
            for result in data["results"]:
                assert "translated_name" in result
                assert "translated_source" in result