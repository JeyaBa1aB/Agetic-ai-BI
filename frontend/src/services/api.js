/**
 * API service for Multi-Agent BI Assistant
 * Handles all HTTP requests to the backend
 */
import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Health check
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    throw new Error(`Health check failed: ${error.message}`);
  }
};

// Configuration endpoints
export const getConfig = async () => {
  try {
    const response = await api.get('/api/config');
    return response.data;
  } catch (error) {
    throw new Error(`Config fetch failed: ${error.message}`);
  }
};

// Upload endpoints
export const getUploadInfo = async () => {
  try {
    const response = await api.get('/api/upload/info');
    return response.data;
  } catch (error) {
    throw new Error(`Upload info fetch failed: ${error.message}`);
  }
};

export const validateCSV = async (csvData) => {
  try {
    const response = await api.post('/api/upload/validate', { csv_data: csvData });
    return response.data;
  } catch (error) {
    throw new Error(`CSV validation failed: ${error.message}`);
  }
};

// Agent endpoints
export const getAgents = async () => {
  try {
    const response = await api.get('/api/agents');
    return response.data;
  } catch (error) {
    throw new Error(`Agents fetch failed: ${error.message}`);
  }
};

export const getAgentInfo = async (agentId) => {
  try {
    const response = await api.get(`/api/agents/${agentId}`);
    return response.data;
  } catch (error) {
    throw new Error(`Agent info fetch failed: ${error.message}`);
  }
};

export const getAgentStatus = async () => {
  try {
    const response = await api.get('/api/agents/status');
    return response.data;
  } catch (error) {
    throw new Error(`Agent status fetch failed: ${error.message}`);
  }
};

// Analysis endpoints
export const startAnalysis = async (analysisData) => {
  try {
    const response = await api.post('/api/analysis/start', analysisData);
    return response.data;
  } catch (error) {
    throw new Error(`Analysis start failed: ${error.message}`);
  }
};

export const getAnalysisStatus = async (sessionId) => {
  try {
    const response = await api.get(`/api/analysis/status/${sessionId}`);
    return response.data;
  } catch (error) {
    throw new Error(`Analysis status fetch failed: ${error.message}`);
  }
};

export const getAnalysisResults = async (sessionId) => {
  try {
    const response = await api.get(`/api/analysis/results/${sessionId}`);
    return response.data;
  } catch (error) {
    throw new Error(`Analysis results fetch failed: ${error.message}`);
  }
};

export const updateAnalysisSession = async (sessionId, updates) => {
  try {
    const response = await api.put(`/api/analysis/session/${sessionId}`, updates);
    return response.data;
  } catch (error) {
    throw new Error(`Analysis session update failed: ${error.message}`);
  }
};

export const getRecentSessions = async (limit = 10) => {
  try {
    const response = await api.get(`/api/analysis/sessions?limit=${limit}`);
    return response.data;
  } catch (error) {
    throw new Error(`Recent sessions fetch failed: ${error.message}`);
  }
};

export const deleteSession = async (sessionId) => {
  try {
    const response = await api.delete(`/api/analysis/session/${sessionId}`);
    return response.data;
  } catch (error) {
    throw new Error(`Session deletion failed: ${error.message}`);
  }
};

// AI endpoints
export const testAI = async (query) => {
  try {
    const response = await api.post('/api/ai/test', { query });
    return response.data;
  } catch (error) {
    throw new Error(`AI test failed: ${error.message}`);
  }
};

export const testAgentAI = async (agentId, query) => {
  try {
    const response = await api.post(`/api/ai/agent/${agentId}`, { query });
    return response.data;
  } catch (error) {
    throw new Error(`Agent AI test failed: ${error.message}`);
  }
};

export default api;