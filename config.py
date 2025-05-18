import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Supported Languages
LANGUAGES = {
    "English": "English",
    "Spanish": "Spanish",
    "French": "French",
    "German": "German",
    "Italian": "Italian",
    "Portuguese": "Portuguese",
    "Chinese": "Chinese",
    "Japanese": "Japanese",
    "Korean": "Korean",
    "Russian": "Russian",
    "Arabic": "Arabic"
}

# Azure Translator API Configuration
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com" 