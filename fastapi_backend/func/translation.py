from sqlalchemy.orm import Session

import schemas
import requests


def translate(db: Session, query: schemas.TranslationQuery):    
    if true: ##This will be if the translation passes
        result = translate()
    else:
        result = lastResortTranslate()
    
    return result

def lastResortTranslate(db: Session, query: schemas.TranslationQuery):
    apiResults =  agnosticApiRequest('')
    
    translationResults: schemas.TranslationResult
    translationResults.translated_name = apiResults ## will be json so will have to adjust most likely depending on API used.
    translationResults.translated_source = "Last Resort" ##not finalized
    translationResults.translated_uid = apiResults ## not sure what this is supposed to be.
    return


def agnosticApiRequest(agnosticUrl:str): ## will most likely have to adjust when testing
    url = agnosticUrl

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None  