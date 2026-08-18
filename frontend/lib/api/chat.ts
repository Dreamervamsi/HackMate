import { OrchestrationRequest, OrchestrationResponse, ApiError } from "@/types/chat";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function sendChatMessage(
  userPrompt: string,
  context?: Record<string, any>,
  priority?: "low" | "normal" | "high" | "urgent"
): Promise<OrchestrationResponse> {
  const request: OrchestrationRequest = {
    user_prompt: userPrompt,
    context,
    priority: priority || "normal",
  };

  const response = await fetch(`${API_BASE_URL}/orchestrate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData: ApiError = await response.json().catch(() => ({
      status: "error",
      detail: "Unknown error occurred",
      error_code: "UNKNOWN_ERROR",
    }));
    throw new Error(errorData.detail || "Failed to send message");
  }

  return response.json();
}

export async function checkHealth(): Promise<{ status: string; active_agents: number }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error("Health check failed");
  }
  
  return response.json();
}
