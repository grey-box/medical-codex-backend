# Import dependencies                                                             
from codex.services.translation_service import translate, sync_translation_data, load_language_pack, language_exists
from codex.neo4j_driver import resolve_to_base_term, driver

"""
CLI Test Harness for Codex Translation System

This script is used for manual testing and validation of the Codex medical
translation pipeline. It allows developers to:
- Enter medical terms interactively
- Test language and country-based translations
- Verify fallback behavior
- Load language packs dynamically
- Run full data-quality analysis on translated terms

This file is NOT part of the production API or UI.
It is intended strictly for development and testing purposes.
"""

no_translation_flag = False

while True:
    term = input("\nEnter a medical term (or 'exit'): ")
    if term.lower() == "exit":
        break

    lang = input("Enter language code (ex: en, es, fr, ru, uk) or press Enter to skip: ")
    lang = lang if lang else None

    country = input("Enter country code (US, GB, MX, FR, ES, NG, RU) or press Enter to skip: ")
    country = country if country else None

    if lang and not language_exists(lang):
        print(f"\nLanguage '{lang}' is not installed in the system.")
        load_choice = input("Would you like to load a language pack now? (y/n): ")

        if load_choice.lower() == "y":
            pack_path = input("Enter path to JSON language pack: ")
            try:
                print(load_language_pack(pack_path))
                break
            except Exception as e:
                print(f"Failed to load language pack: {e}")
                continue
        else:
            fallback_choice = input("Fallback to English instead? (y/n): ")

            if fallback_choice == "y":
                lang = "en"
            else: 
                print("\nCannot translate without a valid language or fallback.")
                continue
    
    
    print("\n--Translation Results--")
    results = translate(term, lang=lang, country=country)

    print(f"Canonical Term: {results['canonical']}")
    print(f"Requested Language: {results['requested_language']}")
    print(f"Used Language: {results['used_language']}")

    if results.get("fallback_used"):
        print("\nFallback Activated")
        print(f"Fallback Type: {results.get('fallback_type', 'unknown')}")
        print(f"Fallback Chain Tried: {results.get('fallback_chain', [])}")
    else:
        print("\nDirect translation used (no fallback needed)")

    print("\nTranslated Term:")
    for r in results["results"]:
        print(f"- {r['translation']} ({r['language']}) | Brand: {r['brand']} | Country: {r['country']}")

    for r in results["results"]:
        translated_term = r["translation"]
        test_more = input(f"\nRun full anaylsis on '{translated_term}'? (y/n): ")
        if test_more.lower() == "y":
            with driver.session() as session:
                base = resolve_to_base_term(session, translated_term)
                print(f"\nChecking term: {translated_term}\n")
                sync_translation_data(base)
                break
        else:
            break