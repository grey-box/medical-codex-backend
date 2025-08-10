"""
Test Configuration and Utilities Module.

This module provides configuration and utility functions for running
the non-regression test suite. It includes test setup, configuration
management, and helper utilities.
"""

import os
import sys
import pytest
from typing import Dict, Any, List
from pathlib import Path

# Add the parent directory to the Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConfig:
    """Configuration class for test settings."""
    
    # Test environment settings
    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
    TEST_MODE = os.getenv("TEST_MODE", "unit")
    
    # API test settings
    BASE_URL = "http://localhost:8080"
    API_TIMEOUT = 30  # seconds
    
    # Test data settings
    MAX_TEST_RESULTS = 10
    DEFAULT_MAX_DISTANCE = 5
    DEFAULT_MAX_RESULTS = 5
    
    # Performance test settings
    CONCURRENT_REQUESTS = 10
    PERFORMANCE_THRESHOLD = 30  # seconds
    
    # Security test settings
    ENABLE_SECURITY_TESTS = True
    ENABLE_INJECTION_TESTS = True
    
    # Language settings for testing
    TEST_LANGUAGES = ["en", "fr", "uk", "ru"]
    
    @classmethod
    def get_test_settings(cls) -> Dict[str, Any]:
        """Get all test settings as a dictionary."""
        return {
            "TEST_DATABASE_URL": cls.TEST_DATABASE_URL,
            "TEST_MODE": cls.TEST_MODE,
            "BASE_URL": cls.BASE_URL,
            "API_TIMEOUT": cls.API_TIMEOUT,
            "MAX_TEST_RESULTS": cls.MAX_TEST_RESULTS,
            "DEFAULT_MAX_DISTANCE": cls.DEFAULT_MAX_DISTANCE,
            "DEFAULT_MAX_RESULTS": cls.DEFAULT_MAX_RESULTS,
            "CONCURRENT_REQUESTS": cls.CONCURRENT_REQUESTS,
            "PERFORMANCE_THRESHOLD": cls.PERFORMANCE_THRESHOLD,
            "ENABLE_SECURITY_TESTS": cls.ENABLE_SECURITY_TESTS,
            "ENABLE_INJECTION_TESTS": cls.ENABLE_INJECTION_TESTS,
            "TEST_LANGUAGES": cls.TEST_LANGUAGES
        }


class TestMarkers:
    """Pytest markers for test categorization."""
    
    UNIT = pytest.mark.unit
    INTEGRATION = pytest.mark.integration
    PERFORMANCE = pytest.mark.performance
    SECURITY = pytest.mark.security
    SMOKE = pytest.mark.smoke
    REGRESSION = pytest.mark.regression


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "security: marks tests as security tests"
    )
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add smoke marker to basic functionality tests
        if "basic" in item.name.lower() or "simple" in item.name.lower():
            item.add_marker(TestMarkers.SMOKE)
        
        # Add unit marker to tests that don't require external dependencies
        if "test_endpoint" in item.name.lower() or "test_" in item.name.lower():
            item.add_marker(TestMarkers.UNIT)
        
        # Add security marker to security-related tests
        if "security" in item.name.lower() or "injection" in item.name.lower():
            item.add_marker(TestMarkers.SECURITY)
        
        # Add performance marker to performance-related tests
        if "performance" in item.name.lower() or "concurrent" in item.name.lower():
            item.add_marker(TestMarkers.PERFORMANCE)


class TestDataManager:
    """Data management utilities for testing."""
    
    @staticmethod
    def get_test_query_params(language: str = "en", query: str = "test") -> Dict[str, Any]:
        """Get standard test query parameters."""
        return {
            "source_language": language,
            "query": query,
            "target_language": "fr",
            "max_distance": TestConfig.DEFAULT_MAX_DISTANCE,
            "max_results": TestConfig.DEFAULT_MAX_RESULTS
        }
    
    @staticmethod
    def get_test_translation_query(fuzzy_result: Dict[str, Any], target_language: str = "fr") -> Dict[str, Any]:
        """Get standard test translation query."""
        return {
            "translation_query": fuzzy_result,
            "target_language": target_language
        }
    
    @staticmethod
    def generate_test_data_scenarios() -> List[Dict[str, Any]]:
        """Generate test data scenarios for different languages."""
        scenarios = []
        
        # Test scenarios for different language pairs
        language_pairs = [
            ("en", "fr"),
            ("fr", "en"),
            ("en", "uk"),
            ("uk", "en"),
            ("en", "ru"),
            ("ru", "en")
        ]
        
        for source_lang, target_lang in language_pairs:
            scenarios.append({
                "name": f"{source_lang}_to_{target_lang}",
                "source_language": source_lang,
                "target_language": target_lang,
                "test_queries": [
                    "test",
                    "medicine",
                    "pain",
                    "inflammation"
                ]
            })
        
        return scenarios
    
    @staticmethod
    def get_edge_case_scenarios() -> List[Dict[str, Any]]:
        """Get edge case scenarios for testing."""
        return [
            {
                "name": "empty_query",
                "query": "",
                "expected_behavior": "should_handle_gracefully"
            },
            {
                "name": "very_long_query",
                "query": "a" * 1000,
                "expected_behavior": "should_handle_gracefully"
            },
            {
                "name": "special_characters",
                "query": "test@#$%^&*()",
                "expected_behavior": "should_handle_gracefully"
            },
            {
                "name": "unicode_characters",
                "query": "café",
                "expected_behavior": "should_handle_gracefully"
            },
            {
                "name": "numeric_query",
                "query": "12345",
                "expected_behavior": "should_handle_gracefully"
            }
        ]


