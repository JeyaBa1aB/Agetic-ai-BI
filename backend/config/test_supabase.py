"""
Test script for Supabase configuration
Run this to verify Supabase setup is working correctly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.supabase_config import SupabaseConfig, SupabaseService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_supabase_setup():
    """Test Supabase configuration and basic operations"""
    
    print("🔥 Testing Supabase Configuration...")
    print("=" * 50)
    
    try:
        # Test 1: Initialize Supabase
        print("1. Initializing Supabase...")
        client = SupabaseConfig.init_supabase()
        if client:
            print("   ✅ Supabase initialized successfully")
        else:
            print("   ❌ Supabase initialization failed")
            return False
        
        # Test 2: Test connection
        print("2. Testing Supabase connection...")
        if SupabaseConfig.test_connection():
            print("   ✅ Supabase connection test passed")
        else:
            print("   ❌ Supabase connection test failed")
            return False
        
        # Test 3: Test SupabaseService operations
        print("3. Testing SupabaseService operations...")
        service = SupabaseService()
        
        # Test session save
        test_session_id = "test_session_123"
        test_data = {
            "query": "Test query",
            "status": "testing",
            "user_id": "test_user"
        }
        
        if service.save_analysis_session(test_session_id, test_data):
            print("   ✅ Session save test passed")
        else:
            print("   ❌ Session save test failed")
            return False
        
        # Test session retrieval
        retrieved_data = service.get_analysis_session(test_session_id)
        if retrieved_data and retrieved_data.get('query') == 'Test query':
            print("   ✅ Session retrieval test passed")
        else:
            print("   ❌ Session retrieval test failed")
            return False
        
        # Test agent result save
        agent_result_id = service.save_agent_result(
            test_session_id, 
            "test_agent", 
            {"analysis": "test result"}
        )
        if agent_result_id:
            print("   ✅ Agent result save test passed")
        else:
            print("   ❌ Agent result save test failed")
            return False
        
        # Test agent results retrieval
        agent_results = service.get_agent_results(test_session_id)
        if agent_results and len(agent_results) > 0:
            print("   ✅ Agent results retrieval test passed")
        else:
            print("   ❌ Agent results retrieval test failed")
            return False
        
        # Cleanup test data
        print("4. Cleaning up test data...")
        if service.delete_session(test_session_id):
            print("   ✅ Test data cleanup successful")
        else:
            print("   ❌ Test data cleanup failed")
        
        print("\n🎉 All Supabase tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Supabase test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_setup()
    sys.exit(0 if success else 1)