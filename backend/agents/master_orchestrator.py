"""
Master Orchestrator agent for Multi-Agent BI Assistant
Coordinates workflow and manages all specialized agents
"""
import logging
import time
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, agent_manager
from .data_agents import DataAnalystAgent, DataProcessorAgent, PatternDetectorAgent
from .visualization_agents import ChartSpecialistAgent, DashboardDesignerAgent
from .business_agents import BusinessStrategistAgent, MarketAnalystAgent
from .reporting_agents import ExecutiveReporterAgent

logger = logging.getLogger(__name__)

class MasterOrchestratorAgent(BaseAgent):
    """Master Orchestrator - Coordinates multi-agent business intelligence analysis"""
    
    def __init__(self):
        super().__init__(
            agent_id="master_orchestrator",
            name="Master Orchestrator",
            role="coordination",
            description="Coordinates multi-agent business intelligence analysis",
            specialization="Multi-Agent Coordination and Workflow Management"
        )
        self.capabilities = [
            "Agent coordination",
            "Workflow management",
            "Task delegation",
            "Result synthesis",
            "Quality assurance",
            "Performance monitoring"
        ]
        
        # Initialize all specialized agents
        self.specialized_agents = {}
        self._initialize_agents()
        
        # Workflow configuration
        self.workflow_stages = [
            'initialization',
            'data_intelligence',
            'visualization_planning',
            'business_analysis',
            'executive_reporting',
            'synthesis'
        ]
        
        self.current_stage = 'initialization'
        self.stage_results = {}
        self.workflow_context = {}
    
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        try:
            # Data Intelligence Team
            self.specialized_agents['data_analyst'] = DataAnalystAgent()
            self.specialized_agents['data_processor'] = DataProcessorAgent()
            self.specialized_agents['pattern_detector'] = PatternDetectorAgent()
            
            # Visualization Team
            self.specialized_agents['chart_specialist'] = ChartSpecialistAgent()
            self.specialized_agents['dashboard_designer'] = DashboardDesignerAgent()
            
            # Business Intelligence Team
            self.specialized_agents['business_strategist'] = BusinessStrategistAgent()
            self.specialized_agents['market_analyst'] = MarketAnalystAgent()
            
            # Reporting Team
            self.specialized_agents['executive_reporter'] = ExecutiveReporterAgent()
            
            # Register all agents with the manager
            for agent in self.specialized_agents.values():
                agent_manager.register_agent(agent)
            
            logger.info(f"Master Orchestrator initialized with {len(self.specialized_agents)} specialized agents")
            
        except Exception as e:
            logger.error(f"Failed to initialize specialized agents: {e}")
            raise    
    
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Orchestrate comprehensive multi-agent analysis"""
        try:
            self.update_status("orchestrating", "Starting multi-agent analysis workflow")
            
            # Initialize workflow
            workflow_id = self._initialize_workflow(data, query, context)
            
            # Execute workflow stages
            workflow_results = self._execute_workflow(data, query, context)
            
            # Generate final orchestration summary
            orchestration_summary = self._generate_orchestration_summary(workflow_results, query)
            
            self.update_status("completed", "Multi-agent analysis orchestration completed")
            
            return {
                'success': True,
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'analysis_type': 'multi_agent_orchestration',
                'workflow_id': workflow_id,
                'workflow_results': workflow_results,
                'orchestration_summary': orchestration_summary,
                'agents_coordinated': len(self.specialized_agents),
                'stages_completed': len(self.workflow_stages),
                'total_insights': self._count_total_insights(workflow_results)
            }
            
        except Exception as e:
            logger.error(f"Master Orchestrator error: {e}")
            self.update_status("error", f"Orchestration failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis': None
            }
    
    def _initialize_workflow(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> str:
        """Initialize the multi-agent workflow"""
        workflow_id = f"workflow_{int(time.time())}"
        
        # Set session for all agents
        if self.session_id:
            for agent in self.specialized_agents.values():
                agent.set_session(self.session_id)
        
        # Initialize workflow context
        self.workflow_context = {
            'workflow_id': workflow_id,
            'query': query,
            'data_summary': self._analyze_data_characteristics(data),
            'analysis_priorities': self._determine_analysis_priorities(query),
            'agent_coordination_plan': self._create_coordination_plan(query, data)
        }
        
        logger.info(f"Workflow {workflow_id} initialized with {len(self.specialized_agents)} agents")
        return workflow_id
    
    def _execute_workflow(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the complete multi-agent workflow"""
        workflow_results = {
            'stage_results': {},
            'agent_results': {},
            'workflow_timeline': [],
            'coordination_insights': []
        }
        
        # Stage 1: Data Intelligence Analysis
        self.current_stage = 'data_intelligence'
        data_intelligence_results = self._execute_data_intelligence_stage(data, query, context)
        workflow_results['stage_results']['data_intelligence'] = data_intelligence_results
        workflow_results['workflow_timeline'].append({
            'stage': 'data_intelligence',
            'timestamp': time.time(),
            'agents_involved': ['data_analyst', 'data_processor', 'pattern_detector'],
            'status': 'completed'
        })
        
        # Stage 2: Visualization Planning
        self.current_stage = 'visualization_planning'
        viz_context = {**context, **data_intelligence_results} if context else data_intelligence_results
        visualization_results = self._execute_visualization_stage(data, query, viz_context)
        workflow_results['stage_results']['visualization_planning'] = visualization_results
        workflow_results['workflow_timeline'].append({
            'stage': 'visualization_planning',
            'timestamp': time.time(),
            'agents_involved': ['chart_specialist', 'dashboard_designer'],
            'status': 'completed'
        })
        
        # Stage 3: Business Intelligence Analysis
        self.current_stage = 'business_analysis'
        business_context = {**viz_context, **visualization_results}
        business_results = self._execute_business_intelligence_stage(data, query, business_context)
        workflow_results['stage_results']['business_analysis'] = business_results
        workflow_results['workflow_timeline'].append({
            'stage': 'business_analysis',
            'timestamp': time.time(),
            'agents_involved': ['business_strategist', 'market_analyst'],
            'status': 'completed'
        })
        
        # Stage 4: Executive Reporting
        self.current_stage = 'executive_reporting'
        reporting_context = {**business_context, **business_results}
        reporting_results = self._execute_reporting_stage(data, query, reporting_context)
        workflow_results['stage_results']['executive_reporting'] = reporting_results
        workflow_results['workflow_timeline'].append({
            'stage': 'executive_reporting',
            'timestamp': time.time(),
            'agents_involved': ['executive_reporter'],
            'status': 'completed'
        })
        
        # Compile all agent results
        workflow_results['agent_results'] = {
            **data_intelligence_results,
            **visualization_results,
            **business_results,
            **reporting_results
        }
        
        return workflow_results
    
    def _execute_data_intelligence_stage(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute data intelligence analysis stage"""
        stage_results = {}
        
        try:
            # Data Analyst
            self.specialized_agents['data_analyst'].update_status("active", "Performing statistical analysis")
            data_analyst_result = self.specialized_agents['data_analyst'].analyze(data, query, context)
            stage_results['data_analyst_results'] = data_analyst_result
            
            # Data Processor
            self.specialized_agents['data_processor'].update_status("active", "Analyzing data processing needs")
            data_processor_result = self.specialized_agents['data_processor'].analyze(data, query, context)
            stage_results['data_processor_results'] = data_processor_result
            
            # Pattern Detector
            self.specialized_agents['pattern_detector'].update_status("active", "Detecting patterns and anomalies")
            pattern_detector_result = self.specialized_agents['pattern_detector'].analyze(data, query, context)
            stage_results['pattern_detector_results'] = pattern_detector_result
            
            logger.info("Data intelligence stage completed successfully")
            
        except Exception as e:
            logger.error(f"Data intelligence stage failed: {e}")
            stage_results['stage_error'] = str(e)
        
        return stage_results
    
    def _execute_visualization_stage(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute visualization planning stage"""
        stage_results = {}
        
        try:
            # Chart Specialist
            self.specialized_agents['chart_specialist'].update_status("active", "Designing chart recommendations")
            chart_specialist_result = self.specialized_agents['chart_specialist'].analyze(data, query, context)
            stage_results['chart_specialist_results'] = chart_specialist_result
            
            # Dashboard Designer
            self.specialized_agents['dashboard_designer'].update_status("active", "Creating dashboard layout")
            # Pass chart recommendations to dashboard designer
            dashboard_context = context.copy() if context else {}
            if chart_specialist_result.get('success'):
                dashboard_context['chart_recommendations'] = chart_specialist_result.get('chart_recommendations', [])
            
            dashboard_designer_result = self.specialized_agents['dashboard_designer'].analyze(data, query, dashboard_context)
            stage_results['dashboard_designer_results'] = dashboard_designer_result
            
            logger.info("Visualization planning stage completed successfully")
            
        except Exception as e:
            logger.error(f"Visualization planning stage failed: {e}")
            stage_results['stage_error'] = str(e)
        
        return stage_results   
 
    def _execute_business_intelligence_stage(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute business intelligence analysis stage"""
        stage_results = {}
        
        try:
            # Business Strategist
            self.specialized_agents['business_strategist'].update_status("active", "Performing strategic analysis")
            business_strategist_result = self.specialized_agents['business_strategist'].analyze(data, query, context)
            stage_results['business_strategist_results'] = business_strategist_result
            
            # Market Analyst
            self.specialized_agents['market_analyst'].update_status("active", "Analyzing market trends")
            market_analyst_result = self.specialized_agents['market_analyst'].analyze(data, query, context)
            stage_results['market_analyst_results'] = market_analyst_result
            
            logger.info("Business intelligence stage completed successfully")
            
        except Exception as e:
            logger.error(f"Business intelligence stage failed: {e}")
            stage_results['stage_error'] = str(e)
        
        return stage_results
    
    def _execute_reporting_stage(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute executive reporting stage"""
        stage_results = {}
        
        try:
            # Executive Reporter
            self.specialized_agents['executive_reporter'].update_status("active", "Compiling executive report")
            executive_reporter_result = self.specialized_agents['executive_reporter'].analyze(data, query, context)
            stage_results['executive_reporter_results'] = executive_reporter_result
            
            logger.info("Executive reporting stage completed successfully")
            
        except Exception as e:
            logger.error(f"Executive reporting stage failed: {e}")
            stage_results['stage_error'] = str(e)
        
        return stage_results
    
    def _analyze_data_characteristics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data characteristics for workflow planning"""
        csv_data = data.get('csv_data', '')
        if not csv_data:
            return {'error': 'No CSV data provided'}
        
        try:
            from io import StringIO
            import pandas as pd
            df = pd.read_csv(StringIO(csv_data))
            
            characteristics = {
                'total_records': len(df),
                'total_columns': len(df.columns),
                'numerical_columns': len(df.select_dtypes(include=['int64', 'float64']).columns),
                'categorical_columns': len(df.select_dtypes(include=['object']).columns),
                'missing_data_ratio': df.isnull().sum().sum() / (len(df) * len(df.columns)),
                'data_complexity': 'high' if len(df.columns) > 15 else 'medium' if len(df.columns) > 8 else 'low',
                'sample_size': 'large' if len(df) > 1000 else 'medium' if len(df) > 100 else 'small'
            }
            
            return characteristics
            
        except Exception as e:
            logger.error(f"Data characteristics analysis failed: {e}")
            return {'error': str(e)}
    
    def _determine_analysis_priorities(self, query: str) -> List[str]:
        """Determine analysis priorities based on the query"""
        query_lower = query.lower()
        priorities = []
        
        # Statistical analysis priority
        if any(word in query_lower for word in ['analyze', 'statistics', 'data', 'distribution']):
            priorities.append('statistical_analysis')
        
        # Visualization priority
        if any(word in query_lower for word in ['chart', 'graph', 'visualize', 'plot', 'dashboard']):
            priorities.append('visualization')
        
        # Business strategy priority
        if any(word in query_lower for word in ['strategy', 'business', 'performance', 'growth']):
            priorities.append('business_strategy')
        
        # Market analysis priority
        if any(word in query_lower for word in ['market', 'competition', 'trends', 'segment']):
            priorities.append('market_analysis')
        
        # Pattern detection priority
        if any(word in query_lower for word in ['pattern', 'trend', 'anomaly', 'outlier']):
            priorities.append('pattern_detection')
        
        # Default priorities if none detected
        if not priorities:
            priorities = ['statistical_analysis', 'business_strategy', 'visualization']
        
        return priorities
    
    def _create_coordination_plan(self, query: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create agent coordination plan"""
        data_chars = self._analyze_data_characteristics(data)
        priorities = self._determine_analysis_priorities(query)
        
        plan = {
            'execution_strategy': 'sequential_with_context_passing',
            'priority_agents': [],
            'parallel_stages': [],
            'context_dependencies': {},
            'estimated_duration': self._estimate_workflow_duration(data_chars, priorities)
        }
        
        # Determine priority agents based on query and data
        if 'statistical_analysis' in priorities:
            plan['priority_agents'].extend(['data_analyst', 'pattern_detector'])
        
        if 'visualization' in priorities:
            plan['priority_agents'].extend(['chart_specialist', 'dashboard_designer'])
        
        if 'business_strategy' in priorities:
            plan['priority_agents'].append('business_strategist')
        
        if 'market_analysis' in priorities:
            plan['priority_agents'].append('market_analyst')
        
        # Always include executive reporter for synthesis
        plan['priority_agents'].append('executive_reporter')
        
        # Define context dependencies
        plan['context_dependencies'] = {
            'chart_specialist': ['data_analyst', 'pattern_detector'],
            'dashboard_designer': ['chart_specialist'],
            'business_strategist': ['data_analyst', 'data_processor'],
            'market_analyst': ['data_analyst', 'pattern_detector'],
            'executive_reporter': ['all_agents']
        }
        
        return plan
    
    def _estimate_workflow_duration(self, data_chars: Dict[str, Any], priorities: List[str]) -> Dict[str, Any]:
        """Estimate workflow duration based on complexity"""
        base_duration = 30  # seconds
        
        # Adjust for data complexity
        if data_chars.get('data_complexity') == 'high':
            base_duration *= 1.5
        elif data_chars.get('data_complexity') == 'low':
            base_duration *= 0.7
        
        # Adjust for sample size
        if data_chars.get('sample_size') == 'large':
            base_duration *= 1.3
        elif data_chars.get('sample_size') == 'small':
            base_duration *= 0.8
        
        # Adjust for number of priorities
        priority_multiplier = 1 + (len(priorities) - 1) * 0.2
        base_duration *= priority_multiplier
        
        return {
            'estimated_seconds': int(base_duration),
            'estimated_minutes': round(base_duration / 60, 1),
            'complexity_factors': {
                'data_complexity': data_chars.get('data_complexity', 'medium'),
                'sample_size': data_chars.get('sample_size', 'medium'),
                'analysis_priorities': len(priorities)
            }
        }
    
    def _generate_orchestration_summary(self, workflow_results: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Generate comprehensive orchestration summary"""
        summary = {
            'workflow_overview': {},
            'agent_performance': {},
            'key_insights_synthesis': {},
            'coordination_effectiveness': {},
            'recommendations_consolidation': {}
        }
        
        # Workflow overview
        successful_agents = sum(1 for agent_result in workflow_results['agent_results'].values() 
                               if isinstance(agent_result, dict) and agent_result.get('success', False))
        
        summary['workflow_overview'] = {
            'total_agents_coordinated': len(self.specialized_agents),
            'successful_analyses': successful_agents,
            'workflow_success_rate': round(successful_agents / len(self.specialized_agents) * 100, 2),
            'total_stages_completed': len(workflow_results['stage_results']),
            'workflow_duration': self._calculate_workflow_duration(workflow_results['workflow_timeline'])
        }
        
        # Agent performance analysis
        summary['agent_performance'] = self._analyze_agent_performance(workflow_results['agent_results'])
        
        # Key insights synthesis
        summary['key_insights_synthesis'] = self._synthesize_key_insights(workflow_results['agent_results'])
        
        # Coordination effectiveness
        summary['coordination_effectiveness'] = self._assess_coordination_effectiveness(workflow_results)
        
        # Recommendations consolidation
        summary['recommendations_consolidation'] = self._consolidate_recommendations(workflow_results['agent_results'])
        
        return summary
    
    def _analyze_agent_performance(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual agent performance"""
        performance = {
            'successful_agents': [],
            'failed_agents': [],
            'performance_metrics': {},
            'insights_contribution': {}
        }
        
        for agent_id, result in agent_results.items():
            if isinstance(result, dict):
                if result.get('success', False):
                    performance['successful_agents'].append({
                        'agent_id': agent_id,
                        'agent_name': result.get('agent_name', agent_id),
                        'analysis_type': result.get('analysis_type', 'unknown'),
                        'insights_generated': self._count_agent_insights(result)
                    })
                else:
                    performance['failed_agents'].append({
                        'agent_id': agent_id,
                        'error': result.get('error', 'Unknown error')
                    })
        
        # Calculate performance metrics
        total_agents = len(agent_results)
        successful_count = len(performance['successful_agents'])
        
        performance['performance_metrics'] = {
            'success_rate': round(successful_count / total_agents * 100, 2) if total_agents > 0 else 0,
            'total_insights': sum(agent['insights_generated'] for agent in performance['successful_agents']),
            'average_insights_per_agent': round(
                sum(agent['insights_generated'] for agent in performance['successful_agents']) / max(successful_count, 1), 2
            )
        }
        
        return performance
    
    def _synthesize_key_insights(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize key insights across all agents"""
        synthesis = {
            'cross_agent_patterns': [],
            'conflicting_insights': [],
            'reinforcing_insights': [],
            'unique_contributions': {}
        }
        
        # Extract insights from each agent
        agent_insights = {}
        for agent_id, result in agent_results.items():
            if isinstance(result, dict) and result.get('success', False):
                insights = self._extract_agent_insights(agent_id, result)
                agent_insights[agent_id] = insights
        
        # Identify cross-agent patterns
        synthesis['cross_agent_patterns'] = self._identify_cross_patterns(agent_insights)
        
        # Identify unique contributions
        for agent_id, insights in agent_insights.items():
            if insights:
                synthesis['unique_contributions'][agent_id] = insights[:2]  # Top 2 unique insights
        
        return synthesis
    
    def _assess_coordination_effectiveness(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess how effectively agents were coordinated"""
        effectiveness = {
            'workflow_efficiency': {},
            'context_utilization': {},
            'stage_transitions': {},
            'overall_coordination_score': 0
        }
        
        # Workflow efficiency
        timeline = workflow_results.get('workflow_timeline', [])
        if timeline:
            total_duration = timeline[-1]['timestamp'] - timeline[0]['timestamp']
            effectiveness['workflow_efficiency'] = {
                'total_duration_seconds': round(total_duration, 2),
                'average_stage_duration': round(total_duration / len(timeline), 2),
                'efficiency_rating': 'high' if total_duration < 60 else 'medium' if total_duration < 120 else 'low'
            }
        
        # Context utilization assessment
        context_usage_score = 0
        successful_agents = sum(1 for result in workflow_results['agent_results'].values() 
                               if isinstance(result, dict) and result.get('success', False))
        
        if successful_agents > 0:
            context_usage_score = min(100, successful_agents * 15)  # Max 100, 15 points per successful agent
        
        effectiveness['context_utilization'] = {
            'context_passing_success': context_usage_score,
            'agents_with_context': successful_agents
        }
        
        # Overall coordination score
        efficiency_score = 100 if effectiveness['workflow_efficiency'].get('efficiency_rating') == 'high' else 70 if effectiveness['workflow_efficiency'].get('efficiency_rating') == 'medium' else 40
        success_rate = workflow_results.get('workflow_overview', {}).get('workflow_success_rate', 0)
        
        effectiveness['overall_coordination_score'] = round((efficiency_score + context_usage_score + success_rate) / 3, 2)
        
        return effectiveness
    
    def _consolidate_recommendations(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Consolidate recommendations from all agents"""
        consolidation = {
            'strategic_recommendations': [],
            'operational_recommendations': [],
            'technical_recommendations': [],
            'priority_matrix': {},
            'implementation_roadmap': []
        }
        
        all_recommendations = []
        
        # Extract recommendations from each agent
        for agent_id, result in agent_results.items():
            if isinstance(result, dict) and result.get('success', False):
                recommendations = self._extract_agent_recommendations(agent_id, result)
                all_recommendations.extend(recommendations)
        
        # Categorize recommendations
        for rec in all_recommendations:
            category = rec.get('category', 'operational')
            if 'strategic' in category or 'business' in category:
                consolidation['strategic_recommendations'].append(rec)
            elif 'technical' in category or 'data' in category:
                consolidation['technical_recommendations'].append(rec)
            else:
                consolidation['operational_recommendations'].append(rec)
        
        # Create priority matrix
        high_priority = [rec for rec in all_recommendations if rec.get('priority') == 'high']
        medium_priority = [rec for rec in all_recommendations if rec.get('priority') == 'medium']
        low_priority = [rec for rec in all_recommendations if rec.get('priority') == 'low']
        
        consolidation['priority_matrix'] = {
            'high_priority': len(high_priority),
            'medium_priority': len(medium_priority),
            'low_priority': len(low_priority),
            'total_recommendations': len(all_recommendations)
        }
        
        # Create implementation roadmap
        consolidation['implementation_roadmap'] = self._create_implementation_roadmap(all_recommendations)
        
        return consolidation    
 
   # Helper methods
    def _calculate_workflow_duration(self, timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate workflow duration from timeline"""
        if not timeline or len(timeline) < 2:
            return {'total_seconds': 0, 'total_minutes': 0}
        
        start_time = timeline[0]['timestamp']
        end_time = timeline[-1]['timestamp']
        duration = end_time - start_time
        
        return {
            'total_seconds': round(duration, 2),
            'total_minutes': round(duration / 60, 2),
            'stages': len(timeline)
        }
    
    def _count_agent_insights(self, agent_result: Dict[str, Any]) -> int:
        """Count insights generated by an agent"""
        insight_count = 0
        
        # Count different types of insights based on agent type
        if 'statistical_summary' in agent_result:
            insight_count += 3  # Statistical insights
        
        if 'patterns_found' in agent_result:
            insight_count += len(agent_result.get('anomalies', [])) + len(agent_result.get('trends', []))
        
        if 'chart_recommendations' in agent_result:
            insight_count += len(agent_result.get('chart_recommendations', []))
        
        if 'business_metrics' in agent_result:
            insight_count += 2  # Business insights
        
        if 'market_trends' in agent_result:
            insight_count += 2  # Market insights
        
        if 'key_findings' in agent_result:
            insight_count += len(agent_result.get('key_findings', []))
        
        return max(insight_count, 1)  # At least 1 insight per successful agent
    
    def _count_total_insights(self, workflow_results: Dict[str, Any]) -> int:
        """Count total insights across all agents"""
        total = 0
        agent_results = workflow_results.get('agent_results', {})
        
        for result in agent_results.values():
            if isinstance(result, dict) and result.get('success', False):
                total += self._count_agent_insights(result)
        
        return total
    
    def _extract_agent_insights(self, agent_id: str, result: Dict[str, Any]) -> List[str]:
        """Extract key insights from agent result"""
        insights = []
        
        if agent_id == 'data_analyst_results':
            if 'ai_insights' in result:
                insights.append(f"Statistical Analysis: {result['ai_insights'][:100]}...")
        
        elif agent_id == 'pattern_detector_results':
            anomalies = result.get('anomalies', [])
            if anomalies:
                insights.append(f"Pattern Detection: {len(anomalies)} anomalies detected")
        
        elif agent_id == 'business_strategist_results':
            recommendations = result.get('recommendations', [])
            if recommendations:
                insights.append(f"Strategic Insight: {recommendations[0].get('title', 'Strategic recommendation')}")
        
        elif agent_id == 'market_analyst_results':
            opportunities = result.get('market_opportunities', [])
            if opportunities:
                insights.append(f"Market Opportunity: {opportunities[0].get('title', 'Market opportunity identified')}")
        
        elif agent_id == 'executive_reporter_results':
            findings = result.get('key_findings', [])
            if findings:
                insights.append(f"Executive Finding: {findings[0].get('finding', 'Key business insight')}")
        
        return insights
    
    def _identify_cross_patterns(self, agent_insights: Dict[str, List[str]]) -> List[str]:
        """Identify patterns that appear across multiple agents"""
        patterns = []
        
        # Simple pattern detection - look for common themes
        common_themes = ['performance', 'trend', 'opportunity', 'risk', 'growth']
        
        for theme in common_themes:
            agents_mentioning = []
            for agent_id, insights in agent_insights.items():
                if any(theme.lower() in insight.lower() for insight in insights):
                    agents_mentioning.append(agent_id)
            
            if len(agents_mentioning) >= 2:
                patterns.append(f"{theme.title()} theme identified across {len(agents_mentioning)} agents")
        
        return patterns
    
    def _extract_agent_recommendations(self, agent_id: str, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract recommendations from agent result"""
        recommendations = []
        
        if 'recommendations' in result:
            agent_recs = result['recommendations']
            if isinstance(agent_recs, list):
                for rec in agent_recs:
                    if isinstance(rec, dict):
                        recommendations.append({
                            **rec,
                            'source_agent': agent_id
                        })
        
        if 'market_opportunities' in result:
            opportunities = result['market_opportunities']
            if isinstance(opportunities, list):
                for opp in opportunities:
                    if isinstance(opp, dict):
                        recommendations.append({
                            'title': opp.get('title', 'Market Opportunity'),
                            'description': opp.get('description', ''),
                            'priority': opp.get('priority', 'medium'),
                            'category': 'market_opportunity',
                            'source_agent': agent_id
                        })
        
        return recommendations
    
    def _create_implementation_roadmap(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create implementation roadmap from recommendations"""
        roadmap = []
        
        # Sort recommendations by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        sorted_recs = sorted(recommendations, 
                           key=lambda x: priority_order.get(x.get('priority', 'medium'), 2), 
                           reverse=True)
        
        # Create phases
        phases = {
            'immediate': [],  # High priority, low effort
            'short_term': [],  # High priority, medium effort or medium priority, low effort
            'long_term': []   # Everything else
        }
        
        for rec in sorted_recs:
            priority = rec.get('priority', 'medium')
            effort = rec.get('implementation_effort', rec.get('effort', 'medium'))
            
            if priority == 'high' and effort in ['low', 'low_to_medium']:
                phases['immediate'].append(rec)
            elif (priority == 'high' and effort == 'medium') or (priority == 'medium' and effort == 'low'):
                phases['short_term'].append(rec)
            else:
                phases['long_term'].append(rec)
        
        # Create roadmap structure
        roadmap = [
            {
                'phase': 'Immediate Actions (0-30 days)',
                'recommendations': phases['immediate'][:3],  # Top 3
                'focus': 'Quick wins and critical issues'
            },
            {
                'phase': 'Short-term Initiatives (1-3 months)',
                'recommendations': phases['short_term'][:4],  # Top 4
                'focus': 'Strategic improvements and process optimization'
            },
            {
                'phase': 'Long-term Strategic Goals (3-12 months)',
                'recommendations': phases['long_term'][:3],  # Top 3
                'focus': 'Transformational changes and major investments'
            }
        ]
        
        return roadmap
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        return {
            'current_stage': self.current_stage,
            'agents_status': {agent_id: agent.get_status_info() 
                            for agent_id, agent in self.specialized_agents.items()},
            'workflow_context': self.workflow_context,
            'stage_results': self.stage_results
        }
    
    def reset_workflow(self):
        """Reset workflow state"""
        self.current_stage = 'initialization'
        self.stage_results = {}
        self.workflow_context = {}
        
        # Reset all specialized agents
        for agent in self.specialized_agents.values():
            agent.reset()
        
        logger.info("Master Orchestrator workflow reset")


# Global master orchestrator instance
master_orchestrator = MasterOrchestratorAgent()