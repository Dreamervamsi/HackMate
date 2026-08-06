from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from orchestrator import orchestrate_agent
from agents import check_agent_plan_conflict

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
    # orchestrator
    res = orchestrate_agent(prompt, client)
    # check_agent_plan_conflict(res)
    pattern = r"(# Implementation Plan:.*)"

    # re.DOTALL is to match across multiple lines
    match = re.search(pattern, res, re.DOTALL)
    
    if match:
        implementation_plan = match.group(1).strip()
        check_agent_plan_conflict(prompt, implementation_plan)
    else:
        print("No implementation plan found in the response.")

if __name__ == "__main__":
    main()