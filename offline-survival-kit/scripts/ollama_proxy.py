#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║  OFFLINE SURVIVAL KIT — OLLAMA PROXY   ║
║  Exposes Ollama AI on your LAN :11435  ║
╚══════════════════════════════════════════╝

WHY THIS EXISTS:
  By default Ollama only listens on 127.0.0.1 (localhost).
  This proxy bridges Ollama to all devices on your network.
  It also adds CORS headers so browser UIs can call it.

INSTALL:
  pip install flask flask-cors requests

START OLLAMA FIRST:
  Linux/Mac :  OLLAMA_HOST=0.0.0.0 ollama serve
  Windows   :  set OLLAMA_HOST=0.0.0.0 && ollama serve
  (Or just let this proxy handle it — it talks to localhost:11434)

USAGE:
  python ollama_proxy.py
  python ollama_proxy.py --port 11435 --ollama http://localhost:11434

THEN:
  Open  ui/ollama_ui.html  in any browser on any device
  Set server IP to this machine's IP address
"""

import os
import sys
import socket
import argparse

try:
    from flask import Flask, request, Response, jsonify
    from flask_cors import CORS
    import requests
except ImportError:
    print()
    print('  [!] Missing packages.')
    print('      Install: pip install flask flask-cors requests')
    print()
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

OLLAMA_INTERNAL = os.environ.get('OLLAMA_INTERNAL', 'http://localhost:11434')

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_local_ip():
    for target in ('10.255.255.255', '192.168.1.1'):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((target, 1))
            ip = s.getsockname()[0]
            s.close()
            if not ip.startswith('127.'):
                return ip
        except Exception:
            pass
    return '127.0.0.1'

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/health')
def health():
    """Health check — tests connection to Ollama."""
    try:
        r = requests.get(f'{OLLAMA_INTERNAL}/api/tags', timeout=5)
        models = r.json().get('models', [])
        names  = [m['name'] for m in models]
        return jsonify({'status': 'ok', 'ollama': 'running', 'models': names})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e),
                        'hint': 'Start Ollama first: ollama serve'}), 503

@app.route('/api/tags', methods=['GET'])
def list_models():
    """List available Ollama models."""
    try:
        r = requests.get(f'{OLLAMA_INTERNAL}/api/tags', timeout=10)
        resp = Response(r.content, status=r.status_code, content_type='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        return jsonify({'error': str(e)}), 503

@app.route('/api/generate', methods=['POST', 'OPTIONS'])
def generate():
    """Proxy /api/generate — supports streaming."""
    if request.method == 'OPTIONS':
        r = Response('', status=200)
        r.headers['Access-Control-Allow-Origin']  = '*'
        r.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        r.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return r

    try:
        upstream = requests.post(
            f'{OLLAMA_INTERNAL}/api/generate',
            data=request.get_data(),
            headers={'Content-Type': 'application/json'},
            stream=True,
            timeout=300,
        )
        def stream():
            for chunk in upstream.iter_content(chunk_size=None):
                yield chunk

        resp = Response(stream(), status=upstream.status_code,
                        content_type=upstream.headers.get('content-type', 'application/json'))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot reach Ollama',
                        'hint': 'Run: ollama serve'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Proxy /api/chat (chat-style API)."""
    if request.method == 'OPTIONS':
        r = Response('', status=200)
        r.headers['Access-Control-Allow-Origin']  = '*'
        r.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        r.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return r

    try:
        upstream = requests.post(
            f'{OLLAMA_INTERNAL}/api/chat',
            data=request.get_data(),
            headers={'Content-Type': 'application/json'},
            stream=True,
            timeout=300,
        )
        def stream():
            for chunk in upstream.iter_content(chunk_size=None):
                yield chunk

        resp = Response(stream(), status=upstream.status_code,
                        content_type=upstream.headers.get('content-type', 'application/json'))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot reach Ollama'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pull', methods=['POST'])
def pull():
    """Proxy model pull requests."""
    try:
        upstream = requests.post(
            f'{OLLAMA_INTERNAL}/api/pull',
            data=request.get_data(),
            headers={'Content-Type': 'application/json'},
            stream=True,
            timeout=600,
        )
        def stream():
            for chunk in upstream.iter_content(chunk_size=None):
                yield chunk

        resp = Response(stream(), status=upstream.status_code,
                        content_type='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        return jsonify({'error': str(e)}), 503

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin']  = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',   type=int, default=11435)
    parser.add_argument('--ollama', type=str, default=OLLAMA_INTERNAL)
    args = parser.parse_args()

    OLLAMA_INTERNAL = args.ollama
    ip = get_local_ip()

    print()
    print('╔' + '═'*50 + '╗')
    print('║  OFFLINE SURVIVAL KIT — OLLAMA PROXY        ║')
    print('╠' + '═'*50 + '╣')
    print(f'║  Proxy port : {args.port}')
    print(f'║  Ollama at  : {OLLAMA_INTERNAL}')
    print()
    print(f'║  Network URL: http://{ip}:{args.port}')
    print()
    print('║  STEP 1: Start Ollama')
    print('║    Linux/Mac: OLLAMA_HOST=0.0.0.0 ollama serve')
    print('║    Windows  : set OLLAMA_HOST=0.0.0.0')
    print('║               ollama serve')
    print()
    print('║  STEP 2: Load a model')
    print('║    ollama pull llama3.2:1b   (800MB — fast)')
    print('║    ollama pull gemma2:2b     (1.6GB)')
    print('║    ollama pull phi3:mini     (2.3GB)')
    print()
    print('║  STEP 3: Open ui/ollama_ui.html')
    print(f'║    Set server IP to: {ip}')
    print()
    print('║  Press Ctrl+C to stop')
    print('╚' + '═'*50 + '╝')
    print()

    app.run(host='0.0.0.0', port=args.port, debug=False, threaded=True)
