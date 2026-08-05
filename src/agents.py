from google.genai import types, Client

active_agents = {}
client = None

def set_client(api_client):
    global client
    client = api_client


def create_agent(agent_name: str, description: str, system_instruction: str):
    if client is None:
        raise ValueError("Agent client has not been initialized.")

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7
    )
    
    chat = client.chats.create(
        model='gemini-2.5-flash',
        config=config,
    )
    active_agents[agent_name] = chat

    return {
        "message": f"Agent '{agent_name}' created successfully.",
        "active_agents": active_agents
    }
