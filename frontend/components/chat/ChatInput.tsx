import { useState, useRef, useEffect } from "react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSendMessage, disabled = false }: ChatInputProps) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const autoResize = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 300)}px`;
    }
  };

  useEffect(() => {
    autoResize();
  }, [input]);

  const handleSubmit = () => {
    const trimmedInput = input.trim();
    if (trimmedInput && !disabled) {
      onSendMessage(trimmedInput);
      setInput("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 pb-8">
      <div className="relative flex items-end bg-white rounded-2xl border border-gray-200 shadow-sm p-4">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask HackMate..."
          disabled={disabled}
          className="flex-1 resize-none bg-transparent text-gray-800 placeholder-gray-400 focus:outline-none min-w-[900px] min-h-[80px] max-h-[300px] px-3 py-3 text-base"
          rows={2}
          aria-label="Chat input"
        />
        <button
          onClick={handleSubmit}
          disabled={!input.trim() || disabled}
          className="ml-1 p-2 rounded-lg  bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
          aria-label="Send message"
        >
        </button>
      </div>
      <p className="text-center text-xs text-gray-400 mt-2">
        Press Enter to send, Shift + Enter for new line
      </p>
    </div>
  );
}
