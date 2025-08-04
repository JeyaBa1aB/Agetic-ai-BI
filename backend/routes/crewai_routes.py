"""
CrewAI routes for Multi-Agent BI Assistant
Handles CrewAI-powered analysis requests
"""
import logging
from flask import Blueprint, request, jsonify
from crews.bi_crew import crewai_integration

logger = logging.getLogger(__name__)

# Create blueprint
crewai_bp = Blueprint('crewai', __name__)

@crewai_bp.route('/analyze', methods=['POST'])
def crewai_analyze():
    """Start CrewAI multi-agent analysis"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['query', 'csv_data', 'session_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        query = data['query']
        csv_data = data['csv_data']
        session_id = data['session_id']
        
        logger.info(f"Starting CrewAI analysis for session {session_id}")
        
        # Start CrewAI analysis
        result = crewai_integration.start_crewai_analysis(csv_data, query, session_id)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"CrewAI analysis error: {e}")
        return jsonify({
            'success': False,
            'error': f'CrewAI analysis failed: {str(e)}'
        }), 500

@crewai_bp.route('/status/<session_id>', methods=['GET'])
def get_crewai_status(session_id):
    """Get CrewAI analysis status for a session"""
    try:
        status = crewai_integration.get_session_status(session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Error getting CrewAI status: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get status: {str(e)}'
        }), 500

@crewai_bp.route('/sessions', methods=['GET'])
def get_all_crewai_sessions():
    """Get all CrewAI sessions"""
    try:
        sessions = crewai_integration.get_all_sessions()
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'count': len(sessions)
        })
        
    except Exception as e:
        logger.error(f"Error getting CrewAI sessions: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get sessions: {str(e)}'
        }), 500

@crewai_bp.route('/crew/status', methods=['GET'])
def get_crew_status():
    """Get CrewAI crew status"""
    try:
        status = crewai_integration.bi_crew.get_crew_status()
        
        return jsonify({
            'success': True,
            'crew_status': status
        })
        
    except Exception as e:
        logger.error(f"Error getting crew status: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get crew status: {str(e)}'
        }), 500