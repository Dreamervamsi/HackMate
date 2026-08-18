interface ErrorMessageProps {
  error: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  return (
    <div className="py-6">
      <div className="max-w-3xl mx-auto px-4">
        <div className="bg-gray-100 border border-gray-200 rounded-lg p-4">
          <p className="text-gray-700 text-sm mb-2">Something went wrong. Please try again.</p>
          {error && (
            <p className="text-gray-600 text-xs mb-3">{error}</p>
          )}
          {onRetry && (
            <button
              onClick={onRetry}
              className="text-sm text-gray-700 hover:text-gray-800 underline"
            >
              Retry
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
