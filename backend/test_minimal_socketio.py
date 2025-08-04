#!/usr/bin/env python3
"""
Minimal Socket.IO server test
Tests if Socket.IO is working properly
"""

from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:5174'])

socketio = SocketIO(app, cors_allowed_origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:5174'])

@app.route('/test')
def test():
    return {'status': 'ok', 'message': 'Test server is running'}

@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')
    emit('connection_response', {'message': 'Connected to test server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')

@socketio.on('ping')
def handle_ping():
    print('🏓 Ping received')
    emit('pong', {'timestamp': 'test'})

if __name__ == '__main__':
    print('🚀 Starting minimal Socket.IO test server on http://localhost:5001')
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)