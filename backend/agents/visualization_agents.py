"""
Visualization Team agents for Multi-Agent BI Assistant
Specialized agents for chart creation and dashboard design
"""
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ChartSpecialistAgent(BaseAgent):
    """Chart Creation Specialist - Designs optimal visualizations for data insights"""
    
    def __init__(self):
        super().__init__(
            agent_id="chart_specialist",
            name="Chart Creation Specialist",
            role="visualization",
            description="Designs optimal visualizations for data insights",
            specialization="Chart Design and Data Visualization"
        )
        self.capabilities = [
            "Chart type selection",
            "Data visualization design",
            "Color scheme optimization",
            "Interactive chart features",
            "Chart accessibility",
            "Visual storytelling"
        ]
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze data and recommend optimal chart types"""
        try:
            self.update_status("analyzing", "Analyzing data for visualization recommendations")
            
            # Parse CSV data
            csv_data = data.get('csv_data', '')
            df = self._parse_csv_data(csv_data)
            if df is None:
                return {
                    'success': False,
                    'error': 'Failed to parse CSV data',
                    'analysis': None
                }
            
            # Analyze data for visualization
            viz_analysis = self._analyze_for_visualization(df)
            
            # Generate chart recommendations
            chart_recommendations = self._recommend_charts(df, query, viz_analysis)
            
            # Generate AI insights
            viz_prompt = self._create_visualization_prompt(query, viz_analysis, chart_recommendations, df)
            ai_response = self.generate_response(viz_prompt, context)
            
            if not ai_response['success']:
                return ai_response
            
            self.update_status("completed", "Chart recommendations completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'chart_recommendations',
                'data_analysis': viz_analysis,
                'chart_recommendations': chart_recommendations,
                'ai_insights': ai_response['content'],
                'priority_charts': self._get_priority_charts(chart_recommendations),
                'chart_configurations': self._generate_chart_configs(chart_recommendations, df)
            }
            
        except Exception as e:
            logger.error(f"Chart Specialist error: {e}")
            self.update_status("error", f"Chart analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis': None
            }
    
    def _parse_csv_data(self, csv_data: str) -> pd.DataFrame:
        """Parse CSV data into DataFrame"""
        try:
            from io import StringIO
            return pd.read_csv(StringIO(csv_data))
        except Exception as e:
            logger.error(f"CSV parsing error: {e}")
            return None
    
    def _analyze_for_visualization(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data characteristics for visualization"""
        analysis = {
            'data_types': {},
            'column_characteristics': {},
            'relationships': [],
            'temporal_columns': [],
            'categorical_columns': [],
            'numerical_columns': []
        }
        
        # Analyze each column
        for col in df.columns:
            col_info = {
                'name': col,
                'dtype': str(df[col].dtype),
                'unique_values': int(df[col].nunique()),
                'null_count': int(df[col].isnull().sum()),
                'null_percentage': round(df[col].isnull().sum() / len(df) * 100, 2)
            }
            
            # Determine column type and characteristics
            if df[col].dtype in ['int64', 'float64']:
                col_info['type'] = 'numerical'
                col_info['min'] = float(df[col].min()) if not df[col].isnull().all() else None
                col_info['max'] = float(df[col].max()) if not df[col].isnull().all() else None
                col_info['mean'] = float(df[col].mean()) if not df[col].isnull().all() else None
                analysis['numerical_columns'].append(col)
                
                # Check if it could be a year or date-like
                if col_info['min'] and col_info['max']:
                    if 1900 <= col_info['min'] <= 2100 and 1900 <= col_info['max'] <= 2100:
                        col_info['potential_temporal'] = True
                        analysis['temporal_columns'].append(col)
                
            elif df[col].dtype == 'object':
                col_info['type'] = 'categorical'
                col_info['top_values'] = df[col].value_counts().head(5).to_dict()
                analysis['categorical_columns'].append(col)
                
                # Check if it could be a date
                try:
                    pd.to_datetime(df[col].dropna().head(10))
                    col_info['potential_temporal'] = True
                    analysis['temporal_columns'].append(col)
                except:
                    pass
            
            analysis['column_characteristics'][col] = col_info
        
        # Analyze relationships between columns
        numerical_cols = analysis['numerical_columns']
        if len(numerical_cols) > 1:
            for i, col1 in enumerate(numerical_cols):
                for col2 in numerical_cols[i+1:]:
                    corr = df[col1].corr(df[col2])
                    if abs(corr) > 0.3:  # Moderate correlation threshold
                        analysis['relationships'].append({
                            'column1': col1,
                            'column2': col2,
                            'correlation': float(corr),
                            'relationship_strength': 'strong' if abs(corr) > 0.7 else 'moderate'
                        })
        
        return analysis
    
    def _recommend_charts(self, df: pd.DataFrame, query: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend appropriate chart types based on data analysis"""
        recommendations = []
        
        numerical_cols = analysis['numerical_columns']
        categorical_cols = analysis['categorical_columns']
        temporal_cols = analysis['temporal_columns']
        
        # Single numerical column visualizations
        for col in numerical_cols:
            col_info = analysis['column_characteristics'][col]
            
            # Histogram for distribution
            recommendations.append({
                'chart_type': 'histogram',
                'title': f'Distribution of {col}',
                'columns': [col],
                'purpose': 'Show data distribution',
                'priority': 'high' if 'distribution' in query.lower() else 'medium',
                'config': {
                    'x_axis': col,
                    'bins': min(30, col_info['unique_values']),
                    'color': '#3b82f6'
                }
            })
            
            # Box plot for outlier detection
            recommendations.append({
                'chart_type': 'box_plot',
                'title': f'Box Plot of {col}',
                'columns': [col],
                'purpose': 'Identify outliers and quartiles',
                'priority': 'medium',
                'config': {
                    'y_axis': col,
                    'color': '#10b981'
                }
            })
        
        # Categorical column visualizations
        for col in categorical_cols:
            col_info = analysis['column_characteristics'][col]
            
            if col_info['unique_values'] <= 20:  # Reasonable number for bar chart
                recommendations.append({
                    'chart_type': 'bar_chart',
                    'title': f'Count by {col}',
                    'columns': [col],
                    'purpose': 'Show category frequencies',
                    'priority': 'high' if any(word in query.lower() for word in ['count', 'frequency', 'category']) else 'medium',
                    'config': {
                        'x_axis': col,
                        'y_axis': 'count',
                        'color': '#f59e0b'
                    }
                })
                
                # Pie chart for proportions
                if col_info['unique_values'] <= 8:  # Good for pie charts
                    recommendations.append({
                        'chart_type': 'pie_chart',
                        'title': f'Proportion by {col}',
                        'columns': [col],
                        'purpose': 'Show category proportions',
                        'priority': 'medium',
                        'config': {
                            'category': col,
                            'colors': ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316']
                        }
                    })
        
        # Numerical vs Categorical
        for num_col in numerical_cols:
            for cat_col in categorical_cols:
                cat_info = analysis['column_characteristics'][cat_col]
                if cat_info['unique_values'] <= 10:  # Reasonable for grouping
                    recommendations.append({
                        'chart_type': 'grouped_bar_chart',
                        'title': f'{num_col} by {cat_col}',
                        'columns': [cat_col, num_col],
                        'purpose': 'Compare numerical values across categories',
                        'priority': 'high' if any(word in query.lower() for word in ['by', 'compare', 'across']) else 'medium',
                        'config': {
                            'x_axis': cat_col,
                            'y_axis': num_col,
                            'group_by': cat_col,
                            'color': '#3b82f6'
                        }
                    })
        
        # Numerical vs Numerical (Scatter plots)
        for i, col1 in enumerate(numerical_cols):
            for col2 in numerical_cols[i+1:]:
                # Check if there's a relationship
                relationship = next((r for r in analysis['relationships'] 
                                   if (r['column1'] == col1 and r['column2'] == col2) or 
                                      (r['column1'] == col2 and r['column2'] == col1)), None)
                
                priority = 'high' if relationship and relationship['relationship_strength'] == 'strong' else 'medium'
                
                recommendations.append({
                    'chart_type': 'scatter_plot',
                    'title': f'{col1} vs {col2}',
                    'columns': [col1, col2],
                    'purpose': 'Show relationship between two numerical variables',
                    'priority': priority,
                    'config': {
                        'x_axis': col1,
                        'y_axis': col2,
                        'color': '#8b5cf6',
                        'show_trend_line': relationship is not None
                    }
                })
        
        # Time series if temporal columns exist
        for temp_col in temporal_cols:
            for num_col in numerical_cols:
                recommendations.append({
                    'chart_type': 'line_chart',
                    'title': f'{num_col} over {temp_col}',
                    'columns': [temp_col, num_col],
                    'purpose': 'Show trends over time',
                    'priority': 'high' if any(word in query.lower() for word in ['trend', 'time', 'over', 'change']) else 'medium',
                    'config': {
                        'x_axis': temp_col,
                        'y_axis': num_col,
                        'color': '#ef4444',
                        'show_points': False
                    }
                })
        
        # Correlation heatmap if multiple numerical columns
        if len(numerical_cols) > 2:
            recommendations.append({
                'chart_type': 'heatmap',
                'title': 'Correlation Matrix',
                'columns': numerical_cols,
                'purpose': 'Show correlations between all numerical variables',
                'priority': 'high' if 'correlation' in query.lower() else 'medium',
                'config': {
                    'color_scale': 'RdBu',
                    'show_values': True
                }
            })
        
        return recommendations
    
    def _get_priority_charts(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get high priority chart recommendations"""
        return [chart for chart in recommendations if chart['priority'] == 'high']
    
    def _generate_chart_configs(self, recommendations: List[Dict[str, Any]], df: pd.DataFrame) -> Dict[str, Any]:
        """Generate detailed chart configurations for frontend"""
        configs = {}
        
        for i, chart in enumerate(recommendations):
            chart_id = f"chart_{i+1}"
            
            # Base configuration
            config = {
                'id': chart_id,
                'type': chart['chart_type'],
                'title': chart['title'],
                'data': self._prepare_chart_data(chart, df),
                'options': chart['config'].copy()
            }
            
            # Add responsive settings
            config['responsive'] = True
            config['maintainAspectRatio'] = False
            
            # Add styling based on chart type
            if chart['chart_type'] in ['bar_chart', 'grouped_bar_chart']:
                config['options']['scales'] = {
                    'x': {'title': {'display': True, 'text': chart['config'].get('x_axis', '')}},
                    'y': {'title': {'display': True, 'text': chart['config'].get('y_axis', '')}}
                }
            elif chart['chart_type'] == 'scatter_plot':
                config['options']['plugins'] = {
                    'legend': {'display': False},
                    'tooltip': {'mode': 'point'}
                }
            
            configs[chart_id] = config
        
        return configs
    
    def _prepare_chart_data(self, chart: Dict[str, Any], df: pd.DataFrame) -> Dict[str, Any]:
        """Prepare data for specific chart type"""
        chart_type = chart['chart_type']
        columns = chart['columns']
        
        if chart_type == 'histogram':
            col = columns[0]
            data = df[col].dropna()
            return {
                'values': data.tolist(),
                'column': col
            }
        
        elif chart_type == 'bar_chart':
            col = columns[0]
            value_counts = df[col].value_counts()
            return {
                'labels': value_counts.index.tolist(),
                'values': value_counts.values.tolist(),
                'column': col
            }
        
        elif chart_type == 'scatter_plot':
            col1, col2 = columns[0], columns[1]
            clean_df = df[[col1, col2]].dropna()
            return {
                'x_values': clean_df[col1].tolist(),
                'y_values': clean_df[col2].tolist(),
                'x_column': col1,
                'y_column': col2
            }
        
        elif chart_type == 'line_chart':
            x_col, y_col = columns[0], columns[1]
            clean_df = df[[x_col, y_col]].dropna().sort_values(x_col)
            return {
                'x_values': clean_df[x_col].tolist(),
                'y_values': clean_df[y_col].tolist(),
                'x_column': x_col,
                'y_column': y_col
            }
        
        elif chart_type == 'heatmap':
            corr_matrix = df[columns].corr()
            return {
                'correlation_matrix': corr_matrix.values.tolist(),
                'labels': corr_matrix.columns.tolist()
            }
        
        else:
            # Generic data preparation
            return {
                'raw_data': df[columns].to_dict('records')[:100],  # Limit for performance
                'columns': columns
            }
    
    def _create_visualization_prompt(self, query: str, analysis: Dict[str, Any], recommendations: List[Dict[str, Any]], df: pd.DataFrame) -> str:
        """Create prompt for AI visualization insights"""
        return f"""
        Based on the data visualization analysis, provide insights for this query: "{query}"
        
        Dataset Overview:
        - Shape: {df.shape}
        - Numerical columns: {len(analysis['numerical_columns'])}
        - Categorical columns: {len(analysis['categorical_columns'])}
        - Temporal columns: {len(analysis['temporal_columns'])}
        
        Data Characteristics:
        {analysis['column_characteristics']}
        
        Relationships Found:
        {analysis['relationships']}
        
        Chart Recommendations ({len(recommendations)} total):
        {[f"{r['chart_type']}: {r['title']} (Priority: {r['priority']})" for r in recommendations[:5]]}
        
        Please provide:
        1. Explanation of why these chart types are recommended
        2. Best practices for visualizing this type of data
        3. Insights that each chart type would reveal
        4. Suggestions for interactive features
        5. Color scheme and styling recommendations
        """


class DashboardDesignerAgent(BaseAgent):
    """Dashboard Design Specialist - Creates comprehensive dashboard layouts"""
    
    def __init__(self):
        super().__init__(
            agent_id="dashboard_designer",
            name="Dashboard Design Specialist",
            role="visualization",
            description="Creates comprehensive dashboard layouts",
            specialization="Dashboard Design and User Experience"
        )
        self.capabilities = [
            "Dashboard layout design",
            "User experience optimization",
            "Responsive design",
            "Information architecture",
            "Interactive features",
            "Visual hierarchy"
        ]
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Design dashboard layout and organization"""
        try:
            self.update_status("designing", "Creating dashboard layout recommendations")
            
            # Parse CSV data
            csv_data = data.get('csv_data', '')
            df = self._parse_csv_data(csv_data)
            if df is None:
                return {
                    'success': False,
                    'error': 'Failed to parse CSV data',
                    'analysis': None
                }
            
            # Get chart recommendations from context if available
            chart_recommendations = []
            if context and 'chart_recommendations' in context:
                chart_recommendations = context['chart_recommendations']
            else:
                # Generate basic chart recommendations
                chart_recommendations = self._generate_basic_charts(df)
            
            # Design dashboard layout
            dashboard_design = self._design_dashboard_layout(df, query, chart_recommendations)
            
            # Generate AI insights
            dashboard_prompt = self._create_dashboard_prompt(query, dashboard_design, df)
            ai_response = self.generate_response(dashboard_prompt, context)
            
            if not ai_response['success']:
                return ai_response
            
            self.update_status("completed", "Dashboard design completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'dashboard_design',
                'dashboard_layout': dashboard_design,
                'ai_insights': ai_response['content'],
                'layout_sections': dashboard_design['sections'],
                'responsive_config': dashboard_design['responsive_config'],
                'interaction_features': dashboard_design['interactions']
            }
            
        except Exception as e:
            logger.error(f"Dashboard Designer error: {e}")
            self.update_status("error", f"Dashboard design failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis': None
            }
    
    def _parse_csv_data(self, csv_data: str) -> pd.DataFrame:
        """Parse CSV data into DataFrame"""
        try:
            from io import StringIO
            return pd.read_csv(StringIO(csv_data))
        except Exception as e:
            logger.error(f"CSV parsing error: {e}")
            return None
    
    def _generate_basic_charts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate basic chart recommendations for dashboard"""
        charts = []
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # Key metrics cards
        for col in numerical_cols:
            charts.append({
                'type': 'metric_card',
                'title': f'{col} Summary',
                'columns': [col],
                'priority': 'high',
                'size': 'small'
            })
        
        # Distribution charts
        for col in numerical_cols[:3]:  # Limit to first 3
            charts.append({
                'type': 'histogram',
                'title': f'Distribution of {col}',
                'columns': [col],
                'priority': 'medium',
                'size': 'medium'
            })
        
        # Category charts
        for col in categorical_cols[:2]:  # Limit to first 2
            if df[col].nunique() <= 10:
                charts.append({
                    'type': 'bar_chart',
                    'title': f'Count by {col}',
                    'columns': [col],
                    'priority': 'medium',
                    'size': 'medium'
                })
        
        return charts
    
    def _design_dashboard_layout(self, df: pd.DataFrame, query: str, chart_recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Design comprehensive dashboard layout"""
        
        # Categorize charts by priority and type
        high_priority = [c for c in chart_recommendations if c.get('priority') == 'high']
        medium_priority = [c for c in chart_recommendations if c.get('priority') == 'medium']
        
        # Design layout sections
        sections = []
        
        # Header section with key metrics
        metric_charts = [c for c in chart_recommendations if c.get('type') == 'metric_card']
        if metric_charts:
            sections.append({
                'id': 'metrics_header',
                'title': 'Key Metrics',
                'type': 'metrics_row',
                'position': 1,
                'height': '120px',
                'charts': metric_charts[:4],  # Max 4 metrics in header
                'layout': 'horizontal',
                'responsive': {
                    'mobile': {'columns': 2},
                    'tablet': {'columns': 3},
                    'desktop': {'columns': 4}
                }
            })
        
        # Main analysis section
        main_charts = [c for c in high_priority if c.get('type') != 'metric_card']
        if main_charts:
            sections.append({
                'id': 'main_analysis',
                'title': 'Primary Analysis',
                'type': 'chart_grid',
                'position': 2,
                'height': 'auto',
                'charts': main_charts[:4],  # Max 4 main charts
                'layout': 'grid',
                'responsive': {
                    'mobile': {'columns': 1},
                    'tablet': {'columns': 2},
                    'desktop': {'columns': 2}
                }
            })
        
        # Secondary analysis section
        secondary_charts = medium_priority[:6]  # Max 6 secondary charts
        if secondary_charts:
            sections.append({
                'id': 'secondary_analysis',
                'title': 'Detailed Analysis',
                'type': 'chart_grid',
                'position': 3,
                'height': 'auto',
                'charts': secondary_charts,
                'layout': 'grid',
                'responsive': {
                    'mobile': {'columns': 1},
                    'tablet': {'columns': 2},
                    'desktop': {'columns': 3}
                }
            })
        
        # Data table section
        sections.append({
            'id': 'data_table',
            'title': 'Data Table',
            'type': 'data_table',
            'position': 4,
            'height': '400px',
            'collapsible': True,
            'data': {
                'columns': df.columns.tolist(),
                'sample_data': df.head(10).to_dict('records')
            },
            'responsive': {
                'mobile': {'scrollable': True},
                'tablet': {'scrollable': True},
                'desktop': {'scrollable': False}
            }
        })
        
        # Dashboard configuration
        dashboard_config = {
            'title': self._generate_dashboard_title(query, df),
            'description': f'Interactive dashboard for {len(df)} records with {len(df.columns)} variables',
            'sections': sections,
            'theme': {
                'primary_color': '#3b82f6',
                'secondary_color': '#10b981',
                'background_color': '#f8fafc',
                'text_color': '#1f2937',
                'card_background': '#ffffff'
            },
            'responsive_config': {
                'breakpoints': {
                    'mobile': 768,
                    'tablet': 1024,
                    'desktop': 1200
                },
                'grid_system': {
                    'columns': 12,
                    'gutter': '16px',
                    'margin': '24px'
                }
            },
            'interactions': {
                'cross_filtering': True,
                'drill_down': True,
                'export_options': ['PNG', 'PDF', 'CSV'],
                'real_time_updates': False
            },
            'performance': {
                'lazy_loading': True,
                'virtual_scrolling': True,
                'data_pagination': True,
                'max_data_points': 10000
            }
        }
        
        return dashboard_config
    
    def _generate_dashboard_title(self, query: str, df: pd.DataFrame) -> str:
        """Generate appropriate dashboard title"""
        # Extract key terms from query
        key_terms = []
        query_lower = query.lower()
        
        # Look for business terms
        business_terms = ['sales', 'revenue', 'profit', 'customer', 'product', 'performance', 'analysis']
        for term in business_terms:
            if term in query_lower:
                key_terms.append(term.title())
        
        # Look for column names in query
        for col in df.columns:
            if col.lower() in query_lower:
                key_terms.append(col)
        
        if key_terms:
            return f"{' & '.join(key_terms[:2])} Dashboard"
        else:
            return "Business Intelligence Dashboard"
    
    def _create_dashboard_prompt(self, query: str, dashboard_design: Dict[str, Any], df: pd.DataFrame) -> str:
        """Create prompt for AI dashboard insights"""
        return f"""
        Based on the dashboard design analysis, provide insights for this query: "{query}"
        
        Dataset Overview:
        - Shape: {df.shape}
        - Columns: {list(df.columns)}
        
        Dashboard Design:
        - Title: {dashboard_design['title']}
        - Sections: {len(dashboard_design['sections'])}
        - Theme: {dashboard_design['theme']}
        
        Layout Sections:
        {[f"{s['title']} ({s['type']})" for s in dashboard_design['sections']]}
        
        Interactive Features:
        {dashboard_design['interactions']}
        
        Please provide:
        1. Explanation of the dashboard layout rationale
        2. User experience considerations
        3. Best practices for dashboard navigation
        4. Suggestions for improving data storytelling
        5. Recommendations for mobile responsiveness
        6. Ideas for advanced interactive features
        """