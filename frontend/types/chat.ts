export type MessageRole = "user" | "assistant";

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  createdAt?: string;
}

export interface OrchestrationRequest {
  user_prompt: string;
  conversation_history?: Message[];
  context?: Record<string, any>;
  priority?: "low" | "normal" | "high" | "urgent";
}

export interface OrchestrationResponse {
  status: "success" | "error";
  result?: string;
  active_agents: string[];
  execution_time?: number;
  error?: string;
  metadata?: {
    priority?: string;
    context_provided?: boolean;
    original_prompt_length?: number;
  };
}

export interface ApiError {
  status: "error";
  detail: string;
  error_code: string;
  timestamp?: string;
}
