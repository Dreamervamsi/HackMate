import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import type { Message } from "@/types/chat";

interface MessageProps {
  message: Message;
}

export default function Message({ message }: MessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`py-6 ${isUser ? "bg-gray-50" : ""}`}>
      <div className="max-w-3xl mx-auto px-4">
        {isUser ? (
          <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
            <p className="text-gray-800 whitespace-pre-wrap">{message.content}</p>
          </div>
        ) : (
          <div className="prose prose-gray max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeHighlight]}
              components={{
                // Custom code block styling
                code({ className, children, ...props }: any) {
                  const match = /language-(\w+)/.exec(className || "");
                  const isInline = !match;
                  return !isInline ? (
                    <code
                      className={`block bg-gray-100 rounded-lg p-4 text-sm overflow-x-auto ${className || ""}`}
                      {...props}
                    >
                      {children}
                    </code>
                  ) : (
                    <code
                      className="bg-gray-100 px-1.5 py-0.5 rounded text-sm"
                      {...props}
                    >
                      {children}
                    </code>
                  );
                },
                // Custom paragraph styling
                p: ({ children }) => (
                  <p className="text-gray-700 mb-4 leading-relaxed">{children}</p>
                ),
                // Custom heading styling
                h1: ({ children }) => (
                  <h1 className="text-2xl font-semibold text-gray-800 mt-6 mb-4">
                    {children}
                  </h1>
                ),
                h2: ({ children }) => (
                  <h2 className="text-xl font-semibold text-gray-800 mt-5 mb-3">
                    {children}
                  </h2>
                ),
                h3: ({ children }) => (
                  <h3 className="text-lg font-medium text-gray-800 mt-4 mb-2">
                    {children}
                  </h3>
                ),
                // Custom list styling
                ul: ({ children }) => (
                  <ul className="list-disc list-inside text-gray-700 mb-4 space-y-1">
                    {children}
                  </ul>
                ),
                ol: ({ children }) => (
                  <ol className="list-decimal list-inside text-gray-700 mb-4 space-y-1">
                    {children}
                  </ol>
                ),
                // Custom link styling
                a: ({ children, href }) => (
                  <a
                    href={href}
                    className="text-blue-600 hover:text-blue-700 underline"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {children}
                  </a>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
