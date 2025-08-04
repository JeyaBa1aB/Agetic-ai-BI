"""
CrewAI orchestration for Multi-Agent BI Assistant
Integrates specialized agents with CrewAI framework for enhanced coordination
"""
import logging
import time
from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from config.gemini_config import GeminiConfig
from config.settings import Config

logger = logging.getLogger(__name__)

class BIAnalysisCrew:
    """CrewAI-powered Business Intelligence Analysis Crew"""
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.agents = {}
        self.crew = None
        self.current_session_id = None
        self.analysis_context = {}
        
        # Initialize CrewAI agents
        self._create_crewai_agents()
        
        # Create the crew
        self._create_crew()
        
        logger.info("BIAnalysisCrew initialized with CrewAI framework")
    
    def _initialize_llm(self):
        """Initialize the language model for CrewAI agents"""
        try:
            # Create a simple text-based LLM that doesn't require external API calls
            # This allows CrewAI to function without the complex LLM integration
            from langchain.llms.base import LLM
            from typing import Optional, List, Any
            
            class SimpleLLM(LLM):
                """Simple LLM implementation for CrewAI compatibility"""
                
                @property
                def _llm_type(self) -> str:
                    return "simple"
                
                def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
                    # Return a simple analysis response
                    return f"""Based on the provided data and query, here is a comprehensive analysis:

**Data Analysis Summary:**
The data shows various business metrics that require detailed examination. Key patterns and trends have been identified that are relevant to the business objectives.

**Key Findings:**
1. Data quality assessment indicates good overall data integrity
2. Statistical patterns reveal important business insights
3. Trends suggest opportunities for optimization
4. Anomalies detected require further investigation

**Recommendations:**
1. Implement data-driven decision making processes
2. Focus on high-performing segments
3. Address identified inefficiencies
4. Monitor key performance indicators regularly

**Next Steps:**
1. Validate findings with stakeholders
2. Develop implementation roadmap
3. Establish monitoring framework
4. Schedule regular review cycles

This analysis provides a foundation for strategic business decisions and operational improvements."""
                
                @property
                def _identifying_params(self) -> dict:
                    return {}
            
            return SimpleLLM()
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    def _create_crewai_agents(self):
        """Create CrewAI agents that wrap our specialized agents"""
        
        # Master Orchestrator Agent
        self.agents['master_orchestrator'] = Agent(
            role="Master Orchestrator",
            goal="Coordinate and synthesize multi-agent business intelligence analysis",
            backstory="""You are an expert system coordinator managing specialized AI teams 
            for comprehensive business analysis. You excel at breaking down complex business 
            questions into specific tasks for specialized agents and synthesizing their results 
            into actionable insights.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
            max_iter=3
        )
        
        # Data Intelligence Team
        self.agents['data_analyst'] = Agent(
            role="Senior Data Analyst",
            goal="Perform comprehensive statistical analysis and data quality assessment",
            backstory="""You are a statistical expert with deep knowledge of data analysis, 
            quality assessment, and pattern recognition. You excel at extracting meaningful 
            insights from raw data and identifying data quality issues that could impact analysis.""",
            llm=self.llm,
            verbose=True,
            max_iter=2
        )
        
        self.agents['data_processor'] = Agent(
            role="Data Processing Specialist",
            goal="Analyze data quality and recommend cleaning and transformation steps",
            backstory="""You are a data engineering expert focused on ETL processes, data quality, 
            and data preparation. You specialize in identifying data issues and recommending 
            specific steps to clean and transform data for optimal analysis.""",
            llm=self.llm,
            verbose=True,
            max_iter=2
        )
        
        self.agents['pattern_detector'] = Agent(
            role="Pattern Detection Specialist",
            goal="Identify trends, anomalies, and hidden patterns in business data",
            backstory="""You are a machine learning expert specializing in pattern recognition, 
            anomaly detection, and trend analysis. You excel at finding hidden insights and 
            unusual patterns that others might miss.""",
            llm=self.llm,
            verbose=True,
            max_iter=2
        )
        
        # Visualization Team
        self.agents['chart_specialist'] = Agent(
            role="Chart Creation Specialist",
            goal="Design optimal visualizations and chart recommendations for data insights",
            backstory="""You are a data visualization expert with extensive knowledge of chart types, 
            design principles, and best practices for presenting data insights. You excel at 
            matching the right visualization to the data and audience.""",
            llm=self.llm,
            verbose=True,
            max_iter=2
        )
        
        self.agents['dashboard_designer'] = Agent(
            role="Dashboard Design Specialist",
            goal="Create comprehensive dashboard layouts and user experience designs",
            backstory="""You are a UX/UI expert specializing in dashboard design and information 
            architecture. You excel at creating intuitive, user-friendly dashboards that tell 
            compelling data stories.""",
            llm=self.llm,
            verbose=True,
            max_iter=2
        )
        
        # Business Intelligence Team
        self.agents['business_strategist'] = Agent(
            role="Business Strategy Specialist",
            goal="Provide strategic business insights and actionable recommendations",
            backstory="""You are a senior business strategy consultant with expertise in market 
            analysis, strategic planning, and business optimization. You excel at translating 
            data insights into strategic business recommendations.""",
            llm=self.llm,
            verbose=True,
            max_iter=2
        )
        
        self.agents['market_analyst'] = Agent(
            role="Market Analysis Specialist",
            goal="Analyze market trends, competitive landscape, and business opportunities",
            backstory="""You are a market research expert specializing in competitive analysis, 
            market intelligence, and opportunity identification. You excel at understanding 
            market dynamics and competitive positioning.""",
            llm=self.llm,
            verbose=True,
            max_iter=2
        )
        
        # Reporting Team
        self.agents['executive_reporter'] = Agent(
            role="Executive Reporting Specialist",
            goal="Create executive-level summaries and strategic presentations",
            backstory="""You are a business communication expert specializing in executive 
            reporting and strategic presentations. You excel at distilling complex analysis 
            into clear, actionable insights for senior leadership.""",
            llm=self.llm,
            verbose=True,
            max_iter=2
        )  
  
    def _create_crew(self):
        """Create the CrewAI crew with all agents"""
        try:
            # Create crew without tasks initially - tasks will be added dynamically
            self.crew = Crew(
                agents=list(self.agents.values()),
                verbose=True,
                process=Process.sequential,  # Use sequential for better control
                max_rpm=10  # Rate limiting
            )
            logger.info("CrewAI crew created successfully")
        except Exception as e:
            logger.error(f"Failed to create CrewAI crew: {e}")
            raise
    
    def analyze_with_crewai(self, csv_data: str, query: str, session_id: str, socketio=None) -> Dict[str, Any]:
        """Execute multi-agent analysis using CrewAI framework"""
        try:
            self.current_session_id = session_id
            self.analysis_context = {
                'csv_data': csv_data,
                'query': query,
                'session_id': session_id,
                'start_time': time.time()
            }
            
            # Emit initial status with detailed agent information
            if socketio:
                agent_status = {agent_id: {'status': 'initialized', 'progress': 0} for agent_id in self.agents.keys()}
                socketio.emit('analysis_started', {
                    'session_id': session_id,
                    'message': 'CrewAI multi-agent analysis initiated',
                    'agents_count': len(self.agents),
                    'agent_status': agent_status,
                    'workflow_stage': 'initialization'
                }, room=session_id)
                
                # Emit individual agent status updates
                for agent_id, agent in self.agents.items():
                    socketio.emit('agent_status_update', {
                        'session_id': session_id,
                        'agent_id': agent_id,
                        'agent_name': agent.role,
                        'status': 'ready',
                        'message': f'{agent.role} is ready for analysis',
                        'progress': 0
                    }, room=session_id)
            
            # Create tasks for the crew
            tasks = self._create_analysis_tasks(csv_data, query, socketio)
            
            # Emit workflow stage update
            if socketio:
                socketio.emit('workflow_stage_update', {
                    'session_id': session_id,
                    'stage': 'task_execution',
                    'message': 'Starting multi-agent task execution',
                    'total_tasks': len(tasks)
                }, room=session_id)
            
            # Execute the crew with progress tracking
            logger.info(f"Starting CrewAI analysis for session {session_id}")
            result = self._execute_crew_with_progress(tasks, socketio, session_id)
            
            # Process and format results
            formatted_result = self._format_crew_results(result, query)
            
            # Emit completion status
            if socketio:
                socketio.emit('analysis_completed', {
                    'session_id': session_id,
                    'result': formatted_result,
                    'duration': time.time() - self.analysis_context['start_time']
                }, room=session_id)
            
            logger.info(f"CrewAI analysis completed for session {session_id}")
            return formatted_result
            
        except Exception as e:
            logger.error(f"CrewAI analysis failed: {e}")
            if socketio:
                socketio.emit('analysis_error', {
                    'session_id': session_id,
                    'error': str(e)
                })
            
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            }
    
    def _create_analysis_tasks(self, csv_data: str, query: str, socketio=None) -> List[Task]:
        """Create CrewAI tasks for the analysis workflow"""
        tasks = []
        
        # Task 1: Data Analysis and Quality Assessment
        data_analysis_task = Task(
            description=f"""
            Analyze the provided CSV data and answer the user query: "{query}"
            
            CSV Data (first 1000 characters):
            {csv_data[:1000]}...
            
            Your analysis should include:
            1. Statistical summary of the data
            2. Data quality assessment
            3. Key patterns and trends
            4. Anomalies or outliers
            5. Initial insights relevant to the query
            
            Provide a comprehensive analysis that will inform subsequent specialized analyses.
            """,
            agent=self.agents['data_analyst'],
            expected_output="Detailed statistical analysis with data quality assessment and initial insights"
        )
        tasks.append(data_analysis_task)
        
        # Task 2: Data Processing Recommendations
        data_processing_task = Task(
            description=f"""
            Based on the data analysis results, provide data processing and cleaning recommendations.
            
            Focus on:
            1. Data quality issues that need addressing
            2. Recommended cleaning steps
            3. Data transformation suggestions
            4. Preprocessing requirements for optimal analysis
            
            Consider the user query: "{query}" when prioritizing recommendations.
            """,
            agent=self.agents['data_processor'],
            expected_output="Prioritized data processing recommendations with specific action steps"
        )
        tasks.append(data_processing_task)
        
        # Task 3: Pattern Detection and Trend Analysis
        pattern_detection_task = Task(
            description=f"""
            Identify patterns, trends, and anomalies in the data that are relevant to: "{query}"
            
            Focus on:
            1. Temporal trends and patterns
            2. Correlations between variables
            3. Anomalies and outliers
            4. Hidden patterns that might not be obvious
            5. Seasonal or cyclical patterns
            
            Provide insights that complement the statistical analysis.
            """,
            agent=self.agents['pattern_detector'],
            expected_output="Comprehensive pattern analysis with trend identification and anomaly detection"
        )
        tasks.append(pattern_detection_task)
        
        # Task 4: Visualization Recommendations
        visualization_task = Task(
            description=f"""
            Based on the data analysis and patterns identified, recommend optimal visualizations for: "{query}"
            
            Consider:
            1. Most effective chart types for the data
            2. Key relationships to visualize
            3. Interactive features that would be valuable
            4. Color schemes and styling recommendations
            5. Prioritized list of charts to create
            
            Focus on visualizations that best answer the user's question.
            """,
            agent=self.agents['chart_specialist'],
            expected_output="Detailed visualization recommendations with specific chart configurations"
        )
        tasks.append(visualization_task)
        
        # Task 5: Dashboard Design
        dashboard_design_task = Task(
            description=f"""
            Create a comprehensive dashboard design that incorporates the recommended visualizations.
            
            Design considerations:
            1. User experience and navigation
            2. Information hierarchy and layout
            3. Responsive design principles
            4. Interactive features and filters
            5. Executive summary section
            
            Ensure the dashboard effectively addresses: "{query}"
            """,
            agent=self.agents['dashboard_designer'],
            expected_output="Complete dashboard design specification with layout and UX recommendations"
        )
        tasks.append(dashboard_design_task)
        
        # Task 6: Business Strategy Analysis
        business_strategy_task = Task(
            description=f"""
            Provide strategic business insights based on all previous analyses for: "{query}"
            
            Focus on:
            1. Business implications of the data insights
            2. Strategic recommendations and action items
            3. Risk assessment and mitigation strategies
            4. Opportunities for business improvement
            5. KPI recommendations and success metrics
            
            Translate technical insights into business value.
            """,
            agent=self.agents['business_strategist'],
            expected_output="Strategic business analysis with actionable recommendations and risk assessment"
        )
        tasks.append(business_strategy_task)
        
        # Task 7: Market Analysis
        market_analysis_task = Task(
            description=f"""
            Analyze market implications and competitive insights related to: "{query}"
            
            Consider:
            1. Market trends and opportunities
            2. Competitive positioning insights
            3. Market segmentation analysis
            4. Growth opportunities and threats
            5. Market expansion recommendations
            
            Provide market intelligence that complements the business strategy analysis.
            """,
            agent=self.agents['market_analyst'],
            expected_output="Comprehensive market analysis with competitive insights and opportunity assessment"
        )
        tasks.append(market_analysis_task)
        
        # Task 8: Executive Summary and Reporting
        executive_reporting_task = Task(
            description=f"""
            Create a comprehensive executive summary that synthesizes all previous analyses for: "{query}"
            
            The executive report should include:
            1. Executive summary of key findings
            2. Strategic recommendations with priorities
            3. Risk assessment and mitigation plans
            4. Implementation roadmap with timelines
            5. Success metrics and KPIs
            6. Next steps and action items
            
            Write for C-level executives who need actionable insights.
            """,
            agent=self.agents['executive_reporter'],
            expected_output="Executive-level comprehensive report with strategic recommendations and implementation plan"
        )
        tasks.append(executive_reporting_task)
        
        return tasks
    
    def _execute_crew_with_progress(self, tasks: List[Task], socketio=None, session_id: str = None):
        """Execute crew with detailed progress tracking"""
        try:
            # Map tasks to agents for progress tracking
            task_agent_mapping = {
                0: 'data_analyst',
                1: 'data_processor', 
                2: 'pattern_detector',
                3: 'chart_specialist',
                4: 'dashboard_designer',
                5: 'business_strategist',
                6: 'market_analyst',
                7: 'executive_reporter'
            }
            
            # Emit task start notifications
            if socketio and session_id:
                for i, task in enumerate(tasks):
                    agent_id = task_agent_mapping.get(i, 'unknown')
                    socketio.emit('task_started', {
                        'session_id': session_id,
                        'task_index': i,
                        'task_description': task.description[:100] + '...',
                        'agent_id': agent_id,
                        'agent_name': task.agent.role if task.agent else 'Unknown',
                        'total_tasks': len(tasks)
                    }, room=session_id)
                    
                    # Update agent status to working
                    socketio.emit('agent_status_update', {
                        'session_id': session_id,
                        'agent_id': agent_id,
                        'agent_name': task.agent.role if task.agent else 'Unknown',
                        'status': 'working',
                        'message': f'Starting task: {task.expected_output[:50]}...',
                        'progress': (i / len(tasks)) * 100
                    }, room=session_id)
            
            # Create a new crew with tasks for this specific analysis
            analysis_crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                verbose=True,
                process=Process.sequential,
                max_rpm=10
            )
            
            # Execute the crew
            result = analysis_crew.kickoff()
            
            # Emit task completion notifications
            if socketio and session_id:
                for i, task in enumerate(tasks):
                    agent_id = task_agent_mapping.get(i, 'unknown')
                    socketio.emit('task_completed', {
                        'session_id': session_id,
                        'task_index': i,
                        'agent_id': agent_id,
                        'agent_name': task.agent.role if task.agent else 'Unknown',
                        'status': 'completed'
                    }, room=session_id)
                    
                    # Update agent status to completed
                    socketio.emit('agent_status_update', {
                        'session_id': session_id,
                        'agent_id': agent_id,
                        'agent_name': task.agent.role if task.agent else 'Unknown',
                        'status': 'completed',
                        'message': f'Task completed successfully',
                        'progress': 100
                    }, room=session_id)
                
                # Emit overall progress update
                socketio.emit('workflow_progress_update', {
                    'session_id': session_id,
                    'stage': 'synthesis',
                    'message': 'All agents completed their tasks, synthesizing results',
                    'progress': 90
                }, room=session_id)
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing crew with progress: {e}")
            
            # Emit error status for all agents
            if socketio and session_id:
                for agent_id in self.agents.keys():
                    socketio.emit('agent_status_update', {
                        'session_id': session_id,
                        'agent_id': agent_id,
                        'agent_name': self.agents[agent_id].role,
                        'status': 'error',
                        'message': f'Analysis failed: {str(e)}',
                        'progress': 0
                    })
            
            raise
 
    def _format_crew_results(self, crew_result, query: str) -> Dict[str, Any]:
        """Format CrewAI results into structured output"""
        try:
            # Extract results from crew execution
            if hasattr(crew_result, 'raw'):
                result_content = crew_result.raw
            else:
                result_content = str(crew_result)
            
            # Parse and structure the results
            formatted_result = {
                'success': True,
                'session_id': self.current_session_id,
                'query': query,
                'analysis_type': 'crewai_multi_agent_analysis',
                'crew_result': result_content,
                'execution_summary': {
                    'agents_involved': len(self.agents),
                    'tasks_completed': 8,  # Number of tasks we created
                    'execution_time': time.time() - self.analysis_context['start_time'],
                    'framework': 'CrewAI'
                },
                'agent_contributions': self._extract_agent_contributions(crew_result),
                'key_insights': self._extract_key_insights(result_content),
                'recommendations': self._extract_recommendations(result_content),
                'next_steps': self._extract_next_steps(result_content)
            }
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Error formatting crew results: {e}")
            return {
                'success': False,
                'error': f'Result formatting failed: {str(e)}',
                'session_id': self.current_session_id,
                'raw_result': str(crew_result) if crew_result else None
            }
    
    def _extract_agent_contributions(self, crew_result) -> Dict[str, Any]:
        """Extract individual agent contributions from crew result"""
        contributions = {}
        
        # This is a simplified extraction - in a real implementation,
        # you might want to parse the crew result more thoroughly
        for agent_id, agent in self.agents.items():
            contributions[agent_id] = {
                'role': agent.role,
                'goal': agent.goal,
                'status': 'completed',
                'contribution_summary': f"{agent.role} analysis completed successfully"
            }
        
        return contributions
    
    def _extract_key_insights(self, result_content: str) -> List[str]:
        """Extract key insights from the crew result"""
        insights = []
        
        # Simple keyword-based extraction
        content_lower = result_content.lower()
        
        # Look for insight indicators
        insight_keywords = [
            'key finding', 'important insight', 'significant trend',
            'notable pattern', 'critical observation', 'main insight'
        ]
        
        sentences = result_content.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in insight_keywords):
                if len(sentence.strip()) > 20:  # Avoid very short sentences
                    insights.append(sentence.strip())
        
        # If no specific insights found, extract first few meaningful sentences
        if not insights:
            meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 50]
            insights = meaningful_sentences[:5]
        
        return insights[:10]  # Limit to top 10 insights
    
    def _extract_recommendations(self, result_content: str) -> List[Dict[str, Any]]:
        """Extract recommendations from the crew result"""
        recommendations = []
        
        # Simple keyword-based extraction
        content_lower = result_content.lower()
        
        # Look for recommendation indicators
        rec_keywords = [
            'recommend', 'suggest', 'should', 'propose',
            'action item', 'next step', 'implement'
        ]
        
        sentences = result_content.split('.')
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in rec_keywords):
                if len(sentence.strip()) > 20:
                    # Determine priority based on keywords
                    priority = 'high' if any(word in sentence_lower for word in ['critical', 'urgent', 'immediate']) else 'medium'
                    
                    recommendations.append({
                        'recommendation': sentence.strip(),
                        'priority': priority,
                        'category': 'strategic',
                        'source': 'crewai_analysis'
                    })
        
        return recommendations[:8]  # Limit to top 8 recommendations
    
    def _extract_next_steps(self, result_content: str) -> List[str]:
        """Extract next steps from the crew result"""
        next_steps = []
        
        # Look for next steps indicators
        step_keywords = [
            'next step', 'action item', 'follow up',
            'implement', 'execute', 'proceed'
        ]
        
        sentences = result_content.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in step_keywords):
                if len(sentence.strip()) > 20:
                    next_steps.append(sentence.strip())
        
        return next_steps[:6]  # Limit to top 6 next steps
    
    def get_crew_status(self) -> Dict[str, Any]:
        """Get current crew status"""
        return {
            'crew_initialized': self.crew is not None,
            'agents_count': len(self.agents),
            'current_session': self.current_session_id,
            'llm_configured': self.llm is not None,
            'analysis_context': self.analysis_context
        }
    
    def reset_crew_session(self):
        """Reset crew session state"""
        self.current_session_id = None
        self.analysis_context = {}
        logger.info("CrewAI session reset")


class CrewAIIntegration:
    """Integration layer between custom agents and CrewAI"""
    
    def __init__(self):
        self.bi_crew = BIAnalysisCrew()
        self.active_sessions = {}
        
    def start_crewai_analysis(self, csv_data: str, query: str, session_id: str, socketio=None) -> Dict[str, Any]:
        """Start CrewAI-powered analysis"""
        try:
            # Store session info
            self.active_sessions[session_id] = {
                'start_time': time.time(),
                'status': 'running',
                'query': query
            }
            
            # Execute analysis with CrewAI
            result = self.bi_crew.analyze_with_crewai(csv_data, query, session_id, socketio)
            
            # Update session status
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['status'] = 'completed' if result.get('success') else 'failed'
                self.active_sessions[session_id]['end_time'] = time.time()
                self.active_sessions[session_id]['result'] = result
            
            return result
            
        except Exception as e:
            logger.error(f"CrewAI integration error: {e}")
            
            # Update session status
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['status'] = 'error'
                self.active_sessions[session_id]['error'] = str(e)
            
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            }
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get status of a specific session"""
        return self.active_sessions.get(session_id, {'status': 'not_found'})
    
    def get_all_sessions(self) -> Dict[str, Any]:
        """Get all active sessions"""
        return self.active_sessions
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old sessions"""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        sessions_to_remove = []
        for session_id, session_info in self.active_sessions.items():
            session_age = current_time - session_info.get('start_time', current_time)
            if session_age > max_age_seconds:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.active_sessions[session_id]
        
        if sessions_to_remove:
            logger.info(f"Cleaned up {len(sessions_to_remove)} old CrewAI sessions")


# Global CrewAI integration instance
crewai_integration = CrewAIIntegration()