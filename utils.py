import json
import openai
from config import OPENAI_API_KEY

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

def translate_text(text, target_lang):
    """Translate text using OpenAI"""
    if not OPENAI_API_KEY:
        return "Please set up your OpenAI API key in the .env file"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a translator. Translate the following text to {target_lang}. Only provide the translation, nothing else."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Translation error: {str(e)}"

def generate_phrases(location, language):
    """Generate common phrases using OpenAI"""
    if not OPENAI_API_KEY:
        return ["Please set up your OpenAI API key in the .env file"]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful travel assistant that provides common phrases in {language} for travelers visiting {location}."
                },
                {
                    "role": "user",
                    "content": f"Give me 5 essential phrases in {language} that I might need in {location}. Include English translation and pronunciation. Format: 'Phrase ({language}) - Pronunciation - English meaning'"
                }
            ]
        )
        phrases = response.choices[0].message.content.split('\n')
        return [phrase for phrase in phrases if phrase.strip()]
    except Exception as e:
        return [f"Error generating phrases: {str(e)}"]

def generate_exercises(language, difficulty):
    """Generate language exercises using OpenAI"""
    if not OPENAI_API_KEY:
        return []
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a language teacher creating exercises. Return the response as a JSON array with objects containing 'question', 'answer', and 'hint' fields."
                },
                {
                    "role": "user",
                    "content": f"Create 3 {difficulty} level {language} exercises focused on travel situations. Include helpful hints."
                }
            ]
        )
        
        content = response.choices[0].message.content
        exercises = json.loads(content) if isinstance(content, str) else content
        return exercises
    except Exception as e:
        return []

def get_travel_advice(query):
    """Get travel advice using OpenAI"""
    if not OPENAI_API_KEY:
        return "Please set up your OpenAI API key in the .env file"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a knowledgeable travel assistant providing helpful, concise advice to travelers."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}" 