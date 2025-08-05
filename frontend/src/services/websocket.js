/**
 * WebSocket service for real-time communication
 * Handles Socket.IO connection and events
 */
import { io } from 'socket.io-client';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.eventListeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  // Initialize WebSocket connection
  connect(url = import.meta.env.VITE_WS_URL || 'http://localhost:5000') {
    if (this.socket) {
      this.disconnect();
    }

    console.log('🔌 Connecting to WebSocket server:', url);

    this.socket = io(url, {
      transports: ['websocket', 'polling'],
      timeout: 60000,  // Increased to 60 seconds for long-running analysis
      forceNew: true,
      reconnection: true,
      reconnectionAttempts: 10,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      maxHttpBufferSize: 1e8,  // 100MB for large data transfers
      pingTimeout: 60000,      // 60 seconds ping timeout
      pingInterval: 25000      // 25 seconds ping interval
    });

    this.setupEventHandlers();
    return this.socket;
  }

  // Setup default event handlers
  setupEventHandlers() {
    if (!this.socket) return;

    // Connection events
    this.socket.on('connect', () => {
      console.log('✅ WebSocket connected');
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.emit('connection_status', { connected: true });
    });

    this.socket.on('disconnect', (reason) => {
      console.log('❌ WebSocket disconnected:', reason);
      this.isConnected = false;
      this.emit('connection_status', { connected: false, reason });
    });

    this.socket.on('connect_error', (error) => {
      console.error('❌ WebSocket connection error:', error);
      this.handleReconnect();
    });

    // Server response events
    this.socket.on('connection_response', (data) => {
      console.log('📡 Connection response:', data);
      this.emit('connection_response', data);
    });

    // Analysis events
    this.socket.on('analysis_started', (data) => {
      console.log('🚀 Analysis started:', data);
      this.emit('analysis_started', data);
    });

    this.socket.on('analysis_completed', (data) => {
      console.log('🎉 Analysis completed:', data);
      this.emit('analysis_completed', data);
    });

    this.socket.on('analysis_error', (data) => {
      console.error('❌ Analysis error:', data);
      this.emit('analysis_error', data);
    });

    // Agent status events
    this.socket.on('agent_status_update', (data) => {
      console.log('🤖 Agent status update:', data);
      this.emit('agent_status_update', data);
    });

    // Task events
    this.socket.on('task_started', (data) => {
      console.log('📋 Task started:', data);
      this.emit('task_started', data);
    });

    this.socket.on('task_completed', (data) => {
      console.log('✅ Task completed:', data);
      this.emit('task_completed', data);
    });

    // Workflow events
    this.socket.on('workflow_stage_update', (data) => {
      console.log('🔄 Workflow stage update:', data);
      this.emit('workflow_stage_update', data);
    });

    this.socket.on('workflow_progress_update', (data) => {
      console.log('📊 Workflow progress update:', data);
      this.emit('workflow_progress_update', data);
    });

    // Session events
    this.socket.on('subscription_confirmed', (data) => {
      console.log('✅ Subscription confirmed:', data);
      this.emit('subscription_confirmed', data);
    });

    this.socket.on('subscription_error', (data) => {
      console.error('❌ Subscription error:', data);
      this.emit('subscription_error', data);
    });

    // Ping/Pong for connection testing
    this.socket.on('pong', (data) => {
      console.log('🏓 Pong received:', data);
      this.emit('pong', data);
    });
  }

  // Handle reconnection logic
  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      
      console.log(`🔄 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms`);
      
      setTimeout(() => {
        if (this.socket && !this.isConnected) {
          this.socket.connect();
        }
      }, delay);
    } else {
      console.error('❌ Max reconnection attempts reached');
      this.emit('max_reconnect_attempts_reached');
    }
  }

  // Disconnect WebSocket
  disconnect() {
    if (this.socket) {
      console.log('🔌 Disconnecting WebSocket');
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
    }
  }

  // Subscribe to session updates
  subscribeToSession(sessionId) {
    if (!this.socket || !sessionId) return;
    
    console.log('📡 Subscribing to session:', sessionId);
    this.socket.emit('subscribe_to_session', { session_id: sessionId });
  }

  // Unsubscribe from session updates
  unsubscribeFromSession(sessionId) {
    if (!this.socket || !sessionId) return;
    
    console.log('📡 Unsubscribing from session:', sessionId);
    this.socket.emit('unsubscribe_from_session', { session_id: sessionId });
  }

  // Start CrewAI analysis
  startCrewAIAnalysis(analysisData) {
    if (!this.socket) return;
    
    console.log('🚀 Starting CrewAI analysis:', analysisData);
    this.socket.emit('start_crewai_analysis', analysisData);
  }

  // Get agent status
  getAgentStatus(sessionId) {
    if (!this.socket) return;
    
    console.log('📊 Getting agent status for session:', sessionId);
    this.socket.emit('get_agent_status', { session_id: sessionId });
  }

  // Get all sessions
  getAllSessions() {
    if (!this.socket) return;
    
    console.log('📋 Getting all sessions');
    this.socket.emit('get_all_sessions');
  }

  // Ping server
  ping() {
    if (!this.socket) return;
    
    console.log('🏓 Pinging server');
    this.socket.emit('ping');
  }

  // Event listener management
  on(event, callback) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event).push(callback);
  }

  off(event, callback) {
    if (this.eventListeners.has(event)) {
      const listeners = this.eventListeners.get(event);
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  emit(event, data) {
    if (this.eventListeners.has(event)) {
      this.eventListeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in event listener for ${event}:`, error);
        }
      });
    }
  }

  // Get connection status
  getConnectionStatus() {
    return {
      connected: this.isConnected,
      socket: this.socket?.connected || false,
      reconnectAttempts: this.reconnectAttempts,
    };
  }
}

// Create singleton instance
const websocketService = new WebSocketService();

export default websocketService;