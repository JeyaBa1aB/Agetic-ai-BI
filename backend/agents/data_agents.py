"""
Data Intelligence Team agents for Multi-Agent BI Assistant
Specialized agents for data analysis, processing, and pattern detection
"""
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class DataAnalystAgent(BaseAgent):
    """Senior Data Analyst - Performs statistical analysis and data quality assessment"""
    
    def __init__(self):
        super().__init__(
            agent_id="data_analyst",
            name="Senior Data Analyst",
            role="data_intelligence",
            description="Performs statistical analysis and data quality assessment",
            specialization="Statistical Analysis and Data Quality Assessment"
        )
        self.capabilities = [
            "Statistical analysis",
            "Data quality assessment",
            "Descriptive statistics",
            "Data profiling",
            "Outlier detection",
            "Missing data analysis"
        ]
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform statistical analysis on the provided data"""
        try:
            self.update_status("analyzing", "Performing statistical analysis")
            
            # Parse CSV data
            csv_data = data.get('csv_data', '')
            if not csv_data:
                return {
                    'success': False,
                    'error': 'No CSV data provided',
                    'analysis': None
                }
            
            # Convert to DataFrame for analysis
            df = self._parse_csv_data(csv_data)
            if df is None:
                return {
                    'success': False,
                    'error': 'Failed to parse CSV data',
                    'analysis': None
                }
            
            # Perform statistical analysis
            stats_analysis = self._perform_statistical_analysis(df)
            
            # Generate AI insights
            analysis_prompt = self._create_analysis_prompt(query, stats_analysis, df)
            ai_response = self.generate_response(analysis_prompt, context)
            
            if not ai_response['success']:
                return ai_response
            
            self.update_status("completed", "Statistical analysis completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'statistical_analysis',
                'statistical_summary': stats_analysis,
                'ai_insights': ai_response['content'],
                'recommendations': self._generate_recommendations(stats_analysis),
                'data_quality_score': self._calculate_data_quality_score(df)
            }
            
        except Exception as e:
            logger.error(f"Data Analyst error: {e}")
            self.update_status("error", f"Analysis failed: {str(e)}")
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
    
    def _perform_statistical_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform comprehensive statistical analysis"""
        analysis = {
            'basic_info': {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'data_types': {col: str(dtype) for col, dtype in df.dtypes.items()}
            },
            'missing_data': {
                'total_missing': int(df.isnull().sum().sum()),
                'missing_by_column': {col: int(count) for col, count in df.isnull().sum().items()},
                'missing_percentage': {col: round(count/len(df)*100, 2) for col, count in df.isnull().sum().items()}
            },
            'numerical_analysis': {},
            'categorical_analysis': {}
        }
        
        # Analyze numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                analysis['numerical_analysis'][col] = {
                    'count': int(len(col_data)),
                    'mean': float(col_data.mean()),
                    'median': float(col_data.median()),
                    'std': float(col_data.std()) if len(col_data) > 1 else 0,
                    'min': float(col_data.min()),
                    'max': float(col_data.max()),
                    'q25': float(col_data.quantile(0.25)),
                    'q75': float(col_data.quantile(0.75)),
                    'skewness': float(col_data.skew()) if len(col_data) > 1 else 0,
                    'outliers_count': int(self._count_outliers(col_data))
                }
        
        # Analyze categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                value_counts = col_data.value_counts()
                analysis['categorical_analysis'][col] = {
                    'unique_values': int(col_data.nunique()),
                    'most_frequent': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                    'most_frequent_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                    'top_5_values': {str(k): int(v) for k, v in value_counts.head(5).items()}
                }
        
        return analysis
    
    def _count_outliers(self, series: pd.Series) -> int:
        """Count outliers using IQR method"""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return len(series[(series < lower_bound) | (series > upper_bound)])
    
    def _create_analysis_prompt(self, query: str, stats: Dict[str, Any], df: pd.DataFrame) -> str:
        """Create prompt for AI analysis"""
        return f"""
        Based on the statistical analysis of the dataset, please provide insights for this query: "{query}"
        
        Dataset Overview:
        - Rows: {stats['basic_info']['rows']}
        - Columns: {stats['basic_info']['columns']}
        - Column Names: {', '.join(stats['basic_info']['column_names'])}
        
        Data Quality:
        - Total Missing Values: {stats['missing_data']['total_missing']}
        - Missing Data by Column: {stats['missing_data']['missing_percentage']}
        
        Numerical Analysis: {stats['numerical_analysis']}
        Categorical Analysis: {stats['categorical_analysis']}
        
        Please provide:
        1. Key statistical insights
        2. Data quality assessment
        3. Notable patterns or anomalies
        4. Recommendations for further analysis
        """
    
    def _generate_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Generate data analysis recommendations"""
        recommendations = []
        
        # Missing data recommendations
        total_missing = stats['missing_data']['total_missing']
        if total_missing > 0:
            recommendations.append(f"Address {total_missing} missing values in the dataset")
        
        # Outlier recommendations
        for col, analysis in stats['numerical_analysis'].items():
            if analysis['outliers_count'] > 0:
                recommendations.append(f"Investigate {analysis['outliers_count']} outliers in {col}")
        
        # Data distribution recommendations
        for col, analysis in stats['numerical_analysis'].items():
            if abs(analysis['skewness']) > 2:
                recommendations.append(f"Consider data transformation for highly skewed column: {col}")
        
        return recommendations
    
    def _calculate_data_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate overall data quality score (0-100)"""
        score = 100.0
        
        # Deduct for missing values
        missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        score -= missing_ratio * 30
        
        # Deduct for duplicate rows
        duplicate_ratio = df.duplicated().sum() / len(df)
        score -= duplicate_ratio * 20
        
        # Deduct for columns with very low variance
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].std() == 0:  # No variance
                score -= 10
        
        return max(0.0, min(100.0, score))


