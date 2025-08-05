/**
 * Chart Renderer component using Recharts library
 * Dynamically renders charts based on data and analysis results
 */
import React, { useState, useMemo } from 'react';
import {
  LineChart, Line, BarChart, Bar, AreaChart, Area, PieChart, Pie, Cell,
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer
} from 'recharts';
import { BarChart3, LineChart as LineChartIcon, PieChart as PieChartIcon, TrendingUp, Download, RefreshCw } from 'lucide-react';
import { 
  CHART_TYPES, 
  CHART_COLORS, 
  transformDataForChart, 
  csvToChartData, 
  recommendChartType,
  formatTooltip,
  formatAxisLabel
} from '../utils/chartHelpers';

const ChartRenderer = ({ data, analysisResults }) => {
  const [selectedChartType, setSelectedChartType] = useState(null);
  const [selectedColumns, setSelectedColumns] = useState({ x: null, y: null });

  // Available chart types
  const chartTypes = [
    { type: CHART_TYPES.BAR, name: 'Bar Chart', icon: BarChart3 },
    { type: CHART_TYPES.LINE, name: 'Line Chart', icon: LineChartIcon },
    { type: CHART_TYPES.AREA, name: 'Area Chart', icon: TrendingUp },
    { type: CHART_TYPES.PIE, name: 'Pie Chart', icon: PieChartIcon },
    { type: CHART_TYPES.SCATTER, name: 'Scatter Plot', icon: TrendingUp }
  ];

  // Process data for charts
  const processedData = useMemo(() => {
    if (!data || data.length === 0) return null;

    // Get column information
    const headers = Object.keys(data[0]);
    const numericColumns = headers.filter(header => 
      data.some(row => !isNaN(parseFloat(row[header])) && isFinite(row[header]))
    );
    const categoricalColumns = headers.filter(header => 
      !numericColumns.includes(header)
    );

    // Auto-select columns if not manually selected
    const xColumn = selectedColumns.x || categoricalColumns[0] || headers[0];
    const yColumn = selectedColumns.y || numericColumns[0] || headers[1];

    // Recommend chart type if not selected
    const chartType = selectedChartType || recommendChartType(data);

    // Transform data for the selected chart type
    const chartData = transformDataForChart(data, chartType, xColumn, yColumn);

    return {
      chartData,
      chartType,
      xColumn,
      yColumn,
      headers,
      numericColumns,
      categoricalColumns
    };
  }, [data, selectedChartType, selectedColumns]);

  // Handle chart type change
  const handleChartTypeChange = (type) => {
    setSelectedChartType(type);
  };

  // Handle column selection
  const handleColumnChange = (axis, column) => {
    setSelectedColumns(prev => ({
      ...prev,
      [axis]: column
    }));
  };

  // Render chart based on type
  const renderChart = () => {
    if (!processedData || !processedData.chartData) return null;

    const { chartData, chartType, xColumn, yColumn } = processedData;
    const colors = CHART_COLORS.primary;

    const commonProps = {
      data: chartData,
      margin: { top: 20, right: 30, left: 20, bottom: 20 }
    };

    switch (chartType) {
      case CHART_TYPES.BAR:
        return (
          <BarChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey={xColumn} 
              tick={{ fontSize: 12 }}
              tickFormatter={formatAxisLabel}
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              tickFormatter={formatAxisLabel}
            />
            <Tooltip formatter={formatTooltip} />
            <Legend />
            <Bar 
              dataKey={yColumn} 
              fill={colors[0]}
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        );

      case CHART_TYPES.LINE:
        return (
          <LineChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey={xColumn} 
              tick={{ fontSize: 12 }}
              tickFormatter={formatAxisLabel}
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              tickFormatter={formatAxisLabel}
            />
            <Tooltip formatter={formatTooltip} />
            <Legend />
            <Line 
              type="monotone" 
              dataKey={yColumn} 
              stroke={colors[0]}
              strokeWidth={2}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        );

      case CHART_TYPES.AREA:
        return (
          <AreaChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey={xColumn} 
              tick={{ fontSize: 12 }}
              tickFormatter={formatAxisLabel}
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              tickFormatter={formatAxisLabel}
            />
            <Tooltip formatter={formatTooltip} />
            <Legend />
            <Area 
              type="monotone" 
              dataKey={yColumn} 
              stroke={colors[0]}
              fill={colors[0]}
              fillOpacity={0.6}
            />
          </AreaChart>
        );

      case CHART_TYPES.PIE:
        return (
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip formatter={formatTooltip} />
          </PieChart>
        );

      case CHART_TYPES.SCATTER:
        return (
          <ScatterChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              type="number" 
              dataKey="x" 
              name={xColumn}
              tick={{ fontSize: 12 }}
              tickFormatter={formatAxisLabel}
            />
            <YAxis 
              type="number" 
              dataKey="y" 
              name={yColumn}
              tick={{ fontSize: 12 }}
              tickFormatter={formatAxisLabel}
            />
            <Tooltip cursor={{ strokeDasharray: '3 3' }} formatter={formatTooltip} />
            <Scatter dataKey="y" fill={colors[0]} />
          </ScatterChart>
        );

      default:
        return <div className="text-center text-gray-500">Unsupported chart type</div>;
    }
  };

  // Render AI-generated charts based on backend specifications
  const renderAIGeneratedChart = (chartSpec, index) => {
    if (!data || !chartSpec.config) {
      return <div className="text-center text-gray-500">No data available for chart</div>;
    }

    const colors = CHART_COLORS.primary;
    const color = colors[index % colors.length];

    // Prepare data based on chart configuration
    const prepareChartData = () => {
      const config = chartSpec.config;
      
      if (chartSpec.type === 'pie') {
        // For pie charts, group data by category and sum values
        const categoryKey = config.nameKey;
        const valueKey = config.dataKey;
        
        if (!categoryKey || !valueKey) return [];
        
        const grouped = data.reduce((acc, item) => {
          const category = item[categoryKey];
          const value = parseFloat(item[valueKey]) || 0;
          
          if (acc[category]) {
            acc[category] += value;
          } else {
            acc[category] = value;
          }
          
          return acc;
        }, {});
        
        return Object.entries(grouped).map(([name, value]) => ({ name, value }));
      } else {
        // For other chart types, use data directly with proper key mapping
        return data.map(item => {
          const result = { ...item };
          
          // Convert numeric values
          if (config.yAxis?.dataKey) {
            const value = parseFloat(item[config.yAxis.dataKey]);
            result[config.yAxis.dataKey] = isNaN(value) ? 0 : value;
          }
          
          return result;
        }).slice(0, 50); // Limit to 50 data points for performance
      }
    };

    const chartData = prepareChartData();
    const config = chartSpec.config;

    // Render different chart types
    switch (chartSpec.type) {
      case 'line':
        return (
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey={config.xAxis?.dataKey} 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey={config.yAxis?.dataKey} 
              stroke={color}
              strokeWidth={2}
              dot={{ r: 3 }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        );

      case 'bar':
        return (
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey={config.xAxis?.dataKey} 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Legend />
            <Bar 
              dataKey={config.yAxis?.dataKey} 
              fill={color}
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        );

      case 'area':
        return (
          <AreaChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey={config.xAxis?.dataKey} 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Legend />
            <Area 
              type="monotone" 
              dataKey={config.yAxis?.dataKey} 
              stroke={color}
              fill={color}
              fillOpacity={0.6}
            />
          </AreaChart>
        );

      case 'pie':
        return (
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            >
              {chartData.map((entry, idx) => (
                <Cell key={`cell-${idx}`} fill={colors[idx % colors.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        );

      case 'scatter':
        return (
          <ScatterChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              type="number" 
              dataKey={config.xAxis?.dataKey} 
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              type="number" 
              dataKey={config.yAxis?.dataKey} 
              tick={{ fontSize: 12 }}
            />
            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
            <Scatter dataKey={config.yAxis?.dataKey} fill={color} />
          </ScatterChart>
        );

      default:
        return (
          <div className="text-center text-gray-500 py-8">
            <BarChart3 className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>Chart type "{chartSpec.type}" not supported</p>
          </div>
        );
    }
  };

  // Export chart data
  const exportData = () => {
    if (!processedData) return;
    
    const dataStr = JSON.stringify(processedData.chartData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `chart-data-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  if (!data && !analysisResults) {
    return (
      <div className="text-center p-8 text-gray-500">
        <BarChart3 className="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>Upload data or complete an analysis to see visualizations</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Chart Controls */}
      {processedData && (
        <div className="space-y-4">
          
          {/* Chart Type Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Chart Type
            </label>
            <div className="flex flex-wrap gap-2">
              {chartTypes.map(({ type, name, icon: Icon }) => (
                <button
                  key={type}
                  onClick={() => handleChartTypeChange(type)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg border text-sm transition-colors duration-200 ${
                    processedData.chartType === type
                      ? 'bg-blue-50 border-blue-200 text-blue-700'
                      : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{name}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Column Selection */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                X-Axis Column
              </label>
              <select
                value={processedData.xColumn}
                onChange={(e) => handleColumnChange('x', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {processedData.headers.map(header => (
                  <option key={header} value={header}>
                    {header}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Y-Axis Column
              </label>
              <select
                value={processedData.yColumn}
                onChange={(e) => handleColumnChange('y', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={processedData.chartType === CHART_TYPES.PIE}
              >
                {processedData.numericColumns.map(header => (
                  <option key={header} value={header}>
                    {header}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Chart Actions */}
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              Showing {processedData.chartData.length} data points
            </div>
            
            <div className="flex space-x-2">
              <button
                onClick={() => {
                  setSelectedChartType(null);
                  setSelectedColumns({ x: null, y: null });
                }}
                className="flex items-center space-x-1 px-3 py-1 text-sm text-gray-600 hover:text-gray-800 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Reset</span>
              </button>
              
              <button
                onClick={exportData}
                className="flex items-center space-x-1 px-3 py-1 text-sm text-blue-600 hover:text-blue-800 transition-colors"
              >
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Chart Display */}
      {processedData && (
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              {renderChart()}
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Analysis Results Charts */}
      {analysisResults && analysisResults.charts && (
        <div className="space-y-4">
          <h3 className="font-medium text-gray-900">
            AI-Generated Visualizations
          </h3>
          
          {analysisResults.charts.map((chart, index) => (
            <div key={index} className="bg-white p-4 rounded-lg border border-gray-200">
              <h4 className="font-medium text-gray-800 mb-2">
                {chart.title}
              </h4>
              <p className="text-sm text-gray-600 mb-4">
                {chart.description}
              </p>
              
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  {renderAIGeneratedChart(chart, index)}
                </ResponsiveContainer>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Chart Insights */}
      {processedData && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-medium text-blue-900 mb-2">
            📊 Chart Insights
          </h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Displaying {processedData.chartData.length} data points</li>
            <li>• Chart type: {processedData.chartType.charAt(0).toUpperCase() + processedData.chartType.slice(1)}</li>
            <li>• X-axis: {processedData.xColumn}</li>
            <li>• Y-axis: {processedData.yColumn}</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ChartRenderer;