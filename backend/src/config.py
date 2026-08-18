from groq import Groq
import os
import time
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

# Configuration
MODEL_NAME = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
API_KEY = os.getenv('GROQ_API_KEY')

if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file.")

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    raise ValueError(f"Failed to initialize Groq client: {e}")

# Chat history management for agents
chat_histories = {}

def get_chat_history(agent_name: str) -> list:
    """Get chat history for a specific agent"""
    if agent_name not in chat_histories:
        chat_histories[agent_name] = []
    return chat_histories[agent_name]

def add_to_chat_history(agent_name: str, role: str, content: str):
    """Add a message to the chat history for a specific agent"""
    if agent_name not in chat_histories:
        chat_histories[agent_name] = []
    chat_histories[agent_name].append({"role": role, "content": content})

def clear_chat_history(agent_name: str):
    """Clear chat history for a specific agent"""
    if agent_name in chat_histories:
        chat_histories[agent_name] = []

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