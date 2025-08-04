/**
 * Agent configuration and metadata
 * Contains information about all 9 specialized agents
 */

export const AGENT_TEAMS = {
  DATA_INTELLIGENCE: 'data_intelligence',
  VISUALIZATION: 'visualization', 
  BUSINESS_INTELLIGENCE: 'business_intelligence',
  REPORTING: 'reporting',
  COORDINATION: 'coordination'
};

export const AGENT_STATUS = {
  IDLE: 'idle',
  READY: 'ready',
  WORKING: 'working',
  COMPLETED: 'completed',
  ERROR: 'error'
};

export const AGENTS_CONFIG = {
  // Data Intelligence Team
  data_analyst: {
    id: 'data_analyst',
    name: 'Senior Data Analyst',
    team: AGENT_TEAMS.DATA_INTELLIGENCE,
    role: 'Statistical Analysis & Data Quality',
    description: 'Performs comprehensive statistical analysis and data quality assessment',
    specialization: 'Statistical Analysis and Data Quality Assessment',
    capabilities: [
      'Statistical analysis',
      'Data quality assessment', 
      'Descriptive statistics',
      'Data profiling',
      'Outlier detection',
      'Missing data analysis'
    ],
    color: '#3B82F6', // Blue
    icon: '📊',
    priority: 1
  },

  data_processor: {
    id: 'data_processor',
    name: 'Data Processing Specialist',
    team: AGENT_TEAMS.DATA_INTELLIGENCE,
    role: 'Data Cleaning & Transformation',
    description: 'Cleans, transforms, and prepares data for analysis',
    specialization: 'Data Cleaning and Transformation',
    capabilities: [
      'Data cleaning',
      'Missing value handling',
      'Data transformation',
      'Data type conversion',
      'Duplicate removal',
      'Data normalization'
    ],
    color: '#06B6D4', // Cyan
    icon: '🔧',
    priority: 2
  },

  pattern_detector: {
    id: 'pattern_detector',
    name: 'Pattern Detection Specialist',
    team: AGENT_TEAMS.DATA_INTELLIGENCE,
    role: 'Pattern Recognition & Anomaly Detection',
    description: 'Identifies trends, anomalies, and hidden patterns in data',
    specialization: 'Pattern Recognition and Anomaly Detection',
    capabilities: [
      'Pattern recognition',
      'Anomaly detection',
      'Trend analysis',
      'Correlation analysis',
      'Distribution analysis',
      'Time series patterns'
    ],
    color: '#8B5CF6', // Purple
    icon: '🔍',
    priority: 3
  },

  // Visualization Team
  chart_specialist: {
    id: 'chart_specialist',
    name: 'Chart Creation Specialist',
    team: AGENT_TEAMS.VISUALIZATION,
    role: 'Chart Design & Data Visualization',
    description: 'Designs optimal visualizations for data insights',
    specialization: 'Chart Design and Data Visualization',
    capabilities: [
      'Chart type selection',
      'Data visualization design',
      'Color scheme optimization',
      'Interactive chart features',
      'Chart accessibility',
      'Visual storytelling'
    ],
    color: '#10B981', // Emerald
    icon: '📈',
    priority: 4
  },

  dashboard_designer: {
    id: 'dashboard_designer',
    name: 'Dashboard Design Specialist',
    team: AGENT_TEAMS.VISUALIZATION,
    role: 'Dashboard Design & User Experience',
    description: 'Creates comprehensive dashboard layouts and user experiences',
    specialization: 'Dashboard Design and User Experience',
    capabilities: [
      'Dashboard layout design',
      'User experience optimization',
      'Responsive design',
      'Information architecture',
      'Interactive features',
      'Visual hierarchy'
    ],
    color: '#F59E0B', // Amber
    icon: '📋',
    priority: 5
  },

  // Business Intelligence Team
  business_strategist: {
    id: 'business_strategist',
    name: 'Business Strategy Specialist',
    team: AGENT_TEAMS.BUSINESS_INTELLIGENCE,
    role: 'Strategic Business Analysis & Planning',
    description: 'Provides strategic business insights and actionable recommendations',
    specialization: 'Strategic Business Analysis and Planning',
    capabilities: [
      'Strategic planning',
      'Business analysis',
      'Performance optimization',
      'Risk assessment',
      'Growth strategies',
      'Competitive analysis'
    ],
    color: '#EF4444', // Red
    icon: '🎯',
    priority: 6
  },

  market_analyst: {
    id: 'market_analyst',
    name: 'Market Analysis Specialist',
    team: AGENT_TEAMS.BUSINESS_INTELLIGENCE,
    role: 'Market Research & Competitive Intelligence',
    description: 'Analyzes market trends and competitive landscape',
    specialization: 'Market Research and Competitive Intelligence',
    capabilities: [
      'Market trend analysis',
      'Competitive intelligence',
      'Market segmentation',
      'Industry benchmarking',
      'Market opportunity assessment',
      'Consumer behavior analysis'
    ],
    color: '#F97316', // Orange
    icon: '📈',
    priority: 7
  },

  // Reporting Team
  executive_reporter: {
    id: 'executive_reporter',
    name: 'Executive Reporting Specialist',
    team: AGENT_TEAMS.REPORTING,
    role: 'Executive Communication & Strategic Reporting',
    description: 'Creates executive-level summaries and strategic presentations',
    specialization: 'Executive Communication and Strategic Reporting',
    capabilities: [
      'Executive reporting',
      'Strategic communication',
      'Data storytelling',
      'Presentation design',
      'Key insights synthesis',
      'Action plan development'
    ],
    color: '#6366F1', // Indigo
    icon: '📄',
    priority: 8
  },

  // Master Orchestrator
  master_orchestrator: {
    id: 'master_orchestrator',
    name: 'Master Orchestrator',
    team: AGENT_TEAMS.COORDINATION,
    role: 'Multi-Agent Coordination & Workflow Management',
    description: 'Coordinates multi-agent business intelligence analysis workflows',
    specialization: 'Multi-Agent Coordination and Workflow Management',
    capabilities: [
      'Agent coordination',
      'Workflow management',
      'Task delegation',
      'Result synthesis',
      'Quality assurance',
      'Performance monitoring'
    ],
    color: '#1F2937', // Gray-800
    icon: '🎭',
    priority: 0
  }
};

