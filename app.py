#!/usr/bin/env python
"
EDUSMART - Render Web Server (Reverse Proxy)
Forwards all requests to local exam system via ngrok tunnel.
"

print("[STARTUP] Python app starting...")

import os
import sys
import requests
from flask import Flask, request

print(f"[STARTUP] Python version: {sys.version.split()[0]}")

# Backend configuration
BACKEND_URL = os.environ.get('BACKEND_URL', 'https://facility-zap-amusable.ngrok-free.dev')
print(f"[STARTUP] Backend URL: {BACKEND_URL}")

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
print("[STARTUP] Flask app created")

def forward_request(path_and_query=''):
    "Forward request to backend via ngrok tunnel."
    try:
        backend_url = BACKEND_URL.rstrip('/') + '/' + path_and_query.lstrip('/')
        print(f"[PROXY] Forwarding {request.method} {request.path}")
        
        headers = {key: val for key, val in request.headers if key.lower() not in ['host', 'connection', 'content-length']}
        
        if request.method == 'GET':
            resp = requests.get(backend_url, headers=headers, params=request.args, timeout=30, allow_redirects=False)
        elif request.method == 'POST':
            data = request.form if not request.is_json else request.get_json()
            resp = requests.post(backend_url, headers=headers, data=data, files=request.files, timeout=30, allow_redirects=False)
        elif request.method == 'PUT':
            resp = requests.put(backend_url, headers=headers, data=request.get_data(), timeout=30, allow_redirects=False)
        elif request.method == 'DELETE':
            resp = requests.delete(backend_url, headers=headers, timeout=30, allow_redirects=False)
        else:
            return {'error': 'Method not allowed'}, 405
        
        return resp.content, resp.status_code, dict(resp.headers)
    
    except requests.exceptions.Timeout:
        return '<html><body><h1>Backend Timeout</h1><p>Exam system not responding.</p></body></html>', 504
    except requests.exceptions.ConnectionError:
        return f'<html><body><h1>Backend Unavailable</h1><p>Cannot connect to {BACKEND_URL}</p><p>Start exam system and ngrok tunnel.</p></body></html>', 503
    except Exception as e:
        print(f"[PROXY] Error: {e}")
        return f'<html><body><h1>Error</h1><p>{str(e)}</p></body></html>', 502

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    "Proxy all requests to backend."
    path_and_query = f"{path}?{request.query_string.decode()}" if request.query_string else path
    return forward_request(path_and_query)

@app.errorhandler(500)
def error_500(e):
    return '<html><body><h1>Server Error</h1></body></html>', 500

@app.errorhandler(404)
def error_404(e):
    return '<html><body><h1>Not Found</h1></body></html>', 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[STARTUP] Starting reverse proxy on port {port}")
    print(f"[STARTUP] Proxying to: {BACKEND_URL}")
    app.run(host='0.0.0.0', port=port, debug=False)
