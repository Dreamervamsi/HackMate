import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-lg p-4 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-100'
        }`}
      >
        {/* Message header with role and timestamp */}
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold opacity-75">
            {isUser ? 'You' : 'HackMate AI'}
          </span>
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
      </div>
    </div>
  );
};

export default MessageBubble;