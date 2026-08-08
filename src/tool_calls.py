import re
from agents import (
        check_agent_plan_conflict,
        parse_conflict_response,
        conflict_resolver,
)

def extract_implementation_plan(res: str):

    # More flexible pattern to handle various formats:
    # - "# Implementation Plan:"
    # - "Implementation Plan:"
    # - Case-insensitive
    # - Optional colon
    pattern = r"(?i)(?:#?\s*)implementation\s*plan\s*:.*"

    # re.DOTALL is to match across multiple lines
    match = re.search(pattern, res, re.DOTALL)

    if match:
        return match.group(0)
    return None

def conflict_checker(plan: str,task_prompt: str):
    try:
        matched_text = extract_implementation_plan(plan)
        if matched_text:
            implementation_plan = matched_text.strip()
            conflict_check = check_agent_plan_conflict(task_prompt, implementation_plan)
            conflict_res = parse_conflict_response(conflict_check)
            if conflict_res and conflict_res.get("has_conflict"):
                summary = conflict_res.get("summary")
                conflicts = conflict_res.get("conflicts")
                clean_plan = conflict_resolver(task_prompt, summary, conflicts)

                if clean_plan.get("success"):
                    print("Clean implementation plan generated successfully:")
                    implementation_plan = clean_plan.get("clean_plan")
                else:
                    print("Failed to generate a clean implementation plan.")
                    return {"success": False, "message": "Failed to generate a clean implementation plan."}
            return {"success": True, "clean_plan": implementation_plan}
        else:
            print("No implementation plan found in the response.")
            return {"success": False, "clean_plan": "", "error": "No implementation plan was found"}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "success": False,
            "clean_plan": "",
            "error": f"An error occurred: {e}"
        }