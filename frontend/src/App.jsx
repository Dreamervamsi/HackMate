import React, { useState } from 'react';
import ChatContainer from './components/ChatContainer';
import GitHubConfig from './components/GitHubConfig';
import GitHubOperations from './components/GitHubOperations';
import { useChat } from './hooks/useChat';

function App() {
  const {
    messages,
    isLoading,
    error,
    sendMessage,
    retryLastMessage,
    clearConversation,
    dismissError,
  } = useChat();

  const [githubConfig, setGithubConfig] = useState({});
  const [showGitHubPanel, setShowGitHubPanel] = useState(false);

  const handleConfigChange = (config) => {
    setGithubConfig(config);
  };

  return (
    <div className="min-h-screen flex">
      {/* Main Chat Area */}
      <div className={`flex-1 transition-all duration-300 ${showGitHubPanel ? 'mr-80' : ''}`}>
        <ChatContainer
          messages={messages}
          isLoading={isLoading}
          error={error}
          onSendMessage={sendMessage}
          onRetry={retryLastMessage}
          onDismissError={dismissError}
          githubConfig={githubConfig}
        />
        
        {/* Clear conversation button */}
        {messages.length > 0 && (
          <button
            onClick={clearConversation}
            className="fixed bottom-20 right-4 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors text-sm z-10"
          >
            Clear Chat
          </button>
        )}

        {/* GitHub Panel Toggle Button */}
        <button
          onClick={() => setShowGitHubPanel(!showGitHubPanel)}
          className="fixed top-4 right-4 px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-600 transition-colors text-sm z-10 flex items-center space-x-2"
        >
          <span>🐙</span>
          <span>{showGitHubPanel ? 'Hide GitHub' : 'GitHub'}</span>
        </button>
      </div>

      {/* GitHub Side Panel */}
      {showGitHubPanel && (
        <div className="w-80 bg-gray-100 dark:bg-gray-900 border-l border-gray-200 dark:border-gray-700 
                      overflow-y-auto h-screen fixed right-0 top-0 transition-all duration-300 z-20">
          <div className="p-4 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                GitHub Integration
              </h2>
              <button
                onClick={() => setShowGitHubPanel(false)}
                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                ✕
              </button>
            </div>

            <GitHubConfig onConfigChange={handleConfigChange} initialConfig={githubConfig} />
            <GitHubOperations config={githubConfig} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;