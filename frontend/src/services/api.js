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
export const validateCSV = async (csvData) => {
  try {
    const response = await api.post('/api/upload/validate', { csv_data: csvData });
    return response.data;
  } catch (error) {
    throw new Error(`CSV validation failed: ${error.message}`);
  }
};