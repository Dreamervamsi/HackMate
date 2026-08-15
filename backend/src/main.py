from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any
import sys
import os
import time

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import orchestrate_agent
from agents import active_agents, create_github_branch, commit_and_push_to_github
from models import (
    OrchestrationRequest,
    OrchestrationResponse,
    HealthResponse,
    AgentListResponse,
    GitHubBranchRequest,
    GitHubBranchResponse,
    GitHubCommitRequest,
    GitHubCommitResponse
)
from middleware import (
    ErrorHandlingMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware
)

# Configure logging
def setup_logging():
    """Configure comprehensive logging for the application"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            # Console handler
            logging.StreamHandler(sys.stdout),
            # File handler for all logs
            logging.FileHandler(os.path.join(logs_dir, 'orchestrator_api.log'))
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    return logger

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Orchestrator API...")
    yield
    # Shutdown
    logger.info("Shutting down Orchestrator API...")
    logger.info(f"Active agents at shutdown: {list(active_agents.keys())}")


# Create FastAPI app
app = FastAPI(
    title="HackMate Orchestrator API",
    description="REST API for handling agent orchestration and task coordination",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware layers
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "HackMate Orchestrator API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "orchestrate": "/orchestrate",
            "agents": "/agents",
            "github_branch": "/github/branch",
            "github_commit": "/github/commit",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        return HealthResponse(
            status="healthy",
            active_agents=len(active_agents),
            agent_names=list(active_agents.keys())
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )


@app.get("/agents", response_model=AgentListResponse)
async def get_agents():
    """Get list of active agents"""
    try:
        return AgentListResponse(
            active_agents=list(active_agents.keys()),
            count=len(active_agents)
        )
    except Exception as e:
        logger.error(f"Failed to get agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve agents: {str(e)}"
        )

@app.post("/orchestrate", response_model=OrchestrationResponse)
async def orchestrate_endpoint(request: OrchestrationRequest):
    start_time = time.time()
    
    try:
        user_prompt = request.user_prompt
        context = request.context or {}
        priority = request.priority
        
        logger.info(f"Received orchestration request (priority: {priority}): {user_prompt[:100]}...")
        logger.info(f"Additional context: {context}")
        
        # Process the orchestration
        result = orchestrate_agent(user_prompt)
        
        execution_time = time.time() - start_time
        logger.info(f"Orchestration completed successfully in {execution_time:.2f}s")
        
        return OrchestrationResponse(
            status="success",
            result=result,
            active_agents=list(active_agents.keys()),
            execution_time=execution_time,
            metadata={
                "priority": priority,
                "context_provided": bool(context),
                "original_prompt_length": len(user_prompt)
            }
        )
        
    except ValueError as e:
        execution_time = time.time() - start_time
        logger.error(f"Validation error after {execution_time:.2f}s: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        execution_time = time.time() - start_time
        error_str = str(e)
        
        # Handle rate limit errors specifically
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
            logger.error(f"Rate limit error after {execution_time:.2f}s: {e}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="API rate limit exceeded. Please wait a moment and try again. The free tier has limited quota."
            )
        
        logger.error(f"Orchestration error after {execution_time:.2f}s: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Orchestration failed: {str(e)}"
        )


@app.post("/github/branch", response_model=GitHubBranchResponse)
async def create_github_branch_endpoint(request: GitHubBranchRequest):
    """Create a new branch in a GitHub repository"""
    try:
        logger.info(f"Creating GitHub branch '{request.branch_name}' in {request.repo_url}")
        
        result = create_github_branch(
            repo_url=request.repo_url,
            branch_name=request.branch_name,
            base_branch=request.base_branch,
            github_token=request.github_token
        )
        
        if result.get("success"):
            logger.info(f"Successfully created branch '{request.branch_name}'")
        else:
            logger.warning(f"Failed to create branch: {result.get('error')}")
        
        return GitHubBranchResponse(**result)
        
    except Exception as e:
        logger.error(f"GitHub branch creation error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"GitHub branch creation failed: {str(e)}"
        )


@app.post("/github/commit", response_model=GitHubCommitResponse)
async def commit_to_github_endpoint(request: GitHubCommitRequest):
    """Commit and push files to a GitHub repository branch"""
    try:
        logger.info(f"Committing {len(request.files)} files to '{request.branch_name}' in {request.repo_url}")
        
        result = commit_and_push_to_github(
            repo_url=request.repo_url,
            branch_name=request.branch_name,
            files=request.files,
            commit_message=request.commit_message,
            github_token=request.github_token
        )
        
        if result.get("success"):
            logger.info(f"Successfully committed {len(result.get('files_committed', []))} files")
        else:
            logger.warning(f"Failed to commit files: {result.get('error')}")
        
        return GitHubCommitResponse(**result)
        
    except Exception as e:
        logger.error(f"GitHub commit error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"GitHub commit failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    from datetime import datetime
    error_response = {
        "status": "error",
        "detail": "An unexpected error occurred",
        "error_code": "INTERNAL_ERROR",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )