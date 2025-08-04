"""
Configuration settings for Multi-Agent BI Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    # Multi-Agent Configuration
    MAX_AGENTS = int(os.getenv('MAX_AGENTS', 9))
    AGENT_TIMEOUT = int(os.getenv('AGENT_TIMEOUT', 30))
    ANALYSIS_TIMEOUT = int(os.getenv('ANALYSIS_TIMEOUT', 300))
    
    # Data Processing Configuration
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'csv').split(',')
    CSV_ENCODING = os.getenv('CSV_ENCODING', 'utf-8')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        required_vars = [
            'SECRET_KEY',
            'GEMINI_API_KEY',
            'SUPABASE_URL',
            'SUPABASE_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var) or getattr(cls, var) in ['your_gemini_api_key_here', 'your_supabase_project_url_here', 'your_supabase_anon_key_here']:
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing or invalid required environment variables: {', '.join(missing_vars)}")
        
        return True
    
    @classmethod
    def get_config_summary(cls):
        """Get a summary of current configuration (without sensitive data)"""
        return {
            'flask_env': cls.FLASK_ENV,
            'debug': cls.FLASK_DEBUG,
            'host': cls.HOST,
            'port': cls.PORT,
            'cors_origins': cls.CORS_ORIGINS,
            'max_agents': cls.MAX_AGENTS,
            'agent_timeout': cls.AGENT_TIMEOUT,
            'analysis_timeout': cls.ANALYSIS_TIMEOUT,
            'max_file_size': cls.MAX_FILE_SIZE,
            'allowed_extensions': cls.ALLOWED_EXTENSIONS,
            'csv_encoding': cls.CSV_ENCODING,
            'log_level': cls.LOG_LEVEL,
            'gemini_api_configured': bool(cls.GEMINI_API_KEY and cls.GEMINI_API_KEY != 'your_gemini_api_key_here'),
            'supabase_configured': bool(cls.SUPABASE_URL and cls.SUPABASE_KEY and 
                                      cls.SUPABASE_URL != 'your_supabase_project_url_here' and 
                                      cls.SUPABASE_KEY != 'your_supabase_anon_key_here')
        }