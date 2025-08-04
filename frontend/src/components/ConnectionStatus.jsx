/**
 * Connection Status component
 * Shows detailed connection information and errors
 */
import React, { useState } from 'react';
import { AlertCircle, CheckCircle, XCircle, ChevronDown, ChevronUp } from 'lucide-react';

const ConnectionStatus = ({ systemStatus, websocketStatus, error }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // Don't show if everything is working
  const hasIssues = !Object.values(systemStatus).every(status => status) || error;
  
  if (!hasIssues) return null;

  const getStatusDetails = () => {
    const details = [];
    
    if (!systemStatus.backend) {
      details.push({
        service: 'Backend API',
        status: 'disconnected',
        message: 'Cannot connect to backend server',
        icon: XCircle,
        color: 'text-red-600'
      });
    }
    
    if (!systemStatus.supabase) {
      details.push({
        service: 'Database',
        status: 'disconnected', 
        message: 'Supabase database connection failed',
        icon: XCircle,
        color: 'text-red-600'
      });
    }
    
    if (!systemStatus.websocket) {
      details.push({
        service: 'Real-time Updates',
        status: websocketStatus || 'disconnected',
        message: error || 'WebSocket connection failed',
        icon: XCircle,
        color: 'text-red-600'
      });
    }

    return details;
  };

  const statusDetails = getStatusDetails();

  return (
    <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-yellow-600 mr-3" />
            <div>
              <h3 className="text-sm font-medium text-yellow-800">
                Connection Issues Detected
              </h3>
              <p className="text-sm text-yellow-700">
                Some services are not available. Click to view details.
              </p>
            </div>
          </div>
          
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center text-yellow-600 hover:text-yellow-800 transition-colors"
          >
            <span className="text-sm font-medium mr-1">
              {isExpanded ? 'Hide Details' : 'Show Details'}
            </span>
            {isExpanded ? (
              <ChevronUp className="w-4 h-4" />
            ) : (
              <ChevronDown className="w-4 h-4" />
            )}
          </button>
        </div>

        {/* Expanded Details */}
        {isExpanded && (
          <div className="mt-4 space-y-3">
            {statusDetails.map((detail, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-white rounded-lg border border-yellow-200">
                <detail.icon className={`w-5 h-5 ${detail.color} mt-0.5`} />
                <div className="flex-1">
                  <h4 className="text-sm font-medium text-gray-900">
                    {detail.service}
                  </h4>
                  <p className="text-sm text-gray-600 mt-1">
                    {detail.message}
                  </p>
                  <div className="flex items-center mt-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      detail.status === 'connected' 
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {detail.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}

            {/* Troubleshooting Tips */}
            <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
              <h4 className="text-sm font-medium text-blue-900 mb-2">
                💡 Troubleshooting Tips
              </h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Make sure the backend server is running on port 5000</li>
                <li>• Check your internet connection</li>
                <li>• Verify Supabase configuration in environment variables</li>
                <li>• Try refreshing the page to reconnect</li>
              </ul>
            </div>

            {/* Retry Button */}
            <div className="flex justify-end">
              <button
                onClick={() => window.location.reload()}
                className="btn-primary text-sm"
              >
                🔄 Retry Connection
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConnectionStatus;