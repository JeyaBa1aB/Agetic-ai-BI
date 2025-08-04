"""
Reporting Team agents for Multi-Agent BI Assistant
Specialized agent for executive reporting and presentation creation
"""
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ExecutiveReporterAgent(BaseAgent):
    """Executive Reporting Specialist - Creates executive-level summaries and presentations"""
    
    def __init__(self):
        super().__init__(
            agent_id="executive_reporter",
            name="Executive Reporting Specialist",
            role="reporting",
            description="Creates executive-level summaries and presentations",
            specialization="Executive Communication and Strategic Reporting"
        )
        self.capabilities = [
            "Executive reporting",
            "Strategic communication",
            "Data storytelling",
            "Presentation design",
            "Key insights synthesis",
            "Action plan development"
        ]
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create comprehensive executive report from all agent analyses"""
        try:
            self.update_status("compiling", "Creating executive summary report")
            
            # Parse CSV data for context
            csv_data = data.get('csv_data', '')
            df = self._parse_csv_data(csv_data)
            if df is None:
                return {
                    'success': False,
                    'error': 'Failed to parse CSV data',
                    'analysis': None
                }
            
            # Compile executive report
            executive_report = self._compile_executive_report(df, query, context)
            
            # Generate executive summary
            exec_prompt = self._create_executive_prompt(query, executive_report, df, context)
            ai_response = self.generate_response(exec_prompt, context)
            
            if not ai_response['success']:
                return ai_response
            
            self.update_status("completed", "Executive report completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'executive_report',
                'executive_summary': ai_response['content'],
                'report_structure': executive_report,
                'key_findings': executive_report['key_findings'],
                'recommendations': executive_report['strategic_recommendations'],
                'presentation_outline': executive_report['presentation_outline']
            }
            
        except Exception as e:
            logger.error(f"Executive Reporter error: {e}")
            self.update_status("error", f"Report generation failed: {str(e)}")
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
    
    def _compile_executive_report(self, df: pd.DataFrame, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Compile comprehensive executive report from all agent analyses"""
        report = {
            'executive_overview': {},
            'key_findings': [],
            'strategic_recommendations': [],
            'risk_assessment': {},
            'performance_metrics': {},
            'market_insights': {},
            'data_quality_assessment': {},
            'presentation_outline': {}
        }
        
        # Extract insights from other agents' analyses if available in context
        if context:
            report = self._extract_agent_insights(report, context)
        
        # Generate executive overview
        report['executive_overview'] = self._generate_executive_overview(df, query, context)
        
        # Compile key findings
        report['key_findings'] = self._compile_key_findings(df, context)
        
        # Generate strategic recommendations
        report['strategic_recommendations'] = self._compile_strategic_recommendations(context)
        
        # Assess risks
        report['risk_assessment'] = self._compile_risk_assessment(df, context)
        
        # Performance metrics summary
        report['performance_metrics'] = self._compile_performance_metrics(df, context)
        
        # Market insights summary
        report['market_insights'] = self._compile_market_insights(context)
        
        # Data quality assessment
        report['data_quality_assessment'] = self._assess_data_quality(df)
        
        # Create presentation outline
        report['presentation_outline'] = self._create_presentation_outline(report, query)
        
        return report
    
    def _extract_agent_insights(self, report: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract insights from other agents' analyses"""
        
        # Extract data analyst insights
        if 'data_analyst_results' in context:
            data_results = context['data_analyst_results']
            if isinstance(data_results, dict) and data_results.get('success'):
                report['data_analysis'] = {
                    'statistical_summary': data_results.get('statistical_summary', {}),
                    'data_quality_score': data_results.get('data_quality_score', 0),
                    'recommendations': data_results.get('recommendations', [])
                }
        
        # Extract pattern detector insights
        if 'pattern_detector_results' in context:
            pattern_results = context['pattern_detector_results']
            if isinstance(pattern_results, dict) and pattern_results.get('success'):
                report['pattern_analysis'] = {
                    'patterns_found': pattern_results.get('patterns_found', {}),
                    'anomalies': pattern_results.get('anomalies', []),
                    'trends': pattern_results.get('trends', []),
                    'correlations': pattern_results.get('correlations', {})
                }
        
        # Extract chart specialist insights
        if 'chart_specialist_results' in context:
            chart_results = context['chart_specialist_results']
            if isinstance(chart_results, dict) and chart_results.get('success'):
                report['visualization_recommendations'] = {
                    'chart_recommendations': chart_results.get('chart_recommendations', []),
                    'priority_charts': chart_results.get('priority_charts', [])
                }
        
        # Extract business strategist insights
        if 'business_strategist_results' in context:
            strategy_results = context['business_strategist_results']
            if isinstance(strategy_results, dict) and strategy_results.get('success'):
                report['strategic_analysis'] = {
                    'business_metrics': strategy_results.get('business_metrics', {}),
                    'recommendations': strategy_results.get('recommendations', []),
                    'risk_assessment': strategy_results.get('risk_assessment', {}),
                    'opportunities': strategy_results.get('opportunities', []),
                    'kpi_analysis': strategy_results.get('kpi_analysis', {})
                }
        
        # Extract market analyst insights
        if 'market_analyst_results' in context:
            market_results = context['market_analyst_results']
            if isinstance(market_results, dict) and market_results.get('success'):
                report['market_analysis'] = {
                    'market_trends': market_results.get('market_trends', {}),
                    'competitive_analysis': market_results.get('competitive_analysis', {}),
                    'market_segments': market_results.get('market_segments', {}),
                    'market_opportunities': market_results.get('market_opportunities', [])
                }
        
        return report 
   
    def _generate_executive_overview(self, df: pd.DataFrame, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate high-level executive overview"""
        overview = {
            'dataset_summary': {
                'total_records': len(df),
                'total_variables': len(df.columns),
                'data_timeframe': self._determine_timeframe(df),
                'business_context': self._identify_business_context(df, query)
            },
            'analysis_scope': {
                'primary_question': query,
                'analysis_depth': 'comprehensive',
                'agents_involved': self._count_agents_involved(context),
                'confidence_level': self._calculate_confidence_level(df, context)
            }
        }
        
        return overview
    
    def _compile_key_findings(self, df: pd.DataFrame, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Compile key findings from all analyses"""
        findings = []
        
        # Data quality findings
        missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if missing_ratio > 0.05:  # More than 5% missing
            findings.append({
                'category': 'data_quality',
                'priority': 'high' if missing_ratio > 0.2 else 'medium',
                'finding': f'Data completeness concern: {missing_ratio*100:.1f}% of data points are missing',
                'impact': 'May affect analysis reliability',
                'source': 'data_quality_assessment'
            })
        
        # Statistical findings
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            for col in numerical_cols[:3]:  # Top 3 numerical columns
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    cv = col_data.std() / col_data.mean() if col_data.mean() > 0 else 0
                    if cv > 1.0:  # High variability
                        findings.append({
                            'category': 'statistical_insight',
                            'priority': 'medium',
                            'finding': f'High variability detected in {col} (CV: {cv:.2f})',
                            'impact': 'Indicates inconsistent performance or diverse data points',
                            'source': 'statistical_analysis'
                        })
        
        # Extract findings from agent results
        if context:
            findings.extend(self._extract_agent_findings(context))
        
        # Sort findings by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        findings.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        
        return findings[:10]  # Top 10 findings
    
    def _extract_agent_findings(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract key findings from agent results"""
        findings = []
        
        # Business strategist findings
        if 'business_strategist_results' in context:
            strategy_results = context['business_strategist_results']
            if isinstance(strategy_results, dict) and strategy_results.get('success'):
                recommendations = strategy_results.get('recommendations', [])
                for rec in recommendations[:3]:  # Top 3 strategic recommendations
                    if isinstance(rec, dict):
                        findings.append({
                            'category': 'strategic_insight',
                            'priority': rec.get('priority', 'medium'),
                            'finding': rec.get('title', 'Strategic recommendation'),
                            'impact': rec.get('description', ''),
                            'source': 'business_strategist'
                        })
        
        # Market analyst findings
        if 'market_analyst_results' in context:
            market_results = context['market_analyst_results']
            if isinstance(market_results, dict) and market_results.get('success'):
                opportunities = market_results.get('market_opportunities', [])
                for opp in opportunities[:2]:  # Top 2 market opportunities
                    if isinstance(opp, dict):
                        findings.append({
                            'category': 'market_opportunity',
                            'priority': opp.get('priority', 'medium'),
                            'finding': opp.get('title', 'Market opportunity identified'),
                            'impact': opp.get('description', ''),
                            'source': 'market_analyst'
                        })
        
        # Pattern detector findings
        if 'pattern_detector_results' in context:
            pattern_results = context['pattern_detector_results']
            if isinstance(pattern_results, dict) and pattern_results.get('success'):
                anomalies = pattern_results.get('anomalies', [])
                for anomaly in anomalies[:2]:  # Top 2 anomalies
                    if isinstance(anomaly, dict):
                        findings.append({
                            'category': 'data_anomaly',
                            'priority': 'medium',
                            'finding': f'Anomaly detected in {anomaly.get("column", "data")}',
                            'impact': f'{anomaly.get("count", 0)} outliers found ({anomaly.get("percentage", 0)}%)',
                            'source': 'pattern_detector'
                        })
        
        return findings 
   
    def _compile_strategic_recommendations(self, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Compile strategic recommendations from all agents"""
        recommendations = []
        
        if context and 'business_strategist_results' in context:
            strategy_results = context['business_strategist_results']
            if isinstance(strategy_results, dict) and strategy_results.get('success'):
                strategy_recs = strategy_results.get('recommendations', [])
                for rec in strategy_recs:
                    if isinstance(rec, dict):
                        recommendations.append({
                            'category': rec.get('category', 'strategic'),
                            'priority': rec.get('priority', 'medium'),
                            'title': rec.get('title', 'Strategic Initiative'),
                            'description': rec.get('description', ''),
                            'expected_impact': rec.get('impact', 'medium'),
                            'implementation_effort': rec.get('effort', 'medium'),
                            'timeline': self._estimate_timeline(rec.get('effort', 'medium')),
                            'source': 'business_strategist'
                        })
        
        # Add market-based recommendations
        if context and 'market_analyst_results' in context:
            market_results = context['market_analyst_results']
            if isinstance(market_results, dict) and market_results.get('success'):
                market_opps = market_results.get('market_opportunities', [])
                for opp in market_opps:
                    if isinstance(opp, dict):
                        recommendations.append({
                            'category': 'market_expansion',
                            'priority': opp.get('priority', 'medium'),
                            'title': opp.get('title', 'Market Opportunity'),
                            'description': opp.get('description', ''),
                            'expected_impact': opp.get('potential_impact', 'medium'),
                            'implementation_effort': opp.get('investment_required', 'medium'),
                            'timeline': self._estimate_timeline(opp.get('investment_required', 'medium')),
                            'source': 'market_analyst'
                        })
        
        # Sort by priority and impact
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        recommendations.sort(key=lambda x: (
            priority_order.get(x['priority'], 0),
            priority_order.get(x['expected_impact'], 0)
        ), reverse=True)
        
        return recommendations[:8]  # Top 8 recommendations
    
    def _compile_risk_assessment(self, df: pd.DataFrame, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Compile comprehensive risk assessment"""
        risks = {
            'data_risks': [],
            'business_risks': [],
            'market_risks': [],
            'overall_risk_level': 'medium'
        }
        
        # Data quality risks
        missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if missing_ratio > 0.1:
            risks['data_risks'].append({
                'type': 'data_quality',
                'severity': 'high' if missing_ratio > 0.3 else 'medium',
                'description': f'High missing data rate ({missing_ratio*100:.1f}%)',
                'mitigation': 'Implement data governance and quality assurance'
            })
        
        # Extract business risks from strategist
        if context and 'business_strategist_results' in context:
            strategy_results = context['business_strategist_results']
            if isinstance(strategy_results, dict) and strategy_results.get('success'):
                business_risks = strategy_results.get('risk_assessment', [])
                if isinstance(business_risks, list):
                    risks['business_risks'] = business_risks[:5]  # Top 5 business risks
        
        # Calculate overall risk level
        high_risks = sum(1 for risk_category in risks.values() 
                        if isinstance(risk_category, list) 
                        for risk in risk_category 
                        if isinstance(risk, dict) and risk.get('severity') == 'high')
        
        if high_risks > 2:
            risks['overall_risk_level'] = 'high'
        elif high_risks > 0:
            risks['overall_risk_level'] = 'medium'
        else:
            risks['overall_risk_level'] = 'low'
        
        return risks
    
    def _compile_performance_metrics(self, df: pd.DataFrame, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Compile key performance metrics"""
        metrics = {
            'data_metrics': {
                'completeness': round((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2),
                'record_count': len(df),
                'variable_count': len(df.columns),
                'numerical_variables': len(df.select_dtypes(include=[np.number]).columns),
                'categorical_variables': len(df.select_dtypes(include=['object']).columns)
            },
            'business_metrics': {},
            'analysis_metrics': {
                'agents_utilized': self._count_agents_involved(context),
                'insights_generated': self._count_insights_generated(context),
                'recommendations_provided': self._count_recommendations(context)
            }
        }
        
        # Extract business KPIs if available
        if context and 'business_strategist_results' in context:
            strategy_results = context['business_strategist_results']
            if isinstance(strategy_results, dict) and strategy_results.get('success'):
                kpis = strategy_results.get('kpi_analysis', {})
                if isinstance(kpis, dict):
                    metrics['business_metrics'] = kpis
        
        return metrics
    
    def _compile_market_insights(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Compile market insights summary"""
        insights = {
            'market_trends': {},
            'competitive_position': {},
            'market_opportunities': [],
            'segment_analysis': {}
        }
        
        if context and 'market_analyst_results' in context:
            market_results = context['market_analyst_results']
            if isinstance(market_results, dict) and market_results.get('success'):
                insights['market_trends'] = market_results.get('market_trends', {})
                insights['competitive_position'] = market_results.get('competitive_analysis', {})
                insights['market_opportunities'] = market_results.get('market_opportunities', [])
                insights['segment_analysis'] = market_results.get('market_segments', {})
        
        return insights
    
    def _assess_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Assess overall data quality"""
        assessment = {
            'overall_score': 0,
            'completeness_score': 0,
            'consistency_score': 0,
            'validity_score': 0,
            'recommendations': []
        }
        
        # Completeness score
        completeness = 1 - (df.isnull().sum().sum() / (len(df) * len(df.columns)))
        assessment['completeness_score'] = round(completeness * 100, 2)
        
        # Consistency score (simplified)
        consistency_scores = []
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    cv = col_data.std() / col_data.mean() if col_data.mean() > 0 else 0
                    consistency = max(0, 100 - (cv * 50))  # Penalize high variability
                    consistency_scores.append(consistency)
        
        assessment['consistency_score'] = round(np.mean(consistency_scores), 2) if consistency_scores else 100
        
        # Validity score (basic checks)
        validity_issues = 0
        total_checks = 0
        
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                total_checks += 1
                # Check for negative values where they might not make sense
                if col.lower() in ['price', 'cost', 'revenue', 'sales', 'amount'] and (df[col] < 0).any():
                    validity_issues += 1
        
        assessment['validity_score'] = round((1 - validity_issues / max(total_checks, 1)) * 100, 2)
        
        # Overall score
        assessment['overall_score'] = round(
            (assessment['completeness_score'] * 0.4 + 
             assessment['consistency_score'] * 0.3 + 
             assessment['validity_score'] * 0.3), 2
        )
        
        # Generate recommendations
        if assessment['completeness_score'] < 90:
            assessment['recommendations'].append('Improve data collection processes to reduce missing values')
        if assessment['consistency_score'] < 70:
            assessment['recommendations'].append('Standardize data entry procedures to improve consistency')
        if assessment['validity_score'] < 80:
            assessment['recommendations'].append('Implement data validation rules to catch invalid entries')
        
        return assessment
    
    def _create_presentation_outline(self, report: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Create executive presentation outline"""
        outline = {
            'title': self._generate_presentation_title(query),
            'slides': [
                {
                    'slide_number': 1,
                    'title': 'Executive Summary',
                    'content_type': 'summary',
                    'key_points': [
                        'Analysis overview and scope',
                        'Primary findings and insights',
                        'Strategic recommendations',
                        'Next steps and timeline'
                    ]
                },
                {
                    'slide_number': 2,
                    'title': 'Data Overview',
                    'content_type': 'data_summary',
                    'key_points': [
                        f"Dataset: {report['executive_overview']['dataset_summary']['total_records']} records",
                        f"Variables: {report['executive_overview']['dataset_summary']['total_variables']} dimensions",
                        f"Data Quality Score: {report['data_quality_assessment']['overall_score']}/100",
                        'Analysis confidence level: High'
                    ]
                },
                {
                    'slide_number': 3,
                    'title': 'Key Findings',
                    'content_type': 'findings',
                    'key_points': [finding['finding'] for finding in report['key_findings'][:4]]
                },
                {
                    'slide_number': 4,
                    'title': 'Strategic Recommendations',
                    'content_type': 'recommendations',
                    'key_points': [rec['title'] for rec in report['strategic_recommendations'][:4]]
                },
                {
                    'slide_number': 5,
                    'title': 'Risk Assessment',
                    'content_type': 'risks',
                    'key_points': [
                        f"Overall Risk Level: {report['risk_assessment']['overall_risk_level'].title()}",
                        'Key risk mitigation priorities',
                        'Monitoring recommendations'
                    ]
                },
                {
                    'slide_number': 6,
                    'title': 'Next Steps',
                    'content_type': 'action_plan',
                    'key_points': [
                        'Immediate actions (0-30 days)',
                        'Short-term initiatives (1-3 months)',
                        'Long-term strategic goals (3-12 months)',
                        'Success metrics and KPIs'
                    ]
                }
            ],
            'appendix': {
                'detailed_analysis': 'Full statistical analysis and methodology',
                'data_sources': 'Data quality assessment and sources',
                'assumptions': 'Key assumptions and limitations'
            }
        }
        
        return outline 
   
    # Helper methods
    def _determine_timeframe(self, df: pd.DataFrame) -> str:
        """Determine the timeframe of the data"""
        # Look for date-like columns
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    if df[col].dtype == 'object':
                        dates = pd.to_datetime(df[col], errors='coerce').dropna()
                        if len(dates) > 0:
                            start_date = dates.min()
                            end_date = dates.max()
                            duration = (end_date - start_date).days
                            
                            if duration < 7:
                                return 'Weekly snapshot'
                            elif duration < 32:
                                return 'Monthly data'
                            elif duration < 366:
                                return 'Annual data'
                            else:
                                return f'Multi-year data ({duration} days)'
                except:
                    continue
        
        return 'Point-in-time snapshot'
    
    def _identify_business_context(self, df: pd.DataFrame, query: str) -> str:
        """Identify the business context from data and query"""
        query_lower = query.lower()
        
        # Business domain keywords
        if any(word in query_lower for word in ['sales', 'revenue', 'customer', 'product']):
            return 'Sales and Revenue Analysis'
        elif any(word in query_lower for word in ['market', 'competition', 'share']):
            return 'Market Analysis'
        elif any(word in query_lower for word in ['performance', 'efficiency', 'productivity']):
            return 'Performance Analysis'
        elif any(word in query_lower for word in ['employee', 'hr', 'staff']):
            return 'Human Resources Analysis'
        else:
            return 'General Business Analysis'
    
    def _count_agents_involved(self, context: Dict[str, Any] = None) -> int:
        """Count how many agents were involved in the analysis"""
        if not context:
            return 1
        
        agent_results = [
            'data_analyst_results',
            'pattern_detector_results',
            'chart_specialist_results',
            'business_strategist_results',
            'market_analyst_results'
        ]
        
        return sum(1 for agent in agent_results if agent in context)
    
    def _calculate_confidence_level(self, df: pd.DataFrame, context: Dict[str, Any] = None) -> str:
        """Calculate confidence level of the analysis"""
        confidence_score = 0
        
        # Data quality factor
        missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if missing_ratio < 0.05:
            confidence_score += 30
        elif missing_ratio < 0.15:
            confidence_score += 20
        else:
            confidence_score += 10
        
        # Sample size factor
        if len(df) > 1000:
            confidence_score += 25
        elif len(df) > 100:
            confidence_score += 20
        else:
            confidence_score += 10
        
        # Number of variables factor
        if len(df.columns) > 10:
            confidence_score += 25
        elif len(df.columns) > 5:
            confidence_score += 20
        else:
            confidence_score += 15
        
        # Agent involvement factor
        agents_count = self._count_agents_involved(context)
        confidence_score += min(agents_count * 4, 20)
        
        if confidence_score >= 85:
            return 'High'
        elif confidence_score >= 65:
            return 'Medium-High'
        elif confidence_score >= 45:
            return 'Medium'
        else:
            return 'Low-Medium'
    
    def _count_insights_generated(self, context: Dict[str, Any] = None) -> int:
        """Count total insights generated across all agents"""
        if not context:
            return 0
        
        insight_count = 0
        
        # Count findings from each agent
        agent_results = [
            'data_analyst_results',
            'pattern_detector_results',
            'business_strategist_results',
            'market_analyst_results'
        ]
        
        for agent in agent_results:
            if agent in context and isinstance(context[agent], dict):
                # Each successful agent analysis counts as insights
                if context[agent].get('success'):
                    insight_count += 3  # Assume 3 insights per agent on average
        
        return insight_count
    
    def _count_recommendations(self, context: Dict[str, Any] = None) -> int:
        """Count total recommendations provided"""
        if not context:
            return 0
        
        rec_count = 0
        
        if 'business_strategist_results' in context:
            strategy_results = context['business_strategist_results']
            if isinstance(strategy_results, dict) and strategy_results.get('success'):
                recommendations = strategy_results.get('recommendations', [])
                rec_count += len(recommendations) if isinstance(recommendations, list) else 0
        
        if 'market_analyst_results' in context:
            market_results = context['market_analyst_results']
            if isinstance(market_results, dict) and market_results.get('success'):
                opportunities = market_results.get('market_opportunities', [])
                rec_count += len(opportunities) if isinstance(opportunities, list) else 0
        
        return rec_count
    
    def _estimate_timeline(self, effort_level: str) -> str:
        """Estimate implementation timeline based on effort level"""
        timeline_map = {
            'low': '1-2 months',
            'low_to_medium': '2-3 months',
            'medium': '3-6 months',
            'medium_to_high': '6-9 months',
            'high': '9-12 months'
        }
        return timeline_map.get(effort_level, '3-6 months')
    
    def _generate_presentation_title(self, query: str) -> str:
        """Generate appropriate presentation title"""
        query_lower = query.lower()
        
        if 'performance' in query_lower:
            return 'Performance Analysis Executive Summary'
        elif any(word in query_lower for word in ['market', 'competition']):
            return 'Market Intelligence Executive Brief'
        elif any(word in query_lower for word in ['sales', 'revenue']):
            return 'Sales & Revenue Analysis Report'
        elif 'strategy' in query_lower:
            return 'Strategic Business Analysis'
        else:
            return 'Business Intelligence Executive Summary'
    
    def _create_executive_prompt(self, query: str, report: Dict[str, Any], df: pd.DataFrame, context: Dict[str, Any] = None) -> str:
        """Create prompt for executive AI summary"""
        return f"""
        As a senior executive reporting specialist, create a comprehensive executive summary for this analysis: "{query}"
        
        EXECUTIVE CONTEXT:
        - Dataset: {len(df)} records across {len(df.columns)} business dimensions
        - Analysis Confidence: {report['executive_overview']['analysis_scope']['confidence_level']}
        - Agents Involved: {report['executive_overview']['analysis_scope']['agents_involved']} specialized analysts
        
        KEY FINDINGS SUMMARY:
        {report['key_findings']}
        
        STRATEGIC RECOMMENDATIONS:
        {report['strategic_recommendations']}
        
        RISK ASSESSMENT:
        - Overall Risk Level: {report['risk_assessment']['overall_risk_level']}
        - Key Risks: {report['risk_assessment']}
        
        PERFORMANCE METRICS:
        {report['performance_metrics']}
        
        DATA QUALITY ASSESSMENT:
        - Overall Score: {report['data_quality_assessment']['overall_score']}/100
        - Key Issues: {report['data_quality_assessment']['recommendations']}
        
        Please provide an executive summary that includes:
        1. **Executive Overview** (2-3 sentences capturing the essence)
        2. **Critical Insights** (Top 3-4 most important findings)
        3. **Strategic Priorities** (Immediate and long-term actions)
        4. **Risk Mitigation** (Key risks and mitigation strategies)
        5. **Success Metrics** (How to measure progress)
        6. **Resource Requirements** (Investment and timeline considerations)
        7. **Next Steps** (Specific actions with owners and timelines)
        
        Write in executive language: concise, action-oriented, and focused on business impact.
        Use bullet points and clear structure for easy consumption by senior leadership.
        """