// Helper functions
export const getAgentById = (agentId) => {
  return AGENTS_CONFIG[agentId] || null;
};

export const getAgentsByTeam = (team) => {
  return Object.values(AGENTS_CONFIG).filter(agent => agent.team === team);
};

export const getAllAgents = () => {
  return Object.values(AGENTS_CONFIG).sort((a, b) => a.priority - b.priority);
};

export const getAgentColor = (agentId) => {
  const agent = getAgentById(agentId);
  return agent ? agent.color : '#6B7280';
};

export const getAgentStatusColor = (status) => {
  const statusColors = {
    [AGENT_STATUS.IDLE]: '#6B7280',      // Gray
    [AGENT_STATUS.READY]: '#10B981',     // Green
    [AGENT_STATUS.WORKING]: '#F59E0B',   // Amber
    [AGENT_STATUS.COMPLETED]: '#3B82F6', // Blue
    [AGENT_STATUS.ERROR]: '#EF4444',     // Red
  };
  
  return statusColors[status] || statusColors[AGENT_STATUS.IDLE];
};

export const formatAgentName = (agentId) => {
  const agent = getAgentById(agentId);
  return agent ? agent.name : agentId.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
};

export const getTeamName = (team) => {
  const teamNames = {
    [AGENT_TEAMS.DATA_INTELLIGENCE]: 'Data Intelligence Team',
    [AGENT_TEAMS.VISUALIZATION]: 'Visualization Team',
    [AGENT_TEAMS.BUSINESS_INTELLIGENCE]: 'Business Intelligence Team',
    [AGENT_TEAMS.REPORTING]: 'Reporting Team',
    [AGENT_TEAMS.COORDINATION]: 'Coordination Team'
  };
  
  return teamNames[team] || team;
};

export default AGENTS_CONFIG;