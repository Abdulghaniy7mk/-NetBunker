╔══════════════════════════════════════════════════════════════╗
║         OFFLINE SURVIVAL KIT — README                       ║
║         Full Local Network Infrastructure                    ║
╚══════════════════════════════════════════════════════════════╝

WHAT IS THIS?
  A complete, self-contained kit for running local network services
  when the internet is unavailable. Everything works on your LAN.

QUICK START
  1. Install Python 3 (python.org — do this before internet goes down)
  2. Open terminal in this folder
  3. Run: pip install pyftpdlib websockets flask flask-cors requests
  4. Run: python scripts/serve_site.py
  5. Open browser and go to: http://YOUR_IP:8080
  6. Share that URL with other devices on your network

FOLDER STRUCTURE
  index.html              ← Main manual (open this in browser)
  README.txt              ← This file
  scripts/
    serve_site.py         ← HTTP web server (port 8080)
    ftp_server.py         ← FTP file server (port 2121)
    chat_server.py        ← WebSocket chat server (port 8765)
    ollama_proxy.py       ← Ollama AI proxy (port 11435)
    setup_hosts.py        ← Custom domain names manager
  ui/
    chat_ui.html          ← Chat web interface
    ollama_ui.html        ← AI chat web interface

SERVICES & PORTS
  Port 8080   → Web server (manual + files)
  Port 2121   → FTP server (file sharing)
  Port 8765   → Chat server (WebSocket)
  Port 11434  → Ollama direct (localhost only)
  Port 11435  → Ollama proxy (LAN accessible)

LAUNCH ORDER
  1. python scripts/serve_site.py    (always first)
  2. python scripts/ftp_server.py    (file sharing)
  3. python scripts/chat_server.py   (group chat)
  4. ollama serve                    (AI — if Ollama installed)
  5. python scripts/ollama_proxy.py  (AI LAN access)

PYTHON DEPENDENCIES
  pip install pyftpdlib websockets flask flask-cors requests

OFFLINE PACKAGE INSTALL (if pip can't reach internet)
  pip install --no-index --find-links=./offline-packages [package]

SUPPORTED DEVICES
  Any device with a web browser and WiFi can access the services.
  Tested: Windows, Linux, macOS, Android, iOS.

NOTES
  - All scripts require Python 3.6+
  - Static IP recommended for server machine
  - Run scripts as admin/sudo for firewall changes
  - For custom domains: run scripts/setup_hosts.py on each device

LICENSE
  Free for personal use. No warranty. Use at your own risk.
  Designed for legitimate offline/disaster-recovery use.
