import React from 'react';
import ChatContainer from './components/ChatContainer';
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

  return (
    <div className="min-h-screen">
      <ChatContainer
        messages={messages}
        isLoading={isLoading}
        error={error}
        onSendMessage={sendMessage}
        onRetry={retryLastMessage}
        onDismissError={dismissError}
      />
      
      {/* Clear conversation button */}
      {messages.length > 0 && (
        <button
          onClick={clearConversation}
          className="fixed bottom-20 right-4 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors text-sm"
        >
          Clear Chat
        </button>
      )}
    </div>
  );
}

export default App;