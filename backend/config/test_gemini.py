"""
Test script for Gemini AI configuration
Run this to verify Gemini AI setup is working correctly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_config import GeminiConfig, GeminiService, AgentGeminiConfig
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gemini_setup():
    """Test Gemini AI configuration and basic operations"""
    
    print("🤖 Testing Gemini AI Configuration...")
    print("=" * 50)
    
    try:
        # Test 1: Initialize Gemini
        print("1. Initializing Gemini AI...")
        model = GeminiConfig.init_gemini()
        if model:
            print("   ✅ Gemini AI initialized successfully")
        else:
            print("   ❌ Gemini AI initialization failed")
            return False
        
        # Test 2: Test connection
        print("2. Testing Gemini AI connection...")
        success, response = GeminiConfig.test_connection()
        if success:
            print("   ✅ Gemini AI connection test passed")
            print(f"   📝 Response: {response[:100]}...")
        else:
            print("   ❌ Gemini AI connection test failed")
            print(f"   📝 Error: {response}")
            return False
        
        # Test 3: Test basic content generation
        print("3. Testing basic content generation...")
        service = GeminiService()
        result = service.generate_content("What is business intelligence? Provide a brief definition.")
        
        if result['success']:
            print("   ✅ Content generation test passed")
            print(f"   📝 Generated content: {result['content'][:150]}...")
            if result['usage']:
                print(f"   📊 Token usage: {result['usage']}")
        else:
            print("   ❌ Content generation test failed")
            print(f"   📝 Error: {result['error']}")
            return False
        
        # Test 4: Test structured content generation
        print("4. Testing structured content generation...")
        structured_result = service.generate_structured_content(
            "Analyze this data: Sales: 100, 150, 200",
            "You are a data analyst. Provide a brief analysis."
        )
        
        if structured_result['success']:
            print("   ✅ Structured content generation test passed")
            print(f"   📝 Structured content: {structured_result['content'][:150]}...")
        else:
            print("   ❌ Structured content generation test failed")
            print(f"   📝 Error: {structured_result['error']}")
            return False
        
        # Test 5: Test agent-specific configurations
        print("5. Testing agent-specific configurations...")
        agent_service, system_instruction = AgentGeminiConfig.get_agent_service('data_analyst')
        
        if agent_service and system_instruction:
            print("   ✅ Agent-specific configuration test passed")
            print(f"   📝 System instruction: {system_instruction[:100]}...")
            
            # Test agent-specific generation
            agent_result = agent_service.generate_content("Analyze the trend: 10, 15, 25, 40, 65")
            if agent_result['success']:
                print("   ✅ Agent-specific generation test passed")
                print(f"   📝 Agent analysis: {agent_result['content'][:150]}...")
            else:
                print("   ❌ Agent-specific generation test failed")
                return False
        else:
            print("   ❌ Agent-specific configuration test failed")
            return False
        
        # Test 6: Test available models
        print("6. Testing available models retrieval...")
        models = GeminiConfig.get_available_models()
        if models:
            print(f"   ✅ Retrieved {len(models)} available models")
            for model in models[:3]:  # Show first 3 models
                print(f"   📋 Model: {model['display_name']} - {model['description'][:50]}...")
        else:
            print("   ⚠️  No models retrieved (this might be normal)")
        
        # Test 7: Test token counting
        print("7. Testing token counting...")
        test_text = "This is a test sentence for token counting."
        token_count = service.count_tokens(test_text)
        if token_count is not None:
            print(f"   ✅ Token counting test passed: {token_count} tokens")
        else:
            print("   ❌ Token counting test failed")
            return False
        
        # Test 8: Test chat session creation
        print("8. Testing chat session creation...")
        chat = service.chat_session()
        if chat:
            print("   ✅ Chat session creation test passed")
        else:
            print("   ❌ Chat session creation test failed")
            return False
        
        print("\n🎉 All Gemini AI tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Gemini AI test failed with error: {e}")
        return False

def test_all_agent_types():
    """Test all agent type configurations"""
    print("\n🔧 Testing All Agent Type Configurations...")
    print("=" * 50)
    
    agent_types = list(AgentGeminiConfig.AGENT_CONFIGS.keys())
    
    for agent_type in agent_types:
        try:
            service, instruction = AgentGeminiConfig.get_agent_service(agent_type)
            if service and instruction:
                print(f"   ✅ {agent_type}: Configuration loaded")
            else:
                print(f"   ❌ {agent_type}: Configuration failed")
                return False
        except Exception as e:
            print(f"   ❌ {agent_type}: Error - {e}")
            return False
    
    print(f"\n✅ All {len(agent_types)} agent configurations tested successfully!")
    return True

if __name__ == "__main__":
    success = test_gemini_setup()
    if success:
        success = test_all_agent_types()
    
    sys.exit(0 if success else 1)