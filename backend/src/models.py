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


class ValidationRequest(BaseModel):
    """Request model for code validation"""
    code: str = Field(..., description="Code to validate")
    language: str = Field(default="python", description="Programming language")
    max_attempts: int = Field(default=2, description="Maximum auto-fix attempts")


class ValidationResponse(BaseModel):
    """Response model for code validation"""
    success: bool = Field(..., description="Whether validation passed")
    validated_code: Optional[str] = Field(None, description="Validated/fixed code")
    original_code: Optional[str] = Field(None, description="Original code if validation failed")
    last_attempt_code: Optional[str] = Field(None, description="Last attempted code")
    test_results: Optional[str] = Field(None, description="Test execution results")
    error: Optional[str] = Field(None, description="Error message if validation failed")
    attempts: int = Field(..., description="Number of validation attempts")
    message: str = Field(..., description="Validation status message")


class BugResolutionRequest(BaseModel):
    """Request model for bug resolution"""
    code: str = Field(..., description="Code with bugs")
    test_results: str = Field(..., description="Test results showing errors")


class BugResolutionResponse(BaseModel):
    """Response model for bug resolution"""
    success: bool = Field(..., description="Whether bug resolution succeeded")
    fixed_code: Optional[str] = Field(None, description="Fixed code")
    error: Optional[str] = Field(None, description="Error message if resolution failed")
    message: str = Field(..., description="Resolution status message")


class TestGenerationRequest(BaseModel):
    """Request model for test generation"""
    code: str = Field(..., description="Code to generate tests for")
    language: str = Field(default="python", description="Programming language")


class TestGenerationResponse(BaseModel):
    """Response model for test generation"""
    success: bool = Field(..., description="Whether test generation succeeded")
    test_code: Optional[str] = Field(None, description="Generated test code")
    language: str = Field(..., description="Language of generated tests")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    message: str = Field(..., description="Generation status message")


class GitHubBranchRequest(BaseModel):
    """Request model for creating a GitHub branch"""
    repo_url: str = Field(..., description="GitHub repository URL (e.g., https://github.com/owner/repo)")
    branch_name: str = Field(..., description="Name for the new branch")
    base_branch: Optional[str] = Field(None, description="Base branch to create from (default: main)")
    github_token: Optional[str] = Field(None, description="GitHub personal access token (optional if set in config)")


class GitHubCommitRequest(BaseModel):
    """Request model for committing and pushing code to GitHub"""
    repo_url: str = Field(..., description="GitHub repository URL")
    branch_name: str = Field(..., description="Branch to commit to")
    files: Dict[str, str] = Field(..., description="Dictionary of file paths and their contents")
    commit_message: str = Field(..., description="Commit message")
    github_token: Optional[str] = Field(None, description="GitHub personal access token (optional if set in config)")


class GitHubBranchResponse(BaseModel):
    """Response model for GitHub branch creation"""
    success: bool = Field(..., description="Whether branch creation succeeded")
    branch_name: str = Field(..., description="Name of the created branch")
    branch_url: Optional[str] = Field(None, description="URL of the created branch")
    error: Optional[str] = Field(None, description="Error message if creation failed")
    message: str = Field(..., description="Operation status message")


class GitHubCommitResponse(BaseModel):
    """Response model for GitHub commit operations"""
    success: bool = Field(..., description="Whether commit/push succeeded")
    commit_sha: Optional[str] = Field(None, description="SHA of the created commit")
    branch_url: Optional[str] = Field(None, description="URL of the branch")
    files_committed: List[str] = Field(default_factory=list, description="List of committed file paths")
    error: Optional[str] = Field(None, description="Error message if operation failed")
    message: str = Field(..., description="Operation status message")