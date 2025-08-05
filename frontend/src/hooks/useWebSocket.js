/**
 * Custom hook for WebSocket management
 * Provides real-time communication with the backend
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import websocketService from '../services/websocket';

export const useWebSocket = (autoConnect = true) => {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [lastMessage, setLastMessage] = useState(null);
  const [error, setError] = useState(null);
  
  const eventListenersRef = useRef(new Map());
  const reconnectTimeoutRef = useRef(null);

  // Connect to WebSocket
  const connect = useCallback((url) => {
    try {
      websocketService.connect(url);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('WebSocket connection error:', err);
    }
  }, []);

  // Disconnect from WebSocket
  const disconnect = useCallback(() => {
    websocketService.disconnect();
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
  }, []);

  // Subscribe to events
  const subscribe = useCallback((event, callback) => {
    websocketService.on(event, callback);
    
    // Store reference for cleanup
    if (!eventListenersRef.current.has(event)) {
      eventListenersRef.current.set(event, []);
    }
    eventListenersRef.current.get(event).push(callback);
  }, []);

  // Unsubscribe from events
  const unsubscribe = useCallback((event, callback) => {
    websocketService.off(event, callback);
    
    // Remove from reference
    if (eventListenersRef.current.has(event)) {
      const listeners = eventListenersRef.current.get(event);
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }, []);

  // Send message
  const sendMessage = useCallback((event, data) => {
    if (websocketService.socket && isConnected) {
      websocketService.socket.emit(event, data);
    } else {
      console.warn('WebSocket not connected. Cannot send message:', event, data);
    }
  }, [isConnected]);

  // Subscribe to session
  const subscribeToSession = useCallback((sessionId) => {
    websocketService.subscribeToSession(sessionId);
  }, []);

  // Unsubscribe from session
  const unsubscribeFromSession = useCallback((sessionId) => {
    websocketService.unsubscribeFromSession(sessionId);
  }, []);

  // Start analysis
  const startAnalysis = useCallback((analysisData) => {
    websocketService.startCrewAIAnalysis(analysisData);
  }, []);

  // Get agent status
  const getAgentStatus = useCallback((sessionId) => {
    websocketService.getAgentStatus(sessionId);
  }, []);

  // Ping server
  const ping = useCallback(() => {
    websocketService.ping();
  }, []);

  // Setup event listeners
  useEffect(() => {
    const handleConnectionStatus = (data) => {
      setIsConnected(data.connected);
      setConnectionStatus(data.connected ? 'connected' : 'disconnected');
      if (!data.connected && data.reason) {
        setError(`Disconnected: ${data.reason}`);
      } else if (data.connected) {
        setError(null);
      }
    };

    const handleMessage = (data) => {
      setLastMessage({
        timestamp: Date.now(),
        data
      });
    };

    const handleError = (error) => {
      setError(error.message || 'WebSocket error occurred');
      setConnectionStatus('error');
    };

    const handleMaxReconnectAttempts = () => {
      setError('Maximum reconnection attempts reached');
      setConnectionStatus('failed');
    };

    // Subscribe to connection events
    websocketService.on('connection_status', handleConnectionStatus);
    websocketService.on('connection_response', handleMessage);
    websocketService.on('analysis_started', handleMessage);
    websocketService.on('analysis_completed', handleMessage);
    websocketService.on('analysis_error', handleMessage);
    websocketService.on('agent_status_update', handleMessage);
    websocketService.on('task_started', handleMessage);
    websocketService.on('task_completed', handleMessage);
    websocketService.on('workflow_stage_update', handleMessage);
    websocketService.on('workflow_progress_update', handleMessage);
    websocketService.on('subscription_confirmed', handleMessage);
    websocketService.on('subscription_error', handleError);
    websocketService.on('max_reconnect_attempts_reached', handleMaxReconnectAttempts);

    // Auto-connect if enabled
    if (autoConnect) {
      connect();
    }

    // Cleanup function
    return () => {
      // Remove all event listeners
      eventListenersRef.current.forEach((listeners, event) => {
        listeners.forEach(callback => {
          websocketService.off(event, callback);
        });
      });
      eventListenersRef.current.clear();

      // Disconnect if connected
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  // Periodic connection check and heartbeat
  useEffect(() => {
    if (!isConnected) return;

    const interval = setInterval(() => {
      ping();
      
      // Send heartbeat if we have an active session
      if (websocketService.socket && websocketService.socket.connected) {
        websocketService.socket.emit('heartbeat', {
          session_id: 'keepalive',
          timestamp: Date.now()
        });
      }
    }, 20000); // Ping every 20 seconds (less than the 25s ping interval)

    return () => clearInterval(interval);
  }, [isConnected, ping]);

  return {
    // Connection state
    isConnected,
    connectionStatus,
    error,
    lastMessage,
    
    // Connection methods
    connect,
    disconnect,
    
    // Event methods
    subscribe,
    unsubscribe,
    sendMessage,
    
    // Specific methods
    subscribeToSession,
    unsubscribeFromSession,
    startAnalysis,
    getAgentStatus,
    ping,
    
    // WebSocket service reference
    websocketService
  };
};

// Hook for specific event listening
export const useWebSocketEvent = (event, callback, dependencies = []) => {
  const { subscribe, unsubscribe } = useWebSocket(false);

  useEffect(() => {
    if (callback) {
      subscribe(event, callback);
      
      return () => {
        unsubscribe(event, callback);
      };
    }
  }, [event, callback, subscribe, unsubscribe, ...dependencies]);
};

// Hook for session-specific WebSocket management
export const useSessionWebSocket = (sessionId) => {
  const webSocket = useWebSocket();
  const [sessionMessages, setSessionMessages] = useState([]);
  const [agentStatuses, setAgentStatuses] = useState({});
  const [analysisProgress, setAnalysisProgress] = useState(0);

  // Subscribe to session when sessionId changes
  useEffect(() => {
    if (sessionId && webSocket.isConnected) {
      webSocket.subscribeToSession(sessionId);
      
      return () => {
        webSocket.unsubscribeFromSession(sessionId);
      };
    }
  }, [sessionId, webSocket.isConnected]);

  // Handle session-specific messages
  useEffect(() => {
    const handleAgentStatusUpdate = (data) => {
      if (data.session_id === sessionId) {
        setAgentStatuses(prev => ({
          ...prev,
          [data.agent_id]: {
            status: data.status,
            message: data.message,
            progress: data.progress,
            timestamp: Date.now()
          }
        }));
      }
    };

    const handleWorkflowProgress = (data) => {
      if (data.session_id === sessionId) {
        setAnalysisProgress(data.progress || 0);
      }
    };

    const handleSessionMessage = (data) => {
      if (data.session_id === sessionId) {
        setSessionMessages(prev => [...prev, {
          ...data,
          timestamp: Date.now()
        }]);
      }
    };

    webSocket.subscribe('agent_status_update', handleAgentStatusUpdate);
    webSocket.subscribe('workflow_progress_update', handleWorkflowProgress);
    webSocket.subscribe('analysis_started', handleSessionMessage);
    webSocket.subscribe('analysis_completed', handleSessionMessage);
    webSocket.subscribe('task_started', handleSessionMessage);
    webSocket.subscribe('task_completed', handleSessionMessage);

    return () => {
      webSocket.unsubscribe('agent_status_update', handleAgentStatusUpdate);
      webSocket.unsubscribe('workflow_progress_update', handleWorkflowProgress);
      webSocket.unsubscribe('analysis_started', handleSessionMessage);
      webSocket.unsubscribe('analysis_completed', handleSessionMessage);
      webSocket.unsubscribe('task_started', handleSessionMessage);
      webSocket.unsubscribe('task_completed', handleSessionMessage);
    };
  }, [sessionId, webSocket]);

  return {
    ...webSocket,
    sessionMessages,
    agentStatuses,
    analysisProgress,
    clearSessionData: () => {
      setSessionMessages([]);
      setAgentStatuses({});
      setAnalysisProgress(0);
    }
  };
};

export default useWebSocket;