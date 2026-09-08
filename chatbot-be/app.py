import os
import json
import socket
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from pyngrok import ngrok

from config import PORT, HOST, USE_NGROK, NGROK_AUTH_TOKEN, MODELS_CONFIG, init_directories
from history_manager import load_history, save_history, clear_history
from model_manager import (
    check_sys,
    download_models,
    load_model,
    unload_model,
    generate_stream,
    get_model_route,
    current_model_name,
    get_vram_usage
)

init_directories()

app = Flask(__name__)
CORS(app)

def find_available_port(start_port=5001, host='127.0.0.1'):
    """Find an open TCP port starting from start_port."""
    for p in range(start_port, start_port + 20):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, p))
                return p
        except OSError:
            continue
    return start_port

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint displaying system and model status."""
    sys_info = check_sys()
    return jsonify({
        "status": "online",
        "active_model": current_model_name or "None",
        "vram_used_mb": round(get_vram_usage(), 2),
        "system": sys_info
    }), 200

@app.route('/models', methods=['GET'])
def list_models():
    """List available LLM models."""
    return jsonify({
        "available_models": list(MODELS_CONFIG.keys()),
        "active_model": current_model_name or "None"
    }), 200

@app.route('/clear', methods=['POST'])
def clear_memory():
    """Endpoint to clear chat history and unload model memory."""
    unload_model()
    clear_history()
    return jsonify({"status": "success", "message": "Memory cleared"}), 200

@app.route('/chat', methods=['POST'])
def chat_api():
    """Streaming chat SSE endpoint for Nox AI assistant."""
    data = request.json or {}
    user_input = data.get('message', '').strip()

    if not user_input:
        return jsonify({"error": "No message prompt provided"}), 400

    try:
        # Load conversation history
        history = load_history()

        def save_on_complete(prompt_text, response_text):
            history.append({"user": prompt_text, "assistant": response_text})
            save_history(history)

        headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
        }

        stream_gen = generate_stream(
            user_input=user_input,
            history=history,
            on_complete_callback=save_on_complete
        )

        return Response(stream_with_context(stream_gen), headers=headers)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_api(port=None, use_ngrok=None):
    """Run Flask application with automatic port selection and optional Ngrok tunnel."""
    target_host = HOST
    desired_port = PORT if port is None else port
    should_use_ngrok = USE_NGROK if use_ngrok is None else use_ngrok

    actual_port = find_available_port(desired_port, target_host)

    if actual_port != desired_port:
        print(f"[!] Warning: Port {desired_port} is reserved/occupied by Windows. Automatically using port {actual_port}.")

    public_url = None
    if should_use_ngrok and NGROK_AUTH_TOKEN:
        try:
            ngrok.set_auth_token(NGROK_AUTH_TOKEN)
            ngrok.kill()
            public_url = ngrok.connect(actual_port).public_url
            print(f"\n[!] NGROK TUNNEL ACTIVE AT: {public_url}")
            print(f"[!] Public Chat Endpoint:  {public_url}/chat")
            print(f"[!] Public Clear Endpoint: {public_url}/clear")
        except Exception as e:
            print(f"[!] Ngrok notice ({e}). Continuing with local server.")

    print(f"\n[!] LOCAL API SERVER ACTIVE AT: http://{target_host}:{actual_port}")
    print(f"[!] Local Chat Endpoint:  http://{target_host}:{actual_port}/chat")
    print(f"[!] Local Health Endpoint: http://{target_host}:{actual_port}/health\n")

    app.run(host=target_host, port=actual_port, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_api()