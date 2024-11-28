import requests
from sqlalchemy.orm import Session
from sqlalchemy import select, distinct, and_
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from app.models import UniqueTranslationsORM
from typing import Callable, Dict, Any
from typing import List

import app.schemas as schemas

def translate(db: Session, query: schemas.TranslationQuery) -> Dict[str, List[Dict[str, Any]]]:

    try:
        term = query.translation_query.matching_name
        target_language = query.target_language

        dbQuery = select(distinct(UniqueTranslationsORM.target_text)).where(and_(
            UniqueTranslationsORM.target_language == target_language, 
            UniqueTranslationsORM.source_text == term
        ))
        result = db.execute(dbQuery).scalars().all()
        db.close()
        resultList = [str(value) for value in result]

        if resultList and resultList[0]:
            finalResults = {
            "results": [
                {
                    "translated_name": medicine,
                    "translated_source": "local_db",
                    "translated_uid": query.translation_query.matching_uid,
                }
                for medicine in resultList
            ]
            }
        else:
            finalResults = lastResortTranslate(query, "gemini")
        
        return finalResults

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def lastResortTranslate(query: schemas.TranslationQuery, translationType: str):

    if translationType == "gemini":
        translatedValue = getGeminiTranslation(query)

    elif translationType == "":
        translatedValue = None

    elif translationType == "":
        translatedValue = None
        
    return translatedValue

def getGeminiTranslation(query: schemas.TranslationQuery)  -> Dict[str, List[Dict[str, Any]]]:
    load_dotenv("env.local")
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    if query.target_language == "en":
        query.target_language = "english"
    elif query.target_language == "uk":
        query.target_language = "ukranian"
    elif query.target_language == "ru":
        query.target_language = "russian"
    elif query.target_language == "fr":
        query.target_language == "french"

    prompt = f'Translate "{query.translation_query.matching_name}" to "{query.target_language}" as a drug name. Convert any brand name to the actual drug name.'
    
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    response = model.generate_content(prompt, safety_settings=safety_settings)

    print(type(response))
    if not response:
        response = "GemeniAPI unable to give response" ## maybe have another API called after?


    finalResults = {
        "results": [
            {
                "translated_name": response.text,
                "translated_source": "gemini_api",
                "translated_uid": query.translation_query.matching_uid,
            }
        ]
    }

    return finalResults


## Problem lies where most translations instruct users to use their python libraries instead of having a url to json call into. 
def agnosticApiRequest(
    agnosticUrl: str,
):  ## will most likely have to adjust when testing
    url = agnosticUrl

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print("Error:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
