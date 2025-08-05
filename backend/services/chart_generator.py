"""
Chart Generation Service
Automatically generates chart specifications based on data analysis and user queries
"""

import json
import logging
from typing import Dict, List, Any, Optional
import pandas as pd

logger = logging.getLogger(__name__)

class ChartGeneratorService:
    """Service for automatically generating chart specifications"""
    
    def __init__(self):
        self.chart_types = {
            'line': 'Time series and trend analysis',
            'bar': 'Categorical comparisons',
            'area': 'Cumulative trends over time',
            'pie': 'Proportional data representation',
            'scatter': 'Correlation analysis'
        }
    
    def generate_charts_for_query(self, csv_data: str, query: str) -> Dict[str, Any]:
        """Generate chart specifications based on CSV data and user query"""
        try:
            # Parse CSV data
            data_info = self._analyze_csv_data(csv_data)
            
            # Determine chart types based on query
            recommended_charts = self._recommend_charts_for_query(query, data_info)
            
            # Generate chart specifications
            chart_specs = self._create_chart_specifications(recommended_charts, data_info)
            
            return {
                'success': True,
                'charts': chart_specs,
                'data_info': data_info,
                'query': query
            }
            
        except Exception as e:
            logger.error(f"Chart generation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'charts': []
            }
    
    def _analyze_csv_data(self, csv_data: str) -> Dict[str, Any]:
        """Analyze CSV data structure and content"""
        try:
            # Parse CSV data
            from io import StringIO
            df = pd.read_csv(StringIO(csv_data))
            
            # Analyze columns
            columns_info = {}
            for col in df.columns:
                col_data = df[col].dropna()
                
                # Determine column type
                if pd.api.types.is_numeric_dtype(col_data):
                    col_type = 'numeric'
                elif pd.api.types.is_datetime64_any_dtype(col_data):
                    col_type = 'datetime'
                else:
                    # Check if it looks like a date
                    if any(word in col.lower() for word in ['date', 'time', 'week', 'month', 'year']):
                        col_type = 'date'
                    else:
                        col_type = 'categorical'
                
                columns_info[col] = {
                    'type': col_type,
                    'sample_values': col_data.head(3).tolist(),
                    'unique_count': col_data.nunique(),
                    'null_count': df[col].isnull().sum()
                }
            
            return {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': columns_info,
                'numeric_columns': [col for col, info in columns_info.items() if info['type'] == 'numeric'],
                'categorical_columns': [col for col, info in columns_info.items() if info['type'] == 'categorical'],
                'date_columns': [col for col, info in columns_info.items() if info['type'] in ['date', 'datetime']]
            }
            
        except Exception as e:
            logger.error(f"CSV analysis failed: {e}")
            return {'error': str(e)}
    
    def _recommend_charts_for_query(self, query: str, data_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend chart types based on query and data structure"""
        query_lower = query.lower()
        recommendations = []
        
        # Get available columns
        numeric_cols = data_info.get('numeric_columns', [])
        categorical_cols = data_info.get('categorical_columns', [])
        date_cols = data_info.get('date_columns', [])
        
        # Chart recommendations based on query keywords
        if any(word in query_lower for word in ['trend', 'over time', 'time series', 'line']):
            if date_cols and numeric_cols:
                recommendations.append({
                    'type': 'line',
                    'priority': 1,
                    'reason': 'Time series analysis requested',
                    'x_axis': date_cols[0],
                    'y_axis': numeric_cols[0]
                })
        
        if any(word in query_lower for word in ['bar', 'compare', 'comparison', 'by country', 'by category']):
            if categorical_cols and numeric_cols:
                recommendations.append({
                    'type': 'bar',
                    'priority': 1,
                    'reason': 'Categorical comparison requested',
                    'x_axis': categorical_cols[0],
                    'y_axis': numeric_cols[0]
                })
        
        if any(word in query_lower for word in ['pie', 'proportion', 'percentage', 'share']):
            if categorical_cols and numeric_cols:
                recommendations.append({
                    'type': 'pie',
                    'priority': 2,
                    'reason': 'Proportional analysis requested',
                    'category': categorical_cols[0],
                    'value': numeric_cols[0]
                })
        
        if any(word in query_lower for word in ['scatter', 'correlation', 'relationship']):
            if len(numeric_cols) >= 2:
                recommendations.append({
                    'type': 'scatter',
                    'priority': 2,
                    'reason': 'Correlation analysis requested',
                    'x_axis': numeric_cols[0],
                    'y_axis': numeric_cols[1]
                })
        
        # Default recommendations if no specific chart type requested
        if not recommendations:
            # Auto-recommend based on data structure
            if date_cols and numeric_cols:
                recommendations.append({
                    'type': 'line',
                    'priority': 1,
                    'reason': 'Time series data detected',
                    'x_axis': date_cols[0],
                    'y_axis': numeric_cols[0]
                })
            
            if categorical_cols and numeric_cols:
                recommendations.append({
                    'type': 'bar',
                    'priority': 1,
                    'reason': 'Categorical data detected',
                    'x_axis': categorical_cols[0],
                    'y_axis': numeric_cols[0]
                })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'])
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def _create_chart_specifications(self, recommendations: List[Dict[str, Any]], data_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create detailed chart specifications"""
        chart_specs = []
        
        for i, rec in enumerate(recommendations):
            chart_spec = {
                'id': f'chart_{i+1}',
                'type': rec['type'],
                'title': self._generate_chart_title(rec),
                'description': rec['reason'],
                'config': self._generate_chart_config(rec),
                'priority': rec['priority']
            }
            
            chart_specs.append(chart_spec)
        
        return chart_specs
    
    def _generate_chart_title(self, recommendation: Dict[str, Any]) -> str:
        """Generate appropriate chart title"""
        chart_type = recommendation['type']
        
        if chart_type == 'line':
            x_axis = recommendation.get('x_axis', 'Time')
            y_axis = recommendation.get('y_axis', 'Value')
            return f"{y_axis} Trends Over {x_axis}"
        
        elif chart_type == 'bar':
            x_axis = recommendation.get('x_axis', 'Category')
            y_axis = recommendation.get('y_axis', 'Value')
            return f"{y_axis} by {x_axis}"
        
        elif chart_type == 'pie':
            category = recommendation.get('category', 'Category')
            return f"Distribution by {category}"
        
        elif chart_type == 'scatter':
            x_axis = recommendation.get('x_axis', 'X')
            y_axis = recommendation.get('y_axis', 'Y')
            return f"{y_axis} vs {x_axis} Correlation"
        
        else:
            return f"{chart_type.title()} Chart"
    
    def _generate_chart_config(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate chart configuration"""
        config = {
            'type': recommendation['type'],
            'responsive': True,
            'animation': True
        }
        
        if recommendation['type'] in ['line', 'bar', 'scatter']:
            config.update({
                'xAxis': {
                    'dataKey': recommendation.get('x_axis'),
                    'type': 'category' if recommendation['type'] == 'bar' else 'auto'
                },
                'yAxis': {
                    'dataKey': recommendation.get('y_axis'),
                    'type': 'number'
                }
            })
        
        elif recommendation['type'] == 'pie':
            config.update({
                'dataKey': recommendation.get('value'),
                'nameKey': recommendation.get('category')
            })
        
        return config

# Global instance
chart_generator = ChartGeneratorService()