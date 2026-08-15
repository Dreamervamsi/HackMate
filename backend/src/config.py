from google import genai
import os
import time
from dotenv import load_dotenv
from functools import wraps

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

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)
GITHUB_DEFAULT_BRANCH = os.getenv('GITHUB_DEFAULT_BRANCH', 'main')

# Rate limiting configuration
RATE_LIMIT_DELAY = 2.0  # Seconds between API calls
LAST_API_CALL_TIME = 0

def rate_limit_decorator(func):
    """Decorator to add rate limiting to API calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        global LAST_API_CALL_TIME
        current_time = time.time()
        time_since_last_call = current_time - LAST_API_CALL_TIME
        
        if time_since_last_call < RATE_LIMIT_DELAY:
            sleep_time = RATE_LIMIT_DELAY - time_since_last_call
            print(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        LAST_API_CALL_TIME = time.time()
        return func(*args, **kwargs)
    return wrapper