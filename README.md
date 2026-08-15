# HackMate

HackMate is a sophisticated multi-agent AI orchestration system with a modern web interface. It uses Google's Gemini AI to decompose complex tasks, coordinate specialized sub-agents, and implement solutions with automatic conflict detection and resolution. The system features a React frontend with real-time GitHub integration and a FastAPI backend with intelligent rate limiting.

## 🚀 Features

- **Multi-Agent Orchestration**: Hierarchical AI agent system with specialized sub-agents
- **Conflict Detection & Resolution**: Automatic identification and resolution of implementation conflicts
- **Modern Web Interface**: React-based frontend with real-time updates
- **GitHub Integration**: Direct GitHub repository operations (branch creation, code commits)
- **Smart Base Branch Detection**: Auto-detects repository branches (main/master/develop)
- **Rate Limiting**: Intelligent API call management to prevent quota exhaustion
- **Real-time Error Handling**: Comprehensive error management with user-friendly messages
- **Docker-based Validation**: Containerized code testing and validation

## 🏗️ Architecture

### System Components

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   React Frontend│         │  FastAPI Backend│         │  GitHub API     │
│                 │◄────────►│                 │◄────────►│                 │
│  - GitHub Panel │         │  - Orchestrator │         │  - Branch Ops  │
│  - Chat UI      │         │  - Agent System │         │  - File Commits │
│  - Config Mgmt  │         │  - Rate Limiting│         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                        │
                                        ▼
                              ┌─────────────────┐
                              │  Gemini AI      │
                              │                 │
                              │  - Task Planning│
                              │  - Code Gen     │
                              │  - Conflict Res │
                              └─────────────────┘
```

### Frontend (React + Vite)
- **GitHub Integration Panel**: Prominent repository URL input with validation
- **Smart Branch Operations**: Auto-detection of base branches for GitHub operations
- **Real-time Feedback**: Instant status updates and error messages
- **Responsive Design**: Modern UI with dark mode support
- **Chat Interface**: Interactive communication with the AI system

### Backend (FastAPI + Python)
- **Orchestrator Agent**: Central coordinator for task decomposition and agent management
- **Multi-Agent System**: Dynamic creation of specialized sub-agents
- **Conflict Management**: Automated detection and resolution of implementation conflicts
- **Rate Limiting**: 2-second delays between API calls to prevent quota exhaustion
- **GitHub Agent**: Direct GitHub API integration for repository operations
- **Validation Pipeline**: Docker-based code testing with automatic bug fixing

## 🛠️ Tech Stack

### Frontend
- **React 19**: Modern React with latest features
- **Vite 8**: Fast build tool and dev server
- **Tailwind CSS 4**: Utility-first CSS framework with PostCSS
- **Axios**: HTTP client for API communication
- **React Markdown**: Markdown rendering for AI responses
- **React Syntax Highlighter**: Code syntax highlighting

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Google GenAI**: Official Gemini AI SDK
- **PyGithub**: GitHub API library for repository operations
- **Python-dotenv**: Environment variable management
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for FastAPI

### AI & Testing
- **Gemini 2.5 Flash**: Primary AI model (configurable)
- **Docker**: Containerized code validation and testing
- **pytest**: Python testing framework

## 📁 Project Structure

```
HackMate/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatContainer.jsx      # Main chat interface
│   │   │   ├── GitHubConfig.jsx       # GitHub configuration panel
│   │   │   └── GitHubOperations.jsx   # GitHub operations UI
│   │   ├── api/
│   │   │   └── orchestratorAPI.js     # API client for backend
│   │   ├── hooks/
│   │   │   └── useChat.js            # Chat state management
│   │   ├── App.jsx                    # Main React component
│   │   ├── main.jsx                   # React entry point
│   │   └── index.css                  # Global styles with Tailwind
│   ├── package.json                   # Frontend dependencies
│   ├── postcss.config.js              # PostCSS configuration
│   └── .env.example                   # Frontend environment variables
├── backend/
│   ├── src/
│   │   ├── main.py                    # FastAPI application and routes
│   │   ├── orchestrator.py           # Main orchestration logic
│   │   ├── agents.py                 # Agent system and GitHub operations
│   │   ├── tool_calls.py             # Tool call handling
│   │   ├── config.py                 # Configuration and rate limiting
│   │   ├── models.py                 # Pydantic data models
│   │   └── middleware.py             # Custom middleware
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Backend environment variables
│   └── .env                         # Backend environment (API keys)
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

