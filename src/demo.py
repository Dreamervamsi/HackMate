from dotenv import load_dotenv
from orchestrator import orchestrate_agent
from config import client

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
   orchestrate_agent(prompt)
    
if __name__ == "__main__":
    main()