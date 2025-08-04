#!/usr/bin/env python3
"""
Simple WebSocket connection test
Tests the Socket.IO connection to verify it's working properly
"""

import socketio
import time
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

def test_websocket_connection():
    """Test WebSocket connection to the backend server"""
    
    # Create a Socket.IO client with debug logging
    sio = socketio.Client(logger=True, engineio_logger=True)
    
    # Connection event handlers
    @sio.event
    def connect():
        print("✅ Connected to WebSocket server")
        
    @sio.event
    def disconnect():
        print("❌ Disconnected from WebSocket server")
        
    @sio.event
    def connect_error(data):
        print(f"❌ Connection error: {data}")
        
    @sio.event
    def connection_response(data):
        print(f"📡 Connection response: {data}")
        
    @sio.event
    def pong(data):
        print(f"🏓 Pong received: {data}")
        
    try:
        print("🔌 Attempting to connect to WebSocket server...")
        print("🔍 Testing different transport methods...")
        
        # Try polling first (more reliable)
        print("📡 Trying polling transport...")
        sio.connect('http://localhost:5000', transports=['polling'])
        
        if sio.connected:
            print("✅ Connected successfully with polling transport")
            
            # Wait a moment for connection to establish
            time.sleep(1)
            
            # Send a ping
            print("🏓 Sending ping...")
            sio.emit('ping')
            
            # Wait for response
            time.sleep(2)
            
            # Disconnect
            sio.disconnect()
            print("✅ Test completed successfully")
        else:
            print("❌ Failed to connect with polling transport")
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        
if __name__ == '__main__':
    test_websocket_connection()