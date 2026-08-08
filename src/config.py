from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
MODEL_NAME = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it in your .env file.")

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    raise ValueError(f"Failed to initialize Gemini client: {e}")