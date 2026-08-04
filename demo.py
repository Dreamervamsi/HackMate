from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def create_agent(agent_name, agent_description, system_instruction):
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7
    )
    
    chat = client.chats.create(
        model = 'gemini-2.5-flash',
        config = config,
    )
    return chat


def interactive_session(chat_model):
    
    user_prompt = input("You: ")
            
    print("Agent is thinking...", end="\r")

    response = chat_model.send_message(user_prompt)

    print("Agent: ", end="", flush=True)
            
    return response

def orchestrate_agent():
    orchestrator_config = types.GenerateContentConfig(
        system_instruction="""You are an orchestrator that manages multiple agents.
                              Coordinate their responses effectively.
                              Use the `create_agent` tool to build specialized sub-agents for distinct tasks.
                              generate agents with specific instructions and capabilities to handle different types of queries.
                        """,
        tools = [create_agent],
        temperature=0.7
    )
    agent_name = "my_agent"
    agent_description = "A helpful assistant that can answer questions."
    system_instruction = "You are a helpful assistant. Answer questions clearly and concisely."


def main():
    

    # Create the agent
    agent = create_agent(agent_name, agent_description, system_instruction)

    print(f"Agent '{agent_name}' created successfully!")

    response = interactive_session(agent)
    print(response.text)

if __name__ == "__main__":
    main()