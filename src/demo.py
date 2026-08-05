from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from orchestrator import orchestrate_agent

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def main():
    # orchestrator
    res = orchestrate_agent("Build a backend application with a REST API", client)
    print(res)

if __name__ == "__main__":
    main()