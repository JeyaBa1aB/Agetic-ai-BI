"""
Analysis routes for Multi-Agent BI Assistant
Handles analysis requests and session management
"""
import logging
import uuid
from flask import Blueprint, request, jsonify
from config.settings import Config
from config.supabase_config import SupabaseService
from config.gemini_config import GeminiService

logger = logging.getLogger(__name__)

# Create blueprint
analysis_bp = Blueprint('analysis', __name__)

# Global Supabase service (will be injected from main app)
supabase_service = None
gemini_service = None

def init_analysis_services(sb_service, gm_service):
    """Initialize services for analysis routes"""
    global supabase_service, gemini_service
    supabase_service = sb_service
    gemini_service = gm_service

@analysis_bp.route('/start', methods=['POST'])
def start_analysis():
    """Start a new analysis session"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['query', 'csv_data']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Prepare session data
        session_data = {
            'session_id': session_id,
            'query': data['query'],
            'csv_data': data['csv_data'],
            'status': 'initialized',
            'user_id': data.get('user_id', 'anonymous'),
            'metadata': data.get('metadata', {}),
            'agents_status': {},
            'results': {}
        }
        
        # Save session to Supabase if available
        if supabase_service:
            success = supabase_service.save_analysis_session(session_id, session_data)
            if not success:
                logger.warning(f"Failed to save session to Supabase: {session_id}")
            else:
                logger.info(f"Successfully saved session to Supabase: {session_id}")
                # Verify the session was saved by trying to retrieve it
                retrieved = supabase_service.get_analysis_session(session_id)
                if retrieved:
                    logger.info(f"Session verification successful: {session_id}")
                else:
                    logger.error(f"Session verification failed: {session_id}")
        
        logger.info(f"Analysis session started: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Analysis session initialized',
            'status': 'initialized'
        })
        
    except Exception as e:
        logger.error(f"Error starting analysis: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to start analysis: {str(e)}'
        }), 500

@analysis_bp.route('/status/<session_id>', methods=['GET'])
def get_analysis_status(session_id):
    """Get analysis session status"""
    try:
        # Retrieve session from Supabase if available
        session_data = None
        if supabase_service:
            session_data = supabase_service.get_analysis_session(session_id)
        
        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'status': session_data.get('status', 'unknown'),
            'agents_status': session_data.get('agents_status', {}),
            'progress': session_data.get('progress', 0),
            'created_at': session_data.get('created_at'),
            'updated_at': session_data.get('updated_at')
        })
        
    except Exception as e:
        logger.error(f"Error getting analysis status: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get status: {str(e)}'
        }), 500

@analysis_bp.route('/results/<session_id>', methods=['GET'])
def get_analysis_results(session_id):
    """Get analysis results for a session"""
    try:
        # Retrieve session from Supabase if available
        session_data = None
        if supabase_service:
            session_data = supabase_service.get_analysis_session(session_id)
        
        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Get agent results if available
        agent_results = []
        if supabase_service:
            agent_results = supabase_service.get_agent_results(session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'status': session_data.get('status', 'unknown'),
            'query': session_data.get('query'),
            'results': session_data.get('results', {}),
            'agent_results': agent_results,
            'created_at': session_data.get('created_at'),
            'updated_at': session_data.get('updated_at')
        })
        
    except Exception as e:
        logger.error(f"Error getting analysis results: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get results: {str(e)}'
        }), 500

@analysis_bp.route('/update/<session_id>', methods=['PUT'])
def update_analysis_session(session_id):
    """Update analysis session"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No update data provided'
            }), 400
        
        # Update session in Supabase if available
        if supabase_service:
            success = supabase_service.update_analysis_session(session_id, data)
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Failed to update session'
                }), 500
        
        logger.info(f"Analysis session updated: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Session updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error updating analysis session: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to update session: {str(e)}'
        }), 500

@analysis_bp.route('/sessions', methods=['GET'])
def get_recent_sessions():
    """Get recent analysis sessions"""
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 50)  # Cap at 50 sessions
        
        sessions = []
        if supabase_service:
            sessions = supabase_service.get_recent_sessions(limit)
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'count': len(sessions)
        })
        
    except Exception as e:
        logger.error(f"Error getting recent sessions: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to get sessions: {str(e)}'
        }), 500

@analysis_bp.route('/delete/<session_id>', methods=['DELETE'])
def delete_analysis_session(session_id):
    """Delete analysis session"""
    try:
        # Delete session from Supabase if available
        if supabase_service:
            success = supabase_service.delete_session(session_id)
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Failed to delete session'
                }), 500
        
        logger.info(f"Analysis session deleted: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Session deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting analysis session: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to delete session: {str(e)}'
        }), 500

@analysis_bp.route('/test', methods=['POST'])
def test_analysis():
    """Test analysis functionality with Gemini AI"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'No query provided'
            }), 400
        
        query = data['query']
        
        # Test Gemini AI if available
        if gemini_service:
            result = gemini_service.generate_content(
                f"As a business intelligence analyst, provide a brief response to this query: {query}"
            )
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'query': query,
                    'response': result['content'],
                    'usage': result.get('usage')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'AI analysis failed: {result["error"]}'
                }), 500
        else:
            return jsonify({
                'success': False,
                'error': 'Gemini AI service not available'
            }), 503
            
    except Exception as e:
        logger.error(f"Error in test analysis: {e}")
        return jsonify({
            'success': False,
            'error': f'Test analysis failed: {str(e)}'
        }), 500