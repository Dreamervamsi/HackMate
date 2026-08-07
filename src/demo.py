from google import genai
from google.genai import types
import os
import re
from dotenv import load_dotenv
from agents import check_agent_plan_conflict, parse_conflict_response

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

prompt  = """
    Create two HTML pages for a handmade candle website.

Page 1:
- unique design and layout
- header with logo and navigation
- main section with product images, descriptions, and prices

Page 2:
- unique design and layout
- contact form for customers to reach out
"""

def main():
   
    
if __name__ == "__main__":
    main()