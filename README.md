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

1. Clone the Repo

   - git clone https://github.com/YourUsername/codex-translation-api.git
   - cd codex-transaltion-api

2. Create and Activate Virtual Enviornment

   - python3 -m venv venv
   - source venv/bin/activate (for mac)

3. Install Dependencies

   - pip install -r requirements.txt

4. Create Your .env File in your project folder

   - NEO4J_URI=bolt://localhost:7687
   - NEO4J_USER=neo4j
   - NEO4J_PASSWORD=yourpassword
   - (Make sure to not commit .env, it's personal to you).

5. Set Up Neo4j Database

   - Open Neo4j Desktop
   - Create a new local database
   - Set the password (the same one inside your .env)
   - Start the database
   - Install the APOC plugin (for future fuzzy matching)

6. Run streamlit dashboard front end

   - pip install streamlit
   - streamlit run ./streamlit_app.py
   - running on python3.11.xx here

7. Project Structure:
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
       
---

Notes
- The system always resolves user input to a canonical medical term
- Translated terms are used as entry points, not database keys
- Designed for offline or local-first usage
- Intended for academic and demonstration purposes
