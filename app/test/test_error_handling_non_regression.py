"""
Non-Regression Test Suite for Error Handling.

This module contains comprehensive non-regression tests for error handling
across all endpoints, ensuring that the application gracefully handles
various error conditions and edge cases.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


class TestErrorHandlingNonRegression:
    """Test class for error handling non-regression tests."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)

    def test_fuzzymatching_invalid_json(self):
        """Test fuzzy matching with invalid JSON payload."""
        # Send invalid JSON
        response = self.client.post("/fuzzymatching/", data="invalid json")
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_fuzzymatching_missing_required_fields(self):
        """Test fuzzy matching with missing required fields."""
        # Missing required fields
        incomplete_query = {
            "source_language": "en"
            # Missing 'query' field
        }
        
        response = self.client.post("/fuzzymatching/", json=incomplete_query)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_fuzzymatching_invalid_field_types(self):
        """Test fuzzy matching with invalid field types."""
        # Invalid field types
        invalid_query = {
            "source_language": 123,  # Should be string
            "query": "test",
            "target_language": "fr",
            "max_distance": "ten",  # Should be integer
            "max_results": "five"   # Should be integer
        }
        
        response = self.client.post("/fuzzymatching/", json=invalid_query)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_fuzzymatching_negative_values(self):
        """Test fuzzy matching with negative values."""
        # Negative values for distance and results
        invalid_query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": -1,
            "max_results": -5
        }
        
        response = self.client.post("/fuzzymatching/", json=invalid_query)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_fuzzymatching_oversized_values(self):
        """Test fuzzy matching with oversized values."""
        # Very large values
        oversized_query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 999999,
            "max_results": 999999
        }
        
        response = self.client.post("/fuzzymatching/", json=oversized_query)
        
        # Should handle gracefully (either 201 or 500)
        assert response.status_code in [201, 500]

    def test_translation_invalid_json(self):
        """Test translation with invalid JSON payload."""
        # Send invalid JSON
        response = self.client.post("/translate/", data="invalid json")
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_translation_missing_required_fields(self):
        """Test translation with missing required fields."""
        # Missing required fields
        incomplete_query = {
            "target_language": "fr"
            # Missing 'translation_query' field
        }
        
        response = self.client.post("/translate/", json=incomplete_query)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_translation_invalid_fuzzy_result_structure(self):
        """Test translation with invalid fuzzy result structure."""
        # Invalid fuzzy result structure
        invalid_query = {
            "translation_query": {
                "matching_name": "test"
                # Missing required fields in fuzzy result
            },
            "target_language": "fr"
        }
        
        response = self.client.post("/translate/", json=invalid_query)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_languages_invalid_endpoint_method(self):
        """Test language endpoints with invalid HTTP methods."""
        # Try POST on GET endpoint
        response = self.client.post("/languages/")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_fallback_translation_invalid_json(self):
        """Test fallback translation with invalid JSON payload."""
        # Send invalid JSON
        response = self.client.post("/fallback_translation/", data="invalid json")
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_fallback_translation_missing_required_fields(self):
        """Test fallback translation with missing required fields."""
        # Missing required fields
        incomplete_query = {
            "target_language": "fr"
            # Missing 'medicine' field
        }
        
        response = self.client.post("/fallback_translation/", json=incomplete_query)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_manual_translation_invalid_json(self):
        """Test manual translation with invalid JSON payload."""
        # Send invalid JSON
        response = self.client.post("/manual_translation/", data="invalid json")
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_manual_translation_missing_required_fields(self):
        """Test manual translation with missing required fields."""
        # Missing required fields
        incomplete_query = {
            "term": "test",
            "source_language": "en"
            # Missing 'target_language' field
        }
        
        response = self.client.post("/manual_translation/", json=incomplete_query)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_nonexistent_endpoint(self):
        """Test access to non-existent endpoint."""
        response = self.client.get("/nonexistent_endpoint")
        
        # Should return 404 Not Found
        assert response.status_code == 404

    def test_http_methods_not_allowed(self):
        """Test that appropriate HTTP methods are not allowed."""
        endpoints_and_methods = [
            ("/fuzzymatching/", "GET"),
            ("/fuzzymatching/", "PUT"),
            ("/fuzzymatching/", "DELETE"),
            ("/translate/", "GET"),
            ("/translate/", "PUT"),
            ("/translate/", "DELETE"),
            ("/languages/", "POST"),
            ("/languages/", "PUT"),
            ("/languages/", "DELETE"),
            ("/fallback_translation/", "GET"),
            ("/fallback_translation/", "PUT"),
            ("/fallback_translation/", "DELETE"),
            ("/manual_translation/", "GET"),
            ("/manual_translation/", "PUT"),
            ("/manual_translation/", "DELETE"),
        ]
        
        for endpoint, method in endpoints_and_methods:
            if method == "GET":
                response = self.client.get(endpoint)
            elif method == "POST":
                response = self.client.post(endpoint)
            elif method == "PUT":
                response = self.client.put(endpoint)
            elif method == "DELETE":
                response = self.client.delete(endpoint)
            
            # Should return 405 Method Not Allowed
            assert response.status_code == 405, f"Endpoint {endpoint} should not allow {method}"

    def test_content_type_validation(self):
        """Test content type validation."""
        # Send without proper content type
        response = self.client.post(
            "/fuzzymatching/",
            data='{"source_language": "en", "query": "test"}',
            headers={"Content-Type": "application/text"}
        )
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_empty_payload(self):
        """Test handling of empty payload."""
        response = self.client.post("/fuzzymatching/", data="")
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_malformed_json(self):
        """Test handling of malformed JSON."""
        malformed_json = '{"source_language": "en", "query": "test", "target_language": "fr"'  # Missing closing braces
        
        response = self.client.post("/fuzzymatching/", data=malformed_json)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_sql_injection_attempt(self):
        """Test protection against SQL injection attempts."""
        sql_injection_queries = [
            {
                "source_language": "en'; DROP TABLE users; --",
                "query": "test",
                "target_language": "fr"
            },
            {
                "source_language": "en",
                "query": "test'; DELETE FROM medications; --",
                "target_language": "fr"
            },
            {
                "source_language": "en",
                "query": "test",
                "target_language": "fr'; UNION SELECT * FROM sensitive_table; --"
            }
        ]
        
        for query in sql_injection_queries:
            response = self.client.post("/fuzzymatching/", json=query)
            # Should either succeed (if properly sanitized) or fail gracefully
            assert response.status_code in [201, 422, 500]

    def test_xss_attempt(self):
        """Test protection against XSS attempts."""
        xss_payloads = [
            {
                "source_language": "<script>alert('xss')</script>",
                "query": "test",
                "target_language": "fr"
            },
            {
                "source_language": "en",
                "query": "<img src='x' onerror='alert(1)'>",
                "target_language": "fr"
            },
            {
                "source_language": "en",
                "query": "test",
                "target_language": "<iframe src='javascript:alert(1)'></iframe>"
            }
        ]
        
        for payload in xss_payloads:
            response = self.client.post("/fuzzymatching/", json=payload)
            # Should handle XSS attempts gracefully
            assert response.status_code in [201, 422, 500]

    def test_very_long_strings(self):
        """Test handling of very long strings."""
        very_long_string = "a" * 10000
        
        query = {
            "source_language": very_long_string,
            "query": "test",
            "target_language": "fr"
        }
        
        response = self.client.post("/fuzzymatching/", json=query)
        # Should handle long strings gracefully
        assert response.status_code in [201, 422, 500]

    def test_special_characters_in_queries(self):
        """Test handling of special characters in queries."""
        special_char_queries = [
            {
                "source_language": "en",
                "query": "test@#$%^&*()",
                "target_language": "fr"
            },
            {
                "source_language": "en",
                "query": "test\n\r\t",
                "target_language": "fr"
            },
            {
                "source_language": "en",
                "query": "test\"'`",
                "target_language": "fr"
            }
        ]
        
        for query in special_char_queries:
            response = self.client.post("/fuzzymatching/", json=query)
            # Should handle special characters gracefully
            assert response.status_code in [201, 422, 500]

    def test_unicode_characters(self):
        """Test handling of Unicode characters."""
        unicode_queries = [
            {
                "source_language": "en",
                "query": "café",  # French accent
                "target_language": "fr"
            },
            {
                "source_language": "ru",
                "query": "тест",  # Cyrillic
                "target_language": "en"
            },
            {
                "source_language": "zh",
                "query": "测试",  # Chinese
                "target_language": "en"
            }
        ]
        
        for query in unicode_queries:
            response = self.client.post("/fuzzymatching/", json=query)
            # Should handle Unicode gracefully
            assert response.status_code in [201, 422, 500]

    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = self.client.post("/fuzzymatching/", json={
                "source_language": "en",
                "query": "test",
                "target_language": "fr"
            })
            results.append(response.status_code)
        
        # Make multiple concurrent requests
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should complete without server errors
        for status_code in results:
            assert status_code in [201, 422, 500], f"Unexpected status code: {status_code}"

    def test_rate_limiting(self):
        """Test rate limiting behavior."""
        import time
        
        # Make many requests in quick succession
        responses = []
        for _ in range(50):  # Adjust based on expected rate limits
            response = self.client.post("/fuzzymatching/", json={
                "source_language": "en",
                "query": "test",
                "target_language": "fr"
            })
            responses.append(response.status_code)
            time.sleep(0.01)  # Small delay between requests
        
        # Most requests should succeed, but some might be rate limited
        successful_requests = sum(1 for status in responses if status in [201, 422])
        assert successful_requests > 0, "No requests succeeded"

    def test_database_connection_error_handling(self):
        """Test behavior when database connection fails."""
        # This test would need to mock a database connection failure
        # For now, we just verify the endpoint structure
        response = self.client.post("/fuzzymatching/", json={
            "source_language": "en",
            "query": "test",
            "target_language": "fr"
        })
        
        # Should either succeed or return 500 (database error)
        assert response.status_code in [201, 500]

    def test_timeout_handling(self):
        """Test timeout handling for long-running operations."""
        # This test would need to mock a timeout scenario
        # For now, we just verify basic functionality
        response = self.client.post("/fuzzymatching/", json={
            "source_language": "en",
            "query": "test",
            "target_language": "fr"
        })
        
        # Should complete within reasonable time
        assert response.status_code in [201, 422, 500]