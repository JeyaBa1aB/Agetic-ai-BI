#!/usr/bin/env python3
"""
Test LiteLLM with Gemini integration
Verifies that LiteLLM can properly use the Gemini API
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_litellm_gemini():
    """Test LiteLLM with Gemini"""
    try:
        from litellm import completion
        
        # Get API key
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        google_api_key = os.getenv('GOOGLE_API_KEY')
        
        print(f"🔑 GEMINI_API_KEY: {'✅ Set' if gemini_api_key else '❌ Not set'}")
        print(f"🔑 GOOGLE_API_KEY: {'✅ Set' if google_api_key else '❌ Not set'}")
        
        if not google_api_key:
            print("❌ GOOGLE_API_KEY not found")
            return False
        
        # Test LiteLLM with Gemini
        print("🧪 Testing LiteLLM with Gemini...")
        
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": "Say hello in one word"}],
            max_tokens=10,
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        print(f"✅ LiteLLM test successful!")
        print(f"📝 Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ LiteLLM test failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Testing LiteLLM with Gemini integration...")
    success = test_litellm_gemini()
    
    if success:
        print("\n🎉 LiteLLM with Gemini is working correctly!")
        print("CrewAI should now be able to use LiteLLM without errors.")
    else:
        print("\n❌ LiteLLM with Gemini is not working.")
        print("CrewAI may still encounter LLM provider errors.")