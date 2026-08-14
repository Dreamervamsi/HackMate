import { useState, useCallback, useEffect } from 'react';
import { orchestratorAPI } from '../api/orchestratorAPI';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load messages from localStorage on mount
  useEffect(() => {
    const savedMessages = localStorage.getItem('hackmate_messages');
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (err) {
        console.error('Failed to load saved messages:', err);
      }
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('hackmate_messages', JSON.stringify(messages));
  }, [messages]);

  const sendMessage = useCallback(async (userPrompt) => {
    setIsLoading(true);
    setError(null);

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: userPrompt,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      // Send prompt to backend
      const response = await orchestratorAPI.sendPrompt(userPrompt);

      // Add AI response to the chat
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.result || 'No response received from HackMate',
        timestamp: new Date().toISOString(),
        metadata: {
          executionTime: response.execution_time,
          activeAgents: response.active_agents,
        },
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      setError(err.message);
      
      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Error: ${err.message}`,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const retryLastMessage = useCallback(() => {
    if (messages.length > 0) {
      const lastUserMessage = [...messages]
        .reverse()
        .find((msg) => msg.role === 'user');
      
      if (lastUserMessage) {
        // Remove the last error message if it exists
        setMessages((prev) => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage.role === 'assistant' && lastMessage.content.startsWith('Error:')) {
            return prev.slice(0, -1);
          }
          return prev;
        });
        
        // Retry the last user message
        sendMessage(lastUserMessage.content);
      }
    }
  }, [messages, sendMessage]);

  const clearConversation = useCallback(() => {
    setMessages([]);
    setError(null);
    localStorage.removeItem('hackmate_messages');
  }, []);

  const dismissError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    retryLastMessage,
    clearConversation,
    dismissError,
  };
};