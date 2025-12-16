# Codex Translation System

Codex is a medical terminology translation system developed as part of Project Codex.
It uses a Neo4j graph database to translate medical terms across languages while preserving a canonical medical concept for consistent analysis.

The system supports:
- Fuzzy matching for misspelled terms
- Language fallback logic
- Brand and country-specific translations
- Data quality analysis (missing translations, brands, equivalents)
  
Codex can be run locally using a CLI or a Streamlit web interface.

---

Features

- Multilingual medical term translation
- Canonical term resolution using fuzzy matching
- Neo4j graph model for terms, languages, countries, and brands
- Language fallback logic (configurable)
- Full analysis on translated terms
- Streamlit-based frontend for demos
- CLI toold for development and testing

---

Requirements

Have the following installed:
- Python 3.10
- Virtual enviornment (venv)
- Neo4j Desktop
- Git

---

Local Setup (Step-by-Step)
The setup steps below apply to both macOS and Windows, with minor differences noted where applicable.

1. Download the Repo

2. Create and Activate Virtual Enviornment
   - macOS/ Linux
     - python3 -m venv venv
     - source venv/bin/activate
   - Windows (Command Prompt) - (Make sure you're in the command prompt, not powershell)
     - python -m venv venv 
     - venv\Scripts\activate 

3. Install Dependencies
   - pip install -r requirements.txt

4. Create Your .env File in your project folder
   - A default enviorment file is provided: .env.example
   - Copy it to create your local enviorment file:
   - macOS / Linux:
     - cp .env.example .env
   - Windows (Command Prompt)
     - copy .env.example .env
   - (You can also just create a .env file and just copy and paste the contents of the .env example)
   - Then update values as needed for your local Neo4j Desktop instance.
   - (Make sure to not commit .env, it's personal to you).

5. Set Up Neo4j Database
   - Download Neo4j Desktop
   - Open Neo4j Desktop
   - Create a new local database
   - Set the password (the same one inside your .env)
   - Start the database
   - Select "Query" (in the tools section)
   - Select "connect to instance", select your database, then click "connect" to view your database
   - Install the APOC plugin (for future fuzzy matching)
   - If it does not allow you to connect to your database and an error shows up, delete the database and create it again and follow from "create a new local database" and the database should connect.
     
6. Run streamlit dashboard front end
   - pip install streamlit
   - streamlit run ./streamlit_app.py
   - running on python3.11.xx here

7. Demo / POC Data Setup
   - Codex does not ship with a pre-populated database. Before using the CLI or Streamlit frontend, the Neo4j database must be populated with demo language-pack      data.
   - Populate Demo Data via Streamlit
     - Ensure Neo4j Desktop is running and .env is configured correctly
     - Start the Streanlit frontend:
       - streamlit run ./streamlit_app.py
       - When you're in the front end, click on the language pack loader section on the left of the screen.
       - From there, copy the path of a language pack from the languagepack/ folder:
         - ex: C:\....\language_packs\english_pack.json
       - Click "Import Language Pack" button and the data from the json file should be uploaded to your database.
     - Check your Neo4j database to see if new nodes and relationships were added
     - From there you can start translating terms

8. Project Structure:
   - codex/
     - api/
       - __init__.py
       - main.py           # CLI for testing
     - config/
       - fallbacks.json    # Language fallback rules
     - language_packs/
       - english_pack.json
       - french_pack.json
       - russian_pack.json
       - spanish_pack.json
       - ukrainian_pack.json
     - services/
       - __init__.py
       - translation_service.py  # Core translation + fallback logic
     - utils/
       - __init__.py             # Shared utilities (reserved for expansion)
     - neo4j_driver.py           # Neo4j connection and Cypher queries
    
     - .env     # Local credientials (ignored)
     - venv/ # Virtual enviornment
     - README.md # Setting up environment
     - streamlit_app.py          # Streamlit frontend (demo UI)
     - requirments.txt           # Python dependencies

9. Language Pack JSON Schema
    - Language packs define how medical terms are represented across languages, countries, and brands.
    - Each JSON file represents one language pack.
    - Structure:
{
  "language": {
    "code": "en",
    "name": "English"
  },
  "terms": [
    {
      "canonical": "Paracetamol",
      "entries": [
        { 
          "translation": "acetaminophen",
          "country": "US",
          "brand": "Tylenol"
        }
      ]
    }
  ]
}

   - Field Definitions:
     - canonical:
       - A system-level medical concept identifier. It represents what the drug is, independent of language, country, or naming convention. All translations and brands map back to this concept.
     - translation:
       - The locally used generic or common name for the canonical concept in a specific country and language context.
       - Even within the same language (e.g., English), medical terminology can differ by country.
       - Example:
         - United States -> acetaminophen
         - United Kingdom -> paracetamol
       - These refer to the same drug, but follow different offical naming standards (USAN vs. INN).
     - brand:
       - A country-specific commercial product name
     - country:
       - ISO-style country code where translation/brand applies. 
---

Notes
- The system always resolves user input to a canonical medical term
- Translated terms are used as entry points, not database keys
- Designed for offline or local-first usage
- Intended for academic and demonstration purposes

Cross-Platform Notes (Windows and macOS)
Codex has been smoke tested on both **macOS** and **Windows** environments.

The core application logic, Neo4j setup, demo data loading, and language pack ingestion behave the same across platforms. The primary differences between macOS and Windows are limited to environment startup details, such as virtual environment activation and shell behavior.

Platform-specific notes:
- On Windows, it is recommended to run the project using Command Prompt rather than PowerShell to avoid execution policy issues.
- JSON language packs are explicitly read using UTF-8 encoding to ensure compatibility with non-Latin scripts (e.g., Russian, Ukrainian) on Windows.
- Neo4j Desktop configuration and database population steps are identical on both platforms.

With these considerations, Codex can be set up and run consistently on macOS and Windows.

References 
- World Health Organization (WHO). International Nonproprietary Names (INN).
https://www.who.int/teams/health-product-policy-and-standards/inn
- United States Adopted Names (USAN) Council.
https://www.usancouncil.org/
- U.S. Food & Drug Administration (FDA). Drug Label Database.
https://www.accessdata.fda.gov/scripts/cder/daf/
- National Health Service (UK). Paracetamol.
https://www.nhs.uk/medicines/paracetamol/

These references support the distinction between canonical medical concepts and country-specific terminology (e.g., USAN vs. INN naming conventions).

