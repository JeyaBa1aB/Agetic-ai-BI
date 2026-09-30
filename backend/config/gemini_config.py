"""
Gemini AI configuration and initialization for Multi-Agent BI Assistant
"""
import os
import logging
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from .settings import Config

logger = logging.getLogger(__name__)

class GeminiConfig:
    """Gemini AI configuration and connection management"""
    
    _client = None
    _model = None
    _is_configured = False
    
    # Default model configuration
    DEFAULT_MODEL = "gemini-2.5-flash"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_OUTPUT_TOKENS = 2048
    DEFAULT_TOP_P = 0.8
    DEFAULT_TOP_K = 40
    
    @classmethod
    def init_gemini(cls):
        """Initialize Gemini AI client"""
        try:
            # Get API key from configuration
            api_key = Config.GEMINI_API_KEY
            
            if not api_key or api_key == 'your_gemini_api_key_here':
                raise ValueError("Gemini API key not configured. Please set GEMINI_API_KEY environment variable")
            
            # Configure Gemini AI
            genai.configure(api_key=api_key)
            
            # Initialize the model
            cls._model = genai.GenerativeModel(
                model_name=cls.DEFAULT_MODEL,
                generation_config=genai.types.GenerationConfig(
                    temperature=cls.DEFAULT_TEMPERATURE,
                    max_output_tokens=cls.DEFAULT_MAX_OUTPUT_TOKENS,
                    top_p=cls.DEFAULT_TOP_P,
                    top_k=cls.DEFAULT_TOP_K,
                ),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }
            )
            
            cls._is_configured = True
            logger.info(f"Gemini AI initialized successfully with model: {cls.DEFAULT_MODEL}")
            
            return cls._model
            
        except Exception as e:
            logger.error(f"Gemini AI initialization error: {e}")
            cls._is_configured = False
            raise
    
    @classmethod
    def get_model(cls):
        """Get Gemini model instance"""
        if not cls._is_configured or cls._model is None:
            cls.init_gemini()
        return cls._model
    
    @classmethod
    def test_connection(cls):
        """Test Gemini AI connection"""
        try:
            model = cls.get_model()
            
            # Test with a simple prompt
            test_prompt = "Hello! Please respond with 'Gemini AI is working correctly.'"
            response = model.generate_content(test_prompt)
            
            if response and response.text:
                logger.info("Gemini AI connection test successful")
                return True, response.text
            else:
                logger.error("Gemini AI connection test failed: no response")
                return False, "No response received"
                
        except Exception as e:
            logger.error(f"Gemini AI connection test failed: {e}")
            return False, str(e)
    
    @classmethod
    def get_available_models(cls):
        """Get list of available Gemini models"""
        try:
            if not cls._is_configured:
                cls.init_gemini()
            
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    models.append({
                        'name': model.name,
                        'display_name': model.display_name,
                        'description': model.description,
                        'input_token_limit': model.input_token_limit,
                        'output_token_limit': model.output_token_limit
                    })
            
            logger.info(f"Retrieved {len(models)} available Gemini models")
            return models
            
        except Exception as e:
            logger.error(f"Error retrieving available models: {e}")
            return []
    
    @classmethod
    def create_custom_model(cls, model_name=None, temperature=None, max_tokens=None):
        """Create a custom configured model instance"""
        try:
            if not cls._is_configured:
                cls.init_gemini()
            
            # Use provided values or defaults
            model_name = model_name or cls.DEFAULT_MODEL
            temperature = temperature if temperature is not None else cls.DEFAULT_TEMPERATURE
            max_tokens = max_tokens or cls.DEFAULT_MAX_OUTPUT_TOKENS
            
            custom_model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    top_p=cls.DEFAULT_TOP_P,
                    top_k=cls.DEFAULT_TOP_K,
                ),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }
            )
            
            logger.info(f"Custom Gemini model created: {model_name} (temp: {temperature}, max_tokens: {max_tokens})")
            return custom_model
            
        except Exception as e:
            logger.error(f"Error creating custom model: {e}")
            return None


