#!/usr/bin/env python3
"""
Basic Socket.IO client test
Tests connection to the basic server
"""

import socketio
import time

def test_basic_connection():
    """Test connection to basic server"""
    
    sio = socketio.Client()
    
    @sio.event
    def connect():
        print("✅ Connected to basic server")
        
    @sio.event
    def disconnect():
        print("❌ Disconnected from basic server")
        
    @sio.event
    def connection_response(data):
        print(f"📡 Connection response: {data}")
        
    @sio.event
    def pong(data):
        print(f"🏓 Pong received: {data}")
        
    try:
        print("🔌 Connecting to basic server on port 5001...")
        sio.connect('http://localhost:5001', transports=['polling'])
        
        if sio.connected:
            print("✅ Connected successfully!")
            
            time.sleep(1)
            
            print("🏓 Sending ping...")
            sio.emit('ping')
            
            time.sleep(2)
            
            sio.disconnect()
            print("✅ Basic test completed successfully")
            return True
        else:
            print("❌ Failed to connect to basic server")
            return False
            
    except Exception as e:
        print(f"❌ Basic connection test failed: {e}")
        return False

if __name__ == '__main__':
    success = test_basic_connection()
    if success:
        print("\n🎉 Basic Socket.IO functionality is working!")
        print("The issue is likely with the main server configuration.")
    else:
        print("\n❌ Basic Socket.IO functionality is not working.")
        print("There may be a deeper issue with the Socket.IO setup.")