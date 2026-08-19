import json
import time
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

# Define OpenAI Native Tool Definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_agent",
            "description": "Creates a sub-agent with a dedicated role and system instructions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {"type": "string", "description": "Unique identifier for the agent"},
                    "description": {"type": "string", "description": "Brief summary of what the agent does"},
                    "system_instruction": {"type": "string", "description": "Detailed prompt instruction for the agent"}
                },
                "required": ["agent_name", "description", "system_instruction"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_agent_plan",
            "description": "Asks a sub-agent to generate an implementation plan for a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {"type": "string"},
                    "instruction_prompt": {"type": "string"}
                },
                "required": ["agent_name", "instruction_prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "conflict_checker",
            "description": "Checks and resolves conflicts in a generated plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_prompt": {"type": "string", "description": "Original task context or prompt"}
                },
                "required": ["task_prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "implement_plan",
            "description": "Executes an agent's code implementation based on an approved plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {"type": "string"},
                    "implementation_plan": {"type": "string"}
                },
                "required": ["agent_name", "implementation_plan"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "validate_code_with_autofix",
            "description": "Runs code in a Docker container and automatically fixes bugs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The source code to validate"},
                    "language": {"type": "string", "default": "python"},
                    "max_attempts": {"type": "integer", "default": 2}
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_github_branch",
            "description": "Creates a new branch on GitHub.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string"},
                    "branch_name": {"type": "string"},
                    "base_branch": {"type": "string", "default": "main"},
                    "github_token": {"type": "string"}
                },
                "required": ["repo_url", "branch_name", "github_token"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "commit_and_push_to_github",
            "description": "Commits files and pushes them to a GitHub repository branch.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string"},
                    "branch_name": {"type": "string"},
                    "files": {
                        "type": "object",
                        "description": "Dictionary of filepath: content mappings"
                    },
                    "commit_message": {"type": "string"},
                    "github_token": {"type": "string"}
                },
                "required": ["repo_url", "branch_name", "files", "commit_message", "github_token"]
            }
        }
    }
]


@rate_limit_decorator
def orchestrate_agent(user_prompt, conversation_history=None, context=None):
    system_instruction = """You are an Orchestrator Agent responsible for decomposing tasks and coordinating sub-agents.

When receiving a user request:
1. Ask for clarification if needed.
2. Break the request into independent sub-tasks and define a shared contract.
3. Create sub-agents with `create_agent`.
4. Ask each sub-agent for an implementation plan with `generate_agent_plan`.
5. The `conflict_checker` will automatically check and resolve any conflicts.
6. Use the clean implementation plan to call `implement_plan`.
7. Automatically validate the code using `validate_code_with_autofix`.
8. If requested, push code to GitHub using `create_github_branch` and `commit_and_push_to_github`.
9. Return the final validated implementation results.

IMPORTANT: GitHub credentials are provided in the context. Use them when calling GitHub functions:
- github_token: Use the github_token from context if available
- github_repo: Use the github_repo from context if available

If GitHub credentials are not available, ask the user to provide them via the sidebar.
"""

    print("Orchestrator initialized.")

    # Extract GitHub credentials from context if available
    github_token = context.get("github_token") if context else None
    github_repo = context.get("github_repo") if context else None

    if github_token or github_repo:
        print(f"GitHub credentials provided in context - Token: {'***' if github_token else 'None'}, Repo: {github_repo or 'None'}")
        system_instruction += "\n\nGitHub credentials provided by user:\n"
        if github_repo:
            system_instruction += f"- Repository URL: {github_repo}\n"
        if github_token:
            system_instruction += f"- GitHub Token: {github_token}\n"
        system_instruction += "Use these credentials when calling GitHub functions. Do not ask the user for them."
    else:
        system_instruction += "\n\nNo GitHub credentials provided in context. Ask the user to provide credentials via the sidebar if needed."

    messages = [{"role": "system", "content": system_instruction}]

    if conversation_history:
        for msg in conversation_history:
            role = msg.get("role")
            content = msg.get("content")
            if role in ["user", "assistant"] and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_prompt})

    current_plan_result = None
    max_iterations = 20
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"Orchestrator iteration {iteration}")

        # Native function call execution
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.7
        )

        response_message = response.choices[0].message
        messages.append(response_message)  # Append full assistant response message object

        # If model didn't ask to execute any tool calls, return its text output
        if not response_message.tool_calls:
            print("No more tool calls detected. Returning final response.")
            return response_message.content

        # Process native tool calls
        for tool_call in response_message.tool_calls:
            time.sleep(1.0)
            func_name = tool_call.function.name
            call_id = tool_call.id

            try:
                args = json.loads(tool_call.function.arguments)
            except Exception as e:
                args = {}
                print(f"Failed to parse arguments for {func_name}: {e}")

            print(f"Processing tool call: {func_name}")

            result = None
            try:
                if func_name == "create_agent":
                    result = create_agent(
                        args.get("agent_name"),
                        args.get("description"),
                        args.get("system_instruction")
                    )

                elif func_name == "generate_agent_plan":
                    current_plan_result = generate_agent_plan(
                        args.get("agent_name"),
                        args.get("instruction_prompt")
                    )
                    result = current_plan_result

                elif func_name == "conflict_checker":
                    plan_text = current_plan_result.get("plan") if isinstance(current_plan_result, dict) else current_plan_result
                    result = conflict_checker(plan_text, args.get("task_prompt"))

                elif func_name == "implement_plan":
                    result = implement_plan(
                        args.get("agent_name"),
                        args.get("implementation_plan")
                    )

                elif func_name == "validate_code_with_autofix":
                    result = validate_code_with_autofix(
                        args.get("code"),
                        args.get("language", "python"),
                        int(args.get("max_attempts", 2))
                    )

                elif func_name == "create_github_branch":
                    result = create_github_branch(
                        args.get("repo_url"),
                        args.get("branch_name"),
                        args.get("base_branch", "main"),
                        args.get("github_token")
                    )

                elif func_name == "commit_and_push_to_github":
                    files = args.get("files", {})
                    if isinstance(files, str):
                        try:
                            files = json.loads(files)
                        except Exception:
                            files = {}

                    result = commit_and_push_to_github(
                        args.get("repo_url"),
                        args.get("branch_name"),
                        files,
                        args.get("commit_message"),
                        args.get("github_token")
                    )

                else:
                    result = {"error": f"Unknown function: {func_name}"}

                print(f"Function {func_name} executed successfully.")

            except Exception as e:
                result = {"error": f"Error executing {func_name}: {str(e)}"}
                print(f"Error executing {func_name}: {e}")

            # Return tool outputs matching the tool_call_id
            messages.append({
                "role": "tool",
                "tool_call_id": call_id,
                "content": json.dumps(result) if not isinstance(result, str) else result
            })

    print("Max iterations reached. Returning last text response.")
    return response_message.content or "Completed orchestration iterations."