/**
 * Chat Interface component for natural language queries
 * Handles user input and analysis requests
 */
import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageSquare, Loader, Sparkles } from 'lucide-react';
import toast from 'react-hot-toast';

const ChatInterface = ({ onAnalysisStart, onAnalysisStop, isAnalyzing, disabled, currentSession }) => {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const textareaRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Sample queries for inspiration
  const sampleQueries = [
    "What are the key trends in this data?",
    "Identify patterns and anomalies in the dataset",
    "Provide strategic recommendations based on the data",
    "Create a comprehensive business analysis report",
    "What insights can help improve performance?",
    "Analyze the data for market opportunities"
  ];

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [query]);

  // Scroll to bottom of chat
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      toast.error('Please enter a query');
      return;
    }

    if (disabled) {
      toast.error('Please upload a CSV file first');
      return;
    }

    // Generate session ID
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    // Add user message to chat history
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: query,
      timestamp: new Date().toISOString()
    };

    setChatHistory(prev => [...prev, userMessage]);

    // Start analysis
    onAnalysisStart(query, sessionId);

    // Add system message
    const systemMessage = {
      id: Date.now() + 1,
      type: 'system',
      content: `🚀 Starting multi-agent analysis for session: ${sessionId}`,
      timestamp: new Date().toISOString(),
      sessionId
    };

    setChatHistory(prev => [...prev, systemMessage]);
    
    // Clear input
    setQuery('');
    
    toast.success('Analysis started! Watch the agent status for real-time updates.');
  };

  // Handle sample query selection
  const handleSampleQuery = (sampleQuery) => {
    setQuery(sampleQuery);
    textareaRef.current?.focus();
  };

  // Handle key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Stop analysis
  const handleStopAnalysis = () => {
    onAnalysisStop();
    toast.info('Analysis stopped');
  };

  return (
    <div className="space-y-4">
      
      {/* Chat History */}
      {chatHistory.length > 0 && (
        <div 
          ref={chatContainerRef}
          className="max-h-64 overflow-y-auto space-y-3 p-3 bg-gray-50 rounded-lg border"
        >
          {chatHistory.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`chat-message ${
                message.type === 'user' 
                  ? 'chat-message-user' 
                  : message.type === 'system'
                  ? 'bg-blue-100 text-blue-900'
                  : 'chat-message-agent'
              }`}>
                {message.type === 'system' && (
                  <div className="flex items-center space-x-1 mb-1">
                    <Sparkles className="w-3 h-3" />
                    <span className="text-xs font-medium">System</span>
                  </div>
                )}
                <p className="text-sm">{message.content}</p>
                <div className="text-xs opacity-75 mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Query Input Form */}
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="relative">
          <textarea
            ref={textareaRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about your data... (e.g., 'What are the key trends and insights?')"
            className="w-full p-3 pr-12 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 min-h-[80px] max-h-[200px]"
            disabled={disabled || isAnalyzing}
            rows={3}
          />
          
          {/* Send Button */}
          <button
            type="submit"
            disabled={disabled || isAnalyzing || !query.trim()}
            className="absolute bottom-3 right-3 p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            {isAnalyzing ? (
              <Loader className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {isAnalyzing && (
              <button
                type="button"
                onClick={handleStopAnalysis}
                className="btn-secondary text-sm"
              >
                Stop Analysis
              </button>
            )}
            
            {currentSession && (
              <div className="text-xs text-gray-500">
                Session: {currentSession}
              </div>
            )}
          </div>

          <div className="text-xs text-gray-500">
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </form>

      {/* Sample Queries */}
      {chatHistory.length === 0 && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <MessageSquare className="w-4 h-4" />
            <span>Try these sample queries:</span>
          </div>
          
          <div className="grid grid-cols-1 gap-2">
            {sampleQueries.map((sampleQuery, index) => (
              <button
                key={index}
                onClick={() => handleSampleQuery(sampleQuery)}
                disabled={disabled}
                className="text-left p-2 text-sm text-gray-600 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                💡 {sampleQuery}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Status Messages */}
      {disabled && (
        <div className="text-center p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            📁 Please upload a CSV file to start asking questions about your data
          </p>
        </div>
      )}

      {isAnalyzing && (
        <div className="text-center p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center justify-center space-x-2">
            <Loader className="w-4 h-4 animate-spin text-blue-600" />
            <p className="text-sm text-blue-800">
              🤖 Multi-agent analysis in progress... Watch the agent status for real-time updates!
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;