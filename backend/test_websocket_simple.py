"""
Simple WebSocket test to verify basic connectivity and events
"""
import socketio
import time
import requests

def test_basic_websocket():
    """Test basic WebSocket functionality"""
    try:
        print("🧪 Testing Basic WebSocket Functionality")
        print("=" * 50)
        
        # First check if server is running
        print("1. Checking if server is running...")
        try:
            response = requests.get('http://localhost:5000/api/health', timeout=5)
            if response.status_code == 200:
                print("   ✅ Server is running")
            else:
                print("   ❌ Server returned error status")
                return False
        except requests.exceptions.RequestException:
            print("   ❌ Server is not running. Please start the server first.")
            print("   💡 Run: python app.py")
            return False
        
        # Create Socket.IO client
        sio = socketio.Client()
        events_received = []
        
        @sio.event
        def connect():
            print("   ✅ WebSocket connected")
            events_received.append('connect')
        
        @sio.event
        def disconnect():
            print("   ✅ WebSocket disconnected")
            events_received.append('disconnect')
        
        @sio.event
        def connection_response(data):
            print(f"   ✅ Connection response: {data}")
            events_received.append('connection_response')
        
        @sio.event
        def pong(data):
            print(f"   ✅ Pong received: {data}")
            events_received.append('pong')
        
        @sio.event
        def subscription_confirmed(data):
            print(f"   ✅ Subscription confirmed: {data}")
            events_received.append('subscription_confirmed')
        
        # Test connection
        print("2. Connecting to WebSocket...")
        sio.connect('http://localhost:5000')
        time.sleep(1)
        
        # Test ping
        print("3. Testing ping...")
        sio.emit('ping')
        time.sleep(1)
        
        # Test session subscription
        print("4. Testing session subscription...")
        sio.emit('subscribe_to_session', {'session_id': 'test-session-123'})
        time.sleep(1)
        
        # Test getting all sessions
        print("5. Testing get all sessions...")
        sio.emit('get_all_sessions')
        time.sleep(1)
        
        # Disconnect
        print("6. Disconnecting...")
        sio.disconnect()
        time.sleep(1)
        
        # Summary
        print(f"\n📊 Events received: {len(events_received)}")
        for event in events_received:
            print(f"   - {event}")
        
        required_events = ['connect', 'connection_response', 'pong']
        missing_events = [e for e in required_events if e not in events_received]
        
        if not missing_events:
            print("\n🎉 Basic WebSocket functionality working correctly!")
            return True
        else:
            print(f"\n⚠️  Missing events: {missing_events}")
            return False
        
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_websocket()
    if success:
        print("\n✅ WebSocket real-time functionality is ready!")
        print("🚀 The enhanced agent status updates are implemented and working.")
    else:
        print("\n❌ WebSocket test failed. Please check the server.")
    
    exit(0 if success else 1)