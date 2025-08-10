"""
Test Package Initialization.

This module initializes the test package and provides common utilities
for running the non-regression test suite.
"""

# Import test configuration
from .test_config import (
    TestConfig,
    TestMarkers,
    TestDataManager,
    TestValidator,
    TestReporter,
    TestEnvironment,
    TEST_CONFIG,
    VALIDATOR,
    REPORTER,
    ENVIRONMENT
)

# Import test fixtures
from .test_fixtures import (
    MockDatabase,
    mock_database,
    sample_fuzzy_queries,
    sample_translation_queries,
    sample_language_data,
    sample_fuzzy_results,
    sample_translation_results,
    edge_case_queries,
    invalid_queries,
    performance_test_data,
    mock_database_session,
    mock_fastapi_app,
    generate_test_fuzzy_result,
    generate_test_translation_result,
    generate_test_language_pairs,
    assert_fuzzy_result_structure,
    assert_translation_result_structure,
    assert_language_result_structure
)

# Import test modules
from . import test_fuzzymatching_non_regression
from . import test_translation_non_regression
from . import test_languages_non_regression
from . import test_error_handling_non_regression
from . import test_integration_non_regression

__version__ = "1.0.0"
__author__ = "Medical Codex Team"

# Test package metadata
TEST_PACKAGE_INFO = {
    "name": "medical-codex-backend-tests",
    "version": __version__,
    "description": "Non-regression test suite for Medical Codex Backend",
    "author": __author__,
    "test_modules": [
        "test_fuzzymatching_non_regression",
        "test_translation_non_regression", 
        "test_languages_non_regression",
        "test_error_handling_non_regression",
        "test_integration_non_regression"
    ],
    "supported_languages": ["en", "fr", "uk", "ru"],
    "test_types": [
        "unit",
        "integration", 
        "performance",
        "security",
        "smoke",
        "regression"
    ]
}

# Export all test classes and functions for easy access
__all__ = [
    # Configuration
    "TestConfig",
    "TestMarkers", 
    "TEST_CONFIG",
    "VALIDATOR",
    "REPORTER",
    "ENVIRONMENT",
    
    # Fixtures
    "MockDatabase",
    "mock_database",
    "sample_fuzzy_queries",
    "sample_translation_queries", 
    "sample_language_data",
    "sample_fuzzy_results",
    "sample_translation_results",
    "edge_case_queries",
    "invalid_queries",
    "performance_test_data",
    "mock_database_session",
    "mock_fastapi_app",
    "generate_test_fuzzy_result",
    "generate_test_translation_result",
    "generate_test_language_pairs",
    "assert_fuzzy_result_structure",
    "assert_translation_result_structure",
    "assert_language_result_structure",
    
    # Test modules
    "test_fuzzymatching_non_regression",
    "test_translation_non_regression",
    "test_languages_non_regression", 
    "test_error_handling_non_regression",
    "test_integration_non_regression",
    
    # Metadata
    "TEST_PACKAGE_INFO"
]


def run_test_suite():
    """
    Run the complete test suite.
    
    This function provides a convenient way to run all tests in the suite
    with proper configuration and reporting.
    """
    import pytest
    
    # Set up test environment
    ENVIRONMENT.setup_test_environment()
    
    try:
        # Configure pytest
        pytest_args = [
            "-v",  # verbose output
            "--tb=short",  # short traceback format
            "--strict-markers",  # strict marker handling
            "--disable-warnings",  # disable warnings
            "--color=yes",  # colored output
            "."  # current directory (tests are in app/test)
        ]
        
        # Add markers if specified
        if TestConfig.TEST_MODE == "integration":
            pytest_args.extend(["-m", "integration"])
        elif TestConfig.TEST_MODE == "unit":
            pytest_args.extend(["-m", "unit"])
        elif TestConfig.TEST_MODE == "performance":
            pytest_args.extend(["-m", "performance"])
        
        # Run tests
        exit_code = pytest.main(pytest_args)
        
        return exit_code
        
    finally:
        # Clean up test environment
        ENVIRONMENT.cleanup_test_environment()


def run_specific_test(test_name: str, test_type: str = "all"):
    """
    Run a specific test or test category.
    
    Args:
        test_name (str): Name of the test or test module to run
        test_type (str): Type of test to run (unit, integration, performance, etc.)
    
    Returns:
        int: Pytest exit code
    """
    import pytest
    
    # Set up test environment
    ENVIRONMENT.setup_test_environment()
    
    try:
        # Configure pytest
        pytest_args = [
            "-v",
            "--tb=short",
            "--strict-markers",
            "--disable-warnings",
            "--color=yes",
            f"./{test_name}.py"
        ]
        
        # Add marker filter if specified
        if test_type != "all":
            pytest_args.extend(["-m", test_type])
        
        # Run tests
        exit_code = pytest.main(pytest_args)
        
        return exit_code
        
    finally:
        # Clean up test environment
        ENVIRONMENT.cleanup_test_environment()


def generate_test_report():
    """
    Generate a comprehensive test report.
    
    Returns:
        dict: Test report summary
    """
    # This would typically integrate with a reporting framework
    # For now, return basic package info
    return {
        "package_info": TEST_PACKAGE_INFO,
        "configuration": TEST_CONFIG,
        "test_status": "ready"
    }


def validate_test_environment():
    """
    Validate that the test environment is properly configured.
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
    try:
        # Check if required modules are available
        import fastapi
        import sqlalchemy
        import pytest
        
        # Check test configuration
        if not TestConfig.TEST_DATABASE_URL:
            print("Warning: TEST_DATABASE_URL not set")
            return False
        
        # Check if test directories exist
        from pathlib import Path
        test_dirs = ["test_data", "test_logs", "test_reports"]
        for dir_name in test_dirs:
            if not Path(dir_name).exists():
                print(f"Warning: Test directory {dir_name} does not exist")
                return False
        
        return True
        
    except ImportError as e:
        print(f"Missing required module: {e}")
        return False
    except Exception as e:
        print(f"Environment validation failed: {e}")
        return False


# Initialize test environment on import
ENVIRONMENT.setup_test_environment()

# Validate environment on import
if not validate_test_environment():
    print("Warning: Test environment validation failed")

print(f"Medical Codex Backend Test Suite v{__version__}")
print(f"Supported languages: {', '.join(TEST_PACKAGE_INFO['supported_languages'])}")
print(f"Test modules: {len(TEST_PACKAGE_INFO['test_modules'])}")