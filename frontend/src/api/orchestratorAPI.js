import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes timeout for long-running tasks
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.config.url}`, response.status);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error);
    
    if (error.response) {
      // Server responded with error status
      console.error('Error Data:', error.response.data);
      console.error('Error Status:', error.response.status);
    } else if (error.request) {
      // Request made but no response
      console.error('No Response:', error.request);
    } else {
      // Error in request setup
      console.error('Request Setup Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export const orchestratorAPI = {
  // Send user prompt for orchestration
  sendPrompt: async (userPrompt, context = {}, priority = 'normal') => {
    try {
      const response = await apiClient.post('/orchestrate', {
        user_prompt: userPrompt,
        context: context,
        priority: priority,
      });
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        'Failed to send prompt to orchestrator'
      );
    }
  },

  // Get health status
  getHealthStatus: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        'Failed to get health status'
      );
    }
  },

  // Get active agents
  getActiveAgents: async () => {
    try {
      const response = await apiClient.get('/agents');
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        'Failed to get active agents'
      );
    }
  },

  // Get API info
  getAPIInfo: async () => {
    try {
      const response = await apiClient.get('/');
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        'Failed to get API info'
      );
    }
  },

  // GitHub Operations
  // Create GitHub branch
  createGitHubBranch: async (repoUrl, branchName, baseBranch = null, githubToken = null) => {
    try {
      const response = await apiClient.post('/github/branch', {
        repo_url: repoUrl,
        branch_name: branchName,
        base_branch: baseBranch,
        github_token: githubToken,
      });
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || 
        error.response?.data?.error ||
        error.message || 
        'Failed to create GitHub branch'
      );
    }
  },

  // Commit and push to GitHub
  commitToGitHub: async (repoUrl, branchName, files, commitMessage, githubToken = null) => {
    try {
      const response = await apiClient.post('/github/commit', {
        repo_url: repoUrl,
        branch_name: branchName,
        files: files,
        commit_message: commitMessage,
        github_token: githubToken,
      });
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.detail || 
        error.response?.data?.error ||
        error.message || 
        'Failed to commit to GitHub'
      );
    }
  },
};

export default apiClient;