from google.genai import types
from agents import (
        check_agent_plan_conflict, 
        parse_conflict_response, 
        resolve_conflicts_and_generate_plan,
        set_client,
        generate_agent_plan,
        implement_tool
)

def orchestrate_agent(user_prompt, client):
    set_client(client)
    
    orchestrator_config = types.GenerateContentConfig(
        system_instruction="""
                You are an Orchestrator Agent responsible for decomposing tasks and coordinating sub-agents.

                When receiving a user request:
                1. Ask for clarification if needed.
                2. Break the request into independent sub-tasks and define a shared contract.
                3. Create sub-agents with create_agent.
                4. Ask each sub-agent for an implementation plan with generate_agent_plan.
                5. For each plan, call check_agent_plan_conflict with:
                - task_prompt
                - implementation_plan
                6. If the conflict checker reports conflicts, call resolve_conflicts_and_generate_plan with:
                - task_prompt
                - summary
                - conflicts
                7. If there are no conflicts, or after resolution, call implement_tool with:
                - agent_name
                - implementation_plan
                8. Return the final implementation results.
                """,
        tools=[create_agent, generate_agent_plan, check_agent_plan_conflict, resolve_conflicts_and_generate_plan, implement_tool],
        temperature=0.7
    )
    print("Orchestrator config created successfully.")

    orchestrator_chat = client.chats.create(
        model='gemini-2.5-flash',
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
           
            elif call.name == "check_agent_plan_conflict":
                task_prompt = call.args.get("task_prompt")
                implementation_plan = call.args.get("implementation_plan")

                result = check_agent_plan_conflict(task_prompt, implementation_plan)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )

            elif call.name == "resolve_conflicts_and_generate_plan":
                task_prompt = call.args.get("task_prompt")
                summary = call.args.get("summary")
                conflicts = call.args.get("conflicts")

                result = resolve_conflicts_and_generate_plan(task_prompt, summary, conflicts)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )

            elif call.name == "implement_tool":
                agent_name = call.args.get("agent_name")
                implementation_plan = call.args.get("implementation_plan")

                result = implement_tool(agent_name, implementation_plan)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )
     
        tool_content = types.Content(role="tool", parts=tool_parts)
        orchestrator_res = orchestrator_chat.send_message(tool_content)
        
    return orchestrator_res.text