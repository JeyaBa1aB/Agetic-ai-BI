"""
Test script for Flask server startup and connectivity
Tests all endpoints and basic functionality
"""
import requests
import json
import time
import sys
import os
from io import StringIO

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_CSV_CONTENT = """Name,Age,Department,Salary
John Doe,30,Engineering,75000
Jane Smith,25,Marketing,65000
Bob Johnson,35,Sales,70000
Alice Brown,28,Engineering,80000
Charlie Wilson,32,Marketing,68000"""

def test_server_health():
    """Test server health endpoint"""
    print("🏥 Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Server is healthy")
            print(f"   📊 Supabase connected: {data.get('supabase_connected', False)}")
            print(f"   🤖 Gemini connected: {data.get('gemini_connected', False)}")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Health check failed: {e}")
        return False

def test_config_status():
    """Test configuration status endpoint"""
    print("⚙️  Testing configuration status...")
    try:
        response = requests.get(f"{BASE_URL}/api/config/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Configuration status retrieved")
            print(f"   🔥 Supabase initialized: {data.get('supabase_initialized', False)}")
            print(f"   🤖 Gemini initialized: {data.get('gemini_initialized', False)}")
            if data.get('supabase_connection_test'):
                print("   ✅ Supabase connection test passed")
            if data.get('gemini_connection_test'):
                print("   ✅ Gemini connection test passed")
            return True
        else:
            print(f"   ❌ Config status failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Config status failed: {e}")
        return False

def test_upload_endpoints():
    """Test file upload endpoints"""
    print("📁 Testing upload endpoints...")
    
    # Test upload info
    try:
        response = requests.get(f"{BASE_URL}/api/upload/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Upload info retrieved")
            print(f"   📏 Max file size: {data.get('max_file_size_mb', 0):.1f}MB")
            print(f"   📋 Allowed extensions: {data.get('allowed_extensions', [])}")
        else:
            print(f"   ❌ Upload info failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Upload info failed: {e}")
        return False
    
    # Test CSV validation
    try:
        response = requests.post(
            f"{BASE_URL}/api/upload/validate",
            json={"csv_content": TEST_CSV_CONTENT},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print("   ✅ CSV validation passed")
            print(f"   📊 Rows: {data.get('validation_info', {}).get('rows', 0)}")
            print(f"   📋 Columns: {data.get('validation_info', {}).get('columns', 0)}")
            return True
        else:
            print(f"   ❌ CSV validation failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ CSV validation failed: {e}")
        return False

def test_agents_endpoints():
    """Test agent endpoints"""
    print("🤖 Testing agent endpoints...")
    
    # Test list agents
    try:
        response = requests.get(f"{BASE_URL}/api/agents/list", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Agents list retrieved")
            print(f"   👥 Total agents: {data.get('total_agents', 0)}")
            
            # Test specific agent info
            if data.get('agents'):
                first_agent = data['agents'][0]
                agent_id = first_agent['id']
                
                response = requests.get(f"{BASE_URL}/api/agents/info/{agent_id}", timeout=10)
                if response.status_code == 200:
                    agent_data = response.json()
                    print(f"   ✅ Agent info retrieved: {agent_data['agent']['name']}")
                else:
                    print(f"   ❌ Agent info failed: {response.status_code}")
                    return False
            
            return True
        else:
            print(f"   ❌ Agents list failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Agents endpoints failed: {e}")
        return False

def test_agents_status():
    """Test agent status endpoint"""
    print("📊 Testing agent status...")
    try:
        response = requests.get(f"{BASE_URL}/api/agents/status", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Agent status retrieved")
            summary = data.get('summary', {})
            print(f"   👥 Available agents: {summary.get('available', 0)}")
            print(f"   ❌ Error agents: {summary.get('errors', 0)}")
            print(f"   🏥 Overall status: {summary.get('overall_status', 'unknown')}")
            return True
        else:
            print(f"   ❌ Agent status failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Agent status failed: {e}")
        return False

def test_analysis_endpoints():
    """Test analysis endpoints"""
    print("🔍 Testing analysis endpoints...")
    
    # Test start analysis
    try:
        analysis_data = {
            "query": "What are the key insights from this employee data?",
            "csv_data": TEST_CSV_CONTENT,
            "user_id": "test_user"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/analysis/start",
            json=analysis_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print("   ✅ Analysis session started")
            print(f"   🆔 Session ID: {session_id}")
            
            # Test get session status (add small delay to ensure database consistency)
            if session_id:
                import time
                time.sleep(0.5)  # Small delay for database consistency
                response = requests.get(f"{BASE_URL}/api/analysis/status/{session_id}", timeout=10)
                if response.status_code == 200:
                    status_data = response.json()
                    print(f"   ✅ Session status: {status_data.get('status', 'unknown')}")
                else:
                    print(f"   ❌ Session status failed: {response.status_code}")
                    return False
            
            return True
        else:
            print(f"   ❌ Analysis start failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Analysis endpoints failed: {e}")
        return False

def test_analysis_ai():
    """Test AI analysis functionality"""
    print("🧠 Testing AI analysis...")
    try:
        test_data = {
            "query": "Explain what business intelligence means in one sentence."
        }
        
        response = requests.post(
            f"{BASE_URL}/api/analysis/test",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ AI analysis test passed")
            print(f"   🤖 Response: {data.get('response', '')[:100]}...")
            if data.get('usage'):
                print(f"   📊 Token usage: {data['usage']}")
            return True
        else:
            print(f"   ❌ AI analysis test failed: {response.status_code}")
            if response.status_code == 503:
                print("   ⚠️  Gemini AI service not available")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ AI analysis test failed: {e}")
        return False

def test_agent_ai():
    """Test individual agent AI functionality"""
    print("🎯 Testing individual agent AI...")
    try:
        # Test data analyst agent
        test_data = {
            "query": "Analyze this sample data and provide insights."
        }
        
        response = requests.post(
            f"{BASE_URL}/api/agents/test/data_analyst",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Agent AI test passed")
            print(f"   🤖 Agent: {data.get('agent_name', 'Unknown')}")
            print(f"   💬 Response: {data.get('response', '')[:100]}...")
            return True
        else:
            print(f"   ❌ Agent AI test failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Agent AI test failed: {e}")
        return False

def run_all_tests():
    """Run all server tests"""
    print("🚀 Starting Flask Server Tests")
    print("=" * 50)
    
    tests = [
        ("Server Health", test_server_health),
        ("Configuration Status", test_config_status),
        ("Upload Endpoints", test_upload_endpoints),
        ("Agent Endpoints", test_agents_endpoints),
        ("Agent Status", test_agents_status),
        ("Analysis Endpoints", test_analysis_endpoints),
        ("AI Analysis", test_analysis_ai),
        ("Agent AI", test_agent_ai)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            if test_func():
                passed += 1
                print(f"   ✅ {test_name} PASSED")
            else:
                print(f"   ❌ {test_name} FAILED")
        except Exception as e:
            print(f"   ❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Server is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the logs above.")
        return False

if __name__ == "__main__":
    print("⏳ Waiting for server to start...")
    time.sleep(2)  # Give server time to start
    
    success = run_all_tests()
    sys.exit(0 if success else 1)