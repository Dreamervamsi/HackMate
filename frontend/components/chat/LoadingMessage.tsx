export default function LoadingMessage() {
  return (
    <div className="py-6">
      <div className="max-w-3xl mx-auto px-4">
        <div className="flex items-center space-x-2 text-gray-500">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: "0.2s" }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: "0.4s" }} />
          </div>
          <span className="text-sm">HackMate is thinking...</span>
        </div>
      </div>
    </div>
  );
}
