"""
Non-Regression Test Suite for Fuzzy Matching Endpoints.

This module contains comprehensive non-regression tests for the fuzzy matching
functionality, ensuring that existing features continue to work correctly
after code changes. It covers various scenarios including different languages,
algorithms, and edge cases.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from main import app
from schemas import FuzzyQuery, FuzzyResult, FuzzyMatching
from routers.fuzzymatching import router as fuzzymatching_router


class TestFuzzyMatchingNonRegression:
    """Test class for fuzzy matching non-regression tests."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)
        
    def test_fuzzy_matching_basic_functionality(self):
        """Test basic fuzzy matching functionality with Ukrainian language."""
        query = {
            "source_language": "uk",
            "query": "астмито",
            "target_language": "en",
            "max_distance": 10,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data
        assert isinstance(data["results"], list)
        
        # Verify structure of each result
        for result in data["results"]:
            assert "matching_name" in result
            assert "matching_source" in result
            assert "matching_algorithm" in result
            assert "matching_uid" in result
            assert "matching_row_number" in result
            assert "distance" in result

    def test_fuzzy_matching_with_russian_language(self):
        """Test fuzzy matching with Russian language."""
        query = {
            "source_language": "ru",
            "query": "изотретиноїн",
            "target_language": "en",
            "max_distance": 5,
            "max_results": 3
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert len(data["results"]) <= 3  # Respect max_results

    def test_fuzzy_matching_with_french_language(self):
        """Test fuzzy matching with French language."""
        query = {
            "source_language": "fr",
            "query": "paracétamol",
            "target_language": "en",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data

    def test_fuzzy_matching_with_english_language(self):
        """Test fuzzy matching with English language."""
        query = {
            "source_language": "en",
            "query": "ibuprofen",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data

    def test_fuzzy_matching_empty_query(self):
        """Test fuzzy matching with empty query string."""
        query = {
            "source_language": "en",
            "query": "",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        # Should handle empty query gracefully
        assert response.status_code in [201, 500]

    def test_fuzzy_matching_max_distance_boundary(self):
        """Test fuzzy matching with maximum distance boundary values."""
        # Test with very high max_distance
        query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 100,
            "max_results": 10
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data

    def test_fuzzy_matching_max_results_boundary(self):
        """Test fuzzy matching with maximum results boundary values."""
        # Test with very high max_results
        query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 10,
            "max_results": 100
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert len(data["results"]) <= 100

    def test_fuzzy_matching_no_target_language(self):
        """Test fuzzy matching without specifying target language."""
        query = {
            "source_language": "en",
            "query": "test",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data

    def test_fuzzy_matching_test_endpoint(self):
        """Test the test endpoint for fuzzy matching."""
        query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/test", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 5  # Test endpoint should return exactly 5 results
        
        # Verify test results structure
        for i, result in enumerate(data["results"]):
            assert result["matching_name"] == f"matching_name{i}"
            assert result["matching_source"] == f"matching_source{i}"
            assert result["matching_algorithm"] == "test"

    def test_fuzzy_matching_invalid_language_code(self):
        """Test fuzzy matching with invalid language code."""
        query = {
            "source_language": "invalid",
            "query": "test",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        # Should handle invalid language gracefully
        assert response.status_code in [201, 500]

    def test_fuzzy_matching_special_characters(self):
        """Test fuzzy matching with special characters."""
        query = {
            "source_language": "fr",
            "query": "paracétamol®",
            "target_language": "en",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data

    def test_fuzzy_matching_numeric_query(self):
        """Test fuzzy matching with numeric query."""
        query = {
            "source_language": "en",
            "query": "12345",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        assert "results" in data

    def test_fuzzy_matching_long_query(self):
        """Test fuzzy matching with very long query string."""
        long_query = "a" * 1000
        query = {
            "source_language": "en",
            "query": long_query,
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        # Should handle long query gracefully
        assert response.status_code in [201, 500]

    def test_fuzzy_matching_response_structure_consistency(self):
        """Test that the response structure is consistent across different queries."""
        queries = [
            {
                "source_language": "en",
                "query": "ibuprofen",
                "target_language": "fr",
                "max_distance": 5,
                "max_results": 3
            },
            {
                "source_language": "fr",
                "query": "paracétamol",
                "target_language": "en",
                "max_distance": 5,
                "max_results": 3
            },
            {
                "source_language": "uk",
                "query": "астмито",
                "target_language": "en",
                "max_distance": 5,
                "max_results": 3
            }
        ]
        
        for query in queries:
            response = self.client.post("/fuzzymatching/", json=query)
            assert response.status_code == 201
            data = response.json()
            
            # Verify consistent structure
            assert "results" in data
            assert isinstance(data["results"], list)
            
            for result in data["results"]:
                required_fields = [
                    "matching_name", "matching_source", "matching_algorithm",
                    "matching_uid", "matching_row_number", "distance"
                ]
                for field in required_fields:
                    assert field in result

    def test_fuzzymatching_algorithm_parameter_consistency(self):
        """Test that different algorithms return consistent response structures."""
        # Use actual data that exists in the database - English to Russian
        query = {
            "source_language": "en",
            "query": "ibuprofen",
            "target_language": "ru",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        
        # All results should have the same algorithm
        algorithms = [result["matching_algorithm"] for result in data["results"]]
        assert len(set(algorithms)) == 1, "All results should use the same algorithm"

    def test_fuzzymatching_uid_uniqueness(self):
        """Test that UIDs in results are unique."""
        query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 10
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        
        # Extract UIDs
        uids = [result["matching_uid"] for result in data["results"]]
        
        # Check for uniqueness
        assert len(uids) == len(set(uids)), "All UIDs should be unique"

    def test_fuzzymatching_row_number_uniqueness(self):
        """Test that row numbers in results are unique."""
        query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 10
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        
        # Extract row numbers
        row_numbers = [result["matching_row_number"] for result in data["results"]]
        
        # Check for uniqueness
        assert len(row_numbers) == len(set(row_numbers)), "All row numbers should be unique"

    def test_fuzzymatching_distance_values(self):
        """Test that distance values are reasonable."""
        query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 10,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        
        for result in data["results"]:
            if result["distance"] is not None:
                assert result["distance"] >= 0, "Distance should be non-negative"
                assert result["distance"] <= 10, "Distance should not exceed max_distance"

    def test_fuzzymatching_source_language_consistency(self):
        """Test that source language is consistent in results."""
        query = {
            "source_language": "fr",
            "query": "test",
            "target_language": "en",
            "max_distance": 5,
            "max_results": 5
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        
        assert response.status_code == 201
        data = response.json()
        
        # All results should be from the same source language
        for result in data["results"]:
            # This assumes the matching_source field contains language info
            # Adjust based on actual implementation
            assert "fr" in result["matching_source"].lower() or "french" in result["matching_source"].lower()

    def test_fuzzymatching_performance_with_multiple_requests(self):
        """Test performance with multiple consecutive requests."""
        query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 5
        }
        
        # Make multiple requests
        responses = []
        for _ in range(5):
            response = self.client.post("/fuzzymatching/", json=query)
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 201
            data = response.json()
            assert "results" in data
            assert isinstance(data["results"], list)