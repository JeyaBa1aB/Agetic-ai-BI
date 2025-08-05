/**
 * Main App component for Multi-Agent BI Assistant
 * Integrates all components and manages global state
 */
import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import useWebSocket from './hooks/useWebSocket';
import { checkHealth, getConfig } from './services/api';
import { supabaseService } from './services/supabase';

// Import components (we'll create these next)
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import AgentHierarchy from './components/AgentHierarchy';
import WorkflowProgress from './components/WorkflowProgress';
import ChartRenderer from './components/ChartRenderer';
import ConnectionStatus from './components/ConnectionStatus';

function App() {
  // Global state
  const [currentSession, setCurrentSession] = useState(null);
  const [csvData, setCsvData] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  
  // Debug analysisResults state changes
  useEffect(() => {
    console.log('🔄 analysisResults state changed:', analysisResults);
    if (analysisResults) {
      console.log('📊 Analysis results structure:', {
        hasKeyInsights: !!analysisResults.key_insights,
        hasRecommendations: !!analysisResults.recommendations,
        hasSuccess: !!analysisResults.success,
        keys: Object.keys(analysisResults)
      });
    }
  }, [analysisResults]);
  const [systemStatus, setSystemStatus] = useState({
    backend: false,
    supabase: false,
    websocket: false
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // WebSocket hook
  const webSocket = useWebSocket(true);

  // Check system health on mount
  useEffect(() => {
    const checkSystemHealth = async () => {
      setLoading(true);
      try {
        // Check backend health
        const healthResponse = await checkHealth();
        const backendHealthy = healthResponse.status === 'healthy';

        // Check Supabase connection
        const supabaseHealthy = await supabaseService.testConnection();

        setSystemStatus({
          backend: backendHealthy,
          supabase: supabaseHealthy,
          websocket: webSocket.isConnected
        });

        if (backendHealthy) {
          // Get system configuration
          try {
            const config = await getConfig();
            console.log('System configuration:', config);
          } catch (configError) {
            console.warn('Could not fetch system configuration:', configError);
          }
        }

      } catch (error) {
        console.error('System health check failed:', error);
        setError('Failed to connect to backend services');
        setSystemStatus({
          backend: false,
          supabase: false,
          websocket: false
        });
      } finally {
        setLoading(false);
      }
    };

    checkSystemHealth();
  }, []);

  // Update WebSocket status
  useEffect(() => {
    setSystemStatus(prev => ({
      ...prev,
      websocket: webSocket.isConnected
    }));
  }, [webSocket.isConnected]);

  // Handle file upload
  const handleFileUpload = (data) => {
    setCsvData(data);
    setAnalysisResults(null); // Clear previous results
    console.log('CSV data uploaded:', data);
  };

  // Handle analysis start
  const handleAnalysisStart = (query, sessionId) => {
    if (!csvData) {
      setError('Please upload a CSV file first');
      return;
    }

    setCurrentSession(sessionId);
    setAnalysisResults(null);

    // Subscribe to session room for real-time updates
    webSocket.subscribeToSession(sessionId);

    // Start analysis via WebSocket
    webSocket.startAnalysis({
      csvData: csvData.raw,
      query: query,
      sessionId: sessionId
    });

    console.log('Analysis started:', { query, sessionId });
  };

  // Handle analysis completion
  useEffect(() => {
    const handleAnalysisComplete = (data) => {
      console.log('🎉 Analysis completed event received:', data);
      console.log('📊 Current session:', currentSession);
      console.log('📋 Data session_id:', data.session_id);
      console.log('📄 Result data:', data.result);
      
      if (data.session_id === currentSession) {
        console.log('✅ Session IDs match, setting analysis results');
        setAnalysisResults(data.result);
        console.log('📈 Analysis results set:', data.result);
      } else {
        console.log('❌ Session ID mismatch, ignoring result');
      }
    };

    const handleAnalysisError = (data) => {
      if (data.session_id === currentSession) {
        setError(`Analysis failed: ${data.error}`);
        console.error('Analysis error:', data);
      }
    };

    webSocket.subscribe('analysis_completed', handleAnalysisComplete);
    webSocket.subscribe('analysis_error', handleAnalysisError);

    return () => {
      webSocket.unsubscribe('analysis_completed', handleAnalysisComplete);
      webSocket.unsubscribe('analysis_error', handleAnalysisError);
    };
  }, [currentSession, webSocket]);

  // Loading screen
  if (loading) {
    return (
      <div className="min-h-screen bg-background-primary flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Initializing Multi-Agent BI Assistant
          </h2>
          <p className="text-gray-600">
            Connecting to backend services...
          </p>
        </div>
      </div>
    );
  }

  // Error screen
  if (error && !systemStatus.backend) {
    return (
      <div className="min-h-screen bg-background-primary flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Connection Failed
          </h2>
          <p className="text-gray-600 mb-4">
            {error}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="btn-primary"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background-primary">
      {/* Toast notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />

      {/* Header */}
      <Header systemStatus={systemStatus} />

      {/* Connection Status */}
      <ConnectionStatus 
        systemStatus={systemStatus}
        websocketStatus={webSocket.connectionStatus}
        error={webSocket.error}
      />

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Column - File Upload & Chat */}
          <div className="lg:col-span-1 space-y-6">
            {/* File Upload */}
            <div className="agent-card p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                📁 Data Upload
              </h2>
              <FileUpload 
                onFileUpload={handleFileUpload}
                currentData={csvData}
              />
            </div>

            {/* Chat Interface */}
            <div className="agent-card p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                💬 Analysis Query
              </h2>
              <ChatInterface 
                onAnalysisStart={handleAnalysisStart}
                disabled={!csvData || !systemStatus.backend}
                currentSession={currentSession}
              />
            </div>
          </div>

          {/* Middle Column - Agent Hierarchy & Progress */}
          <div className="lg:col-span-1 space-y-6">
            {/* Agent Hierarchy */}
            <div className="agent-card p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                🤖 Agent Status
              </h2>
              <AgentHierarchy 
                sessionId={currentSession}
                websocket={webSocket}
              />
            </div>

            {/* Workflow Progress */}
            {currentSession && (
              <div className="agent-card p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  📊 Analysis Progress
                </h2>
                <WorkflowProgress 
                  sessionId={currentSession}
                  websocket={webSocket}
                />
              </div>
            )}
          </div>

          {/* Right Column - Results & Charts */}
          <div className="lg:col-span-1 space-y-6">
            {/* Chart Renderer */}
            {(csvData || analysisResults) && (
              <div className="agent-card p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  📈 Data Visualization
                </h2>
                <ChartRenderer 
                  data={csvData?.parsed}
                  analysisResults={analysisResults}
                />
              </div>
            )}

            {/* Analysis Results */}
            {analysisResults && (
              <div className="agent-card p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  📋 Analysis Results
                </h2>
                <div className="space-y-4">
                  {analysisResults.key_insights && (
                    <div>
                      <h3 className="font-medium text-gray-900 mb-2">Key Insights</h3>
                      <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                        {analysisResults.key_insights.map((insight, index) => (
                          <li key={index}>{insight}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {analysisResults.recommendations && (
                    <div>
                      <h3 className="font-medium text-gray-900 mb-2">Recommendations</h3>
                      <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                        {analysisResults.recommendations.map((rec, index) => (
                          <li key={index}>{rec.recommendation || rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;