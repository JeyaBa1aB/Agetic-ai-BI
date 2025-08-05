from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import logging
import time
from dotenv import load_dotenv

# Import configuration modules
from config.settings import Config
from config.supabase_config import SupabaseConfig, SupabaseService
from config.gemini_config import GeminiConfig, GeminiService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB default

# Get CORS origins from environment
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')

# Enable CORS for cross-origin requests from React frontend
CORS(app, origins=cors_origins)

# Initialize SocketIO for real-time communication with extended timeouts for long-running analysis
socketio = SocketIO(
    app, 
    cors_allowed_origins=cors_origins,
    ping_timeout=60,      # 60 seconds ping timeout
    ping_interval=25,     # 25 seconds ping interval
    max_http_buffer_size=100000000,  # 100MB for large data transfers
    logger=True,
    engineio_logger=True
)

# Initialize Supabase
try:
    supabase_client = SupabaseConfig.init_supabase()
    supabase_service = SupabaseService()
    logger.info("Supabase initialized successfully")
except Exception as e:
    logger.error(f"Supabase initialization failed: {e}")
    supabase_client = None
    supabase_service = None

# Initialize Gemini AI
try:
    gemini_model = GeminiConfig.init_gemini()
    gemini_service = GeminiService()
    logger.info("Gemini AI initialized successfully")
except Exception as e:
    logger.error(f"Gemini AI initialization failed: {e}")
    gemini_model = None
    gemini_service = None

# Import and register blueprints
from routes.upload import upload_bp
from routes.analysis import analysis_bp, init_analysis_services
from routes.agents import agents_bp
from routes.crewai_routes import crewai_bp

# Initialize analysis services
init_analysis_services(supabase_service, gemini_service)

# Register blueprints
app.register_blueprint(upload_bp, url_prefix='/api/upload')
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(agents_bp, url_prefix='/api/agents')
app.register_blueprint(crewai_bp, url_prefix='/api/crewai')

logger.info("All blueprints registered successfully")

# Basic health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server is running"""
    return jsonify({
        'status': 'healthy',
        'message': 'Multi-Agent BI Assistant Backend is running',
        'supabase_connected': supabase_client is not None,
        'gemini_connected': gemini_model is not None,
        'config': Config.get_config_summary()
    })

