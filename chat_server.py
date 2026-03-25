#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║   OFFLINE SURVIVAL KIT — CHAT SERVER    ║
║   LAN group chat via WebSocket :8765    ║
╚══════════════════════════════════════════╝

INSTALL:
  pip install websockets

USAGE:
  python chat_server.py
  python chat_server.py --port 8765 --maxusers 50

CONNECT:
  Open ui/chat_ui.html in any browser
  Enter this machine's IP when prompted

FEATURES:
  • Multi-room support (#general, #emergency, custom)
  • Message history (last 100 msgs per room)
  • User join/leave notifications
  • Private messages with /pm username message
  • /users  — list online users
  • /rooms  — list active rooms
  • /nick   — change display name
  • /clear  — clear own chat
"""

import asyncio
import json
import socket
import argparse
import logging
from datetime import datetime
from collections import defaultdict

try:
    import websockets
except ImportError:
    print()
    print('  [!] Missing package: websockets')
    print('      Install it:  pip install websockets')
    print()
    import sys; sys.exit(1)

logging.basicConfig(level=logging.WARNING)

# ── State ─────────────────────────────────────────────────────────────────────
# { websocket: {'name': str, 'room': str} }
clients  = {}
# { room_name: [msg_dict, ...] }
history  = defaultdict(list)
MAX_HIST = 100

ROOMS = {'general': '📡 General', 'emergency': '🆘 Emergency', 'supply': '📦 Supply'}

# ── Helpers ───────────────────────────────────────────────────────────────────
def ts():
    return datetime.now().strftime('%H:%M')

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

def make_msg(type_, **kw):
    return json.dumps({'type': type_, 'time': ts(), **kw})

def users_in_room(room):
    return [v['name'] for ws, v in clients.items() if v.get('room') == room]

def users_in_room_sockets(room):
    return [ws for ws, v in clients.items() if v.get('room') == room]

async def broadcast_room(room, msg_str, exclude=None):
    targets = users_in_room_sockets(room)
    for ws in targets:
        if ws is exclude:
            continue
        try:
            await ws.send(msg_str)
        except Exception:
            pass

async def send(ws, msg_str):
    try:
        await ws.send(msg_str)
    except Exception:
        pass

def save_history(room, msg_dict):
    history[room].append(msg_dict)
    if len(history[room]) > MAX_HIST:
        history[room].pop(0)

# ── Command Handler ───────────────────────────────────────────────────────────
async def handle_command(ws, text):
    parts = text.strip().split(None, 2)
    cmd   = parts[0].lower()
    info  = clients.get(ws, {})
    name  = info.get('name', 'Unknown')
    room  = info.get('room', 'general')

    if cmd == '/users':
        ul = users_in_room(room)
        await send(ws, make_msg('system', text=f'Online in #{room}: {", ".join(ul)}'))

    elif cmd == '/rooms':
        rl = [f'#{r} ({len(users_in_room(r))} online)' for r in ROOMS]
        await send(ws, make_msg('system', text='Rooms: ' + ' | '.join(rl)))

    elif cmd == '/join' and len(parts) >= 2:
        new_room = parts[1].lstrip('#')
        clients[ws]['room'] = new_room
        hist = history.get(new_room, [])
        await send(ws, make_msg('history', messages=hist[-50:], room=new_room))
        await send(ws, make_msg('system', text=f'Joined #{new_room}'))

    elif cmd == '/nick' and len(parts) >= 2:
        old_name = name
        new_name = parts[1][:24]
        clients[ws]['name'] = new_name
        msg = make_msg('system', text=f'{old_name} is now known as {new_name}')
        await broadcast_room(room, msg)

    elif cmd == '/pm' and len(parts) >= 3:
        target_name = parts[1]
        pm_text     = parts[2]
        target_ws   = next((w for w, v in clients.items() if v['name'] == target_name), None)
        if target_ws:
            await send(target_ws, make_msg('pm', from_=name, text=pm_text))
            await send(ws,        make_msg('pm_sent', to=target_name, text=pm_text))
        else:
            await send(ws, make_msg('system', text=f'User {target_name} not found'))

    elif cmd == '/help':
        help_text = (
            'Commands: /users | /rooms | /join <room> | '
            '/nick <name> | /pm <user> <msg> | /help'
        )
        await send(ws, make_msg('system', text=help_text))

    else:
        await send(ws, make_msg('system', text=f'Unknown command: {cmd}  — try /help'))

# ── Connection Handler ────────────────────────────────────────────────────────
async def handler(websocket):
    try:
        async for raw in websocket:
            data = json.loads(raw)
            mtype = data.get('type')

            # ── JOIN ──────────────────────────────────────────────────────────
            if mtype == 'join':
                name = data.get('name', 'User')[:24]
                room = data.get('room', 'general')
                clients[websocket] = {'name': name, 'room': room}

                # Send history
                hist = history.get(room, [])
                await send(websocket, make_msg('history', messages=hist[-50:], room=room))

                # Notify room
                sys_msg = make_msg('system', text=f'{name} joined #{room}')
                d       = {'type': 'system', 'time': ts(), 'text': f'{name} joined #{room}'}
                save_history(room, d)
                await broadcast_room(room, sys_msg, exclude=websocket)
                await send(websocket, make_msg('system', text=f'Welcome {name}! Type /help for commands'))

            # ── MESSAGE ───────────────────────────────────────────────────────
            elif mtype == 'message':
                info = clients.get(websocket)
                if not info:
                    continue
                name = info['name']
                room = info['room']
                text = data.get('text', '').strip()[:500]

                if text.startswith('/'):
                    await handle_command(websocket, text)
                elif text:
                    msg_dict = {'type': 'message', 'time': ts(), 'name': name, 'text': text}
                    save_history(room, msg_dict)
                    await broadcast_room(room, json.dumps(msg_dict))

    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f'  [err] {e}')
    finally:
        info = clients.pop(websocket, None)
        if info:
            name = info.get('name')
            room = info.get('room', 'general')
            if name:
                msg = make_msg('system', text=f'{name} left the network')
                save_history(room, {'type': 'system', 'time': ts(), 'text': f'{name} left'})
                await broadcast_room(room, msg)

# ── Main ──────────────────────────────────────────────────────────────────────
async def main(port):
    ip = get_local_ip()
    print()
    print('╔' + '═'*50 + '╗')
    print('║   OFFLINE SURVIVAL KIT — CHAT SERVER         ║')
    print('╠' + '═'*50 + '╣')
    print(f'║  WebSocket: ws://{ip}:{port}')
    print('║                                                  ║')
    print('║  Open  ui/chat_ui.html  in any browser           ║')
    print(f'║  Enter server IP: {ip}')
    print('║                                                  ║')
    print('║  Default rooms: #general  #emergency  #supply    ║')
    print('║  Press Ctrl+C to stop                            ║')
    print('╚' + '═'*50 + '╝')
    print()

    async with websockets.serve(handler, '0.0.0.0', port, ping_interval=30):
        await asyncio.Future()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    asyncio.run(main(args.port))
