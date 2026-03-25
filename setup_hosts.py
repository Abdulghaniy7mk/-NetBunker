#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║  OFFLINE SURVIVAL KIT — HOSTS MANAGER  ║
║  Custom domains on your local network  ║
╚══════════════════════════════════════════╝

WHAT THIS DOES:
  Adds human-readable names to your hosts file so you can
  type  http://survival.local  instead of  http://192.168.1.5:8080

  Run this on EVERY device that needs the friendly names.

USAGE:
  python setup_hosts.py            — auto-detect IP, interactive
  python setup_hosts.py --ip 192.168.1.5
  python setup_hosts.py --remove   — remove all entries
  python setup_hosts.py --list     — show current kit entries

RUN AS:
  Windows : Run Command Prompt as Administrator
  Linux   : sudo python setup_hosts.py
  Mac     : sudo python setup_hosts.py
  Android : Requires root (or use a DNS app like DNSMasq)

NOTE FOR ANDROID (no root):
  Use a DNS/VPN app: "DNS Changer" or "personalDNSfilter"
  Add: 192.168.x.x  survival.local
"""

import os
import sys
import socket
import argparse
import platform
import re

# ── Config ────────────────────────────────────────────────────────────────────
MARKER_START = '# === OFFLINE SURVIVAL KIT — START ==='
MARKER_END   = '# === OFFLINE SURVIVAL KIT — END ==='

HOSTS_FILE = {
    'Windows': r'C:\Windows\System32\drivers\etc\hosts',
    'Linux'  : '/etc/hosts',
    'Darwin' : '/etc/hosts',
}.get(platform.system(), '/etc/hosts')

DOMAIN_MAP = [
    ('survival.local',   8080, 'Web Manual + File Browser'),
    ('chat.local',       80,   'Chat Web UI'),
    ('ai.local',         80,   'Ollama AI Web UI'),
    ('files.local',      2121, 'FTP File Server'),
    ('network.local',    8080, 'Network Dashboard'),
]

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
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return '127.0.0.1'

def check_admin():
    if platform.system() == 'Windows':
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False
    else:
        return os.geteuid() == 0

def read_hosts():
    try:
        with open(HOSTS_FILE, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except FileNotFoundError:
        return ''
    except PermissionError:
        return None

def write_hosts(content):
    try:
        with open(HOSTS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except PermissionError:
        return False

def strip_kit_entries(content):
    """Remove everything between our markers."""
    pattern = re.compile(
        r'\n?' + re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END) + r'\n?',
        re.DOTALL
    )
    return pattern.sub('', content)

def build_entries(ip):
    lines = [MARKER_START]
    for domain, port, desc in DOMAIN_MAP:
        lines.append(f'{ip}\t{domain}\t# {desc}')
    lines.append(MARKER_END)
    return '\n' + '\n'.join(lines) + '\n'

def list_entries(content):
    in_block = False
    entries  = []
    for line in content.splitlines():
        if MARKER_START in line:
            in_block = True
            continue
        if MARKER_END in line:
            in_block = False
            continue
        if in_block and line.strip() and not line.startswith('#'):
            entries.append(line)
    return entries

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Offline Survival Kit – Hosts Manager')
    parser.add_argument('--ip',     type=str, help='Force IP address to use')
    parser.add_argument('--remove', action='store_true', help='Remove kit entries')
    parser.add_argument('--list',   action='store_true', help='List kit entries')
    args = parser.parse_args()

    print()
    print('╔' + '═'*50 + '╗')
    print('║  OFFLINE SURVIVAL KIT — HOSTS MANAGER       ║')
    print('╚' + '═'*50 + '╝')
    print()

    is_admin = check_admin()
    if not is_admin:
        print('  ⚠  WARNING: Not running as Administrator / root.')
        print('     Changes to hosts file may fail.')
        print('     Windows: Run cmd.exe as Administrator')
        print('     Linux  : sudo python setup_hosts.py')
        print()

    content = read_hosts()
    if content is None:
        print(f'  [!] Cannot read {HOSTS_FILE} — permission denied')
        sys.exit(1)

    # ── List ──────────────────────────────────────────────────────────────────
    if args.list:
        entries = list_entries(content)
        if entries:
            print('  Current Survival Kit entries:')
            for e in entries:
                print(f'    {e}')
        else:
            print('  No Survival Kit entries found in hosts file.')
        print()
        return

    # ── Remove ────────────────────────────────────────────────────────────────
    if args.remove:
        new_content = strip_kit_entries(content)
        if write_hosts(new_content):
            print('  ✓ Removed all Survival Kit entries from hosts file.')
        else:
            print('  [!] Failed to write hosts file — run as Administrator/root')
        print()
        return

    # ── Add / Update ──────────────────────────────────────────────────────────
    ip = args.ip or get_local_ip()
    print(f'  Detected IP : {ip}')
    print(f'  Hosts file  : {HOSTS_FILE}')
    print()
    print('  Entries to add:')
    for domain, port, desc in DOMAIN_MAP:
        print(f'    {ip}  →  {domain}  ({desc})')
    print()

    confirm = input('  Proceed? [yes/no]: ').strip().lower()
    if confirm != 'yes':
        print('  Aborted.')
        print()
        return

    clean   = strip_kit_entries(content)
    entries = build_entries(ip)
    new_content = clean.rstrip('\n') + '\n' + entries

    if write_hosts(new_content):
        print()
        print('  ✓ Hosts file updated successfully!')
        print()
        print('  You can now use:')
        for domain, port, desc in DOMAIN_MAP:
            proto = 'ftp' if port == 2121 else 'http'
            port_str = f':{port}' if port not in (80, 443, 2121) else f':{port}'
            print(f'    {proto}://{domain}{port_str}  —  {desc}')
        print()
        print('  NOTE: Each device needs to run this script.')
        print('  On Android without root, edit DNS settings manually.')
    else:
        print()
        print('  [!] Failed to write hosts file.')
        print('      Manual entries to add:')
        for domain, port, desc in DOMAIN_MAP:
            print(f'      {ip}  {domain}')
        print()
        if platform.system() == 'Windows':
            print(f'  File location: {HOSTS_FILE}')
            print('  Right-click → Open with Notepad as Administrator')
    print()

if __name__ == '__main__':
    main()