# Configuration endpoint
@app.route('/api/config', methods=['GET'])
def get_config():
    """Get basic configuration for frontend"""
    try:
        return jsonify({
            'status': 'success',
            'config': Config.get_config_summary(),
            'supabase_connected': supabase_client is not None,
            'gemini_connected': gemini_model is not None
        })
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Configuration status endpoint
@app.route('/api/config/status', methods=['GET'])
def config_status():
    """Get configuration status for debugging"""
    try:
        # Test Supabase connection if available
        supabase_status = False
        if supabase_service:
            supabase_status = SupabaseConfig.test_connection()
        
        # Test Gemini AI connection if available
        gemini_status = False
        gemini_response = None
        if gemini_service:
            gemini_status, gemini_response = GeminiConfig.test_connection()
        
        return jsonify({
            'status': 'success',
            'config': Config.get_config_summary(),
            'supabase_initialized': supabase_client is not None,
            'supabase_connection_test': supabase_status,
            'gemini_initialized': gemini_model is not None,
            'gemini_connection_test': gemini_status,
            'gemini_test_response': gemini_response[:100] + '...' if gemini_response and len(gemini_response) > 100 else gemini_response
        })
    except Exception as e:
        logger.error(f"Error getting config status: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# WebSocket connection handler
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('✅ Client connected')
    emit('connection_response', {'data': 'Connected to Multi-Agent BI Assistant'})
    return True  # Explicitly return True to accept the connection

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

# WebSocket session join handler
@socketio.on('join')
def handle_join(session_id):
    """Handle client joining a session"""
    print(f'Client joined session: {session_id}')
    emit('session_joined', {'session_id': session_id})

# CrewAI analysis handler
@socketio.on('start_crewai_analysis')
def handle_crewai_analysis(data):
    """Handle CrewAI multi-agent analysis request"""
    try:
        csv_data = data.get('csvData')
        query = data.get('query')
        session_id = data.get('sessionId')
        
        if not csv_data or not query or not session_id:
            emit('analysis_error', {'error': 'Missing required data for analysis'})
            return
        
        logger.info(f"Starting CrewAI analysis for session {session_id}")
        
        # Import CrewAI integration
        from crews.bi_crew import crewai_integration
        
        # Start analysis (this will emit updates via socketio)
        result = crewai_integration.start_crewai_analysis(csv_data, query, session_id, socketio)
        
        logger.info(f"CrewAI analysis completed for session {session_id}")
        
    except Exception as e:
        logger.error(f"CrewAI analysis error: {e}")
        emit('analysis_error', {'error': str(e)})

# Additional WebSocket event handlers for enhanced real-time functionality

@socketio.on('get_agent_status')
def handle_get_agent_status(data):
    """Handle request for current agent status"""
    try:
        session_id = data.get('session_id')
        if not session_id:
            emit('agent_status_error', {'error': 'Session ID required'})
            return
        
        # Get agent status from CrewAI integration
        from crews.bi_crew import crewai_integration
        session_status = crewai_integration.get_session_status(session_id)
        
        emit('agent_status_response', {
            'session_id': session_id,
            'status': session_status,
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        emit('agent_status_error', {'error': str(e)})

@socketio.on('subscribe_to_session')
def handle_subscribe_to_session(data):
    """Handle client subscription to session updates"""
    try:
        session_id = data.get('session_id')
        if not session_id:
            emit('subscription_error', {'error': 'Session ID required'})
            return
        
        # Join the session room for targeted updates
        from flask_socketio import join_room
        join_room(session_id)
        
        emit('subscription_confirmed', {
            'session_id': session_id,
            'message': f'Subscribed to updates for session {session_id}'
        })
        
        logger.info(f"Client subscribed to session: {session_id}")
        
    except Exception as e:
        logger.error(f"Error subscribing to session: {e}")
        emit('subscription_error', {'error': str(e)})

@socketio.on('unsubscribe_from_session')
def handle_unsubscribe_from_session(data):
    """Handle client unsubscription from session updates"""
    try:
        session_id = data.get('session_id')
        if not session_id:
            emit('unsubscription_error', {'error': 'Session ID required'})
            return
        
        # Leave the session room
        from flask_socketio import leave_room
        leave_room(session_id)
        
        emit('unsubscription_confirmed', {
            'session_id': session_id,
            'message': f'Unsubscribed from updates for session {session_id}'
        })
        
        logger.info(f"Client unsubscribed from session: {session_id}")
        
    except Exception as e:
        logger.error(f"Error unsubscribing from session: {e}")
        emit('unsubscription_error', {'error': str(e)})

@socketio.on('get_all_sessions')
def handle_get_all_sessions():
    """Handle request for all active sessions"""
    try:
        from crews.bi_crew import crewai_integration
        all_sessions = crewai_integration.get_all_sessions()
        
        emit('all_sessions_response', {
            'sessions': all_sessions,
            'count': len(all_sessions),
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Error getting all sessions: {e}")
        emit('all_sessions_error', {'error': str(e)})

@socketio.on('ping')
def handle_ping():
    """Handle ping for connection testing"""
    emit('pong', {'timestamp': time.time()})

@socketio.on('heartbeat')
def handle_heartbeat(data):
    """Handle heartbeat to keep connection alive during long analysis"""
    session_id = data.get('session_id')
    emit('heartbeat_response', {
        'session_id': session_id,
        'timestamp': time.time(),
        'status': 'alive'
    })

if __name__ == '__main__':
    # Get server configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f'Starting Multi-Agent BI Assistant server on {host}:{port}')
    logger.info(f'Debug mode: {debug}')
    logger.info(f'CORS origins: {cors_origins}')
    
    # Run the Flask-SocketIO server
    socketio.run(app, debug=debug, host=host, port=port)