class DataProcessorAgent(BaseAgent):
    """Data Processing Specialist - Cleans, transforms, and prepares data for analysis"""
    
    def __init__(self):
        super().__init__(
            agent_id="data_processor",
            name="Data Processing Specialist",
            role="data_intelligence",
            description="Cleans, transforms, and prepares data for analysis",
            specialization="Data Cleaning and Transformation"
        )
        self.capabilities = [
            "Data cleaning",
            "Missing value handling",
            "Data transformation",
            "Data type conversion",
            "Duplicate removal",
            "Data normalization"
        ]
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze data processing needs and provide recommendations"""
        try:
            self.update_status("processing", "Analyzing data processing requirements")
            
            # Parse CSV data
            csv_data = data.get('csv_data', '')
            df = self._parse_csv_data(csv_data)
            if df is None:
                return {
                    'success': False,
                    'error': 'Failed to parse CSV data',
                    'analysis': None
                }
            
            # Analyze data processing needs
            processing_analysis = self._analyze_processing_needs(df)
            
            # Generate AI recommendations
            processing_prompt = self._create_processing_prompt(query, processing_analysis, df)
            ai_response = self.generate_response(processing_prompt, context)
            
            if not ai_response['success']:
                return ai_response
            
            self.update_status("completed", "Data processing analysis completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'data_processing',
                'processing_recommendations': processing_analysis,
                'ai_insights': ai_response['content'],
                'data_cleaning_steps': self._generate_cleaning_steps(processing_analysis),
                'transformation_suggestions': self._suggest_transformations(df)
            }
            
        except Exception as e:
            logger.error(f"Data Processor error: {e}")
            self.update_status("error", f"Processing failed: {str(e)}")
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
    
    def _analyze_processing_needs(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze what data processing is needed"""
        analysis = {
            'data_issues': [],
            'cleaning_needed': False,
            'transformation_opportunities': [],
            'data_types_issues': [],
            'encoding_issues': []
        }
        
        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            analysis['data_issues'].append({
                'type': 'missing_values',
                'severity': 'high' if missing_data.sum() > len(df) * 0.1 else 'medium',
                'details': {col: int(count) for col, count in missing_data.items() if count > 0}
            })
            analysis['cleaning_needed'] = True
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            analysis['data_issues'].append({
                'type': 'duplicate_rows',
                'severity': 'medium',
                'count': int(duplicates)
            })
            analysis['cleaning_needed'] = True
        
        # Check data types
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if numeric data is stored as string
                try:
                    pd.to_numeric(df[col].dropna(), errors='raise')
                    analysis['data_types_issues'].append({
                        'column': col,
                        'issue': 'numeric_as_string',
                        'recommendation': 'convert_to_numeric'
                    })
                except:
                    pass
        
        # Check for transformation opportunities
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                skewness = col_data.skew()
                if abs(skewness) > 2:
                    analysis['transformation_opportunities'].append({
                        'column': col,
                        'issue': 'high_skewness',
                        'skewness': float(skewness),
                        'recommendation': 'log_transform' if skewness > 0 else 'square_transform'
                    })
        
        return analysis
    
    def _create_processing_prompt(self, query: str, analysis: Dict[str, Any], df: pd.DataFrame) -> str:
        """Create prompt for AI processing recommendations"""
        return f"""
        Based on the data processing analysis, provide recommendations for this query: "{query}"
        
        Dataset Info:
        - Shape: {df.shape}
        - Columns: {list(df.columns)}
        
        Data Issues Found:
        {analysis['data_issues']}
        
        Data Type Issues:
        {analysis['data_types_issues']}
        
        Transformation Opportunities:
        {analysis['transformation_opportunities']}
        
        Please provide:
        1. Priority order for data cleaning steps
        2. Specific transformation recommendations
        3. Data quality improvement strategies
        4. Best practices for this type of dataset
        """
    
    def _generate_cleaning_steps(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate step-by-step data cleaning recommendations"""
        steps = []
        
        # Handle missing values
        for issue in analysis['data_issues']:
            if issue['type'] == 'missing_values':
                steps.append({
                    'step': 'handle_missing_values',
                    'priority': 'high',
                    'description': 'Address missing values in dataset',
                    'affected_columns': list(issue['details'].keys()),
                    'methods': ['drop_rows', 'fill_mean', 'fill_median', 'forward_fill']
                })
        
        # Handle duplicates
        for issue in analysis['data_issues']:
            if issue['type'] == 'duplicate_rows':
                steps.append({
                    'step': 'remove_duplicates',
                    'priority': 'medium',
                    'description': f'Remove {issue["count"]} duplicate rows',
                    'method': 'drop_duplicates'
                })
        
        # Fix data types
        for issue in analysis['data_types_issues']:
            steps.append({
                'step': 'fix_data_types',
                'priority': 'medium',
                'description': f'Convert {issue["column"]} to proper data type',
                'column': issue['column'],
                'action': issue['recommendation']
            })
        
        return steps
    
    def _suggest_transformations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Suggest data transformations"""
        suggestions = []
        
        # Normalization suggestions
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 1:
            suggestions.append({
                'type': 'normalization',
                'description': 'Normalize numerical columns for better analysis',
                'columns': list(numerical_cols),
                'methods': ['min_max_scaling', 'z_score_normalization']
            })
        
        # Encoding suggestions for categorical data
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            suggestions.append({
                'type': 'categorical_encoding',
                'description': 'Encode categorical variables for analysis',
                'columns': list(categorical_cols),
                'methods': ['one_hot_encoding', 'label_encoding']
            })
        
        return suggestions


class PatternDetectorAgent(BaseAgent):
    """Pattern Detection Specialist - Identifies trends, anomalies, and hidden patterns"""
    
    def __init__(self):
        super().__init__(
            agent_id="pattern_detector",
            name="Pattern Detection Specialist",
            role="data_intelligence",
            description="Identifies trends, anomalies, and hidden patterns",
            specialization="Pattern Recognition and Anomaly Detection"
        )
        self.capabilities = [
            "Pattern recognition",
            "Anomaly detection",
            "Trend analysis",
            "Correlation analysis",
            "Distribution analysis",
            "Time series patterns"
        ]
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Detect patterns and anomalies in the data"""
        try:
            self.update_status("detecting", "Analyzing patterns and anomalies")
            
            # Parse CSV data
            csv_data = data.get('csv_data', '')
            df = self._parse_csv_data(csv_data)
            if df is None:
                return {
                    'success': False,
                    'error': 'Failed to parse CSV data',
                    'analysis': None
                }
            
            # Detect patterns
            pattern_analysis = self._detect_patterns(df)
            
            # Generate AI insights
            pattern_prompt = self._create_pattern_prompt(query, pattern_analysis, df)
            ai_response = self.generate_response(pattern_prompt, context)
            
            if not ai_response['success']:
                return ai_response
            
            self.update_status("completed", "Pattern detection completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'pattern_detection',
                'patterns_found': pattern_analysis,
                'ai_insights': ai_response['content'],
                'anomalies': pattern_analysis.get('anomalies', []),
                'trends': pattern_analysis.get('trends', []),
                'correlations': pattern_analysis.get('correlations', {})
            }
            
        except Exception as e:
            logger.error(f"Pattern Detector error: {e}")
            self.update_status("error", f"Pattern detection failed: {str(e)}")
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
    
    def _detect_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect various patterns in the data"""
        patterns = {
            'trends': [],
            'anomalies': [],
            'correlations': {},
            'distributions': {},
            'seasonal_patterns': []
        }
        
        # Detect correlations between numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 1:
            corr_matrix = df[numerical_cols].corr()
            strong_correlations = []
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:  # Strong correlation threshold
                        strong_correlations.append({
                            'column1': corr_matrix.columns[i],
                            'column2': corr_matrix.columns[j],
                            'correlation': float(corr_value),
                            'strength': 'strong' if abs(corr_value) > 0.8 else 'moderate'
                        })
            
            patterns['correlations'] = strong_correlations
        
        # Detect outliers/anomalies
        for col in numerical_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                if len(outliers) > 0:
                    patterns['anomalies'].append({
                        'column': col,
                        'type': 'statistical_outliers',
                        'count': len(outliers),
                        'percentage': round(len(outliers) / len(col_data) * 100, 2),
                        'values': outliers.tolist()[:10]  # First 10 outliers
                    })
        
        # Analyze distributions
        for col in numerical_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                patterns['distributions'][col] = {
                    'skewness': float(col_data.skew()),
                    'kurtosis': float(col_data.kurtosis()),
                    'distribution_type': self._identify_distribution_type(col_data)
                }
        
        # Detect trends (if there's a time-like column or sequential data)
        for col in numerical_cols:
            col_data = df[col].dropna()
            if len(col_data) > 2:
                # Simple trend detection using linear regression slope
                x = np.arange(len(col_data))
                slope = np.polyfit(x, col_data, 1)[0]
                
                if abs(slope) > col_data.std() * 0.01:  # Significant trend threshold
                    patterns['trends'].append({
                        'column': col,
                        'trend_direction': 'increasing' if slope > 0 else 'decreasing',
                        'slope': float(slope),
                        'strength': 'strong' if abs(slope) > col_data.std() * 0.05 else 'weak'
                    })
        
        return patterns
    
    def _identify_distribution_type(self, data: pd.Series) -> str:
        """Identify the likely distribution type of the data"""
        skewness = data.skew()
        kurtosis = data.kurtosis()
        
        if abs(skewness) < 0.5 and abs(kurtosis) < 0.5:
            return "normal"
        elif skewness > 1:
            return "right_skewed"
        elif skewness < -1:
            return "left_skewed"
        elif kurtosis > 3:
            return "heavy_tailed"
        elif kurtosis < -1:
            return "light_tailed"
        else:
            return "unknown"
    
    def _create_pattern_prompt(self, query: str, patterns: Dict[str, Any], df: pd.DataFrame) -> str:
        """Create prompt for AI pattern analysis"""
        return f"""
        Based on the pattern detection analysis, provide insights for this query: "{query}"
        
        Dataset Overview:
        - Shape: {df.shape}
        - Columns: {list(df.columns)}
        
        Patterns Detected:
        - Correlations: {len(patterns['correlations'])} strong correlations found
        - Anomalies: {len(patterns['anomalies'])} anomaly types detected
        - Trends: {len(patterns['trends'])} trends identified
        
        Detailed Findings:
        Correlations: {patterns['correlations']}
        Anomalies: {patterns['anomalies']}
        Trends: {patterns['trends']}
        Distributions: {patterns['distributions']}
        
        Please provide:
        1. Interpretation of the most significant patterns
        2. Business implications of detected anomalies
        3. Trend analysis and predictions
        4. Recommendations for further investigation
        """