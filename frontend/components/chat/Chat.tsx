"use client";

import { useState, useRef, useEffect } from "react";
import { Message } from "@/types/chat";
import { sendChatMessage } from "@/lib/api/chat";
import ChatHeader from "./ChatHeader";
import EmptyState from "./EmptyState";
import MessageList from "./MessageList";
import ChatInput from "./ChatInput";
import LoadingMessage from "./LoadingMessage";
import ErrorMessage from "./ErrorMessage";
import Sidebar from "./Sidebar";

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUserMessage, setLastUserMessage] = useState<string>("");
  const [githubToken, setGithubToken] = useState<string>("");
  const [githubRepo, setGithubRepo] = useState<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleCredentialsChange = (token: string, repo: string) => {
    setGithubToken(token);
    setGithubRepo(repo);
  };

  const handleSendMessage = async (content: string) => {
    if (isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      createdAt: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLastUserMessage(content);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendChatMessage(
        content,
        messages,
        {
          github_token: githubToken,
          github_repo: githubRepo,
        }
      );

      if (response.status === "success" && response.result) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: response.result,
          createdAt: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        throw new Error(response.error || "Failed to get response");
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Unknown error occurred";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastUserMessage) {
      handleSendMessage(lastUserMessage);
    }
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar onCredentialsChange={handleCredentialsChange} />
      
      <div className="flex-1 flex flex-col">
        <ChatHeader />
        
        <div className="flex-1 overflow-hidden">
          {!hasMessages && !isLoading ? (
            <EmptyState />
          ) : (
            <div className="h-full overflow-y-auto">
              <MessageList messages={messages} />
              {isLoading && <LoadingMessage />}
              {error && <ErrorMessage error={error} onRetry={handleRetry} />}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
