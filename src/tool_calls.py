from orchestrator import orchestrate_agent
from demo import client
from agents import (
        check_agent_plan_conflict, 
        parse_conflict_response, 
        resolve_conflicts_and_generate_plan,
        set_client,
        generate_agent_plan,
        implement_tool
)

def extract_implementation_plan(prompt: str):
     # orchestrator
    res = orchestrate_agent(prompt, client)
    
    # check_agent_plan_conflict(res)
    pattern = r"(# Implementation Plan:.*)"

    # re.DOTALL is to match across multiple lines
    match = re.search(pattern, res, re.DOTALL)
    
    return match

def resolve_conflicts_and_generate_plan(task_prompt: str, summary: str, conflicts: list):
   try:
    match = extract_implementation_plan(task_prompt)
    if match:
        implementation_plan = match.group(1).strip()
        conflict_check = check_agent_plan_conflict(task_prompt, implementation_plan)
        conflict_res = parse_conflict_response(conflict_check)
        if conflict_res and conflict_res.get("has_conflict"):
            summary = conflict_res.get("summary")
            conflicts = conflict_res.get("conflicts")
            clean_plan = resolve_conflicts_and_generate_plan(task_prompt, summary, conflicts)
            
            if clean_plan.get("success"):
                print("Clean implementation plan generated successfully:")
                global implement_plan
                implement_plan = clean_plan.get("clean_plan")
            else:
                print("Failed to generate a clean implementation plan.")
                return {"success": False, "message": "Failed to generate a clean implementation plan."}
        return {"success": True, "clean_plan": implementation_plan}
    else:
        print("No implementation plan found in the response.")
   except Exception as e:
        print(f"An error occurred: {e}")