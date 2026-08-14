# HackMate Frontend

A modern React-based chat interface for the HackMate AI orchestration system.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **React Markdown** - Markdown rendering for AI responses
- **React Syntax Highlighter** - Code syntax highlighting

## Features

- Clean, modern chat interface
- Real-time AI response streaming
- Markdown rendering with syntax highlighting
- Copy-to-clipboard functionality
- Conversation history persistence (localStorage)
- Backend health status monitoring
- Responsive design for mobile and desktop
- Dark mode support
- Error handling with retry functionality

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Running HackMate backend on http://localhost:8000

### Installation

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   Create a `.env` file in the frontend directory:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

   (You can copy from `.env.example`)

### Development

Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

### Production Build

Build for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── orchestratorAPI.js    # API client with axios
│   ├── components/
│   │   ├── ChatContainer.jsx     # Main chat interface
│   │   ├── MessageList.jsx       # Message display area
│   │   ├── MessageBubble.jsx     # Individual message component
│   │   ├── ChatInput.jsx         # Input field with send button
│   │   ├── LoadingIndicator.jsx  # Loading state display
│   │   ├── ErrorMessage.jsx      # Error display with retry
│   │   └── HealthStatus.jsx      # Backend health status
│   ├── hooks/
│   │   └── useChat.js            # Custom hook for chat logic
│   ├── utils/
│   │   └── formatters.js         # Utility functions
│   ├── App.jsx                   # Main application component
│   ├── main.jsx                  # React entry point
│   └── index.css                 # Global styles with Tailwind
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── .env.example                  # Environment variables template
```

## API Integration

The frontend communicates with the HackMate backend via the following endpoints:

- `POST /orchestrate` - Send user prompts for AI orchestration
- `GET /health` - Check backend health status
- `GET /agents` - Get list of active agents

## Usage

1. **Start the backend** (if not already running):
   ```bash
   cd backend
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open the chat interface**:
   Navigate to http://localhost:5173 in your browser

4. **Start chatting**:
   - Type your message in the input field
   - Press Enter or click Send to submit
   - Use Shift+Enter for new lines
   - View AI responses with markdown rendering
   - Copy code blocks or entire responses

## Features in Detail

### Message Display
- User messages appear on the right (blue)
- AI responses appear on the left (gray)
- Timestamps for each message
- Markdown rendering for formatted text
- Syntax highlighting for code blocks

### Input Features
- Auto-expanding textarea
- Enter to send, Shift+Enter for new line
- Disabled state during API calls
- Character limit validation

### State Management
- Conversation history saved to localStorage
- Auto-scroll to latest message
- Loading indicators during API calls
- Error handling with retry option

### Health Monitoring
- Real-time backend connection status
- Active agent count display
- Automatic health checks every 30 seconds
- Visual status indicators

## Customization

### API URL
Change the backend URL by modifying the `VITE_API_URL` in your `.env` file.

### Styling
The interface uses Tailwind CSS. Customize colors and styles by:
- Modifying `tailwind.config.js`
- Adding custom classes in components
- Extending the Tailwind theme

### Components
Each component is self-contained and can be customized independently:
- `MessageBubble.jsx` - Message appearance and formatting
- `ChatInput.jsx` - Input field behavior and validation
- `ChatContainer.jsx` - Overall layout and structure

## Troubleshooting

### Backend Connection Issues
- Ensure the backend is running on port 8000
- Check CORS configuration in backend
- Verify API URL in `.env` file

### Styling Issues
- Clear browser cache
- Restart development server
- Check Tailwind CSS configuration

### Build Issues
- Delete `node_modules` and reinstall dependencies
- Clear Vite cache: `rm -rf node_modules/.vite`
- Ensure Node.js version is 16+

## Development

### Adding New Features
1. Create new components in `src/components/`
2. Add custom hooks in `src/hooks/`
3. Update API calls in `src/api/orchestratorAPI.js`
4. Add utility functions in `src/utils/`

### Code Style
- Use functional components with hooks
- Follow React best practices
- Maintain consistent naming conventions
- Add comments for complex logic

## License

[Specify your license here]