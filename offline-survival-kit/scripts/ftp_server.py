#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║   OFFLINE SURVIVAL KIT — FTP SERVER     ║
║   LAN file sharing on port 2121         ║
╚══════════════════════════════════════════╝

INSTALL:
  pip install pyftpdlib

USAGE:
  python ftp_server.py
  python ftp_server.py --port 2121 --dir /shared
  python ftp_server.py --readonly    (no uploads)

CONNECT FROM:
  Windows Explorer : ftp://192.168.x.x:2121
  Android (FX File): ftp://192.168.x.x:2121
  Linux terminal   : ftp 192.168.x.x 2121
  Browser          : ftp://192.168.x.x:2121
  FileZilla        : host=192.168.x.x  port=2121

ACCOUNTS:
  Username: survival   Password: offline123  (read+write)
  Username: anonymous  (no password)         (read only)
"""

import os
import sys
import socket
import argparse

try:
    from pyftpdlib.handlers   import FTPHandler
    from pyftpdlib.servers    import FTPServer
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.log        import config_logging
except ImportError:
    print()
    print('  [!] Missing package: pyftpdlib')
    print('      Install it with:  pip install pyftpdlib')
    print()
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
DEFAULT_PORT  = 2121
DEFAULT_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RW_USER       = 'survival'
RW_PASS       = 'offline123'
PASSIVE_PORTS = range(60000, 60100)

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

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Offline Survival Kit – FTP Server')
    parser.add_argument('--port',     type=int, default=DEFAULT_PORT)
    parser.add_argument('--dir',      type=str, default=DEFAULT_DIR)
    parser.add_argument('--readonly', action='store_true')
    args = parser.parse_args()

    shared_dir = os.path.abspath(args.dir)
    port       = args.port
    readonly   = args.readonly

    config_logging(level='ERROR')

    authorizer = DummyAuthorizer()

    if readonly:
        authorizer.add_user(RW_USER, RW_PASS, shared_dir, perm='elr')
        perm_label = 'READ ONLY'
    else:
        # elradfmwMT = full permissions
        authorizer.add_user(RW_USER, RW_PASS, shared_dir, perm='elradfmwMT')
        perm_label = 'READ + WRITE'

    authorizer.add_anonymous(shared_dir, perm='elr')

    handler                = FTPHandler
    handler.authorizer     = authorizer
    handler.passive_ports  = PASSIVE_PORTS
    handler.banner         = 'OFFLINE SURVIVAL KIT FTP SERVER — Ready.'
    handler.max_cons       = 50
    handler.max_cons_per_ip = 5

    server = FTPServer(('0.0.0.0', port), handler)
    ip     = get_local_ip()

    print()
    print('╔' + '═'*50 + '╗')
    print('║   OFFLINE SURVIVAL KIT — FTP SERVER          ║')
    print('╠' + '═'*50 + '╣')
    print(f'║  Sharing: {shared_dir[:40]:<40} ║')
    print(f'║  Mode   : {perm_label:<40} ║')
    print('║                                                  ║')
    print(f'║  Address : ftp://{ip}:{port}')
    print(f'║  Username: {RW_USER}')
    print(f'║  Password: {RW_PASS}')
    print('║  Anon    : read-only, no password               ║')
    print('║                                                  ║')
    print('║  Windows: Open File Explorer → type address     ║')
    print('║  Android: FX File / Solid Explorer / ES File    ║')
    print('║  Linux  : ftp <ip> 2121  OR  filezilla          ║')
    print('║  Press Ctrl+C to stop                           ║')
    print('╚' + '═'*50 + '╝')
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  [!] FTP server stopped.')

if __name__ == '__main__':
    main()
