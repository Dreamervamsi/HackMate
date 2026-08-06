from google.genai import types
from agents import create_agent, set_client, generate_agent_plan

def orchestrate_agent(user_prompt, client):
    set_client(client)
    
    orchestrator_config = types.GenerateContentConfig(
        system_instruction="""
 You are an Orchestrator Agent responsible for decomposing tasks and creating specialized sub-agents.

When receiving a user request:
1. Ask any necessary clarification questions first.
2. Break the request into distinct, independent sub-tasks and identify dependencies between them.
3. Define a SHARED CONTRACT for the whole job (naming conventions, file paths, export style, and interfaces). This SHARED CONTRACT must be included in every sub-agent's `system_instruction` so outputs remain compatible.
4. For every sub-task:
   a) invoke the `create_agent` tool to create a new agent for that task,
   b) then invoke the `generate_agent_plan` tool with the same `agent_name` and an instruction prompt so the agent itself produces the implementation plan.
5. Do not generate agent plans directly inside the orchestrator. The orchestrator must delegate plan creation to the agent via `generate_agent_plan`.
6. When calling generate_agent_plan, never pass the raw task directly. Always wrap it in a prompt that explicitly asks for an implementation plan only.

When invoking `create_agent`, supply:
- `agent_name`
- `description`
- `system_instruction`

When invoking `generate_agent_plan`, supply:
- `agent_name`
- `instruction_prompt` (the clean task prompt the agent should use to produce its plan)

The orchestrator should aggregate the returned plans from `generate_agent_plan` and return those plans as the final result.
""",
        tools=[create_agent, generate_agent_plan],
        temperature=0.7
    )
    print("Orchestrator config created successfully.")

    orchestrator_chat = client.chats.create(
        model='gemini-3.5-flash',
        config=orchestrator_config
    )
    print("Orchestrator chat created successfully.")
    orchestrator_res = orchestrator_chat.send_message(user_prompt)

    print("Agent thinking....")
    while orchestrator_res.function_calls:
        tool_parts = []
        
        for call in orchestrator_res.function_calls:
            if call.name == "create_agent":
                agent_name = call.args.get("agent_name")
                description = call.args.get("description")
                system_instruction = call.args.get("system_instruction")

                # Execute your local python function
                agent_result = create_agent(agent_name, description, system_instruction)
                
                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": agent_result}
                    )
                )
            elif call.name == "generate_agent_plan":
                agent_name = call.args.get("agent_name")
                instruction_prompt = call.args.get("instruction_prompt")

                # Execute your local python function
                plan_result = generate_agent_plan(agent_name, instruction_prompt)
                
                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": plan_result}
                    )
                )
        tool_content = types.Content(role="tool", parts=tool_parts)
        orchestrator_res = orchestrator_chat.send_message(tool_content)
        
    return orchestrator_res.text