class TestValidator:
    """Validation utilities for test results."""
    
    @staticmethod
    def validate_fuzzy_result(result: Dict[str, Any]) -> bool:
        """Validate fuzzy matching result structure."""
        required_fields = [
            "matching_name", "matching_source", "matching_algorithm",
            "matching_uid", "matching_row_number", "distance"
        ]
        
        for field in required_fields:
            if field not in result:
                return False
        
        # Validate field types
        if not isinstance(result["matching_name"], str):
            return False
        if not isinstance(result["matching_source"], str):
            return False
        if not isinstance(result["matching_algorithm"], str):
            return False
        if not isinstance(result["matching_uid"], int):
            return False
        if not isinstance(result["matching_row_number"], int):
            return False
        if result["distance"] is not None and not isinstance(result["distance"], int):
            return False
        
        return True
    
    @staticmethod
    def validate_translation_result(result: Dict[str, Any]) -> bool:
        """Validate translation result structure."""
        required_fields = [
            "translated_name", "translated_source", "translated_uid",
            "source_term", "source_language", "target_language",
            "confidence", "alternatives", "additionalDetails"
        ]
        
        for field in required_fields:
            if field not in result:
                return False
        
        # Validate field types
        if not isinstance(result["translated_name"], str):
            return False
        if not isinstance(result["translated_source"], str):
            return False
        if not isinstance(result["translated_uid"], int):
            return False
        if not isinstance(result["source_term"], str):
            return False
        if not isinstance(result["source_language"], str):
            return False
        if not isinstance(result["target_language"], str):
            return False
        if result["confidence"] is not None and not isinstance(result["confidence"], (int, float)):
            return False
        if not isinstance(result["alternatives"], list):
            return False
        if result["additionalDetails"] is not None and not isinstance(result["additionalDetails"], dict):
            return False
        
        return True
    
    @staticmethod
    def validate_language_result(result: Dict[str, Any]) -> bool:
        """Validate language result structure."""
        if "source_language" not in result or "target_languages" not in result:
            return False
        
        if not isinstance(result["source_language"], str):
            return False
        
        if not isinstance(result["target_languages"], list):
            return False
        
        for lang in result["target_languages"]:
            if not isinstance(lang, str):
                return False
        
        return True


class TestReporter:
    """Test reporting utilities."""
    
    @staticmethod
    def generate_test_summary(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of test results."""
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result["status"] == "passed")
        failed_tests = sum(1 for result in test_results if result["status"] == "failed")
        skipped_tests = sum(1 for result in test_results if result["status"] == "skipped")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "skipped_tests": skipped_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "test_results": test_results
        }
    
    @staticmethod
    def format_test_result(result: Dict[str, Any]) -> str:
        """Format a test result for display."""
        status = result["status"].upper()
        name = result["name"]
        duration = result.get("duration", 0)
        
        return f"[{status}] {name} ({duration:.2f}s)"
    
    @staticmethod
    def print_test_summary(summary: Dict[str, Any]):
        """Print a formatted test summary."""
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Skipped: {summary['skipped_tests']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print("="*50)


class TestEnvironment:
    """Test environment management utilities."""
    
    @staticmethod
    def setup_test_environment():
        """Set up the test environment."""
        # Set environment variables for testing
        os.environ["TEST_MODE"] = "true"
        os.environ["LOG_LEVEL"] = "ERROR"
        
        # Create test directories if they don't exist
        test_dirs = ["test_data", "test_logs", "test_reports"]
        for dir_name in test_dirs:
            Path(dir_name).mkdir(exist_ok=True)
    
    @staticmethod
    def cleanup_test_environment():
        """Clean up the test environment."""
        # Remove test files
        test_files = ["test.db", "test.log"]
        for file_name in test_files:
            if os.path.exists(file_name):
                os.remove(file_name)
        
        # Clean up test directories
        test_dirs = ["test_data", "test_logs", "test_reports"]
        for dir_name in test_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                for file in dir_path.glob("*"):
                    if file.is_file():
                        file.unlink()
                # Remove directory if empty
                try:
                    dir_path.rmdir()
                except OSError:
                    pass
    
    @staticmethod
    def get_test_database_url() -> str:
        """Get the test database URL."""
        return TestConfig.TEST_DATABASE_URL
    
    @staticmethod
    def is_test_environment() -> bool:
        """Check if running in test environment."""
        return os.getenv("TEST_MODE", "false").lower() == "true"


# Test configuration constants
TEST_CONFIG = TestConfig.get_test_settings()

# Test data manager
TEST_DATA = TestDataManager()

# Test validator
VALIDATOR = TestValidator()

# Test reporter
REPORTER = TestReporter()

# Test environment
ENVIRONMENT = TestEnvironment()