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
import re
import time
import json

@rate_limit_decorator
def orchestrate_agent(user_prompt):
    system_instruction = """
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
                
                IMPORTANT: When you need to call a function, use this EXACT format:
                FUNCTION_CALL: function_name|param1=value1|param2=value2
                
                Available functions:
                - create_agent(agent_name, description, system_instruction)
                - generate_agent_plan(agent_name, instruction_prompt)
                - conflict_checker(plan, task_prompt)
                - implement_plan(agent_name, implementation_plan)
                - validate_code_with_autofix(code, language, max_attempts)
                - create_github_branch(repo_url, branch_name, base_branch, github_token)
                - commit_and_push_to_github(repo_url, branch_name, files, commit_message, github_token)
                
                Example: FUNCTION_CALL: create_agent|agent_name=coder|description=writes code|system_instruction=You are a coder
                """
    
    print("Orchestrator initialized.")
    
    # Initialize conversation
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_prompt}
    ]
    
    # Track the latest plan result for conflict checking
    current_plan_result = None
    
    # Simple function calling loop
    max_iterations = 20  # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"Orchestrator iteration {iteration}")
        
        # Make API call
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7
        )
        
        response_message = response.choices[0].message
        response_text = response_message.content
        
        print(f"Orchestrator response: {response_text[:200]}...")
        
        # Check if the response contains a function call
        # Look for FUNCTION_CALL: function_name|param1=value1|param2=value2
        function_pattern = r'FUNCTION_CALL:\s*(\w+)\s*\|(.*)'
        function_matches = re.findall(function_pattern, response_text)
        
        if not function_matches:
            # No more function calls, return the final response
            print("No more function calls detected. Returning final response.")
            return response_text
        
        # Process all function calls in this response
        function_results = []
        for func_name, args_str in function_matches:
            # Add rate limiting for each function call
            time.sleep(1.0)  # Add 1 second delay between function calls
            
            print(f"Processing function call: {func_name}")
            
            # Parse arguments (split by | and then by =)
            args = {}
            if args_str.strip():
                arg_pairs = [pair.strip() for pair in args_str.split('|')]
                for pair in arg_pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        args[key] = value
            
            # Execute the function
            result = None
            try:
                if func_name == "create_agent":
                    agent_name = args.get("agent_name")
                    description = args.get("description")
                    system_instruction = args.get("system_instruction")
                    result = create_agent(agent_name, description, system_instruction)
                
                elif func_name == "generate_agent_plan":
                    agent_name = args.get("agent_name")
                    instruction_prompt = args.get("instruction_prompt")
                    current_plan_result = generate_agent_plan(agent_name, instruction_prompt)
                    result = current_plan_result
                
                elif func_name == "conflict_checker":
                    task_prompt = args.get("task_prompt")
                    plan_text = current_plan_result.get("plan") if isinstance(current_plan_result, dict) else current_plan_result
                    result = conflict_checker(plan_text, task_prompt)
                
                elif func_name == "implement_plan":
                    agent_name = args.get("agent_name")
                    implementation_plan = args.get("implementation_plan")
                    result = implement_plan(agent_name, implementation_plan)
                
                elif func_name == "validate_code_with_autofix":
                    code = args.get("code")
                    language = args.get("language", "python")
                    max_attempts = int(args.get("max_attempts", 2))
                    result = validate_code_with_autofix(code, language, max_attempts)
                
                elif func_name == "create_github_branch":
                    repo_url = args.get("repo_url")
                    branch_name = args.get("branch_name")
                    base_branch = args.get("base_branch")
                    github_token = args.get("github_token")
                    result = create_github_branch(repo_url, branch_name, base_branch, github_token)
                
                elif func_name == "commit_and_push_to_github":
                    repo_url = args.get("repo_url")
                    branch_name = args.get("branch_name")
                    files = args.get("files")
                    commit_message = args.get("commit_message")
                    github_token = args.get("github_token")
                    # Parse files dict from string
                    if isinstance(files, str):
                        try:
                            files = json.loads(files)
                        except:
                            files = {}
                    result = commit_and_push_to_github(repo_url, branch_name, files, commit_message, github_token)
                
                else:
                    result = {"error": f"Unknown function: {func_name}"}
                
                print(f"Function {func_name} executed: {result}")
                function_results.append(f"{func_name}: {result}")
                
            except Exception as e:
                result = {"error": f"Error executing {func_name}: {str(e)}"}
                print(f"Error executing {func_name}: {e}")
                function_results.append(f"{func_name}: {result}")
        
        # Add the function results to the conversation
        messages.append({"role": "assistant", "content": response_text})
        messages.append({"role": "user", "content": f"Functions executed: {'; '.join(function_results)}"})
    
    print("Max iterations reached. Returning last response.")
    return response_text