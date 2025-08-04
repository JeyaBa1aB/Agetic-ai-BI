#!/usr/bin/env python3
"""
Basic Socket.IO server test
Minimal server to test Socket.IO functionality
"""

from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

# Configure CORS
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:5174'])

# Initialize SocketIO
socketio = SocketIO(app, 
                   cors_allowed_origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:5174'],
                   logger=True,
                   engineio_logger=True)

@app.route('/test')
def test():
    return {'status': 'ok', 'message': 'Basic test server is running'}

@socketio.on('connect')
def handle_connect():
    print('✅ Client connected to basic server')
    emit('connection_response', {'message': 'Connected to basic test server'})
    return True

@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected from basic server')

@socketio.on('ping')
def handle_ping():
    print('🏓 Ping received by basic server')
    emit('pong', {'timestamp': time.time(), 'message': 'Pong from basic server'})

if __name__ == '__main__':
    print('🚀 Starting basic Socket.IO test server on http://localhost:5001')
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)