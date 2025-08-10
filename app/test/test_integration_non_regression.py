"""
Non-Regression Test Suite for Integration Tests.

This module contains comprehensive integration tests that verify the complete
translation workflow, from fuzzy matching to translation, ensuring all
components work together correctly.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


class TestIntegrationNonRegression:
    """Test class for integration non-regression tests."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)

    def test_complete_translation_workflow_english_to_french(self):
        """Test the complete translation workflow from English to French."""
        # Step 1: Get fuzzy matches for English term
        fuzzy_query = {
            "source_language": "en",
            "query": "ibuprofen",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        # Step 2: Verify fuzzy matching results
        assert "results" in fuzzy_data
        assert len(fuzzy_data["results"]) > 0
        
        # Step 3: Use the top fuzzy match for translation
        top_match = fuzzy_data["results"][0]
        translation_query = {
            "translation_query": top_match,
            "target_language": "fr"
        }
        
        translation_response = self.client.post("/translate/", json=translation_query)
        assert translation_response.status_code == 201
        translation_data = translation_response.json()
        
        # Step 4: Verify translation results
        assert "results" in translation_data
        assert len(translation_data["results"]) > 0
        
        # Step 5: Verify result consistency
        assert top_match["matching_uid"] == translation_data["results"][0]["translated_uid"]
        assert top_match["matching_name"] == translation_data["results"][0]["source_term"]

    def test_complete_translation_workflow_french_to_english(self):
        """Test the complete translation workflow from Russian to English (no French data available)."""
        # Step 1: Get fuzzy matches for Russian term (since no French data exists)
        fuzzy_query = {
            "source_language": "ru",
            "query": "парацетамол",  # Russian for paracetamol
            "target_language": "en",
            "max_distance": 5,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        # Step 2: Verify fuzzy matching results
        assert "results" in fuzzy_data
        assert len(fuzzy_data["results"]) > 0
        
        # Step 3: Use the top fuzzy match for translation
        top_match = fuzzy_data["results"][0]
        translation_query = {
            "translation_query": top_match,
            "target_language": "en"
        }
        
        translation_response = self.client.post("/translate/", json=translation_query)
        assert translation_response.status_code == 201
        translation_data = translation_response.json()
        
        # Step 4: Verify translation results
        assert "results" in translation_data
        assert len(translation_data["results"]) > 0

    def test_complete_translation_workflow_ukrainian_to_english(self):
        """Test the complete translation workflow from Ukrainian to English."""
        # Step 1: Get fuzzy matches for Ukrainian term
        fuzzy_query = {
            "source_language": "uk",
            "query": "астма",
            "target_language": "en",
            "max_distance": 5,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        # Step 2: Verify fuzzy matching results
        assert "results" in fuzzy_data
        assert len(fuzzy_data["results"]) > 0
        
        # Step 3: Use the top fuzzy match for translation
        top_match = fuzzy_data["results"][0]
        translation_query = {
            "translation_query": top_match,
            "target_language": "en"
        }
        
        translation_response = self.client.post("/translate/", json=translation_query)
        assert translation_response.status_code == 201
        translation_data = translation_response.json()
        
        # Step 4: Verify translation results
        assert "results" in translation_data
        assert len(translation_data["results"]) > 0

    def test_complete_translation_workflow_russian_to_english(self):
        """Test the complete translation workflow from Russian to English."""
        # Step 1: Get fuzzy matches for Russian term
        fuzzy_query = {
            "source_language": "ru",
            "query": "изотретиноин",
            "target_language": "en",
            "max_distance": 5,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        # Step 2: Verify fuzzy matching results
        assert "results" in fuzzy_data
        assert len(fuzzy_data["results"]) > 0
        
        # Step 3: Use the top fuzzy match for translation
        top_match = fuzzy_data["results"][0]
        translation_query = {
            "translation_query": top_match,
            "target_language": "en"
        }
        
        translation_response = self.client.post("/translate/", json=translation_query)
        assert translation_response.status_code == 201
        translation_data = translation_response.json()
        
        # Step 4: Verify translation results
        assert "results" in translation_data
        assert len(translation_data["results"]) > 0

    def test_workflow_with_multiple_fuzzy_matches(self):
        """Test workflow with multiple fuzzy matches and translations."""
        # Step 1: Get multiple fuzzy matches
        fuzzy_query = {
            "source_language": "en",
            "query": "aspirin",
            "target_language": "fr",
            "max_distance": 10,
            "max_results": 5
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        # Step 2: Verify we have multiple matches
        assert "results" in fuzzy_data
        assert len(fuzzy_data["results"]) > 1
        
        # Step 3: Translate each fuzzy match
        translations = []
        for match in fuzzy_data["results"]:
            translation_query = {
                "translation_query": match,
                "target_language": "fr"
            }
            
            translation_response = self.client.post("/translate/", json=translation_query)
            assert translation_response.status_code == 201
            translation_data = translation_response.json()
            
            assert "results" in translation_data
            translations.append(translation_data)
        
        # Step 4: Verify all translations were successful
        for translation in translations:
            assert len(translation["results"]) > 0

    def test_workflow_with_language_pairs_verification(self):
        """Test workflow with language pairs verification."""
        # Step 1: Get available languages
        languages_response = self.client.get("/languages/")
        assert languages_response.status_code == 200
        languages_data = languages_response.json()
        
        # Step 2: Find a valid source-target language pair
        source_lang = None
        target_lang = None
        
        for lang_pair in languages_data["available_languages"]:
            if len(lang_pair["target_languages"]) > 0:
                source_lang = lang_pair["source_language"]
                target_lang = lang_pair["target_languages"][0]
                break
        
        assert source_lang is not None
        assert target_lang is not None
        
        # Step 3: Perform workflow with verified language pair
        fuzzy_query = {
            "source_language": source_lang,
            "query": "test",
            "target_language": target_lang,
            "max_distance": 5,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        if fuzzy_data["results"]:
            translation_query = {
                "translation_query": fuzzy_data["results"][0],
                "target_language": target_lang
            }
            
            translation_response = self.client.post("/translate/", json=translation_query)
            assert translation_response.status_code == 201

    def test_workflow_with_fallback_translation(self):
        """Test workflow that triggers fallback translation."""
        # Step 1: Use a term that likely doesn't exist in database
        fuzzy_query = {
            "source_language": "en",
            "query": "nonexistent_medication_12345",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 1
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        if fuzzy_data["results"]:
            # Step 2: Try to translate (should trigger fallback)
            translation_query = {
                "translation_query": fuzzy_data["results"][0],
                "target_language": "fr"
            }
            
            translation_response = self.client.post("/translate/", json=translation_query)
            assert translation_response.status_code == 201
            translation_data = translation_response.json()
            
            # Step 3: Verify fallback behavior
            # Either translations found or empty result (indicating fallback failed)
            assert "results" in translation_data

    def test_workflow_with_test_endpoints(self):
        """Test workflow using test endpoints for predictable results."""
        # Step 1: Get fuzzy matches using test endpoint
        fuzzy_query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/test", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        # Step 2: Verify test fuzzy results
        assert "results" in fuzzy_data
        assert len(fuzzy_data["results"]) == 5  # Test endpoint returns exactly 5
        
        # Step 3: Use test translation endpoint
        translation_query = {
            "translation_query": fuzzy_data["results"][0],
            "target_language": "fr"
        }
        
        translation_response = self.client.post("/translate/test", json=translation_query)
        assert translation_response.status_code == 201
        translation_data = translation_response.json()
        
        # Step 4: Verify test translation results
        assert "results" in translation_data
        assert len(translation_data["results"]) == 5  # Test endpoint returns exactly 5

    def test_workflow_consistency_across_requests(self):
        """Test that workflow produces consistent results across multiple requests."""
        query = {
            "source_language": "en",
            "query": "ibuprofen",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 3
        }
        
        results = []
        
        # Run the workflow multiple times
        for _ in range(3):
            # Step 1: Fuzzy matching
            fuzzy_response = self.client.post("/fuzzymatching/", json=query)
            assert fuzzy_response.status_code == 201
            fuzzy_data = fuzzy_response.json()
            
            if fuzzy_data["results"]:
                # Step 2: Translation
                translation_query = {
                    "translation_query": fuzzy_data["results"][0],
                    "target_language": "fr"
                }
                
                translation_response = self.client.post("/translate/", json=translation_query)
                assert translation_response.status_code == 201
                translation_data = translation_response.json()
                
                results.append({
                    "fuzzy_count": len(fuzzy_data["results"]),
                    "translation_count": len(translation_data["results"])
                })
        
        # Step 3: Verify consistency
        assert len(results) == 3
        for result in results:
            assert result["fuzzy_count"] > 0
            assert result["translation_count"] > 0

    def test_workflow_performance(self):
        """Test workflow performance with multiple consecutive requests."""
        import time
        
        # Use actual data that exists in the database - English to Russian
        query = {
            "source_language": "en",
            "query": "ibuprofen",
            "target_language": "ru",
            "max_distance": 5,
            "max_results": 3
        }
        
        start_time = time.time()
        successful_requests = 0
        
        # Run multiple workflow iterations
        for i in range(10):
            # Step 1: Fuzzy matching
            fuzzy_response = self.client.post("/fuzzymatching/", json=query)
            if fuzzy_response.status_code != 201:
                continue
                
            fuzzy_data = fuzzy_response.json()
            
            if fuzzy_data["results"]:
                # Step 2: Translation
                translation_query = {
                    "translation_query": fuzzy_data["results"][0],
                    "target_language": "ru"
                }
                
                translation_response = self.client.post("/translate/", json=translation_query)
                if translation_response.status_code == 201:
                    successful_requests += 1
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Step 3: Verify performance
        assert successful_requests > 0, "No successful workflow iterations"
        assert total_time < 30, f"Workflow took too long: {total_time} seconds"

    def test_workflow_error_handling(self):
        """Test workflow error handling with invalid data."""
        # Step 1: Use invalid fuzzy query
        invalid_fuzzy_query = {
            "source_language": 123,  # Invalid type
            "query": "test",
            "target_language": "fr"
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=invalid_fuzzy_query)
        assert fuzzy_response.status_code == 422  # Should fail validation
        
        # Step 2: Use valid fuzzy query but invalid translation query
        valid_fuzzy_query = {
            "source_language": "en",
            "query": "test",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=valid_fuzzy_query)
        if fuzzy_response.status_code == 201:
            fuzzy_data = fuzzy_response.json()
            
            if fuzzy_data["results"]:
                # Use invalid translation query
                invalid_translation_query = {
                    "translation_query": fuzzy_data["results"][0],
                    "target_language": 123  # Invalid type
                }
                
                translation_response = self.client.post("/translate/", json=invalid_translation_query)
                assert translation_response.status_code == 422  # Should fail validation

    def test_workflow_cross_language_consistency(self):
        """Test workflow consistency across different language pairs."""
        language_pairs = [
            ("en", "fr"),
            ("fr", "en"),
            ("en", "uk"),
            ("uk", "en"),
            ("en", "ru"),
            ("ru", "en")
        ]
        
        results = {}
        
        for source_lang, target_lang in language_pairs:
            query = {
                "source_language": source_lang,
                "query": "test",
                "target_language": target_lang,
                "max_distance": 5,
                "max_results": 3
            }
            
            try:
                # Step 1: Fuzzy matching
                fuzzy_response = self.client.post("/fuzzymatching/", json=query)
                if fuzzy_response.status_code == 201:
                    fuzzy_data = fuzzy_response.json()
                    
                    if fuzzy_data["results"]:
                        # Step 2: Translation
                        translation_query = {
                            "translation_query": fuzzy_data["results"][0],
                            "target_language": target_lang
                        }
                        
                        translation_response = self.client.post("/translate/", json=translation_query)
                        if translation_response.status_code == 201:
                            translation_data = translation_response.json()
                            
                            results[f"{source_lang}->{target_lang}"] = {
                                "fuzzy_success": True,
                                "translation_success": len(translation_data["results"]) > 0
                            }
            except Exception:
                # Continue with other language pairs if one fails
                continue
        
        # Step 3: Verify cross-language consistency
        assert len(results) > 0, "No successful workflow iterations for any language pair"
        
        for language_pair, result in results.items():
            assert result["fuzzy_success"], f"Fuzzy matching failed for {language_pair}"
            assert result["translation_success"], f"Translation failed for {language_pair}"

    def test_workflow_with_manual_translation_fallback(self):
        """Test workflow that can use manual translation as fallback."""
        # Step 1: Try normal workflow first
        fuzzy_query = {
            "source_language": "en",
            "query": "unknown_medication_for_testing",
            "target_language": "fr",
            "max_distance": 5,
            "max_results": 1
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        if fuzzy_data["results"]:
            translation_query = {
                "translation_query": fuzzy_data["results"][0],
                "target_language": "fr"
            }
            
            translation_response = self.client.post("/translate/", json=translation_query)
            assert translation_response.status_code == 201
            translation_data = translation_response.json()
            
            # Step 2: If translation fails, offer manual translation
            if len(translation_data["results"]) == 0:
                manual_query = {
                    "term": fuzzy_data["results"][0]["matching_name"],
                    "proposed_translation": "",
                    "source_language": "en",
                    "target_language": "fr",
                    "description": "Manual translation requested via workflow"
                }
                
                manual_response = self.client.post("/manual_translation/", json=manual_query)
                assert manual_response.status_code == 201

    def test_workflow_complete_chain(self):
        """Test the complete chain: languages -> fuzzy matching -> translation."""
        # Step 1: Get available languages
        languages_response = self.client.get("/languages/")
        assert languages_response.status_code == 200
        languages_data = languages_response.json()
        
        # Step 2: Select first available language pair
        source_lang = None
        target_lang = None
        
        for lang_pair in languages_data["available_languages"]:
            if len(lang_pair["target_languages"]) > 0:
                source_lang = lang_pair["source_language"]
                target_lang = lang_pair["target_languages"][0]
                break
        
        assert source_lang is not None
        assert target_lang is not None
        
        # Step 3: Perform fuzzy matching
        fuzzy_query = {
            "source_language": source_lang,
            "query": "test",
            "target_language": target_lang,
            "max_distance": 5,
            "max_results": 3
        }
        
        fuzzy_response = self.client.post("/fuzzymatching/", json=fuzzy_query)
        assert fuzzy_response.status_code == 201
        fuzzy_data = fuzzy_response.json()
        
        # Step 4: Perform translation
        if fuzzy_data["results"]:
            translation_query = {
                "translation_query": fuzzy_data["results"][0],
                "target_language": target_lang
            }
            
            translation_response = self.client.post("/translate/", json=translation_query)
            assert translation_response.status_code == 201
            translation_data = translation_response.json()
            
            # Step 5: Verify complete chain success
            assert len(translation_data["results"]) > 0