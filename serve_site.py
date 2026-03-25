#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║   OFFLINE SURVIVAL KIT — WEB SERVER     ║
║   Serves all kit files on LAN port 8080 ║
╚══════════════════════════════════════════╝

USAGE:
  python serve_site.py
  python serve_site.py --port 9090
  python serve_site.py --dir /path/to/folder

REQUIREMENTS: Python 3.6+ (no extra packages)
"""

import http.server
import socketserver
import socket
import os
import sys
import argparse
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
DEFAULT_PORT = 8080
# Serve from one level up (the kit root, not the scripts folder)
DEFAULT_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_local_ip():
    """Best-effort LAN IP detection."""
    for target in ('10.255.255.255', '192.168.1.1', '8.8.8.8'):
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

def get_all_ips():
    """Return all non-loopback IPs."""
    ips = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if not ip.startswith('127.') and ':' not in ip and ip not in ips:
                ips.append(ip)
    except Exception:
        pass
    if not ips:
        ips.append(get_local_ip())
    return ips

# ── Custom Handler ────────────────────────────────────────────────────────────
class SurvivalHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, serve_dir=DEFAULT_DIR, **kwargs):
        self._serve_dir = serve_dir
        super().__init__(*args, directory=serve_dir, **kwargs)

    def log_message(self, fmt, *args):
        ts = datetime.now().strftime('%H:%M:%S')
        client = self.client_address[0]
        print(f"  [{ts}] {client} → {fmt % args}")

    def end_headers(self):
        # Allow cross-origin for UI files
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Offline Survival Kit – Web Server')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('--dir',  type=str, default=DEFAULT_DIR)
    args = parser.parse_args()

    serve_dir = os.path.abspath(args.dir)
    port      = args.port

    handler = lambda *a, **kw: SurvivalHandler(*a, serve_dir=serve_dir, **kw)

    with socketserver.TCPServer(('0.0.0.0', port), handler) as httpd:
        httpd.allow_reuse_address = True
        ips = get_all_ips()

        print()
        print('╔' + '═'*50 + '╗')
        print('║   OFFLINE SURVIVAL KIT — WEB SERVER          ║')
        print('╠' + '═'*50 + '╣')
        print(f'║  Serving: {serve_dir[:40]:<40} ║')
        print('║                                                  ║')
        print(f'║  LOCAL   → http://localhost:{port:<5}               ║')
        for ip in ips:
            print(f'║  NETWORK → http://{ip}:{port}  ')
        print('║                                                  ║')
        print('║  Share the NETWORK address with other devices    ║')
        print('║  Press Ctrl+C to stop                            ║')
        print('╚' + '═'*50 + '╝')
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n  [!] Server stopped.')

if __name__ == '__main__':
    main()
