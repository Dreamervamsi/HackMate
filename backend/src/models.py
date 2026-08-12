from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum


class TaskStatus(str, Enum):
    """Enumeration for task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class OrchestrationRequest(BaseModel):
    """Request model for orchestration endpoint"""
    user_prompt: str = Field(
        ...,
        description="The user prompt/task description to be orchestrated",
        min_length=1,
        max_length=10000
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context for the orchestration task"
    )
    priority: Optional[str] = Field(
        "normal",
        description="Task priority level"
    )

    @validator('user_prompt')
    def validate_user_prompt(cls, v):
        if not v or not v.strip():
            raise ValueError('user_prompt cannot be empty')
        return v.strip()

    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ['low', 'normal', 'high', 'urgent']
        if v.lower() not in valid_priorities:
            raise ValueError(f'priority must be one of: {valid_priorities}')
        return v.lower()

    class Config:
        schema_extra = {
            "example": {
                "user_prompt": "Create a REST API for a task management system",
                "context": {"project": "HackMate", "tech_stack": "Python/FastAPI"},
                "priority": "normal"
            }
        }


class AgentInfo(BaseModel):
    """Model for agent information"""
    agent_name: str
    description: Optional[str] = None
    status: str = "active"
    created_at: Optional[str] = None


class OrchestrationResponse(BaseModel):
    """Response model for orchestration endpoint"""
    status: str = Field(..., description="Overall status of the orchestration")
    result: Optional[str] = Field(None, description="The orchestration result/response")
    active_agents: List[str] = Field(default_factory=list, description="List of active agent names")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")
    error: Optional[str] = Field(None, description="Error message if orchestration failed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the orchestration")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "result": "Task completed successfully with 3 agents",
                "active_agents": ["agent1", "agent2", "conflict_checker"],
                "execution_time": 15.5,
                "metadata": {"steps_completed": 5, "conflicts_resolved": 1}
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(..., description="Health status of the service")
    active_agents: int = Field(..., description="Number of active agents")
    agent_names: List[str] = Field(default_factory=list, description="Names of active agents")
    version: str = Field(default="1.0.0", description="API version")


class ErrorResponse(BaseModel):
    """Standard error response model"""
    status: str = Field(default="error", description="Error status")
    detail: str = Field(..., description="Error detail message")
    error_code: Optional[str] = Field(None, description="Application-specific error code")
    timestamp: Optional[str] = Field(None, description="Error timestamp")

    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "detail": "Orchestration failed due to invalid agent configuration",
                "error_code": "ORCH_001",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class AgentListResponse(BaseModel):
    """Response model for agents list endpoint"""
    active_agents: List[str] = Field(..., description="List of active agent names")
    count: int = Field(..., description="Total number of active agents")
    agents_info: Optional[List[AgentInfo]] = Field(None, description="Detailed information about agents")


class ConflictInfo(BaseModel):
    """Model for conflict information"""
    type: str = Field(..., description="Type of conflict")
    message: str = Field(..., description="Conflict description")
    suggestion: str = Field(..., description="Suggested resolution")


class ConflictAnalysisResponse(BaseModel):
    """Response model for conflict analysis"""
    has_conflict: bool = Field(..., description="Whether conflicts were detected")
    verdict: str = Field(..., description="Overall verdict (pass/needs_revision)")
    summary: str = Field(..., description="Summary of the analysis")
    conflicts: List[ConflictInfo] = Field(default_factory=list, description="List of detected conflicts")