## 🚀 Getting Started

### Prerequisites

- **Node.js 18+** (for frontend)
- **Python 3.8+** (for backend)
- **Google Gemini API Key**
- **GitHub Personal Access Token** (for GitHub operations)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dreamervamsi/HackMate.git
   cd HackMate
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   # On Unix/MacOS:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Configure Backend Environment**
   Create a `.env` file in the `backend` directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   GITHUB_TOKEN=your_github_token_here
   GITHUB_DEFAULT_BRANCH=main
   ```

   Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   
   Create a GitHub token from GitHub Settings → Developer settings → Personal access tokens

4. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Configure Frontend Environment**
   Create a `.env` file in the `frontend` directory:
   ```env
   VITE_API_URL=http://localhost:8080
   ```

### Running the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Unix/MacOS
python -m uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs

## 💡 Usage

### Basic Chat Interaction

1. Open the frontend in your browser
2. Type your task in the chat interface
3. The AI will break down the task and coordinate multiple agents
4. View the real-time progress and final results

### GitHub Integration

1. Click the GitHub button (🐙) in the top-right corner
2. Enter your GitHub repository URL in the prominent input field
3. Add your GitHub Personal Access Token
4. Use the GitHub Operations panel to:
   - **Create Branch**: Automatically detects base branch and creates new branches
   - **Commit & Push**: Push code changes to your repository

### API Usage

You can also interact with the backend directly via API:

```bash
# Health check
curl http://localhost:8080/health

# Get active agents
curl http://localhost:8080/agents

# Orchestrate a task
curl -X POST http://localhost:8080/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"user_prompt": "Create a simple web server"}'

# Create GitHub branch
curl -X POST http://localhost:8080/github/branch \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/owner/repo",
    "branch_name": "feature/new-feature",
    "github_token": "your_token"
  }'
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_MODEL`: Gemini model to use (default: `gemini-2.5-flash`)
- `GITHUB_TOKEN`: GitHub personal access token (optional, can be provided in UI)
- `GITHUB_DEFAULT_BRANCH`: Default branch name (default: `main`)

**Frontend (.env):**
- `VITE_API_URL`: Backend API URL (default: `http://localhost:8080`)

### Rate Limiting

The system implements automatic rate limiting to prevent API quota exhaustion:
- **2-second delay** between Gemini API calls
- **1-second delay** between orchestrator function calls
- **Automatic retry** with clear error messages when limits are reached

### Model Selection

Available Gemini models:
- `gemini-2.5-flash`: Fast, efficient model (default, recommended)
- `gemini-2.5-pro`: More capable, slower model
- Other Gemini models as they become available

## 🎯 Key Features Explained

### Smart GitHub Branch Detection
The system automatically detects the correct base branch for your repository:
- First tries the repository's default branch
- Falls back to common names: `main`, `master`, `develop`
- Provides clear error messages with available branches if none match

### Conflict Resolution Pipeline
1. **Plan Generation**: Each agent creates an implementation plan
2. **Conflict Detection**: Analyzes plans for overlapping work, dependencies, and inconsistencies
3. **Automatic Resolution**: Generates consolidated, conflict-free plans
4. **Implementation**: Executes clean plans with validation

### Code Validation
- **Docker Integration**: Tests code in isolated containers
- **Automatic Bug Fixing**: Attempts to fix issues up to 2 times
- **Comprehensive Testing**: Includes unit tests and integration tests

## 🛡️ Security

- **Environment Variables**: Sensitive data stored in `.env` files (never committed)
- **GitHub Token Security**: Tokens can be provided per-session or stored securely
- **API Rate Limiting**: Prevents API abuse and quota exhaustion
- **CORS Configuration**: Configurable cross-origin resource sharing

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify your `.env` file has valid API keys

**Frontend styling not working:**
- Ensure Node.js 18+ is installed
- Run `npm install` to install all dependencies
- Check that PostCSS is configured correctly

**GitHub operations failing:**
- Verify your GitHub token has the `repo` scope
- Check that the repository URL is correct
- Ensure the repository exists and you have access

**Rate limit errors:**
- The system automatically handles rate limits
- Wait for the suggested retry time
- Consider upgrading your Gemini API plan for higher quotas

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Google Gemini** for providing the AI capabilities
- **FastAPI** for the excellent web framework
- **React** for the modern frontend library
- **GitHub** for the repository management tools

## 📞 Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.