# HackMate

HackMate is a multi-agent AI orchestration system that uses Google's Gemini AI to decompose complex tasks, coordinate specialized sub-agents, and implement solutions with automatic conflict detection and resolution.

## Architecture

HackMate implements a hierarchical multi-agent architecture with the following components:

### Orchestrator Agent
The central coordinator that:
- Receives user requests and asks for clarification when needed
- Decomposes tasks into independent sub-tasks
- Creates specialized sub-agents for each sub-task
- Coordinates the workflow from planning to implementation
- Manages the overall execution flow

### Sub-Agent System
Specialized agents that can be dynamically created with:
- Custom names and descriptions
- Specific system instructions for their domain
- Individual chat sessions and contexts
- Task-specific capabilities

### Conflict Detection & Resolution
A sophisticated conflict management system:
- **Conflict Checker**: Analyzes implementation plans for:
  - Overlapping work or duplicate effort
  - Conflicting file changes or responsibilities
  - Missing dependencies or bad sequencing
  - Incompatible interfaces, naming, or contracts
  - Scope mismatch between sub-tasks
  - Unclear assumptions or missing prerequisites

- **Conflict Resolver**: Automatically resolves detected conflicts by:
  - Generating consolidated, conflict-free implementation plans
  - Producing structured change recommendations
  - Maintaining task coherence across agents

### Implementation Pipeline
The complete workflow:
1. User submits a task to the Orchestrator
2. Orchestrator creates specialized sub-agents
3. Each sub-agent generates an implementation plan
4. Conflict Checker analyzes plans for issues
5. Conflict Resolver resolves any detected conflicts
6. Clean plans are executed by sub-agents
7. Final implementation results are returned

## Tech Stack

- **Python**: Core programming language
- **Google GenAI**: AI/ML framework for Gemini integration
- **python-dotenv**: Environment variable management
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation using Python type annotations
- **Gemini 2.5 Flash**: Primary AI model (configurable)

## Project Structure

```
HackMate/
├── src/
│   ├── orchestrator.py    # Main orchestration logic and workflow coordination
│   ├── agents.py          # Agent creation, plan generation, and conflict management
│   ├── tool_calls.py      # Tool call handling and implementation plan extraction
│   ├── config.py          # Configuration and API client initialization
│   ├── main.py            # FastAPI REST API application
│   ├── models.py          # Pydantic models for request/response validation
│   ├── middleware.py      # Custom middleware for error handling and logging
│   └── demo.py            # Demo script showing example usage
├── logs/                  # Application logs (created automatically)
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables file
├── .gitignore            # Git ignore patterns
├── test_api.py           # API testing script
├── API_DOCUMENTATION.md  # Detailed API documentation
└── README.md            # This file
```

### Key Components

- **orchestrator.py**: Contains the `orchestrate_agent()` function that manages the entire workflow, handles function calls, and coordinates between different agents.

- **agents.py**: Implements core agent functionality:
  - `create_agent()`: Creates new specialized agents
  - `generate_agent_plan()`: Gets implementation plans from agents
  - `check_agent_plan_conflict()`: Conflict detection logic
  - `conflict_resolver()`: Automatic conflict resolution
  - `implement_plan()`: Executes implementation plans

- **tool_calls.py**: Provides utility functions for processing tool calls and extracting implementation plans from agent responses.

- **config.py**: Handles configuration loading, environment variables, and Gemini client initialization.

- **main.py**: FastAPI REST API application that provides HTTP endpoints for orchestration, health checks, and agent management.

- **models.py**: Pydantic models for request/response validation and type safety.

- **middleware.py**: Custom middleware for error handling, request logging, and security headers.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd HackMate
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix/MacOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Running the Demo

The project includes a demo script that shows how to use the orchestration system:

```bash
python src/demo.py
```

The demo will create a multi-agent system to build two HTML pages for a handmade candle website, demonstrating the conflict detection and resolution capabilities.

### Running the REST API

The project now includes a REST API built with FastAPI for handling orchestration requests:

**Start the API server:**
```bash
# Development mode with auto-reload
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main script directly
cd src
python main.py
```

**API Endpoints:**
- `GET /` - API information and available endpoints
- `GET /health` - Health check and active agents status
- `GET /agents` - List all active agents
- `POST /orchestrate` - Main orchestration endpoint

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Example API Request:**
```bash
curl -X POST "http://localhost:8000/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "Create a simple REST API with user authentication",
    "priority": "high"
  }'
```

**Test the API:**
```bash
python test_api.py
```

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Usage Example

```python
from orchestrator import orchestrate_agent

# Define your task
task = """
Create a Python web application with:
- A Flask backend with user authentication
- A React frontend with a dashboard
- Database models for user management
"""

# Run the orchestration
result = orchestrate_agent(task)
print(result)
```

## Features

- **Dynamic Agent Creation**: Create specialized agents on-the-fly for different tasks
- **Automatic Conflict Detection**: Identifies potential issues before implementation
- **Intelligent Conflict Resolution**: Automatically resolves conflicts between agent plans
- **Flexible Architecture**: Easy to extend with new agent types and capabilities
- **Google Gemini Integration**: Leverages state-of-the-art AI for reasoning and implementation
- **Environment-based Configuration**: Secure API key management through environment variables
- **REST API**: FastAPI-based REST API for easy integration and testing
- **Comprehensive Error Handling**: Robust error handling with detailed error responses
- **Request Logging**: Detailed logging of all requests and responses
- **Security Features**: CORS support, security headers, and input validation

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_MODEL`: The Gemini model to use (default: `gemini-2.5-flash`)

### Model Selection

You can configure different Gemini models by setting the `GEMINI_MODEL` environment variable:
- `gemini-2.5-flash`: Fast, efficient model (default)
- `gemini-2.5-pro`: More capable, slower model
- Other Gemini models as they become available

## Development

### Adding New Agent Types

To add new specialized agent types, extend the `create_agent()` function in `agents.py` with custom system instructions for your specific use case.

### Extending Conflict Detection

The conflict detection logic in `check_agent_plan_conflict()` can be extended to handle additional conflict types specific to your domain.

## License

[Specify your license here]

## Contributing

[Specify your contribution guidelines here]