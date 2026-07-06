#!/usr/bin/env python3
"""
rag_server.py - Standalone RAG Server for MCI Chatbot
Runs your RAG system independently from Nanobot.
Can be called by Nanobot later via HTTP or MCP.
"""

import sys
import os
import json
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add current directory to path
CURRENT_DIR = Path(__file__).parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# ============================================================
# Import your RAG system
# ============================================================
try:
    from knowledge_tool import process_message
    from intent_recognizer import IntentRecognizer
    from safety_handler import SafetyHandler
    from caregiver_memory import CaregiverMemory
    print("✅ RAG system loaded successfully!")
except ImportError as e:
    print(f"❌ Error importing RAG: {e}")
    sys.exit(1)

# ============================================================
# Initialize Flask app
# ============================================================
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# ============================================================
# API Endpoints
# ============================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'MCI RAG Server',
        'version': '1.0.0'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Accepts: {"message": "用戶訊息", "user_id": "optional_user_id"}
    Returns: {"response": "小安回答", "intent": "knowledge_qa", "sources": []}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process through your RAG
        response = process_message(message)
        
        # Return response with metadata
        return jsonify({
            'response': response,
            'intent': 'processed',
            'sources': [],
            'user_id': user_id
        })
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/intent', methods=['POST'])
def detect_intent():
    """
    Intent detection endpoint
    Accepts: {"message": "用戶訊息"}
    Returns: {"intent": "knowledge_qa", "description": "知識問答"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        message = data.get('message', '')
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        recognizer = IntentRecognizer()
        intent = recognizer.detect_intent(message)
        description = recognizer.get_intent_description(intent)
        
        return jsonify({
            'intent': intent,
            'description': description
        })
        
    except Exception as e:
        print(f"❌ Error in intent endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/memory', methods=['GET', 'POST'])
def caregiver_memory():
    """Caregiver memory management endpoint"""
    try:
        memory = CaregiverMemory()
        
        if request.method == 'GET':
            user_id = request.args.get('user_id', 'default_user')
            profile = memory.get_user_profile(user_id)
            return jsonify({'profile': profile})
        
        if request.method == 'POST':
            data = request.get_json()
            user_id = data.get('user_id', 'default_user')
            key = data.get('key')
            value = data.get('value')
            
            if not key:
                return jsonify({'error': 'Missing key'}), 400
            
            memory.set_memory(user_id, key, value)
            return jsonify({'success': True, 'key': key, 'value': value})
            
    except Exception as e:
        print(f"❌ Error in memory endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/commands', methods=['POST'])
def process_command():
    """
    Process caregiver commands
    Accepts: {"command": "/setname 陳婆婆", "user_id": "optional"}
    Returns: {"response": "✅ 已記住你的名字：陳婆婆"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        command = data.get('command', '')
        user_id = data.get('user_id', 'default_user')
        
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        # Process through your RAG (which handles commands)
        response = process_message(command)
        
        return jsonify({
            'response': response,
            'command': command,
            'user_id': user_id
        })
        
    except Exception as e:
        print(f"❌ Error in command endpoint: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================
# Main entry point
# ============================================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 MCI RAG Server Starting...")
    print("=" * 60)
    print(f"📁 Working directory: {CURRENT_DIR}")
    print("✅ RAG system ready")
    print("🌐 Server running on http://localhost:5001")
    print("=" * 60)
    print("\n📋 Available endpoints:")
    print("  GET  /health           - Health check")
    print("  POST /chat             - Send a message")
    print("  POST /intent           - Detect intent")
    print("  POST /memory           - Manage caregiver memory")
    print("  POST /commands         - Process caregiver commands")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=False)