import requests
from sqlalchemy.orm import Session
from sqlalchemy import select, distinct, and_
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from app.models import UniqueTranslationsORM

import app.schemas as schemas

def translate(db: Session, query: schemas.TranslationQuery):

    print()
    try:
        term = query.translation_query.matching_name.lower()
        target_language = query.target_language.lower()

        dbQuery = select(distinct(UniqueTranslationsORM.target_text)).where(and_(
            UniqueTranslationsORM.target_language == target_language, 
            UniqueTranslationsORM.source_text == term
        ))
        result = db.execute(dbQuery).scalars().all()
        print("RESULTS: ")
        print(result)
        db.close()
        return [str(value) for value in result]

        if result:
            translated_term = result[0]

            return result
            # return {
            #     "results": [
            #         {
            #             "translated_name": "test",
            #             "translated_source": "local_db",
            #             "translated_uid": query.translation_query.matching_uid,
            #         }
            #     ]
            # }
        # else:
        #     return lastResortTranslate(query, "gemini") ##change the type of last resort translation here.

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
        

    # translationResults.translated_source = query.target_language 
    # translationResults.translated_uid = query.translation_query.matching_uid
    return translatedValue

def getGeminiTranslation(query: schemas.TranslationQuery):
    load_dotenv("env.local")

    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print(query)

    prompt = f'Translate "{query.translation_query.matching_name}" to "{query.target_language}". Do not use brand names. Only respond with the translated term.'
    
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    response = model.generate_content(prompt, safety_settings=safety_settings)

    if not response:
        response = "GemeniAPI unable to give response" ## maybe have another API called after?

    return response


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
