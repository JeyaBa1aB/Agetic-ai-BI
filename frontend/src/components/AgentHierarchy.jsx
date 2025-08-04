/**
 * Agent Hierarchy component with real-time status indicators
 * Displays all 9 agents organized by teams with live status updates
 */
import React, { useState, useEffect } from 'react';
import { useSessionWebSocket } from '../hooks/useWebSocket';
import { AGENTS_CONFIG, AGENT_TEAMS, AGENT_STATUS, getAgentsByTeam, getTeamName, getAgentStatusColor } from '../utils/agentConfig';
import { Activity, Clock, CheckCircle, XCircle, Pause, Users } from 'lucide-react';

const AgentHierarchy = ({ sessionId, websocket }) => {
  const [agentStatuses, setAgentStatuses] = useState({});
  const [expandedTeams, setExpandedTeams] = useState({
    [AGENT_TEAMS.DATA_INTELLIGENCE]: true,
    [AGENT_TEAMS.VISUALIZATION]: true,
    [AGENT_TEAMS.BUSINESS_INTELLIGENCE]: true,
    [AGENT_TEAMS.REPORTING]: true,
    [AGENT_TEAMS.COORDINATION]: true
  });

  // Initialize agent statuses
  useEffect(() => {
    const initialStatuses = {};
    Object.keys(AGENTS_CONFIG).forEach(agentId => {
      initialStatuses[agentId] = {
        status: AGENT_STATUS.IDLE,
        message: 'Ready for analysis',
        progress: 0,
        timestamp: Date.now()
      };
    });
    setAgentStatuses(initialStatuses);
  }, []);

  // Listen for agent status updates
  useEffect(() => {
    if (!websocket || !sessionId) return;

    const handleAgentStatusUpdate = (data) => {
      if (data.session_id === sessionId) {
        setAgentStatuses(prev => ({
          ...prev,
          [data.agent_id]: {
            status: data.status,
            message: data.message || 'Working...',
            progress: data.progress || 0,
            timestamp: Date.now()
          }
        }));
      }
    };

    websocket.subscribe('agent_status_update', handleAgentStatusUpdate);

    return () => {
      websocket.unsubscribe('agent_status_update', handleAgentStatusUpdate);
    };
  }, [websocket, sessionId]);

  // Get status icon
  const getStatusIcon = (status) => {
    switch (status) {
      case AGENT_STATUS.WORKING:
        return <Activity className="w-4 h-4 animate-pulse" />;
      case AGENT_STATUS.COMPLETED:
        return <CheckCircle className="w-4 h-4" />;
      case AGENT_STATUS.ERROR:
        return <XCircle className="w-4 h-4" />;
      case AGENT_STATUS.READY:
        return <Clock className="w-4 h-4" />;
      default:
        return <Pause className="w-4 h-4" />;
    }
  };

  // Get status badge class
  const getStatusBadgeClass = (status) => {
    const baseClass = "inline-flex items-center px-2 py-1 rounded-full text-xs font-medium";
    
    switch (status) {
      case AGENT_STATUS.WORKING:
        return `${baseClass} bg-yellow-100 text-yellow-800`;
      case AGENT_STATUS.COMPLETED:
        return `${baseClass} bg-green-100 text-green-800`;
      case AGENT_STATUS.ERROR:
        return `${baseClass} bg-red-100 text-red-800`;
      case AGENT_STATUS.READY:
        return `${baseClass} bg-blue-100 text-blue-800`;
      default:
        return `${baseClass} bg-gray-100 text-gray-800`;
    }
  };

  // Toggle team expansion
  const toggleTeam = (team) => {
    setExpandedTeams(prev => ({
      ...prev,
      [team]: !prev[team]
    }));
  };

  // Get team status summary
  const getTeamStatus = (team) => {
    const teamAgents = getAgentsByTeam(team);
    const statuses = teamAgents.map(agent => agentStatuses[agent.id]?.status || AGENT_STATUS.IDLE);
    
    const counts = {
      [AGENT_STATUS.IDLE]: 0,
      [AGENT_STATUS.READY]: 0,
      [AGENT_STATUS.WORKING]: 0,
      [AGENT_STATUS.COMPLETED]: 0,
      [AGENT_STATUS.ERROR]: 0
    };

    statuses.forEach(status => {
      counts[status] = (counts[status] || 0) + 1;
    });

    return counts;
  };

  // Render team header
  const renderTeamHeader = (team) => {
    const teamStatus = getTeamStatus(team);
    const isExpanded = expandedTeams[team];
    const teamAgents = getAgentsByTeam(team);

    return (
      <button
        onClick={() => toggleTeam(team)}
        className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors duration-200"
      >
        <div className="flex items-center space-x-3">
          <Users className="w-5 h-5 text-gray-600" />
          <div className="text-left">
            <h3 className="font-medium text-gray-900">
              {getTeamName(team)}
            </h3>
            <p className="text-sm text-gray-600">
              {teamAgents.length} agents
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* Status indicators */}
          <div className="flex space-x-1">
            {teamStatus[AGENT_STATUS.WORKING] > 0 && (
              <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
            )}
            {teamStatus[AGENT_STATUS.COMPLETED] > 0 && (
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            )}
            {teamStatus[AGENT_STATUS.ERROR] > 0 && (
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
            )}
            {teamStatus[AGENT_STATUS.READY] > 0 && (
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            )}
          </div>

          {/* Expand/collapse icon */}
          <div className={`transform transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}>
            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </button>
    );
  };

  // Render agent card
  const renderAgentCard = (agent) => {
    const status = agentStatuses[agent.id] || { 
      status: AGENT_STATUS.IDLE, 
      message: 'Ready for analysis', 
      progress: 0 
    };

    return (
      <div
        key={agent.id}
        className="p-3 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-all duration-200"
      >
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center space-x-2">
            <div 
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: getAgentStatusColor(status.status) }}
            ></div>
            <div>
              <h4 className="font-medium text-gray-900 text-sm">
                {agent.icon} {agent.name}
              </h4>
              <p className="text-xs text-gray-600">
                {agent.role}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-1">
            <div style={{ color: getAgentStatusColor(status.status) }}>
              {getStatusIcon(status.status)}
            </div>
          </div>
        </div>

        {/* Status badge */}
        <div className="mb-2">
          <span className={getStatusBadgeClass(status.status)}>
            {status.status.charAt(0).toUpperCase() + status.status.slice(1)}
          </span>
        </div>

        {/* Progress bar */}
        {status.progress > 0 && (
          <div className="mb-2">
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ 
                  width: `${status.progress}%`,
                  backgroundColor: getAgentStatusColor(status.status)
                }}
              ></div>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {status.progress}% complete
            </div>
          </div>
        )}

        {/* Status message */}
        <p className="text-xs text-gray-600 truncate" title={status.message}>
          {status.message}
        </p>

        {/* Timestamp */}
        <div className="text-xs text-gray-400 mt-1">
          {new Date(status.timestamp).toLocaleTimeString()}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      
      {/* Overall Status */}
      <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-blue-600" />
            <span className="font-medium text-blue-900">
              Multi-Agent System Status
            </span>
          </div>
          
          <div className="text-sm text-blue-700">
            {Object.values(agentStatuses).filter(s => s.status === AGENT_STATUS.WORKING).length} working •{' '}
            {Object.values(agentStatuses).filter(s => s.status === AGENT_STATUS.COMPLETED).length} completed
          </div>
        </div>
      </div>

      {/* Teams */}
      {Object.values(AGENT_TEAMS).map(team => {
        const teamAgents = getAgentsByTeam(team);
        if (teamAgents.length === 0) return null;

        return (
          <div key={team} className="space-y-2">
            {renderTeamHeader(team)}
            
            {expandedTeams[team] && (
              <div className="grid grid-cols-1 gap-2 pl-4">
                {teamAgents.map(agent => renderAgentCard(agent))}
              </div>
            )}
          </div>
        );
      })}

      {/* No session message */}
      {!sessionId && (
        <div className="text-center p-6 text-gray-500">
          <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p className="text-sm">
            Start an analysis to see real-time agent status updates
          </p>
        </div>
      )}
    </div>
  );
};

export default AgentHierarchy;