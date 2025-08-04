"""
Base agent class for Multi-Agent BI Assistant
Provides common functionality for all specialized agents
"""
import logging
import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from config.gemini_config import AgentGeminiConfig

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all BI agents"""
    
    def __init__(self, agent_id: str, name: str, role: str, description: str, specialization: str = None):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.description = description
        self.specialization = specialization or description
        self.capabilities = []  # Will be set by individual agents
        self.status = "initialized"
        self.created_at = time.time()
        self.last_activity = time.time()
        self.session_id = None
        self.results_history = []
        
        # Initialize AI service for this agent
        try:
            self.ai_service, self.system_instruction = AgentGeminiConfig.get_agent_service(agent_id)
            logger.info(f"Agent {self.name} initialized with AI service")
        except Exception as e:
            logger.error(f"Failed to initialize AI service for {self.name}: {e}")
            self.ai_service = None
            self.system_instruction = None
    
    def set_session(self, session_id: str):
        """Set the current session ID"""
        self.session_id = session_id
        self.last_activity = time.time()
        logger.info(f"Agent {self.name} assigned to session {session_id}")
    
    def update_status(self, status: str, message: str = None):
        """Update agent status"""
        self.status = status
        self.last_activity = time.time()
        
        status_info = {
            'agent_id': self.agent_id,
            'name': self.name,
            'status': status,
            'message': message,
            'timestamp': self.last_activity
        }
        
        logger.info(f"Agent {self.name} status: {status}" + (f" - {message}" if message else ""))
        return status_info
    
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate AI response using the agent's specialized service"""
        try:
            if not self.ai_service:
                return {
                    'success': False,
                    'error': 'AI service not available',
                    'content': None
                }
            
            # Prepare full prompt with system instruction and context
            full_prompt = self._prepare_prompt(prompt, context)
            
            # Generate response
            result = self.ai_service.generate_content(full_prompt)
            
            if result['success']:
                # Store result in history
                self.results_history.append({
                    'prompt': prompt,
                    'response': result['content'],
                    'timestamp': time.time(),
                    'session_id': self.session_id
                })
                
                logger.info(f"Agent {self.name} generated response ({len(result['content'])} chars)")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating response for {self.name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    def _prepare_prompt(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Prepare the full prompt with system instruction and context"""
        parts = []
        
        # Add system instruction
        if self.system_instruction:
            parts.append(f"System: {self.system_instruction}")
        
        # Add context if provided
        if context:
            context_str = self._format_context(context)
            if context_str:
                parts.append(f"Context: {context_str}")
        
        # Add user prompt
        parts.append(f"User Query: {prompt}")
        
        return "\n\n".join(parts)
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context information for the prompt"""
        context_parts = []
        
        if 'csv_data' in context:
            csv_preview = context['csv_data'][:500] + "..." if len(context['csv_data']) > 500 else context['csv_data']
            context_parts.append(f"CSV Data Preview:\n{csv_preview}")
        
        if 'previous_results' in context:
            for i, result in enumerate(context['previous_results'][-3:]):  # Last 3 results
                context_parts.append(f"Previous Analysis {i+1}: {result}")
        
        if 'session_info' in context:
            context_parts.append(f"Session Info: {context['session_info']}")
        
        return "\n".join(context_parts)
    
    @abstractmethod
    def analyze(self, data: Dict[str, Any], query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Abstract method for agent-specific analysis"""
        pass
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get current agent status information"""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'role': self.role,
            'description': self.description,
            'status': self.status,
            'session_id': self.session_id,
            'created_at': self.created_at,
            'last_activity': self.last_activity,
            'results_count': len(self.results_history),
            'ai_service_available': self.ai_service is not None
        }
    
    def get_recent_results(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent analysis results"""
        return self.results_history[-limit:] if self.results_history else []
    
    def reset(self):
        """Reset agent state for new session"""
        self.status = "initialized"
        self.session_id = None
        self.last_activity = time.time()
        logger.info(f"Agent {self.name} reset for new session")


class AgentManager:
    """Manager class for handling multiple agents"""
    
    def __init__(self):
        self.agents = {}
        self.active_sessions = {}
        logger.info("Agent Manager initialized")
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the manager"""
        self.agents[agent.agent_id] = agent
        logger.info(f"Agent registered: {agent.name} ({agent.agent_id})")
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def get_agents_by_role(self, role: str) -> List[BaseAgent]:
        """Get all agents with a specific role"""
        return [agent for agent in self.agents.values() if agent.role == role]
    
    def assign_session(self, session_id: str, agent_ids: List[str] = None):
        """Assign agents to a session"""
        if agent_ids is None:
            agent_ids = list(self.agents.keys())
        
        session_agents = []
        for agent_id in agent_ids:
            if agent_id in self.agents:
                self.agents[agent_id].set_session(session_id)
                session_agents.append(self.agents[agent_id])
        
        self.active_sessions[session_id] = session_agents
        logger.info(f"Session {session_id} assigned to {len(session_agents)} agents")
        
        return session_agents
    
    def get_session_agents(self, session_id: str) -> List[BaseAgent]:
        """Get agents assigned to a session"""
        return self.active_sessions.get(session_id, [])
    
    def get_all_agents_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all agents"""
        return {
            agent_id: agent.get_status_info() 
            for agent_id, agent in self.agents.items()
        }
    
    def reset_session(self, session_id: str):
        """Reset all agents in a session"""
        if session_id in self.active_sessions:
            for agent in self.active_sessions[session_id]:
                agent.reset()
            del self.active_sessions[session_id]
            logger.info(f"Session {session_id} reset")
    
    def cleanup_inactive_sessions(self, max_age_hours: int = 24):
        """Clean up inactive sessions"""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        inactive_sessions = []
        for session_id, agents in self.active_sessions.items():
            if agents and (current_time - agents[0].last_activity) > max_age_seconds:
                inactive_sessions.append(session_id)
        
        for session_id in inactive_sessions:
            self.reset_session(session_id)
        
        if inactive_sessions:
            logger.info(f"Cleaned up {len(inactive_sessions)} inactive sessions")


# Global agent manager instance
agent_manager = AgentManager()