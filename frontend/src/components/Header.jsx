/**
 * Header component for Multi-Agent BI Assistant
 * Displays system status and navigation
 */
import React from 'react';
import { Activity, Database, Wifi, WifiOff } from 'lucide-react';

const Header = ({ systemStatus }) => {
  const getStatusIcon = (status) => {
    return status ? (
      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
    ) : (
      <div className="w-2 h-2 bg-red-500 rounded-full"></div>
    );
  };

  const getStatusColor = (status) => {
    return status ? 'text-green-600' : 'text-red-600';
  };

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">🤖</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Multi-Agent BI Assistant
              </h1>
              <p className="text-sm text-gray-600">
                Powered by 9 Specialized AI Agents
              </p>
            </div>
          </div>

          {/* System Status */}
          <div className="flex items-center space-x-6">
            
            {/* Backend Status */}
            <div className="flex items-center space-x-2">
              <Activity className={`w-4 h-4 ${getStatusColor(systemStatus.backend)}`} />
              <span className="text-sm font-medium text-gray-700">Backend</span>
              {getStatusIcon(systemStatus.backend)}
            </div>

            {/* Database Status */}
            <div className="flex items-center space-x-2">
              <Database className={`w-4 h-4 ${getStatusColor(systemStatus.supabase)}`} />
              <span className="text-sm font-medium text-gray-700">Database</span>
              {getStatusIcon(systemStatus.supabase)}
            </div>

            {/* WebSocket Status */}
            <div className="flex items-center space-x-2">
              {systemStatus.websocket ? (
                <Wifi className="w-4 h-4 text-green-600" />
              ) : (
                <WifiOff className="w-4 h-4 text-red-600" />
              )}
              <span className="text-sm font-medium text-gray-700">Real-time</span>
              {getStatusIcon(systemStatus.websocket)}
            </div>

            {/* Overall Status Badge */}
            <div className="flex items-center space-x-2">
              <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                Object.values(systemStatus).every(status => status)
                  ? 'bg-green-100 text-green-800'
                  : Object.values(systemStatus).some(status => status)
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {Object.values(systemStatus).every(status => status)
                  ? '🟢 All Systems Operational'
                  : Object.values(systemStatus).some(status => status)
                  ? '🟡 Partial Service'
                  : '🔴 Service Unavailable'
                }
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;