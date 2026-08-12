# HackMate Orchestrator API Documentation

## Overview

The HackMate Orchestrator API is a REST API built with FastAPI that handles agent orchestration and task coordination. It processes user prompts, coordinates multiple AI agents, manages conflict detection and resolution, and returns implementation results.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Root Endpoint
**GET /**

Returns basic API information and available endpoints.

**Response:**
```json
{
  "message": "HackMate Orchestrator API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "health": "/health",
    "orchestrate": "/orchestrate",
    "agents": "/agents",
    "docs": "/docs"
  }
}
```

### 2. Health Check
**GET /health**

Checks the health status of the API and returns information about active agents.

**Response:**
```json
{
  "status": "healthy",
  "active_agents": 3,
  "agent_names": ["agent1", "agent2", "conflict_checker"],
  "version": "1.0.0"
}
```

**Error Response:**
```json
{
  "status": "error",
  "detail": "Service unhealthy",
  "error_code": "HTTP_503",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 3. Get Active Agents
**GET /agents**

Returns a list of all currently active agents.

**Response:**
```json
{
  "active_agents": ["agent1", "agent2", "conflict_checker"],
  "count": 3
}
```

**Error Response:**
```json
{
  "status": "error",
  "detail": "Failed to retrieve agents: ...",
  "error_code": "HTTP_500",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 4. Orchestrate Task
**POST /orchestrate**

Main endpoint for orchestrating tasks. This endpoint processes user prompts, coordinates multiple agents, and returns implementation results.

**Request Body:**
```json
{
  "user_prompt": "Create a REST API for a task management system",
  "context": {
    "project": "HackMate",
    "tech_stack": "Python/FastAPI"
  },
  "priority": "normal"
}
```

**Request Parameters:**
- `user_prompt` (required): The task description (1-10,000 characters)
- `context` (optional): Additional context for the task
- `priority` (optional): Task priority - "low", "normal", "high", or "urgent" (default: "normal")

**Success Response:**
```json
{
  "status": "success",
  "result": "Task completed successfully with implementation details...",
  "active_agents": ["agent1", "agent2", "conflict_checker"],
  "execution_time": 15.5,
  "metadata": {
    "priority": "normal",
    "context_provided": true,
    "original_prompt_length": 50
  }
}
```

**Error Responses:**

**400 Bad Request (Validation Error):**
```json
{
  "status": "error",
  "detail": "user_prompt is required in request body",
  "error_code": "HTTP_400",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "detail": "Orchestration failed: ...",
  "error_code": "HTTP_500",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Error Codes

| Error Code | Description |
|------------|-------------|
| HTTP_400 | Bad Request - Invalid input or validation error |
| HTTP_500 | Internal Server Error - Unexpected server error |
| HTTP_503 | Service Unavailable - Service health check failed |
| VALIDATION_ERROR | Input validation failed |
| INTERNAL_ERROR | Unexpected internal error |

## Request/Response Models

### OrchestrationRequest
```typescript
{
  user_prompt: string        // Required, 1-10000 chars
  context?: object          // Optional additional context
  priority?: string         // Optional: "low", "normal", "high", "urgent"
}
```

### OrchestrationResponse
```typescript
{
  status: string            // "success" or "error"
  result?: string           // Implementation result
  active_agents: string[]   // List of active agent names
  execution_time?: number   // Execution time in seconds
  error?: string            // Error message if failed
  metadata?: object         // Additional metadata
}
```

### HealthResponse
```typescript
{
  status: string            // "healthy" or "unhealthy"
  active_agents: number     // Count of active agents
  agent_names: string[]     // Names of active agents
  version: string           // API version
}
```

### AgentListResponse
```typescript
{
  active_agents: string[]   // List of agent names
  count: number             // Total count of agents
}
```

## Running the API

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Configuration
Set up your environment variables in a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

### Start the Server
```bash
# Development mode with auto-reload
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using the Main Script
```bash
cd src
python main.py
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Features

### Error Handling
- Comprehensive error handling middleware
- Consistent error response format
- Detailed error logging
- HTTP status code mapping

### Logging
- Request/response logging
- Error-specific log files
- Structured log format
- Console and file output

### Security
- CORS support
- Security headers (XSS protection, content type options, etc.)
- Input validation
- SQL injection prevention (when database is added)

### Performance
- Request timing tracking
- Efficient response collection
- Concurrent request handling
- Middleware-based processing

## Orchestration Flow

1. **Request Validation**: Validates the incoming request structure and content
2. **Agent Creation**: Creates necessary agents for the task
3. **Plan Generation**: Each agent generates an implementation plan
4. **Conflict Detection**: Automatically checks for conflicts in plans
5. **Conflict Resolution**: Resolves any detected conflicts
6. **Implementation**: Executes the clean implementation plan
7. **Code Validation**: Automatically validates implemented code using Docker containers
8. **Test Generation**: Generates comprehensive tests for the code
9. **Bug Detection**: Runs tests in isolated Docker environments
10. **Auto-Fix Loop**: Automatically fixes bugs up to 2 times if validation fails
11. **Response Collection**: Gathers validated results and returns them

## Example Usage

### cURL Example
```bash
curl -X POST "http://localhost:8000/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "Create a simple REST API with user authentication",
    "priority": "high"
  }'
```

### Python Example
```python
import requests

response = requests.post(
    "http://localhost:8000/orchestrate",
    json={
        "user_prompt": "Create a simple REST API with user authentication",
        "context": {"project": "MyApp"},
        "priority": "high"
    }
)

print(response.json())
```

### JavaScript Example
```javascript
fetch('http://localhost:8000/orchestrate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_prompt: 'Create a simple REST API with user authentication',
    priority: 'high'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Monitoring

### Logs
- **General logs**: `backend/logs/orchestrator_api.log`
- **Error logs**: `backend/logs/orchestrator_api_errors.log`

### Health Monitoring
Use the `/health` endpoint to monitor service status and active agents.

### Performance Metrics
- Execution time is included in orchestration responses
- Request processing time is added as a response header (`X-Process-Time`)

## Troubleshooting

### Common Issues

**Issue**: "GEMINI_API_KEY environment variable is not set"
- **Solution**: Ensure your `.env` file contains the `GEMINI_API_KEY`

**Issue**: "Agent client has not been initialized"
- **Solution**: Check that your API key is valid and the Gemini service is accessible

**Issue**: Orchestration takes too long
- **Solution**: Consider breaking down complex tasks into smaller sub-tasks

## Future Enhancements

- [ ] Add authentication and authorization
- [ ] Implement rate limiting
- [ ] Add request queuing for high-load scenarios
- [ ] Implement caching for repeated requests
- [ ] Add WebSocket support for real-time updates
- [ ] Add database integration for persistence
- [ ] Implement request history and replay
- [ ] Add more detailed analytics and monitoring

## Code Validation Phase

### Overview

The HackMate Orchestrator now includes an automatic code validation phase that runs after implementation. This phase ensures that all generated code is tested, validated, and automatically fixed if bugs are detected.

### Validation Components

#### 1. Bug Resolver Agent
- **Purpose**: Fixes syntax, logical, and deprecation errors in code
- **Input**: Code with bugs + test results showing errors
- **Output**: Clean, bug-free code
- **Capabilities**:
  - Syntax error correction
  - Logical error fixing
  - Module deprecation updates
  - Import error resolution
  - Runtime error handling
  - Test failure resolution

#### 2. Test Generation Agent
- **Purpose**: Generates comprehensive tests for implemented code
- **Input**: Code to test + programming language
- **Output**: Complete test suite
- **Features**:
  - Unit test generation
  - Edge case coverage
  - Positive/negative test cases
  - Error handling tests
  - Framework-specific tests (pytest for Python)

#### 3. Python Validation Agent
- **Purpose**: Validates Python code in isolated Docker containers
- **Environment**: `python:3.11-slim` Docker image
- **Security Features**:
  - Network isolation (`--network none`)
  - Memory limits (512MB)
  - CPU limits (1.0 core)
  - Ephemeral containers (`--rm`)
  - Non-root user execution
- **Tools Available**: pytest, flake8, mypy, black, pylint, bandit, safety

#### 4. Validation Workflow
- **Auto-Fix Loop**: Automatically attempts to fix bugs up to 2 times
- **Process**:
  1. Generate comprehensive tests
  2. Run code + tests in Docker container
  3. Analyze test results for errors
  4. If errors detected, use Bug Resolver Agent
  5. Re-validate with fixed code
  6. Repeat up to 2 times if needed
  7. Return validated code or error report

### Validation Response Format

#### Successful Validation
```json
{
  "success": true,
  "validated_code": "clean, bug-free code",
  "test_results": "All tests passed",
  "attempts": 1,
  "message": "Code validated successfully"
}
```

#### Failed Validation
```json
{
  "success": false,
  "original_code": "original buggy code",
  "last_attempt_code": "last attempted fix",
  "error": "Validation error details",
  "attempts": 2,
  "message": "Validation failed after 2 attempts"
}
```

### Docker Setup

#### Build Validation Containers
```bash
cd backend/docker/validation
docker-compose build
```

#### Start Validation Containers
```bash
docker-compose up -d
```

#### Container Configuration
- **Image**: `hackmate/python-validator:latest`
- **Network**: Internal bridge network (isolated)
- **Resources**: 1 CPU core, 512MB memory limit
- **Security**: Non-root user, read-only filesystem

### Integration with Orchestration

The validation phase is automatically integrated into the orchestration workflow:

1. After `implement_plan` completes successfully
2. Orchestrator calls `validate_code_with_autofix` with:
   - `code`: The implemented code
   - `language`: Programming language (default: python)
   - `max_attempts`: Maximum fix attempts (default: 2)
3. Validation runs automatically with Docker isolation
4. Bugs are auto-fixed if detected
5. Final validated code is returned to the user

### Validation API Models

#### ValidationRequest
```typescript
{
  code: string           // Code to validate
  language: string       // Programming language (default: "python")
  max_attempts: number   // Maximum auto-fix attempts (default: 2)
}
```

#### ValidationResponse
```typescript
{
  success: boolean                    // Validation passed/failed
  validated_code?: string             // Fixed code if successful
  original_code?: string              // Original code if failed
  last_attempt_code?: string         // Last attempted fix
  test_results?: string              // Test execution output
  error?: string                     // Error message if failed
  attempts: number                   // Number of attempts made
  message: string                    // Status message
}
```

#### BugResolutionRequest
```typescript
{
  code: string           // Code with bugs
  test_results: string   // Test results showing errors
}
```

#### BugResolutionResponse
```typescript
{
  success: boolean        // Resolution succeeded/failed
  fixed_code?: string     // Fixed code if successful
  error?: string          // Error message if failed
  message: string         // Status message
}
```

### Security Considerations

- **Network Isolation**: Validation containers have no external network access
- **Resource Limits**: CPU and memory constraints prevent resource exhaustion
- **Ephemeral Containers**: Containers are automatically removed after execution
- **Non-root Execution**: Code runs as non-privileged user
- **Timeout Protection**: 30-second timeout prevents infinite loops

### Troubleshooting Validation

#### Docker Not Available
```json
{
  "success": false,
  "error": "Docker is not installed or not running. Code validation requires Docker."
}
```

**Solution**: Ensure Docker is installed and running:
```bash
docker --version
```

#### Validation Timeout
```json
{
  "success": false,
  "error": "Validation failed: Code execution timed out (possible infinite loop)."
}
```

**Solution**: Check code for infinite loops or long-running operations

#### Max Attempts Reached
```json
{
  "success": false,
  "message": "Validation failed after 2 attempts"
}
```

**Solution**: Review the error details and manually fix the code, or increase `max_attempts`