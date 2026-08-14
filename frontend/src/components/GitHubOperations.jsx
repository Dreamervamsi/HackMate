import React, { useState } from 'react';
import { orchestratorAPI } from '../api/orchestratorAPI';

const GitHubOperations = ({ config }) => {
  const [activeTab, setActiveTab] = useState('branch');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Branch creation state
  const [branchName, setBranchName] = useState('');
  const [baseBranch, setBaseBranch] = useState(config.defaultBranch || 'main');

  // Commit state
  const [commitBranch, setCommitBranch] = useState('');
  const [commitMessage, setCommitMessage] = useState('');
  const [fileContent, setFileContent] = useState('');
  const [filePath, setFilePath] = useState('');

  const handleCreateBranch = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await orchestratorAPI.createGitHubBranch(
        config.repoUrl,
        branchName,
        baseBranch,
        config.githubToken
      );
      
      setResult({
        type: 'branch',
        success: response.success,
        message: response.message,
        data: response,
      });
      
      if (response.success) {
        setBranchName(''); // Reset on success
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCommit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const files = {};
      if (filePath && fileContent) {
        files[filePath] = fileContent;
      }

      const response = await orchestratorAPI.commitToGitHub(
        config.repoUrl,
        commitBranch,
        files,
        commitMessage,
        config.githubToken
      );
      
      setResult({
        type: 'commit',
        success: response.success,
        message: response.message,
        data: response,
      });
      
      if (response.success) {
        setFilePath('');
        setFileContent('');
        setCommitMessage('');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const isConfigValid = config.githubToken && config.repoUrl;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
        GitHub Operations
      </h3>

      {!isConfigValid && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 
                     rounded-md p-3 mb-4">
          <p className="text-sm text-yellow-800 dark:text-yellow-200">
            ⚠️ Please complete GitHub configuration to use these operations
          </p>
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 mb-4">
        <button
          onClick={() => setActiveTab('branch')}
          className={`px-4 py-2 text-sm font-medium transition-colors ${
            activeTab === 'branch'
              ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400'
              : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
          }`}
          disabled={!isConfigValid}
        >
          Create Branch
        </button>
        <button
          onClick={() => setActiveTab('commit')}
          className={`px-4 py-2 text-sm font-medium transition-colors ${
            activeTab === 'commit'
              ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400'
              : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
          }`}
          disabled={!isConfigValid}
        >
          Commit & Push
        </button>
      </div>

      {/* Branch Creation Tab */}
      {activeTab === 'branch' && (
        <form onSubmit={handleCreateBranch} className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Branch Name
            </label>
            <input
              type="text"
              value={branchName}
              onChange={(e) => setBranchName(e.target.value)}
              placeholder="feature/my-new-feature"
              required
              disabled={!isConfigValid || isLoading}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Base Branch
            </label>
            <input
              type="text"
              value={baseBranch}
              onChange={(e) => setBaseBranch(e.target.value)}
              placeholder="main"
              disabled={!isConfigValid || isLoading}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          <button
            type="submit"
            disabled={!isConfigValid || isLoading || !branchName}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 
                     disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Creating Branch...' : 'Create Branch'}
          </button>
        </form>
      )}

      {/* Commit Tab */}
      {activeTab === 'commit' && (
        <form onSubmit={handleCommit} className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Target Branch
            </label>
            <input
              type="text"
              value={commitBranch}
              onChange={(e) => setCommitBranch(e.target.value)}
              placeholder="feature/my-new-feature"
              required
              disabled={!isConfigValid || isLoading}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              File Path
            </label>
            <input
              type="text"
              value={filePath}
              onChange={(e) => setFilePath(e.target.value)}
              placeholder="src/example.py"
              required
              disabled={!isConfigValid || isLoading}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              File Content
            </label>
            <textarea
              value={fileContent}
              onChange={(e) => setFileContent(e.target.value)}
              placeholder="# Your code here"
              required
              disabled={!isConfigValid || isLoading}
              rows={6}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       disabled:opacity-50 disabled:cursor-not-allowed font-mono text-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Commit Message
            </label>
            <input
              type="text"
              value={commitMessage}
              onChange={(e) => setCommitMessage(e.target.value)}
              placeholder="Add new feature"
              required
              disabled={!isConfigValid || isLoading}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          <button
            type="submit"
            disabled={!isConfigValid || isLoading || !commitBranch || !filePath || !fileContent || !commitMessage}
            className="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 
                     disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Committing...' : 'Commit & Push'}
          </button>
        </form>
      )}

      {/* Results */}
      {result && (
        <div className={`mt-4 p-3 rounded-md ${
          result.success 
            ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800' 
            : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
        }`}>
          <div className="flex items-start">
            <span className="text-xl mr-2">{result.success ? '✅' : '❌'}</span>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                {result.message}
              </p>
              {result.data && result.success && result.data.branch_url && (
                <a 
                  href={result.data.branch_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 mt-1 block"
                >
                  View Branch →
                </a>
              )}
              {result.data && result.success && result.data.files_committed && (
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  Files committed: {result.data.files_committed.join(', ')}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
          <p className="text-sm text-red-800 dark:text-red-200">❌ {error}</p>
        </div>
      )}
    </div>
  );
};

export default GitHubOperations;