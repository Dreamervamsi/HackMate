import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  // Check if message contains GitHub-related content
  const isGitHubMessage = message.content && (
    message.content.includes('GitHub') || 
    message.content.includes('branch') || 
    message.content.includes('commit') ||
    message.content.includes('repository')
  );

  // Check if message is a success/error message
  const isSuccess = message.content && message.content.includes('successfully');
  const isError = message.content && message.content.toLowerCase().includes('error');

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-lg p-4 ${
          isUser
            ? 'bg-blue-600 text-white'
            : isGitHubMessage
              ? isSuccess
                ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-200 border border-green-300 dark:border-green-700'
                : isError
                  ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-200 border border-red-300 dark:border-red-700'
                  : 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-200 border border-purple-300 dark:border-purple-700'
              : 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-100'
        }`}
      >
        {/* Message header with role and timestamp */}
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold opacity-75">
              {isUser ? 'You' : 'HackMate AI'}
            </span>
            {isGitHubMessage && (
              <span className="text-xs">🐙</span>
            )}
          </div>
          <span className="text-xs opacity-50">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>

        {/* Message content with markdown support */}
        <div className="prose prose-sm max-w-none dark:prose-invert">
          <ReactMarkdown
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '');
                return !inline && match ? (
                  <div className="relative group">
                    <button
                      onClick={() => copyToClipboard(String(children).replace(/\n$/, ''))}
                      className="absolute top-2 right-2 px-2 py-1 text-xs bg-gray-700 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      Copy
                    </button>
                    <SyntaxHighlighter
                      style={vscDarkPlus}
                      language={match[1]}
                      PreTag="div"
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  </div>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              },
              a({ node, children, ...props }) {
                return (
                  <a 
                    {...props}
                    className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 underline"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {children}
                  </a>
                );
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Copy button for non-code content */}
        {!isUser && (
          <button
            onClick={() => copyToClipboard(message.content)}
            className="mt-2 text-xs opacity-50 hover:opacity-100 transition-opacity"
          >
            Copy response
          </button>
        )}

        {/* GitHub-specific metadata */}
        {message.metadata?.githubOperation && (
          <div className="mt-2 pt-2 border-t border-current opacity-75">
            <p className="text-xs">
              GitHub Operation: {message.metadata.githubOperation}
            </p>
            {message.metadata.branchUrl && (
              <a 
                href={message.metadata.branchUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs underline hover:opacity-100"
              >
                View Branch →
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;