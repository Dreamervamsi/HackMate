import React, { useEffect, useState } from 'react';
import { orchestratorAPI } from '../api/orchestratorAPI';

const HealthStatus = () => {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const healthData = await orchestratorAPI.getHealthStatus();
        setHealth(healthData);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchHealth();
    // Poll health status every 30 seconds
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
        <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
        <span>Checking backend status...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center gap-2 text-xs text-red-500 dark:text-red-400">
        <div className="w-2 h-2 bg-red-500 rounded-full"></div>
        <span>Backend disconnected: {error}</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2 text-xs text-green-600 dark:text-green-400">
      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
      <span>
        Backend connected ({health.active_agents} agents active)
      </span>
    </div>
  );
};

export default HealthStatus;