class GeminiService:
    """Service class for Gemini AI operations"""
    
    def __init__(self, model=None, temperature=None, max_tokens=None):
        """Initialize Gemini service with optional custom configuration"""
        if model:
            self.model = model
        elif temperature is not None or max_tokens is not None:
            self.model = GeminiConfig.create_custom_model(
                temperature=temperature, 
                max_tokens=max_tokens
            )
        else:
            self.model = GeminiConfig.get_model()
    
    def generate_content(self, prompt, **kwargs):
        """Generate content using Gemini AI"""
        try:
            if not self.model:
                raise ValueError("Gemini model not initialized")
            
            response = self.model.generate_content(prompt, **kwargs)
            
            if response and response.text:
                logger.debug(f"Generated content for prompt (length: {len(prompt)})")
                return {
                    'success': True,
                    'content': response.text,
                    'usage': {
                        'prompt_tokens': response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
                        'completion_tokens': response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None,
                        'total_tokens': response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
                    }
                }
            else:
                logger.warning("Gemini AI returned empty response")
                return {
                    'success': False,
                    'error': 'Empty response from Gemini AI',
                    'content': None
                }
                
        except Exception as e:
            logger.error(f"Error generating content with Gemini AI: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    def generate_structured_content(self, prompt, system_instruction=None):
        """Generate structured content with system instruction"""
        try:
            if system_instruction:
                full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"
            else:
                full_prompt = prompt
            
            return self.generate_content(full_prompt)
            
        except Exception as e:
            logger.error(f"Error generating structured content: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    def chat_session(self, history=None):
        """Create a chat session for multi-turn conversations"""
        try:
            if not self.model:
                raise ValueError("Gemini model not initialized")
            
            chat = self.model.start_chat(history=history or [])
            logger.info("Gemini chat session created")
            return chat
            
        except Exception as e:
            logger.error(f"Error creating chat session: {e}")
            return None
    
    def count_tokens(self, text):
        """Count tokens in text"""
        try:
            if not self.model:
                raise ValueError("Gemini model not initialized")
            
            token_count = self.model.count_tokens(text)
            return token_count.total_tokens
            
        except Exception as e:
            logger.error(f"Error counting tokens: {e}")
            return None


# Agent-specific Gemini configurations
class AgentGeminiConfig:
    """Specialized Gemini configurations for different agent types"""
    
    # Configuration for different agent types
    AGENT_CONFIGS = {
        'master_orchestrator': {
            'temperature': 0.3,  # Lower temperature for more focused coordination
            'max_tokens': 1024,
            'system_instruction': "You are a master orchestrator coordinating multiple AI agents for business intelligence analysis."
        },
        'data_analyst': {
            'temperature': 0.2,  # Very low temperature for precise data analysis
            'max_tokens': 2048,
            'system_instruction': "You are a senior data analyst specializing in statistical analysis and data quality assessment."
        },
        'data_processor': {
            'temperature': 0.1,  # Minimal creativity for data processing
            'max_tokens': 1024,
            'system_instruction': "You are a data processing specialist focused on ETL processes and data cleaning."
        },
        'pattern_detector': {
            'temperature': 0.4,  # Moderate temperature for pattern recognition
            'max_tokens': 1536,
            'system_instruction': "You are a pattern detection specialist identifying trends and anomalies in data."
        },
        'chart_specialist': {
            'temperature': 0.5,  # Higher temperature for creative visualization ideas
            'max_tokens': 1024,
            'system_instruction': "You are a data visualization expert creating optimal charts and graphs."
        },
        'dashboard_designer': {
            'temperature': 0.6,  # Creative temperature for dashboard design
            'max_tokens': 1536,
            'system_instruction': "You are a dashboard design specialist creating comprehensive layouts."
        },
        'business_strategist': {
            'temperature': 0.7,  # Higher temperature for strategic thinking
            'max_tokens': 2048,
            'system_instruction': "You are a business strategy consultant providing strategic insights and recommendations."
        },
        'market_analyst': {
            'temperature': 0.5,  # Balanced temperature for market analysis
            'max_tokens': 1536,
            'system_instruction': "You are a market analysis specialist focusing on competitive landscape and trends."
        },
        'executive_reporter': {
            'temperature': 0.4,  # Moderate temperature for clear reporting
            'max_tokens': 2048,
            'system_instruction': "You are an executive reporting specialist creating clear, actionable business reports."
        }
    }
    
    @classmethod
    def get_agent_service(cls, agent_type):
        """Get a Gemini service configured for specific agent type"""
        config = cls.AGENT_CONFIGS.get(agent_type, {})
        
        if not config:
            logger.warning(f"No specific configuration found for agent type: {agent_type}")
            return GeminiService()
        
        model = GeminiConfig.create_custom_model(
            temperature=config.get('temperature'),
            max_tokens=config.get('max_tokens')
        )
        
        service = GeminiService(model=model)
        logger.info(f"Created specialized Gemini service for agent: {agent_type}")
        
        return service, config.get('system_instruction')


# Initialize Gemini on module import (optional)
def initialize_gemini():
    """Initialize Gemini configuration"""
    try:
        GeminiConfig.init_gemini()
        logger.info("Gemini configuration module loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        return False