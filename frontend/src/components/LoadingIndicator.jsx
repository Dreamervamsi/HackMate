import React from 'react';

const LoadingIndicator = () => {
  return (
    <div className="flex items-center justify-center p-4">
      <div className="flex items-center space-x-2">
        <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-3 h-3 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        <span className="ml-2 text-gray-600 dark:text-gray-400 text-sm">
          HackMate is thinking...
        </span>
      </div>
    </div>
  );
};

export default LoadingIndicator;