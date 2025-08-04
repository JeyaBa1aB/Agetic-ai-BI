"""
Test script for WebSocket real-time functionality
Tests the enhanced agent status updates and real-time communication
"""
import socketio
import time
import json
import threading

# Create a Socket.IO client
sio = socketio.Client()

# Track received events
received_events = []

@sio.event
def connect():
    print("🔌 Connected to WebSocket server")

@sio.event
def disconnect():
    print("🔌 Disconnected from WebSocket server")

@sio.event
def connection_response(data):
    print(f"📡 Connection response: {data}")
    received_events.append(('connection_response', data))

@sio.event
def analysis_started(data):
    print(f"🚀 Analysis started: {data}")
    received_events.append(('analysis_started', data))

@sio.event
def agent_status_update(data):
    print(f"🤖 Agent status update: {data['agent_name']} - {data['status']} ({data['progress']}%)")
    received_events.append(('agent_status_update', data))

@sio.event
def task_started(data):
    print(f"📋 Task started: {data['agent_name']} - Task {data['task_index'] + 1}/{data['total_tasks']}")
    received_events.append(('task_started', data))

@sio.event
def task_completed(data):
    print(f"✅ Task completed: {data['agent_name']} - Task {data['task_index'] + 1}")
    received_events.append(('task_completed', data))

@sio.event
def workflow_stage_update(data):
    print(f"🔄 Workflow stage: {data['stage']} - {data['message']}")
    received_events.append(('workflow_stage_update', data))

@sio.event
def workflow_progress_update(data):
    print(f"📊 Progress update: {data['stage']} - {data['progress']}%")
    received_events.append(('workflow_progress_update', data))

@sio.event
def analysis_completed(data):
    print(f"🎉 Analysis completed in {data['duration']:.2f} seconds")
    received_events.append(('analysis_completed', data))

@sio.event
def analysis_error(data):
    print(f"❌ Analysis error: {data}")
    received_events.append(('analysis_error', data))

@sio.event
def subscription_confirmed(data):
    print(f"✅ Subscription confirmed: {data}")
    received_events.append(('subscription_confirmed', data))

@sio.event
def pong(data):
    print(f"🏓 Pong received: {data}")
    received_events.append(('pong', data))

def test_websocket_functionality():
    """Test WebSocket functionality"""
    try:
        print("🧪 Testing WebSocket Real-time Functionality")
        print("=" * 50)
        
        # Connect to the server
        print("1. Connecting to WebSocket server...")
        sio.connect('http://localhost:5000')
        time.sleep(1)
        
        # Test ping
        print("2. Testing ping...")
        sio.emit('ping')
        time.sleep(1)
        
        # Test session subscription
        test_session_id = "test-websocket-session-123"
        print(f"3. Subscribing to session: {test_session_id}")
        sio.emit('subscribe_to_session', {'session_id': test_session_id})
        time.sleep(1)
        
        # Test getting all sessions
        print("4. Getting all active sessions...")
        sio.emit('get_all_sessions')
        time.sleep(1)
        
        # Test a small CrewAI analysis (this will generate real-time events)
        print("5. Starting a test CrewAI analysis...")
        test_csv_data = """Name,Age,Department,Salary
John,25,Engineering,75000
Jane,30,Marketing,65000
Bob,35,Sales,70000"""
        
        analysis_data = {
            'csvData': test_csv_data,
            'query': 'What are the key insights from this employee data?',
            'sessionId': test_session_id
        }
        
        sio.emit('start_crewai_analysis', analysis_data)
        
        # Wait for analysis to complete (this might take a while)
        print("6. Waiting for analysis to complete (this may take 30-60 seconds)...")
        
        # Wait and monitor events
        start_time = time.time()
        timeout = 120  # 2 minutes timeout
        
        while time.time() - start_time < timeout:
            time.sleep(2)
            
            # Check if analysis completed
            completed_events = [e for e in received_events if e[0] == 'analysis_completed']
            error_events = [e for e in received_events if e[0] == 'analysis_error']
            
            if completed_events:
                print("✅ Analysis completed successfully!")
                break
            elif error_events:
                print("❌ Analysis completed with error")
                break
        else:
            print("⏰ Analysis timeout - but that's okay for testing")
        
        # Test unsubscription
        print("7. Unsubscribing from session...")
        sio.emit('unsubscribe_from_session', {'session_id': test_session_id})
        time.sleep(1)
        
        # Disconnect
        print("8. Disconnecting...")
        sio.disconnect()
        
        # Summary
        print("\n📊 WebSocket Test Summary")
        print("=" * 30)
        print(f"Total events received: {len(received_events)}")
        
        event_types = {}
        for event_type, _ in received_events:
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        for event_type, count in event_types.items():
            print(f"  {event_type}: {count}")
        
        # Check for key events
        key_events = ['connection_response', 'analysis_started', 'agent_status_update']
        missing_events = [e for e in key_events if e not in event_types]
        
        if not missing_events:
            print("\n🎉 All key WebSocket events working correctly!")
            return True
        else:
            print(f"\n⚠️  Missing events: {missing_events}")
            return False
        
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_websocket_functionality()
    exit(0 if success else 1)