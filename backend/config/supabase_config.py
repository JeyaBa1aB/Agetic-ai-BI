"""
Supabase configuration and initialization for Multi-Agent BI Assistant
"""
import os
import logging
from supabase import create_client, Client
from .settings import Config

logger = logging.getLogger(__name__)

class SupabaseConfig:
    """Supabase configuration and connection management"""
    
    _client = None
    _is_configured = False
    
    @classmethod
    def init_supabase(cls):
        """Initialize Supabase client"""
        try:
            # Get configuration
            supabase_url = Config.SUPABASE_URL
            supabase_key = Config.SUPABASE_KEY
            
            if not supabase_url or not supabase_key:
                raise ValueError("Supabase configuration missing. Please set SUPABASE_URL and SUPABASE_KEY")
            
            if supabase_url == 'your_supabase_project_url_here' or supabase_key == 'your_supabase_anon_key_here':
                raise ValueError("Please configure actual Supabase credentials in .env file")
            
            # Initialize Supabase client
            cls._client = create_client(supabase_url, supabase_key)
            cls._is_configured = True
            
            logger.info("Supabase client initialized successfully")
            return cls._client
            
        except Exception as e:
            logger.error(f"Supabase initialization error: {e}")
            cls._is_configured = False
            raise
    
    @classmethod
    def get_client(cls) -> Client:
        """Get Supabase client instance"""
        if cls._client is None or not cls._is_configured:
            cls.init_supabase()
        return cls._client
    
    @classmethod
    def test_connection(cls):
        """Test Supabase connection"""
        try:
            client = cls.get_client()
            
            # Try to perform a simple query to test connection
            # We'll create tables if they don't exist
            result = client.table('analysis_sessions').select('*').limit(1).execute()
            
            logger.info("Supabase connection test successful")
            return True
                
        except Exception as e:
            logger.error(f"Supabase connection test failed: {e}")
            return False


class SupabaseService:
    """Service class for Supabase operations"""
    
    def __init__(self):
        self.client = SupabaseConfig.get_client()
        self._ensure_tables_exist()
    
    def _ensure_tables_exist(self):
        """Ensure required tables exist in Supabase"""
        try:
            # Create analysis_sessions table if it doesn't exist
            self.client.table('analysis_sessions').select('id').limit(1).execute()
        except Exception:
            logger.info("Creating analysis_sessions table...")
            # Table doesn't exist, but we can't create it via the client
            # Tables should be created via Supabase dashboard or SQL
            pass
        
        try:
            # Create agent_results table if it doesn't exist
            self.client.table('agent_results').select('id').limit(1).execute()
        except Exception:
            logger.info("Creating agent_results table...")
            # Table doesn't exist, but we can't create it via the client
            pass
    
    def save_analysis_session(self, session_id, data):
        """Save analysis session to Supabase"""
        try:
            session_data = {
                'session_id': session_id,
                'query': data.get('query', ''),
                'csv_data': data.get('csv_data', ''),
                'status': data.get('status', 'initialized'),
                'user_id': data.get('user_id', 'anonymous'),
                'metadata': data.get('metadata', {}),
                'agents_status': data.get('agents_status', {}),
                'results': data.get('results', {}),
                # created_at and updated_at will be set automatically by the database
            }
            
            # Use upsert to handle both insert and update
            result = self.client.table('analysis_sessions').upsert(session_data).execute()
            
            logger.info(f"Analysis session saved: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving analysis session {session_id}: {e}")
            return False
    
    def update_analysis_session(self, session_id, updates):
        """Update analysis session in Supabase"""
        try:
            update_data = {
                **updates
                # updated_at will be set automatically by the database trigger
            }
            
            result = self.client.table('analysis_sessions').update(update_data).eq('session_id', session_id).execute()
            
            logger.info(f"Analysis session updated: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating analysis session {session_id}: {e}")
            return False
    
    def get_analysis_session(self, session_id):
        """Retrieve analysis session from Supabase"""
        try:
            result = self.client.table('analysis_sessions').select('*').eq('session_id', session_id).execute()
            
            if result.data and len(result.data) > 0:
                logger.info(f"Analysis session retrieved: {session_id}")
                return result.data[0]
            else:
                logger.warning(f"Analysis session not found: {session_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving analysis session {session_id}: {e}")
            return None
    
    def save_agent_result(self, session_id, agent_id, result):
        """Save individual agent result"""
        try:
            agent_data = {
                'session_id': session_id,
                'agent_id': agent_id,
                'result': result
                # created_at will be set automatically by the database
            }
            
            result = self.client.table('agent_results').insert(agent_data).execute()
            
            if result.data and len(result.data) > 0:
                logger.info(f"Agent result saved: {agent_id} for session {session_id}")
                return result.data[0]['id']
            else:
                logger.error(f"Failed to save agent result for {agent_id}")
                return None
            
        except Exception as e:
            logger.error(f"Error saving agent result for {agent_id} in session {session_id}: {e}")
            return None
    
    def get_agent_results(self, session_id):
        """Get all agent results for a session"""
        try:
            result = self.client.table('agent_results').select('*').eq('session_id', session_id).order('created_at').execute()
            
            if result.data:
                logger.info(f"Retrieved {len(result.data)} agent results for session {session_id}")
                return result.data
            else:
                return []
            
        except Exception as e:
            logger.error(f"Error retrieving agent results for session {session_id}: {e}")
            return []
    
    def get_recent_sessions(self, limit=10):
        """Get recent analysis sessions"""
        try:
            result = self.client.table('analysis_sessions').select('*').order('created_at', desc=True).limit(limit).execute()
            
            if result.data:
                logger.info(f"Retrieved {len(result.data)} recent sessions")
                return result.data
            else:
                return []
            
        except Exception as e:
            logger.error(f"Error retrieving recent sessions: {e}")
            return []
    
    def delete_session(self, session_id):
        """Delete analysis session and related data"""
        try:
            # Delete related agent results first
            self.client.table('agent_results').delete().eq('session_id', session_id).execute()
            
            # Delete main session
            result = self.client.table('analysis_sessions').delete().eq('session_id', session_id).execute()
            
            logger.info(f"Session deleted: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            return False


# Initialize Supabase on module import (optional)
def initialize_supabase():
    """Initialize Supabase configuration"""
    try:
        SupabaseConfig.init_supabase()
        logger.info("Supabase configuration module loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {e}")
        return False