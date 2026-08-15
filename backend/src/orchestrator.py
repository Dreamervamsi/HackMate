from google.genai import types
from config import client, MODEL_NAME, rate_limit_decorator
from agents import (
        create_agent,
        generate_agent_plan,
        implement_plan,
        validate_code_with_autofix,
        create_github_branch,
        commit_and_push_to_github
)
from tool_calls import conflict_checker

@rate_limit_decorator
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
                7. After implementation, automatically validate the code using validate_code_with_autofix with:
                - code: the implemented code
                - language: the programming language (default: python)
                This will run tests in Docker containers and automatically fix bugs up to 2 times.
                8. If the user wants to push code to GitHub, use create_github_branch to create a new branch and commit_and_push_to_github to push the code.
                9. Return the final validated implementation results.
                """,
        tools=[create_agent, generate_agent_plan, conflict_checker, implement_plan, validate_code_with_autofix, create_github_branch, commit_and_push_to_github],
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
            # Add rate limiting for each function call
            import time
            time.sleep(1.0)  # Add 1 second delay between function calls
            if call.name == "create_agent":
                agent_name = call.args.get("agent_name")
                description = call.args.get("description")
                system_instruction = call.args.get("system_instruction")

                # create agents
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

            elif call.name == "validate_code_with_autofix":
                code = call.args.get("code")
                language = call.args.get("language", "python")
                max_attempts = call.args.get("max_attempts", 2)

                result = validate_code_with_autofix(code, language, max_attempts)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )

            elif call.name == "create_github_branch":
                repo_url = call.args.get("repo_url")
                branch_name = call.args.get("branch_name")
                base_branch = call.args.get("base_branch")
                github_token = call.args.get("github_token")

                result = create_github_branch(repo_url, branch_name, base_branch, github_token)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )

            elif call.name == "commit_and_push_to_github":
                repo_url = call.args.get("repo_url")
                branch_name = call.args.get("branch_name")
                files = call.args.get("files")
                commit_message = call.args.get("commit_message")
                github_token = call.args.get("github_token")

                result = commit_and_push_to_github(repo_url, branch_name, files, commit_message, github_token)

                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )
     
        tool_content = types.Content(role="tool", parts=tool_parts)
        orchestrator_res = orchestrator_chat.send_message(tool_content)
        
    return orchestrator_res.text