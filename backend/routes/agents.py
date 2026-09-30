"""
Agent routes for Multi-Agent BI Assistant
Handles agent status and communication endpoints
"""
import logging
from flask import Blueprint, request, jsonify
from config.settings import Config
from config.gemini_config import AgentGeminiConfig

logger = logging.getLogger(__name__)

# Create blueprint
agents_bp = Blueprint('agents', __name__)

# Agent type definitions
AGENT_TYPES = {
    'master_orchestrator': {
        'name': 'Master Orchestrator',
        'description': 'Coordinates multi-agent business intelligence analysis',
        'role': 'coordination',
        'color': '#9333ea'
    },
    'data_analyst': {
        'name': 'Senior Data Analyst',
        'description': 'Performs statistical analysis and data quality assessment',
        'role': 'data_intelligence',
        'color': '#3b82f6'
    },
    'data_processor': {
        'name': 'Data Processing Specialist',
        'description': 'Cleans, transforms, and prepares data for analysis',
        'role': 'data_intelligence',
        'color': '#3b82f6'
    },
    'pattern_detector': {
        'name': 'Pattern Detection Specialist',
        'description': 'Identifies trends, anomalies, and hidden patterns',
        'role': 'data_intelligence',
        'color': '#3b82f6'
    },
    'chart_specialist': {
        'name': 'Chart Creation Specialist',
        'description': 'Designs optimal visualizations for data insights',
        'role': 'visualization',
        'color': '#10b981'
    },
    'dashboard_designer': {
        'name': 'Dashboard Design Specialist',
        'description': 'Creates comprehensive dashboard layouts',
        'role': 'visualization',
        'color': '#10b981'
    },
    'business_strategist': {
        'name': 'Business Strategy Specialist',
        'description': 'Provides strategic business insights and recommendations',
        'role': 'business_intelligence',
        'color': '#f59e0b'
    },
    'market_analyst': {
        'name': 'Market Analysis Specialist',
        'description': 'Analyzes market trends and competitive landscape',
        'role': 'business_intelligence',
        'color': '#f59e0b'
    },
    'executive_reporter': {
        'name': 'Executive Reporting Specialist',
        'description': 'Creates executive-level summaries and presentations',
        'role': 'reporting',
        'color': '#ef4444'
    }
}

@agents_bp.route('/list', methods=['GET'])
def list_agents():
    """Get list of all available agents"""
    try:
        agents = []
        for agent_id, agent_info in AGENT_TYPES.items():
            # Get agent configuration
            config = AgentGeminiConfig.AGENT_CONFIGS.get(agent_id, {})
            
            agent_data = {
                'id': agent_id,
                'name': agent_info['name'],
                'description': agent_info['description'],
                'role': agent_info['role'],
                'color': agent_info['color'],
                'config': {
                    'temperature': config.get('temperature'),
                    'max_tokens': config.get('max_tokens'),
                    'system_instruction': config.get('system_instruction', '')[:100] + '...' if config.get('system_instruction') else None
                }
            }
            agents.append(agent_data)
        
        return jsonify({
            'success': True,
            'agents': agents,
            'total_agents': len(agents),
            'roles': {
                'coordination': [a for a in agents if a['role'] == 'coordination'],
                'data_intelligence': [a for a in agents if a['role'] == 'data_intelligence'],
                'visualization': [a for a in agents if a['role'] == 'visualization'],
                'business_intelligence': [a for a in agents if a['role'] == 'business_intelligence'],
                'reporting': [a for a in agents if a['role'] == 'reporting']
            }
        })
        
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to list agents: {str(e)}'
        }), 500

@agents_bp.route('/info/<agent_id>', methods=['GET'])
def get_agent_info(agent_id):
    """Get detailed information about a specific agent"""
    try:
        if agent_id not in AGENT_TYPES:
            return jsonify({
                'success': False,
                'error': 'Agent not found'
            }), 404
        
        agent_info = AGENT_TYPES[agent_id]
        config = AgentGeminiConfig.AGENT_CONFIGS.get(agent_id, {})
        
        return jsonify({
            'success': True,
            'agent': {
                'id': agent_id,
                'name': agent_info['name'],
                'description': agent_info['description'],
                'role': agent_info['role'],
                'color': agent_info['color'],
                'config': {
                    'temperature': config.get('temperature'),
                    'max_tokens': config.get('max_tokens'),
                    'system_instruction': config.get('system_instruction')
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting agent info: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get agent info: {str(e)}'
        }), 500

@agents_bp.route('/status', methods=['GET'])
def get_agents_status():
    """Get status of all agents"""
    try:
        # This would typically check if agents are running, their health, etc.
        # For now, we'll return basic configuration status
        
        agents_status = {}
        for agent_id in AGENT_TYPES.keys():
            try:
                # Try to create agent service to test availability
                agent_service, _ = AgentGeminiConfig.get_agent_service(agent_id)
                agents_status[agent_id] = {
                    'status': 'available' if agent_service else 'unavailable',
                    'name': AGENT_TYPES[agent_id]['name'],
                    'role': AGENT_TYPES[agent_id]['role']
                }
            except Exception as e:
                agents_status[agent_id] = {
                    'status': 'error',
                    'error': str(e),
                    'name': AGENT_TYPES[agent_id]['name'],
                    'role': AGENT_TYPES[agent_id]['role']
                }
        
        # Count statuses
        available_count = sum(1 for status in agents_status.values() if status['status'] == 'available')
        error_count = sum(1 for status in agents_status.values() if status['status'] == 'error')
        
        return jsonify({
            'success': True,
            'agents_status': agents_status,
            'summary': {
                'total_agents': len(AGENT_TYPES),
                'available': available_count,
                'errors': error_count,
                'overall_status': 'healthy' if error_count == 0 else 'degraded'
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting agents status: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get agents status: {str(e)}'
        }), 500

@agents_bp.route('/roles', methods=['GET'])
def get_agent_roles():
    """Get agents organized by roles"""
    try:
        roles = {
            'coordination': {
                'name': 'Coordination',
                'description': 'Orchestrates and coordinates the multi-agent workflow',
                'color': '#9333ea',
                'agents': []
            },
            'data_intelligence': {
                'name': 'Data Intelligence',
                'description': 'Analyzes data quality, patterns, and statistical insights',
                'color': '#3b82f6',
                'agents': []
            },
            'visualization': {
                'name': 'Visualization',
                'description': 'Creates charts, graphs, and dashboard designs',
                'color': '#10b981',
                'agents': []
            },
            'business_intelligence': {
                'name': 'Business Intelligence',
                'description': 'Provides strategic insights and market analysis',
                'color': '#f59e0b',
                'agents': []
            },
            'reporting': {
                'name': 'Reporting',
                'description': 'Creates executive summaries and presentations',
                'color': '#ef4444',
                'agents': []
            }
        }
        
        # Organize agents by role
        for agent_id, agent_info in AGENT_TYPES.items():
            role = agent_info['role']
            if role in roles:
                roles[role]['agents'].append({
                    'id': agent_id,
                    'name': agent_info['name'],
                    'description': agent_info['description']
                })
        
        return jsonify({
            'success': True,
            'roles': roles
        })
        
    except Exception as e:
        logger.error(f"Error getting agent roles: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get agent roles: {str(e)}'
        }), 500