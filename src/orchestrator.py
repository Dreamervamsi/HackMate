from google.genai import types
from agents import create_agent, set_client


def orchestrate_agent(user_prompt, client):
    set_client(client)

    orchestrator_config = types.GenerateContentConfig(
        system_instruction="""You are an Orchestrator Agent responsible for decomposing tasks and creating specialized sub-agents.

When receiving a user request:
1. You must clarify the user needs by asking relevant clarification questions, before proceeding with creating agents.
2. Break down the request into distinct, independent sub-tasks.
3. For EVERY sub-task required, you MUST invoke the `create_agent` tool.

When invoking `create_agent`, you must supply the following arguments clearly:
- `agent_name`: A clear, identifier string (e.g., "mem-1", "navbar_agent", "database_designer").
- `description`: A concise summary of the agent's specific responsibility and domain.
- `system_instruction`: A complete, explicit, and self-contained system prompt for that sub-agent, defining its exact role, constraints, available context, and expected output.

Do not merely describe or talk about creating an agent in prose—you MUST execute the tool call with these structured details.""",
        tools=[create_agent],
        temperature=0.7
    )

    orchestrator_chat = client.chats.create(
        model='gemini-2.5-flash',
        config=orchestrator_config
    )
    
    orchestrator_res = orchestrator_chat.send_message(user_prompt)

    tool_outputs = []
    if orchestrator_res.function_calls:
        for call in orchestrator_res.function_calls:
            if call.name == "create_agent":
                agent_name = call.args.get("agent_name")
                description = call.args.get("description")
                system_instruction = call.args.get("system_instruction")

                agent_result = create_agent(agent_name, description, system_instruction)
                tool_outputs.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": agent_result}
                    )
                )
        final_res = orchestrator_chat.send_message(tool_outputs)

        return final_res.text

    return orchestrator_res.text

