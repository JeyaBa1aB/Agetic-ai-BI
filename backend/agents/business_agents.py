"""
Business Intelligence Team agents for Multi-Agent BI Assistant
Specialized agents for strategic business insights and market analysis
"""
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class BusinessStrategistAgent(BaseAgent):
    """Business Strategy Specialist - Provides strategic business insights and recommendations"""
    
    def __init__(self):
        super().__init__(
            agent_id="business_strategist",
            name="Business Strategy Specialist",
            role="business_intelligence",
            description="Provides strategic business insights and recommendations",
            specialization="Strategic Business Analysis and Planning"
        )
        self.capabilities = [
            "Strategic planning",
            "Business analysis",
            "Performance optimization",
            "Risk assessment",
            "Growth strategies",
            "Competitive analysis"
        ]
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze data from a strategic business perspective"""
        try:
            self.update_status("analyzing", "Performing strategic business analysis")
            
            # Parse CSV data
            csv_data = data.get('csv_data', '')
            df = self._parse_csv_data(csv_data)
            if df is None:
                return {
                    'success': False,
                    'error': 'Failed to parse CSV data',
                    'analysis': None
                }
            
            # Perform business analysis
            business_analysis = self._perform_business_analysis(df, query)
            
            # Generate strategic insights
            strategy_prompt = self._create_strategy_prompt(query, business_analysis, df, context)
            ai_response = self.generate_response(strategy_prompt, context)
            
            if not ai_response['success']:
                return ai_response
            
            self.update_status("completed", "Strategic business analysis completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'strategic_business_analysis',
                'business_metrics': business_analysis['metrics'],
                'strategic_insights': ai_response['content'],
                'recommendations': business_analysis['recommendations'],
                'risk_assessment': business_analysis['risks'],
                'opportunities': business_analysis['opportunities'],
                'kpi_analysis': business_analysis['kpis']
            }
            
        except Exception as e:
            logger.error(f"Business Strategist error: {e}")
            self.update_status("error", f"Strategic analysis failed: {str(e)}")
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
    
    def _perform_business_analysis(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Perform comprehensive business analysis"""
        analysis = {
            'metrics': {},
            'recommendations': [],
            'risks': [],
            'opportunities': [],
            'kpis': {},
            'business_context': {}
        }
        
        # Identify business-relevant columns
        business_columns = self._identify_business_columns(df)
        analysis['business_context'] = business_columns
        
        # Calculate key business metrics
        if business_columns['revenue_columns']:
            analysis['metrics']['revenue_analysis'] = self._analyze_revenue_metrics(df, business_columns['revenue_columns'])
        
        if business_columns['customer_columns']:
            analysis['metrics']['customer_analysis'] = self._analyze_customer_metrics(df, business_columns['customer_columns'])
        
        if business_columns['product_columns']:
            analysis['metrics']['product_analysis'] = self._analyze_product_metrics(df, business_columns['product_columns'])
        
        if business_columns['time_columns']:
            analysis['metrics']['temporal_analysis'] = self._analyze_temporal_trends(df, business_columns['time_columns'])
        
        # Generate strategic recommendations
        analysis['recommendations'] = self._generate_strategic_recommendations(df, business_columns, query)
        
        # Identify risks and opportunities
        analysis['risks'] = self._identify_business_risks(df, business_columns)
        analysis['opportunities'] = self._identify_opportunities(df, business_columns)
        
        # Calculate KPIs
        analysis['kpis'] = self._calculate_business_kpis(df, business_columns)
        
        return analysis
    
    def _identify_business_columns(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Identify columns that likely contain business-relevant data"""
        business_columns = {
            'revenue_columns': [],
            'cost_columns': [],
            'customer_columns': [],
            'product_columns': [],
            'time_columns': [],
            'quantity_columns': [],
            'performance_columns': []
        }
        
        # Keywords to identify different types of business columns
        revenue_keywords = ['revenue', 'sales', 'income', 'earnings', 'price', 'amount', 'value', 'total']
        cost_keywords = ['cost', 'expense', 'spend', 'budget', 'fee']
        customer_keywords = ['customer', 'client', 'user', 'buyer', 'account']
        product_keywords = ['product', 'item', 'service', 'category', 'type', 'model']
        time_keywords = ['date', 'time', 'year', 'month', 'day', 'period']
        quantity_keywords = ['quantity', 'count', 'number', 'volume', 'units']
        performance_keywords = ['performance', 'rating', 'score', 'efficiency', 'productivity']
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Check for revenue-related columns
            if any(keyword in col_lower for keyword in revenue_keywords):
                if df[col].dtype in ['int64', 'float64']:
                    business_columns['revenue_columns'].append(col)
            
            # Check for cost-related columns
            elif any(keyword in col_lower for keyword in cost_keywords):
                if df[col].dtype in ['int64', 'float64']:
                    business_columns['cost_columns'].append(col)
            
            # Check for customer-related columns
            elif any(keyword in col_lower for keyword in customer_keywords):
                business_columns['customer_columns'].append(col)
            
            # Check for product-related columns
            elif any(keyword in col_lower for keyword in product_keywords):
                business_columns['product_columns'].append(col)
            
            # Check for time-related columns
            elif any(keyword in col_lower for keyword in time_keywords):
                business_columns['time_columns'].append(col)
            
            # Check for quantity-related columns
            elif any(keyword in col_lower for keyword in quantity_keywords):
                if df[col].dtype in ['int64', 'float64']:
                    business_columns['quantity_columns'].append(col)
            
            # Check for performance-related columns
            elif any(keyword in col_lower for keyword in performance_keywords):
                if df[col].dtype in ['int64', 'float64']:
                    business_columns['performance_columns'].append(col)
        
        return business_columns
    
    def _analyze_revenue_metrics(self, df: pd.DataFrame, revenue_columns: List[str]) -> Dict[str, Any]:
        """Analyze revenue-related metrics"""
        metrics = {}
        
        for col in revenue_columns:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                metrics[col] = {
                    'total_revenue': float(col_data.sum()),
                    'average_revenue': float(col_data.mean()),
                    'median_revenue': float(col_data.median()),
                    'revenue_std': float(col_data.std()),
                    'min_revenue': float(col_data.min()),
                    'max_revenue': float(col_data.max()),
                    'revenue_growth_potential': self._calculate_growth_potential(col_data),
                    'revenue_consistency': self._calculate_consistency_score(col_data)
                }
        
        return metrics
    
    def _analyze_customer_metrics(self, df: pd.DataFrame, customer_columns: List[str]) -> Dict[str, Any]:
        """Analyze customer-related metrics"""
        metrics = {}
        
        for col in customer_columns:
            if df[col].dtype == 'object':  # Categorical customer data
                unique_customers = df[col].nunique()
                total_records = len(df)
                
                metrics[col] = {
                    'unique_customers': unique_customers,
                    'total_interactions': total_records,
                    'avg_interactions_per_customer': round(total_records / unique_customers, 2) if unique_customers > 0 else 0,
                    'customer_distribution': df[col].value_counts().head(10).to_dict(),
                    'customer_concentration': self._calculate_customer_concentration(df[col])
                }
        
        return metrics
    
    def _analyze_product_metrics(self, df: pd.DataFrame, product_columns: List[str]) -> Dict[str, Any]:
        """Analyze product-related metrics"""
        metrics = {}
        
        for col in product_columns:
            if df[col].dtype == 'object':  # Categorical product data
                product_counts = df[col].value_counts()
                
                metrics[col] = {
                    'total_products': df[col].nunique(),
                    'product_distribution': product_counts.head(10).to_dict(),
                    'top_product': product_counts.index[0] if len(product_counts) > 0 else None,
                    'top_product_share': round(product_counts.iloc[0] / len(df) * 100, 2) if len(product_counts) > 0 else 0,
                    'product_diversity_index': self._calculate_diversity_index(product_counts)
                }
        
        return metrics
    
    def _analyze_temporal_trends(self, df: pd.DataFrame, time_columns: List[str]) -> Dict[str, Any]:
        """Analyze temporal trends in the data"""
        metrics = {}
        
        for col in time_columns:
            try:
                # Try to convert to datetime
                if df[col].dtype == 'object':
                    time_data = pd.to_datetime(df[col], errors='coerce').dropna()
                else:
                    time_data = df[col].dropna()
                
                if len(time_data) > 0:
                    metrics[col] = {
                        'time_range': {
                            'start': str(time_data.min()),
                            'end': str(time_data.max()),
                            'duration_days': (time_data.max() - time_data.min()).days if hasattr(time_data.max() - time_data.min(), 'days') else None
                        },
                        'data_frequency': self._analyze_data_frequency(time_data),
                        'seasonal_patterns': self._detect_seasonal_patterns(df, col)
                    }
            except Exception as e:
                logger.warning(f"Could not analyze temporal column {col}: {e}")
        
        return metrics
    
    def _calculate_growth_potential(self, data: pd.Series) -> str:
        """Calculate growth potential based on data trends"""
        if len(data) < 3:
            return "insufficient_data"
        
        # Simple trend analysis
        x = np.arange(len(data))
        slope = np.polyfit(x, data, 1)[0]
        
        if slope > data.std() * 0.1:
            return "high_growth"
        elif slope > 0:
            return "moderate_growth"
        elif slope > -data.std() * 0.1:
            return "stable"
        else:
            return "declining"
    
    def _calculate_consistency_score(self, data: pd.Series) -> float:
        """Calculate consistency score (lower coefficient of variation = more consistent)"""
        if data.mean() == 0:
            return 0.0
        cv = data.std() / data.mean()
        # Convert to 0-100 scale where 100 is most consistent
        return max(0, 100 - (cv * 100))
    
    def _calculate_customer_concentration(self, customer_data: pd.Series) -> Dict[str, Any]:
        """Calculate customer concentration metrics"""
        value_counts = customer_data.value_counts()
        total = len(customer_data)
        
        # Top 20% of customers' share
        top_20_percent_count = max(1, int(len(value_counts) * 0.2))
        top_20_percent_share = value_counts.head(top_20_percent_count).sum() / total * 100
        
        return {
            'top_20_percent_share': round(top_20_percent_share, 2),
            'concentration_risk': 'high' if top_20_percent_share > 80 else 'medium' if top_20_percent_share > 60 else 'low'
        }
    
    def _calculate_diversity_index(self, value_counts: pd.Series) -> float:
        """Calculate diversity index (Shannon entropy)"""
        proportions = value_counts / value_counts.sum()
        entropy = -np.sum(proportions * np.log2(proportions + 1e-10))  # Add small value to avoid log(0)
        max_entropy = np.log2(len(proportions))
        return round(entropy / max_entropy * 100, 2) if max_entropy > 0 else 0
    
    def _analyze_data_frequency(self, time_data: pd.Series) -> str:
        """Analyze the frequency of data points"""
        if len(time_data) < 2:
            return "insufficient_data"
        
        # Calculate average time difference
        time_diffs = time_data.sort_values().diff().dropna()
        avg_diff = time_diffs.mean()
        
        if hasattr(avg_diff, 'days'):
            if avg_diff.days < 1:
                return "hourly_or_less"
            elif avg_diff.days <= 1:
                return "daily"
            elif avg_diff.days <= 7:
                return "weekly"
            elif avg_diff.days <= 31:
                return "monthly"
            else:
                return "yearly_or_more"
        else:
            return "unknown"
    
    def _detect_seasonal_patterns(self, df: pd.DataFrame, time_col: str) -> Dict[str, Any]:
        """Detect seasonal patterns in the data"""
        # This is a simplified seasonal detection
        # In a real implementation, you might use more sophisticated time series analysis
        try:
            if df[time_col].dtype == 'object':
                time_data = pd.to_datetime(df[time_col], errors='coerce')
            else:
                time_data = df[time_col]
            
            # Group by month to detect monthly patterns
            if hasattr(time_data.dt, 'month'):
                monthly_counts = time_data.dt.month.value_counts().sort_index()
                peak_month = monthly_counts.idxmax()
                low_month = monthly_counts.idxmin()
                
                return {
                    'has_seasonal_pattern': monthly_counts.std() > monthly_counts.mean() * 0.2,
                    'peak_month': int(peak_month),
                    'low_month': int(low_month),
                    'seasonality_strength': round(monthly_counts.std() / monthly_counts.mean(), 2)
                }
        except Exception as e:
            logger.warning(f"Could not detect seasonal patterns: {e}")
        
        return {'has_seasonal_pattern': False}
    
    def _generate_strategic_recommendations(self, df: pd.DataFrame, business_columns: Dict[str, List[str]], query: str) -> List[Dict[str, Any]]:
        """Generate strategic business recommendations"""
        recommendations = []
        
        # Revenue optimization recommendations
        if business_columns['revenue_columns']:
            for col in business_columns['revenue_columns']:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    cv = col_data.std() / col_data.mean() if col_data.mean() > 0 else 0
                    if cv > 0.5:  # High variability
                        recommendations.append({
                            'category': 'revenue_optimization',
                            'priority': 'high',
                            'title': f'Stabilize {col} Performance',
                            'description': f'High variability in {col} suggests inconsistent performance. Consider implementing standardized processes.',
                            'impact': 'medium_to_high',
                            'effort': 'medium'
                        })
        
        # Customer concentration recommendations
        if business_columns['customer_columns']:
            for col in business_columns['customer_columns']:
                if df[col].dtype == 'object':
                    concentration = self._calculate_customer_concentration(df[col])
                    if concentration['concentration_risk'] == 'high':
                        recommendations.append({
                            'category': 'customer_diversification',
                            'priority': 'high',
                            'title': 'Reduce Customer Concentration Risk',
                            'description': f'Top 20% of customers account for {concentration["top_20_percent_share"]}% of business. Diversify customer base.',
                            'impact': 'high',
                            'effort': 'high'
                        })
        
        # Product diversification recommendations
        if business_columns['product_columns']:
            for col in business_columns['product_columns']:
                if df[col].dtype == 'object':
                    diversity = self._calculate_diversity_index(df[col].value_counts())
                    if diversity < 50:  # Low diversity
                        recommendations.append({
                            'category': 'product_diversification',
                            'priority': 'medium',
                            'title': f'Increase {col} Diversity',
                            'description': f'Product portfolio shows low diversity (score: {diversity}/100). Consider expanding offerings.',
                            'impact': 'medium',
                            'effort': 'high'
                        })
        
        # Data quality recommendations
        missing_data_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if missing_data_ratio > 0.1:
            recommendations.append({
                'category': 'data_quality',
                'priority': 'medium',
                'title': 'Improve Data Collection',
                'description': f'{missing_data_ratio*100:.1f}% of data is missing. Better data quality will improve decision-making.',
                'impact': 'medium',
                'effort': 'medium'
            })
        
        return recommendations
    
    def _identify_business_risks(self, df: pd.DataFrame, business_columns: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Identify potential business risks from the data"""
        risks = []
        
        # Revenue concentration risk
        if business_columns['revenue_columns']:
            for col in business_columns['revenue_columns']:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    # Check for revenue decline trend
                    if len(col_data) > 5:
                        recent_avg = col_data.tail(int(len(col_data) * 0.3)).mean()
                        early_avg = col_data.head(int(len(col_data) * 0.3)).mean()
                        
                        if recent_avg < early_avg * 0.9:  # 10% decline
                            risks.append({
                                'category': 'revenue_decline',
                                'severity': 'high',
                                'title': f'Declining {col} Trend',
                                'description': f'Recent {col} shows declining trend compared to earlier periods.',
                                'mitigation': 'Investigate root causes and implement corrective measures'
                            })
        
        # Customer concentration risk
        if business_columns['customer_columns']:
            for col in business_columns['customer_columns']:
                if df[col].dtype == 'object':
                    concentration = self._calculate_customer_concentration(df[col])
                    if concentration['concentration_risk'] == 'high':
                        risks.append({
                            'category': 'customer_concentration',
                            'severity': 'high',
                            'title': 'High Customer Concentration',
                            'description': f'Heavy dependence on top customers creates vulnerability.',
                            'mitigation': 'Develop customer acquisition and retention strategies'
                        })
        
        # Data quality risk
        missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if missing_ratio > 0.2:
            risks.append({
                'category': 'data_quality',
                'severity': 'medium',
                'title': 'Poor Data Quality',
                'description': f'High missing data rate ({missing_ratio*100:.1f}%) may lead to poor decisions.',
                'mitigation': 'Implement data governance and quality assurance processes'
            })
        
        return risks
    
    def _identify_opportunities(self, df: pd.DataFrame, business_columns: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Identify business opportunities from the data"""
        opportunities = []
        
        # Growth opportunities
        if business_columns['revenue_columns']:
            for col in business_columns['revenue_columns']:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    growth_potential = self._calculate_growth_potential(col_data)
                    if growth_potential in ['high_growth', 'moderate_growth']:
                        opportunities.append({
                            'category': 'revenue_growth',
                            'potential': 'high' if growth_potential == 'high_growth' else 'medium',
                            'title': f'Scale {col} Operations',
                            'description': f'{col} shows {growth_potential.replace("_", " ")} trend. Consider scaling operations.',
                            'action': 'Invest in capacity expansion and market development'
                        })
        
        # Market expansion opportunities
        if business_columns['customer_columns'] and business_columns['product_columns']:
            # Cross-selling opportunities
            opportunities.append({
                'category': 'market_expansion',
                'potential': 'medium',
                'title': 'Cross-selling Opportunities',
                'description': 'Analyze customer-product combinations to identify cross-selling potential.',
                'action': 'Develop targeted marketing campaigns for underserved segments'
            })
        
        # Efficiency opportunities
        if business_columns['performance_columns']:
            for col in business_columns['performance_columns']:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    # Check for performance improvement potential
                    q75 = col_data.quantile(0.75)
                    median = col_data.median()
                    if q75 > median * 1.2:  # Top quartile significantly better
                        opportunities.append({
                            'category': 'operational_efficiency',
                            'potential': 'high',
                            'title': f'Improve {col} Consistency',
                            'description': f'Top performers in {col} significantly outperform median. Standardize best practices.',
                            'action': 'Identify and replicate best practices across organization'
                        })
        
        return opportunities
    
    def _calculate_business_kpis(self, df: pd.DataFrame, business_columns: Dict[str, List[str]]) -> Dict[str, Any]:
        """Calculate key business KPIs"""
        kpis = {}
        
        # Revenue KPIs
        if business_columns['revenue_columns']:
            revenue_col = business_columns['revenue_columns'][0]  # Use first revenue column
            revenue_data = df[revenue_col].dropna()
            
            kpis['revenue_kpis'] = {
                'total_revenue': float(revenue_data.sum()),
                'average_transaction': float(revenue_data.mean()),
                'revenue_volatility': float(revenue_data.std() / revenue_data.mean()) if revenue_data.mean() > 0 else 0,
                'revenue_growth_rate': self._calculate_growth_rate(revenue_data)
            }
        
        # Customer KPIs
        if business_columns['customer_columns']:
            customer_col = business_columns['customer_columns'][0]
            unique_customers = df[customer_col].nunique()
            total_transactions = len(df)
            
            kpis['customer_kpis'] = {
                'total_customers': unique_customers,
                'transactions_per_customer': round(total_transactions / unique_customers, 2) if unique_customers > 0 else 0,
                'customer_concentration_index': self._calculate_herfindahl_index(df[customer_col])
            }
        
        # Operational KPIs
        kpis['operational_kpis'] = {
            'data_completeness': round((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2),
            'data_consistency': self._calculate_data_consistency_score(df),
            'business_complexity': len(df.columns)  # Simple measure of business complexity
        }
        
        return kpis
    
    def _calculate_growth_rate(self, data: pd.Series) -> float:
        """Calculate growth rate from time series data"""
        if len(data) < 2:
            return 0.0
        
        # Simple growth rate calculation
        first_half = data.head(len(data) // 2).mean()
        second_half = data.tail(len(data) // 2).mean()
        
        if first_half > 0:
            return round(((second_half - first_half) / first_half) * 100, 2)
        return 0.0
    
    def _calculate_herfindahl_index(self, data: pd.Series) -> float:
        """Calculate Herfindahl-Hirschman Index for concentration"""
        value_counts = data.value_counts()
        proportions = value_counts / len(data)
        hhi = (proportions ** 2).sum()
        return round(hhi * 10000, 2)  # Scale to 0-10000
    
    def _calculate_data_consistency_score(self, df: pd.DataFrame) -> float:
        """Calculate overall data consistency score"""
        scores = []
        
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                # For numerical columns, check for outliers
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    Q1 = col_data.quantile(0.25)
                    Q3 = col_data.quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = len(col_data[(col_data < Q1 - 1.5 * IQR) | (col_data > Q3 + 1.5 * IQR)])
                    consistency = max(0, 100 - (outliers / len(col_data) * 100))
                    scores.append(consistency)
            else:
                # For categorical columns, check for data quality
                null_ratio = df[col].isnull().sum() / len(df)
                consistency = max(0, 100 - (null_ratio * 100))
                scores.append(consistency)
        
        return round(np.mean(scores), 2) if scores else 0.0
    
    def _create_strategy_prompt(self, query: str, analysis: Dict[str, Any], df: pd.DataFrame, context: Dict[str, Any] = None) -> str:
        """Create prompt for strategic AI analysis"""
        return f"""
        As a senior business strategist, provide strategic insights for this query: "{query}"
        
        Business Context Analysis:
        - Dataset: {df.shape[0]} records with {df.shape[1]} variables
        - Business Columns Identified: {analysis['business_context']}
        
        Key Business Metrics:
        {analysis['metrics']}
        
        Current KPIs:
        {analysis['kpis']}
        
        Identified Risks:
        {analysis['risks']}
        
        Identified Opportunities:
        {analysis['opportunities']}
        
        Strategic Recommendations:
        {analysis['recommendations']}
        
        Please provide:
        1. Executive summary of key strategic insights
        2. Priority strategic initiatives based on the data
        3. Risk mitigation strategies
        4. Growth opportunity assessment
        5. Resource allocation recommendations
        6. Long-term strategic implications
        7. Competitive positioning insights
        8. Market expansion possibilities
        """


class MarketAnalystAgent(BaseAgent):
    """Market Analysis Specialist - Analyzes market trends and competitive landscape"""
    
    def __init__(self):
        super().__init__(
            agent_id="market_analyst",
            name="Market Analysis Specialist",
            role="business_intelligence",
            description="Analyzes market trends and competitive landscape",
            specialization="Market Research and Competitive Intelligence"
        )
        self.capabilities = [
            "Market trend analysis",
            "Competitive intelligence",
            "Market segmentation",
            "Industry benchmarking",
            "Market opportunity assessment",
            "Consumer behavior analysis"
        ]
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze data from a market and competitive perspective"""
        try:
            self.update_status("analyzing", "Performing market trend analysis")
            
            # Parse CSV data
            csv_data = data.get('csv_data', '')
            df = self._parse_csv_data(csv_data)
            if df is None:
                return {
                    'success': False,
                    'error': 'Failed to parse CSV data',
                    'analysis': None
                }
            
            # Perform market analysis
            market_analysis = self._perform_market_analysis(df, query)
            
            # Generate market insights
            market_prompt = self._create_market_prompt(query, market_analysis, df, context)
            ai_response = self.generate_response(market_prompt, context)
            
            if not ai_response['success']:
                return ai_response
            
            self.update_status("completed", "Market analysis completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'market_analysis',
                'market_trends': market_analysis['trends'],
                'competitive_analysis': market_analysis['competitive_insights'],
                'market_insights': ai_response['content'],
                'market_segments': market_analysis['segments'],
                'performance_benchmarks': market_analysis['benchmarks'],
                'market_opportunities': market_analysis['market_opportunities']
            }
            
        except Exception as e:
            logger.error(f"Market Analyst error: {e}")
            self.update_status("error", f"Market analysis failed: {str(e)}")
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
    
    def _perform_market_analysis(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Perform comprehensive market analysis"""
        analysis = {
            'trends': {},
            'competitive_insights': {},
            'segments': {},
            'benchmarks': {},
            'market_opportunities': []
        }
        
        # Identify market-relevant columns
        market_columns = self._identify_market_columns(df)
        
        # Analyze market trends
        analysis['trends'] = self._analyze_market_trends(df, market_columns)
        
        # Perform competitive analysis
        analysis['competitive_insights'] = self._analyze_competitive_landscape(df, market_columns)
        
        # Segment analysis
        analysis['segments'] = self._analyze_market_segments(df, market_columns)
        
        # Performance benchmarking
        analysis['benchmarks'] = self._calculate_performance_benchmarks(df, market_columns)
        
        # Identify market opportunities
        analysis['market_opportunities'] = self._identify_market_opportunities(df, market_columns, query)
        
        return analysis
    
    def _identify_market_columns(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Identify columns relevant to market analysis"""
        market_columns = {
            'geographic_columns': [],
            'segment_columns': [],
            'competitor_columns': [],
            'performance_columns': [],
            'time_columns': [],
            'channel_columns': []
        }
        
        # Keywords for different market dimensions
        geo_keywords = ['region', 'country', 'state', 'city', 'location', 'territory', 'market']
        segment_keywords = ['segment', 'category', 'type', 'class', 'group', 'tier']
        competitor_keywords = ['competitor', 'brand', 'company', 'vendor', 'supplier']
        performance_keywords = ['share', 'rank', 'position', 'performance', 'score', 'rating']
        time_keywords = ['date', 'time', 'year', 'month', 'quarter', 'period']
        channel_keywords = ['channel', 'platform', 'medium', 'source', 'method']
        
        for col in df.columns:
            col_lower = col.lower()
            
            if any(keyword in col_lower for keyword in geo_keywords):
                market_columns['geographic_columns'].append(col)
            elif any(keyword in col_lower for keyword in segment_keywords):
                market_columns['segment_columns'].append(col)
            elif any(keyword in col_lower for keyword in competitor_keywords):
                market_columns['competitor_columns'].append(col)
            elif any(keyword in col_lower for keyword in performance_keywords):
                market_columns['performance_columns'].append(col)
            elif any(keyword in col_lower for keyword in time_keywords):
                market_columns['time_columns'].append(col)
            elif any(keyword in col_lower for keyword in channel_keywords):
                market_columns['channel_columns'].append(col)
        
        return market_columns
    
    def _analyze_market_trends(self, df: pd.DataFrame, market_columns: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyze market trends over time"""
        trends = {}
        
        # Time-based trend analysis
        if market_columns['time_columns']:
            time_col = market_columns['time_columns'][0]
            
            # Analyze trends by different dimensions
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            
            for num_col in numerical_cols:
                try:
                    # Group by time periods and calculate trends
                    if df[time_col].dtype == 'object':
                        time_data = pd.to_datetime(df[time_col], errors='coerce')
                    else:
                        time_data = df[time_col]
                    
                    df_with_time = df.copy()
                    df_with_time['parsed_time'] = time_data
                    df_clean = df_with_time.dropna(subset=['parsed_time', num_col])
                    
                    if len(df_clean) > 0:
                        # Monthly trend analysis
                        monthly_data = df_clean.groupby(df_clean['parsed_time'].dt.to_period('M'))[num_col].mean()
                        
                        if len(monthly_data) > 1:
                            # Calculate trend direction
                            x = np.arange(len(monthly_data))
                            slope = np.polyfit(x, monthly_data.values, 1)[0]
                            
                            trends[f'{num_col}_trend'] = {
                                'direction': 'increasing' if slope > 0 else 'decreasing',
                                'slope': float(slope),
                                'strength': 'strong' if abs(slope) > monthly_data.std() * 0.1 else 'weak',
                                'volatility': float(monthly_data.std()),
                                'recent_performance': 'above_average' if monthly_data.iloc[-1] > monthly_data.mean() else 'below_average'
                            }
                
                except Exception as e:
                    logger.warning(f"Could not analyze trend for {num_col}: {e}")
        
        return trends
    
    def _analyze_competitive_landscape(self, df: pd.DataFrame, market_columns: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyze competitive landscape"""
        competitive_insights = {}
        
        # Competitor analysis
        if market_columns['competitor_columns']:
            for comp_col in market_columns['competitor_columns']:
                if df[comp_col].dtype == 'object':
                    competitor_data = df[comp_col].value_counts()
                    total_market = len(df)
                    
                    competitive_insights[comp_col] = {
                        'market_leaders': competitor_data.head(5).to_dict(),
                        'market_concentration': {
                            'top_3_share': round(competitor_data.head(3).sum() / total_market * 100, 2),
                            'hhi_index': self._calculate_hhi(competitor_data)
                        },
                        'competitive_intensity': self._assess_competitive_intensity(competitor_data),
                        'market_fragmentation': len(competitor_data)
                    }
        
        # Performance comparison analysis
        if market_columns['performance_columns']:
            for perf_col in market_columns['performance_columns']:
                if df[perf_col].dtype in ['int64', 'float64']:
                    perf_data = df[perf_col].dropna()
                    
                    competitive_insights[f'{perf_col}_benchmarks'] = {
                        'market_average': float(perf_data.mean()),
                        'top_quartile': float(perf_data.quantile(0.75)),
                        'bottom_quartile': float(perf_data.quantile(0.25)),
                        'performance_gap': float(perf_data.quantile(0.75) - perf_data.quantile(0.25)),
                        'leaders_advantage': float(perf_data.max() - perf_data.mean())
                    }
        
        return competitive_insights
    
    def _analyze_market_segments(self, df: pd.DataFrame, market_columns: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyze market segments"""
        segments = {}
        
        # Geographic segmentation
        if market_columns['geographic_columns']:
            for geo_col in market_columns['geographic_columns']:
                if df[geo_col].dtype == 'object':
                    geo_distribution = df[geo_col].value_counts()
                    
                    segments[f'{geo_col}_segments'] = {
                        'total_markets': len(geo_distribution),
                        'market_distribution': geo_distribution.head(10).to_dict(),
                        'market_concentration': round(geo_distribution.head(3).sum() / len(df) * 100, 2),
                        'emerging_markets': geo_distribution.tail(5).to_dict()
                    }
        
        # Product/Service segmentation
        if market_columns['segment_columns']:
            for seg_col in market_columns['segment_columns']:
                if df[seg_col].dtype == 'object':
                    segment_data = df[seg_col].value_counts()
                    
                    segments[f'{seg_col}_analysis'] = {
                        'segment_count': len(segment_data),
                        'segment_distribution': segment_data.to_dict(),
                        'dominant_segment': segment_data.index[0] if len(segment_data) > 0 else None,
                        'segment_diversity': self._calculate_diversity_index(segment_data)
                    }
        
        # Channel segmentation
        if market_columns['channel_columns']:
            for channel_col in market_columns['channel_columns']:
                if df[channel_col].dtype == 'object':
                    channel_data = df[channel_col].value_counts()
                    
                    segments[f'{channel_col}_channels'] = {
                        'channel_count': len(channel_data),
                        'channel_performance': channel_data.to_dict(),
                        'primary_channel': channel_data.index[0] if len(channel_data) > 0 else None,
                        'channel_concentration': round(channel_data.iloc[0] / len(df) * 100, 2) if len(channel_data) > 0 else 0
                    }
        
        return segments
    
    def _calculate_performance_benchmarks(self, df: pd.DataFrame, market_columns: Dict[str, List[str]]) -> Dict[str, Any]:
        """Calculate performance benchmarks"""
        benchmarks = {}
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                benchmarks[col] = {
                    'industry_average': float(col_data.mean()),
                    'best_in_class': float(col_data.quantile(0.95)),
                    'worst_in_class': float(col_data.quantile(0.05)),
                    'median_performance': float(col_data.median()),
                    'performance_spread': float(col_data.std()),
                    'excellence_threshold': float(col_data.quantile(0.8))
                }
        
        return benchmarks
    
    def _identify_market_opportunities(self, df: pd.DataFrame, market_columns: Dict[str, List[str]], query: str) -> List[Dict[str, Any]]:
        """Identify market opportunities"""
        opportunities = []
        
        # Geographic expansion opportunities
        if market_columns['geographic_columns']:
            for geo_col in market_columns['geographic_columns']:
                if df[geo_col].dtype == 'object':
                    geo_data = df[geo_col].value_counts()
                    underserved_markets = geo_data.tail(5)  # Bottom 5 markets
                    
                    if len(underserved_markets) > 0:
                        opportunities.append({
                            'type': 'geographic_expansion',
                            'priority': 'medium',
                            'title': 'Underserved Geographic Markets',
                            'description': f'Several markets show low penetration: {list(underserved_markets.index)}',
                            'potential_impact': 'medium_to_high',
                            'investment_required': 'medium'
                        })
        
        # Segment opportunities
        if market_columns['segment_columns']:
            for seg_col in market_columns['segment_columns']:
                if df[seg_col].dtype == 'object':
                    segment_data = df[seg_col].value_counts()
                    # Look for segments with growth potential
                    if len(segment_data) > 3:
                        mid_tier_segments = segment_data.iloc[2:5]  # Middle segments
                        opportunities.append({
                            'type': 'segment_development',
                            'priority': 'medium',
                            'title': 'Mid-tier Segment Development',
                            'description': f'Opportunity to grow in segments: {list(mid_tier_segments.index)}',
                            'potential_impact': 'medium',
                            'investment_required': 'low_to_medium'
                        })
        
        # Performance improvement opportunities
        if market_columns['performance_columns']:
            for perf_col in market_columns['performance_columns']:
                if df[perf_col].dtype in ['int64', 'float64']:
                    perf_data = df[perf_col].dropna()
                    if len(perf_data) > 0:
                        median = perf_data.median()
                        top_quartile = perf_data.quantile(0.75)
                        
                        if top_quartile > median * 1.3:  # Significant performance gap
                            opportunities.append({
                                'type': 'performance_optimization',
                                'priority': 'high',
                                'title': f'Close {perf_col} Performance Gap',
                                'description': f'Top performers significantly outperform median in {perf_col}',
                                'potential_impact': 'high',
                                'investment_required': 'medium'
                            })
        
        # Market consolidation opportunities
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0 and market_columns['competitor_columns']:
            opportunities.append({
                'type': 'market_consolidation',
                'priority': 'low_to_medium',
                'title': 'Market Consolidation Potential',
                'description': 'Fragmented market structure may present consolidation opportunities',
                'potential_impact': 'high',
                'investment_required': 'high'
            })
        
        return opportunities
    
    def _calculate_hhi(self, market_shares: pd.Series) -> float:
        """Calculate Herfindahl-Hirschman Index"""
        proportions = market_shares / market_shares.sum()
        hhi = (proportions ** 2).sum()
        return round(hhi * 10000, 2)
    
    def _assess_competitive_intensity(self, competitor_data: pd.Series) -> str:
        """Assess competitive intensity based on market distribution"""
        hhi = self._calculate_hhi(competitor_data)
        
        if hhi > 2500:
            return "low_competition"  # Highly concentrated
        elif hhi > 1500:
            return "moderate_competition"  # Moderately concentrated
        else:
            return "high_competition"  # Highly competitive
    
    def _calculate_diversity_index(self, data: pd.Series) -> float:
        """Calculate diversity index (Shannon entropy)"""
        proportions = data / data.sum()
        entropy = -np.sum(proportions * np.log2(proportions + 1e-10))
        max_entropy = np.log2(len(proportions))
        return round(entropy / max_entropy * 100, 2) if max_entropy > 0 else 0
    
    def _create_market_prompt(self, query: str, analysis: Dict[str, Any], df: pd.DataFrame, context: Dict[str, Any] = None) -> str:
        """Create prompt for market AI analysis"""
        return f"""
        As a senior market analyst, provide market insights for this query: "{query}"
        
        Market Context:
        - Dataset: {df.shape[0]} market observations with {df.shape[1]} variables
        - Analysis Period: Current market snapshot
        
        Market Trends Analysis:
        {analysis['trends']}
        
        Competitive Landscape:
        {analysis['competitive_insights']}
        
        Market Segmentation:
        {analysis['segments']}
        
        Performance Benchmarks:
        {analysis['benchmarks']}
        
        Market Opportunities:
        {analysis['market_opportunities']}
        
        Please provide:
        1. Market overview and key trends
        2. Competitive positioning analysis
        3. Market share and concentration insights
        4. Segment performance evaluation
        5. Growth opportunities assessment
        6. Competitive threats and challenges
        7. Market entry/expansion recommendations
        8. Pricing and positioning strategies
        9. Market timing considerations
        10. Risk factors and mitigation strategies
        """