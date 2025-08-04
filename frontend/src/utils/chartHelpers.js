/**
 * Chart configuration and data transformation utilities
 * Helpers for Recharts library integration
 */

// Chart type configurations
export const CHART_TYPES = {
  LINE: 'line',
  BAR: 'bar',
  AREA: 'area',
  PIE: 'pie',
  SCATTER: 'scatter',
  RADAR: 'radar',
  TREEMAP: 'treemap',
  FUNNEL: 'funnel'
};

// Color palettes for charts
export const CHART_COLORS = {
  primary: ['#3B82F6', '#06B6D4', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#F97316', '#6366F1'],
  agents: ['#3B82F6', '#06B6D4', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#F97316', '#6366F1', '#1F2937'],
  status: {
    ready: '#10B981',
    working: '#F59E0B', 
    completed: '#3B82F6',
    error: '#EF4444',
    idle: '#6B7280'
  },
  gradient: [
    { offset: '0%', color: '#3B82F6' },
    { offset: '100%', color: '#06B6D4' }
  ]
};

// Chart configuration presets
export const CHART_CONFIGS = {
  [CHART_TYPES.LINE]: {
    margin: { top: 20, right: 30, left: 20, bottom: 20 },
    strokeWidth: 2,
    dot: { r: 4 },
    activeDot: { r: 6 }
  },
  
  [CHART_TYPES.BAR]: {
    margin: { top: 20, right: 30, left: 20, bottom: 20 },
    barSize: 40,
    radius: [4, 4, 0, 0]
  },
  
  [CHART_TYPES.AREA]: {
    margin: { top: 20, right: 30, left: 20, bottom: 20 },
    strokeWidth: 2,
    fillOpacity: 0.6
  },
  
  [CHART_TYPES.PIE]: {
    cx: '50%',
    cy: '50%',
    outerRadius: 100,
    innerRadius: 0,
    paddingAngle: 2
  },
  
  [CHART_TYPES.SCATTER]: {
    margin: { top: 20, right: 30, left: 20, bottom: 20 },
    dot: { r: 6, fill: '#3B82F6' }
  }
};

// Data transformation utilities
export const transformDataForChart = (data, chartType, xKey, yKey) => {
  if (!data || !Array.isArray(data)) return [];
  
  switch (chartType) {
    case CHART_TYPES.PIE:
      return data.map((item, index) => ({
        name: item[xKey] || `Item ${index + 1}`,
        value: parseFloat(item[yKey]) || 0,
        fill: CHART_COLORS.primary[index % CHART_COLORS.primary.length]
      }));
      
    case CHART_TYPES.LINE:
    case CHART_TYPES.BAR:
    case CHART_TYPES.AREA:
      return data.map(item => ({
        ...item,
        [xKey]: item[xKey],
        [yKey]: parseFloat(item[yKey]) || 0
      }));
      
    case CHART_TYPES.SCATTER:
      return data.map(item => ({
        x: parseFloat(item[xKey]) || 0,
        y: parseFloat(item[yKey]) || 0,
        name: item.name || `Point ${data.indexOf(item) + 1}`
      }));
      
    default:
      return data;
  }
};

// Agent status chart data
export const transformAgentStatusData = (agentStatuses) => {
  const statusCounts = {};
  
  Object.values(agentStatuses).forEach(status => {
    statusCounts[status] = (statusCounts[status] || 0) + 1;
  });
  
  return Object.entries(statusCounts).map(([status, count]) => ({
    name: status.charAt(0).toUpperCase() + status.slice(1),
    value: count,
    fill: CHART_COLORS.status[status] || CHART_COLORS.status.idle
  }));
};

// Progress chart data
export const transformProgressData = (progressData) => {
  return Object.entries(progressData).map(([agent, progress]) => ({
    agent: agent.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    progress: Math.round(progress),
    fill: CHART_COLORS.agents[Object.keys(progressData).indexOf(agent) % CHART_COLORS.agents.length]
  }));
};

// Time series data transformation
export const transformTimeSeriesData = (data, timeKey = 'timestamp', valueKey = 'value') => {
  return data.map(item => ({
    ...item,
    time: new Date(item[timeKey]).toLocaleTimeString(),
    value: parseFloat(item[valueKey]) || 0
  }));
};

// CSV data to chart data transformation
export const csvToChartData = (csvData, chartType = CHART_TYPES.BAR) => {
  if (!csvData || csvData.length === 0) return [];
  
  const headers = Object.keys(csvData[0]);
  const numericHeaders = headers.filter(header => 
    csvData.some(row => !isNaN(parseFloat(row[header])))
  );
  
  if (numericHeaders.length === 0) return [];
  
  const xKey = headers[0]; // First column as X-axis
  const yKey = numericHeaders[0]; // First numeric column as Y-axis
  
  return transformDataForChart(csvData, chartType, xKey, yKey);
};

// Chart recommendation based on data
export const recommendChartType = (data) => {
  if (!data || data.length === 0) return CHART_TYPES.BAR;
  
  const headers = Object.keys(data[0]);
  const numericColumns = headers.filter(header => 
    data.some(row => !isNaN(parseFloat(row[header])))
  );
  
  // Recommendations based on data characteristics
  if (data.length <= 10 && numericColumns.length === 1) {
    return CHART_TYPES.PIE;
  }
  
  if (data.length > 20 && numericColumns.length >= 1) {
    return CHART_TYPES.LINE;
  }
  
  if (numericColumns.length >= 2) {
    return CHART_TYPES.SCATTER;
  }
  
  return CHART_TYPES.BAR;
};

// Format chart tooltip
export const formatTooltip = (value, name, props) => {
  if (typeof value === 'number') {
    return [value.toLocaleString(), name];
  }
  return [value, name];
};

// Format chart axis labels
export const formatAxisLabel = (value) => {
  if (typeof value === 'number') {
    if (value >= 1000000) {
      return `${(value / 1000000).toFixed(1)}M`;
    }
    if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}K`;
    }
    return value.toLocaleString();
  }
  
  if (typeof value === 'string' && value.length > 10) {
    return `${value.substring(0, 10)}...`;
  }
  
  return value;
};

// Generate chart configuration
export const generateChartConfig = (chartType, data, options = {}) => {
  const baseConfig = CHART_CONFIGS[chartType] || {};
  
  return {
    ...baseConfig,
    data: data,
    colors: options.colors || CHART_COLORS.primary,
    responsive: true,
    maintainAspectRatio: false,
    ...options
  };
};

// Export all utilities
export default {
  CHART_TYPES,
  CHART_COLORS,
  CHART_CONFIGS,
  transformDataForChart,
  transformAgentStatusData,
  transformProgressData,
  transformTimeSeriesData,
  csvToChartData,
  recommendChartType,
  formatTooltip,
  formatAxisLabel,
  generateChartConfig
};