import React from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import LoadingIndicator from './LoadingIndicator';
import ErrorMessage from './ErrorMessage';
import HealthStatus from './HealthStatus';

const ChatContainer = ({
  messages,
  isLoading,
  error,
  onSendMessage,
  onRetry,
  onDismissError,
  githubConfig,
}) => {
  const handleSendMessage = (message) => {
    // Pass GitHub context if available
    const githubContext = githubConfig && githubConfig.githubToken && githubConfig.repoUrl 
      ? {
          repoUrl: githubConfig.repoUrl,
          defaultBranch: githubConfig.defaultBranch,
        }
      : null;
    
    onSendMessage(message, githubContext);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-2">
          <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
            HackMate AI
          </h1>
          {githubConfig && githubConfig.githubToken && githubConfig.repoUrl && (
            <span className="text-xs bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-200 px-2 py-1 rounded-full">
              🐙 GitHub Ready
            </span>
          )}
        </div>
        <HealthStatus />
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} />
        
        {isLoading && <LoadingIndicator />}
        
        {error && (
          <ErrorMessage
            error={error}
            onRetry={onRetry}
            onDismiss={onDismissError}
          />
        )}
      </div>

      {/* Input area */}
      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
};

export default ChatContainer;