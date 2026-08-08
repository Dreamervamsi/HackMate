from google.genai import types
from config import client, MODEL_NAME
from agents import (
        create_agent,
        conflict_checker,
        generate_agent_plan,
        implement_plan
)

def orchestrate_agent(user_prompt):
    orchestrator_config = types.GenerateContentConfig(
        system_instruction="""
                You are an Orchestrator Agent responsible for decomposing tasks and coordinating sub-agents.
                
                When receiving a user request:
                1. Ask for clarification if needed.
                2. Break the request into independent sub-tasks and define a shared contract.
                3. Create sub-agents with create_agent.
                4. Ask each sub-agent for an implementation plan with generate_agent_plan.
                5. The conflict_checker will automatically checks and resolve any conflicts and return a clean implementation plan.
                6. Use the clean implementation plan to call implement_plan with:
                - agent_name
                - implementation_plan
                7. Return the final implementation results.

                """,
        tools=[create_agent, generate_agent_plan, conflict_checker, implement_plan],
        temperature=0.7
    )
    print("Orchestrator config created successfully.")

    orchestrator_chat = client.chats.create(
        model=MODEL_NAME,
        config=orchestrator_config
    )
    print("Orchestrator chat created successfully.")
    orchestrator_res = orchestrator_chat.send_message(user_prompt)

    print("Agent thinking....")
    # Track the latest plan result for conflict checking
    current_plan_result = None

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
                current_plan_result = generate_agent_plan(agent_name, instruction_prompt)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": current_plan_result}
                    )
                )

            elif call.name == "conflict_checker":
                task_prompt = call.args.get("task_prompt")

                # Extract the plan text from the result dict
                plan_text = current_plan_result.get("plan") if isinstance(current_plan_result, dict) else current_plan_result
                result = conflict_checker(plan_text, task_prompt)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )

            elif call.name == "implement_plan":
                agent_name = call.args.get("agent_name")
                implementation_plan = call.args.get("implementation_plan")

                result = implement_plan(agent_name, implementation_plan)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )
     
        tool_content = types.Content(role="tool", parts=tool_parts)
        orchestrator_res = orchestrator_chat.send_message(tool_content)
        
    return orchestrator_res.text