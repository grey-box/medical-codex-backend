import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv("env.local")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def last_resort_translation(selected_medicine: str, target_language: str) -> str:
    prompt = f'Translate "{selected_medicine}" to "{target_language}". Do not use brand names. Only respond with the translated term.'
    
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    response = model.generate_content(prompt, safety_settings=safety_settings)

    if not response or not response.text:
        return 'No valid content found in the response from Gemini AI.'
    
    return response.text
