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
}) => {
  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
          HackMate AI
        </h1>
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
      <ChatInput onSendMessage={onSendMessage} disabled={isLoading} />
    </div>
  );
};

export default ChatContainer;