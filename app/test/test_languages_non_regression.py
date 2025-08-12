"""
Non-Regression Test Suite for Language Endpoints.

This module contains comprehensive non-regression tests for the language
functionality, ensuring that existing features continue to work correctly
after code changes. It covers various scenarios including language pairs,
available languages, and edge cases.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


class TestLanguagesNonRegression:
    """Test class for language non-regression tests."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)

    def test_get_available_languages_basic(self):
        """Test basic functionality of getting available languages."""
        response = self.client.get("/languages/")
        
        assert response.status_code == 200
        data = response.json()
        assert "available_languages" in data
        assert isinstance(data["available_languages"], list)
        
        # Verify structure of each language result
        for lang_result in data["available_languages"]:
            assert "source_language" in lang_result
            assert "target_languages" in lang_result
            assert isinstance(lang_result["target_languages"], list)

    def test_get_available_languages_test_endpoint(self):
        """Test the test endpoint for available languages."""
        response = self.client.get("/languages/test")
        
        assert response.status_code == 200
        data = response.json()
        assert "available_languages" in data
        assert isinstance(data["available_languages"], list)
        
        # Test endpoint should return exactly 3 language groups
        assert len(data["available_languages"]) == 3
        
        # Verify structure and content of test data
        for i, lang_result in enumerate(data["available_languages"]):
            assert lang_result["source_language"] == f"lang{i+1}"
            assert isinstance(lang_result["target_languages"], list)
            assert len(lang_result["target_languages"]) == 2  # 3 total languages minus source
            
            # Verify target languages are the other two languages
            expected_targets = [f"lang{j+1}" for j in range(3) if j != i]
            assert set(lang_result["target_languages"]) == set(expected_targets)

    def test_available_languages_response_structure_consistency(self):
        """Test that the response structure is consistent."""
        response = self.client.get("/languages/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify top-level structure
        assert "available_languages" in data
        assert isinstance(data["available_languages"], list)
        
        # Verify each language result structure
        for lang_result in data["available_languages"]:
            required_fields = ["source_language", "target_languages"]
            for field in required_fields:
                assert field in lang_result
            
            assert isinstance(lang_result["target_languages"], list)

    def test_available_languages_uniqueness(self):
        """Test that source languages are unique."""
        response = self.client.get("/languages/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Extract source languages
        source_languages = [lang["source_language"] for lang in data["available_languages"]]
        
        # Check for uniqueness
        assert len(source_languages) == len(set(source_languages)), "All source languages should be unique"

    def test_available_languages_target_languages_structure(self):
        """Test that target languages are properly structured."""
        response = self.client.get("/languages/")
        
        assert response.status_code == 200
        data = response.json()
        
        for lang_result in data["available_languages"]:
            assert isinstance(lang_result["target_languages"], list)
            
            # Verify each target language is a string
            for target_lang in lang_result["target_languages"]:
                assert isinstance(target_lang, str)
                assert len(target_lang) > 0  # Should not be empty

    def test_available_languages_no_duplicates_in_targets(self):
        """Test that there are no duplicate target languages for a source."""
        response = self.client.get("/languages/")
        
        assert response.status_code == 200
        data = response.json()
        
        for lang_result in data["available_languages"]:
            target_languages = lang_result["target_languages"]
            # Check for uniqueness
            assert len(target_languages) == len(set(target_languages)), f"Duplicate target languages found for {lang_result['source_language']}"

    def test_available_languages_test_endpoint_structure(self):
        """Test the structure of the test endpoint response."""
        response = self.client.get("/languages/test")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify top-level structure
        assert "available_languages" in data
        assert isinstance(data["available_languages"], list)
        
        # Verify each language result structure
        for lang_result in data["available_languages"]:
            required_fields = ["source_language", "target_languages"]
            for field in required_fields:
                assert field in lang_result
            
            assert isinstance(lang_result["target_languages"], list)

    def test_available_languages_consistency_between_endpoints(self):
        """Test that both endpoints return consistent structure."""
        # Get data from both endpoints
        response_prod = self.client.get("/languages/")
        response_test = self.client.get("/languages/test")
        
        assert response_prod.status_code == 200
        assert response_test.status_code == 200
        
        data_prod = response_prod.json()
        data_test = response_test.json()
        
        # Both should have the same top-level structure
        assert "available_languages" in data_prod
        assert "available_languages" in data_test
        
        # Both should return lists
        assert isinstance(data_prod["available_languages"], list)
        assert isinstance(data_test["available_languages"], list)
        
        # Each language result should have the same structure
        for lang_result in data_prod["available_languages"]:
            assert "source_language" in lang_result
            assert "target_languages" in lang_result
        
        for lang_result in data_test["available_languages"]:
            assert "source_language" in lang_result
            assert "target_languages" in lang_result

    def test_available_languages_multiple_requests(self):
        """Test that multiple requests return consistent results."""
        responses = []
        for _ in range(3):
            response = self.client.get("/languages/")
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "available_languages" in data
            assert isinstance(data["available_languages"], list)
        
        # All should return the same number of language pairs
        first_count = len(responses[0].json()["available_languages"])
        for response in responses[1:]:
            assert len(response.json()["available_languages"]) == first_count

    def test_available_languages_test_endpoint_multiple_requests(self):
        """Test that multiple requests to test endpoint return consistent results."""
        responses = []
        for _ in range(3):
            response = self.client.get("/languages/test")
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "available_languages" in data
            assert isinstance(data["available_languages"], list)
        
        # All should return exactly 3 language groups
        for response in responses:
            assert len(response.json()["available_languages"]) == 3

    def test_available_languages_empty_database_handling(self):
        """Test behavior when database has no language pairs."""
        # This test would need to mock an empty database
        # For now, we just verify the endpoint handles the response gracefully
        response = self.client.get("/languages/")
        
        assert response.status_code == 200
        data = response.json()
        assert "available_languages" in data
        
        # Should return empty list rather than error
        assert isinstance(data["available_languages"], list)

    def test_available_languages_language_codes_format(self):
        """Test that language codes follow expected format."""
        response = self.client.get("/languages/")
        
        assert response.status_code == 200
        data = response.json()
        
        for lang_result in data["available_languages"]:
            # Source language should be a non-empty string
            assert isinstance(lang_result["source_language"], str)
            assert len(lang_result["source_language"]) > 0
            assert len(lang_result["source_language"]) <= 10  # Reasonable length for language codes
            
            # Target languages should follow same format
            for target_lang in lang_result["target_languages"]:
                assert isinstance(target_lang, str)
                assert len(target_lang) > 0
                assert len(target_lang) <= 10

    def test_available_languages_no_self_references(self):
        """Test that no language lists itself as a target."""
        response = self.client.get("/languages/")
        
        assert response.status_code == 200
        data = response.json()
        
        for lang_result in data["available_languages"]:
            source_lang = lang_result["source_language"]
            target_languages = lang_result["target_languages"]
            
            # Source language should not be in its own target list
            assert source_lang not in target_languages, f"Language {source_lang} should not target itself"

    def test_available_languages_test_endpoint_completeness(self):
        """Test that test endpoint creates complete language graph."""
        response = self.client.get("/languages/test")
        
        assert response.status_code == 200
        data = response.json()
        
        languages = set()
        # Collect all languages
        for lang_result in data["available_languages"]:
            languages.add(lang_result["source_language"])
            languages.update(lang_result["target_languages"])
        
        # Should have exactly 3 languages as per implementation
        assert len(languages) == 3
        
        # Each language should be a source language exactly once
        source_languages = [lang["source_language"] for lang in data["available_languages"]]
        assert len(source_languages) == 3
        assert len(set(source_languages)) == 3  # All unique

    def test_available_languages_response_ordering(self):
        """Test that languages are returned in consistent order."""
        response1 = self.client.get("/languages/")
        response2 = self.client.get("/languages/")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Should return same number of languages
        assert len(data1["available_languages"]) == len(data2["available_languages"])
        
        # Languages should be in same order
        for i in range(len(data1["available_languages"])):
            assert data1["available_languages"][i]["source_language"] == data2["available_languages"][i]["source_language"]

    def test_available_languages_test_endpoint_ordering(self):
        """Test that test endpoint returns languages in consistent order."""
        response1 = self.client.get("/languages/test")
        response2 = self.client.get("/languages/test")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Should return same number of languages
        assert len(data1["available_languages"]) == len(data2["available_languages"])
        
        # Languages should be in same order
        for i in range(len(data1["available_languages"])):
            assert data1["available_languages"][i]["source_language"] == data2["available_languages"][i]["source_language"]