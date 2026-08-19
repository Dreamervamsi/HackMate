"use client";

import { useState, useEffect } from "react";

interface SidebarProps {
  onCredentialsChange: (githubToken: string, githubRepo: string) => void;
}

export default function Sidebar({ onCredentialsChange }: SidebarProps) {
  const [githubToken, setGithubToken] = useState("");
  const [githubRepo, setGithubRepo] = useState("");
  const [isExpanded, setIsExpanded] = useState(true);

  useEffect(() => {
    // Load credentials from localStorage on mount
    const savedToken = localStorage.getItem("github_token");
    const savedRepo = localStorage.getItem("github_repo");
    if (savedToken) setGithubToken(savedToken);
    if (savedRepo) setGithubRepo(savedRepo);
    if (savedToken && savedRepo) {
      onCredentialsChange(savedToken, savedRepo);
    }
  }, [onCredentialsChange]);

  const handleTokenChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newToken = e.target.value;
    setGithubToken(newToken);
    localStorage.setItem("github_token", newToken);
    onCredentialsChange(newToken, githubRepo);
  };

  const handleRepoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newRepo = e.target.value;
    setGithubRepo(newRepo);
    localStorage.setItem("github_repo", newRepo);
    onCredentialsChange(githubToken, newRepo);
  };

  return (
    <div
      className={`bg-white border-r border-gray-200 transition-all duration-300 ${
        isExpanded ? "w-80" : "w-16"
      }`}
    >
      <div className="p-4">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="mb-4 p-2 hover:bg-gray-100 rounded-lg transition-colors"
          aria-label={isExpanded ? "Collapse sidebar" : "Expand sidebar"}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="text-gray-600"
          >
            {isExpanded ? (
              <>
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                <line x1="9" y1="3" x2="9" y2="21" />
              </>
            ) : (
              <>
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                <line x1="9" y1="3" x2="9" y2="21" />
                <line x1="15" y1="3" x2="15" y2="21" />
              </>
            )}
          </svg>
        </button>

        {isExpanded && (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">
                GitHub Credentials
              </h3>
              <div className="space-y-3">
                <div>
                  <label
                    htmlFor="github-token"
                    className="block text-xs font-medium text-gray-600 mb-1"
                  >
                    GitHub Token
                  </label>
                  <input
                    id="github-token"
                    type="password"
                    value={githubToken}
                    onChange={handleTokenChange}
                    placeholder="ghp_xxxxxxxxxxxx"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    aria-label="GitHub personal access token"
                  />
                </div>
                <div>
                  <label
                    htmlFor="github-repo"
                    className="block text-xs font-medium text-gray-600 mb-1"
                  >
                    Repository URL
                  </label>
                  <input
                    id="github-repo"
                    type="text"
                    value={githubRepo}
                    onChange={handleRepoChange}
                    placeholder="https://github.com/username/repo"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    aria-label="GitHub repository URL"
                  />
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                These credentials will be used when you ask to create branches or commit code to GitHub.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
