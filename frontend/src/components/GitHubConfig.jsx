import React, { useState, useEffect } from 'react';

const GitHubConfig = ({ onConfigChange, initialConfig = {} }) => {
  const [config, setConfig] = useState({
    githubToken: initialConfig.githubToken || '',
    repoUrl: initialConfig.repoUrl || '',
    defaultBranch: initialConfig.defaultBranch || 'main',
  });

  const [showToken, setShowToken] = useState(false);

  useEffect(() => {
    // Load saved config from localStorage
    const savedConfig = localStorage.getItem('github_config');
    if (savedConfig) {
      try {
        const parsed = JSON.parse(savedConfig);
        setConfig(prev => ({ ...prev, ...parsed }));
        if (onConfigChange) {
          onConfigChange(parsed);
        }
      } catch (err) {
        console.error('Failed to load saved GitHub config:', err);
      }
    }
  }, [onConfigChange]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newConfig = { ...config, [name]: value };
    setConfig(newConfig);
    
    // Save to localStorage
    localStorage.setItem('github_config', JSON.stringify(newConfig));
    
    if (onConfigChange) {
      onConfigChange(newConfig);
    }
  };

  const handleClearConfig = () => {
    const clearedConfig = {
      githubToken: '',
      repoUrl: '',
      defaultBranch: 'main',
    };
    setConfig(clearedConfig);
    localStorage.removeItem('github_config');
    if (onConfigChange) {
      onConfigChange(clearedConfig);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 mb-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          GitHub Configuration
        </h3>
        <button
          onClick={handleClearConfig}
          className="text-sm text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
        >
          Clear Config
        </button>
      </div>

      <div className="space-y-3">
        {/* GitHub Token */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            GitHub Personal Access Token
          </label>
          <div className="relative">
            <input
              type={showToken ? 'text' : 'password'}
              name="githubToken"
              value={config.githubToken}
              onChange={handleChange}
              placeholder="ghp_xxxxxxxxxxxx"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       pr-10"
            />
            <button
              type="button"
              onClick={() => setShowToken(!showToken)}
              className="absolute right-2 top-1/2 transform -translate-y-1/2
                       text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              {showToken ? '🙈' : '👁️'}
            </button>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Required for repository operations. Create one in GitHub Settings → Developer settings → Personal access tokens
          </p>
        </div>

        {/* Repository URL */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Repository URL
          </label>
          <input
            type="url"
            name="repoUrl"
            value={config.repoUrl}
            onChange={handleChange}
            placeholder="https://github.com/owner/repo"
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                     focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            The GitHub repository where you want to push code
          </p>
        </div>

        {/* Default Branch */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Default Branch
          </label>
          <input
            type="text"
            name="defaultBranch"
            value={config.defaultBranch}
            onChange={handleChange}
            placeholder="main"
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                     focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Configuration Status */}
        <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${
              config.githubToken && config.repoUrl ? 'bg-green-500' : 'bg-yellow-500'
            }`} />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {config.githubToken && config.repoUrl 
                ? 'GitHub configuration complete' 
                : 'GitHub configuration incomplete'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GitHubConfig;