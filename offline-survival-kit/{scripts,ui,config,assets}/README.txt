╔══════════════════════════════════════════════════════════════════╗
║         OFFLINE SURVIVAL KIT — README                           ║
║         Full Local Network Infrastructure                        ║
╚══════════════════════════════════════════════════════════════════╝


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  QUICK START (60 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Install Python 3  →  python.org/downloads
  2. Open Command Prompt in this folder
  3. Run:  pip install pyftpdlib websockets flask flask-cors requests
  4. Run:  python scripts\serve_site.py
  5. Note the IP shown  (e.g. http://192.168.1.5:8080)
  6. Open that address in any browser on any device on your network


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FOLDER STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  offline-survival-kit\
  ├── index.html                ← Open this — the full manual
  ├── README.txt                ← This file
  ├── Modelfile                 ← Ollama config for qwen2.5-1.5b
  ├── qwen2.5-1.5b.gguf         ← AI model (copy here from downloads)
  │
  ├── scripts\
  │   ├── serve_site.py         ← Web server        (port 8080)
  │   ├── ftp_server.py         ← FTP file server   (port 2121)
  │   ├── chat_server.py        ← Chat server       (port 8765)
  │   ├── ollama_proxy.py       ← Ollama LAN proxy  (port 11435)
  │   └── setup_hosts.py        ← Custom domain names
  │
  ├── ui\
  │   ├── chat_ui.html          ← Chat web interface
  │   └── ollama_ui.html        ← AI chat web interface
  │
  └── config\
      └── requirements.txt      ← Python package list


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SERVICES & PORTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Port 8080   → Web server  (open in browser)
  Port 2121   → FTP server  (file manager or ftp command)
  Port 8765   → Chat server (WebSocket — used by chat_ui.html)
  Port 11434  → Ollama      (localhost only — internal)
  Port 11435  → Ollama proxy (accessible from all LAN devices)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  LAUNCH ORDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Open a SEPARATE Command Prompt window for each service:

  Window 1:  python scripts\serve_site.py
  Window 2:  python scripts\ftp_server.py
  Window 3:  python scripts\chat_server.py
  Window 4:  set OLLAMA_HOST=0.0.0.0  &&  ollama serve
  Window 5:  python scripts\ollama_proxy.py

  Or all at once (PowerShell — each in background):
  Start-Process python -ArgumentList "scripts\serve_site.py"
  Start-Process python -ArgumentList "scripts\ftp_server.py"
  Start-Process python -ArgumentList "scripts\chat_server.py"


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OLLAMA AI SETUP — FULL GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  You already have:  qwen2.5-1.5b.gguf  (good choice — fast, smart)
  You already have:  Modelfile           (config file for Ollama)

  ── STEP 1: Install Ollama ──────────────────────────────────────

    Download:  https://ollama.com/download/OllamaSetup.exe
    Run the installer. Ollama installs as a Windows service.
    It adds  ollama  to your PATH automatically.

    Verify install — open CMD and type:
      ollama --version

  ── STEP 2: Copy files to one folder ───────────────────────────

    Both the Modelfile AND the .gguf must be in the same folder.

    Option A — Put both in the kit root folder:
      D:\sirvival\offline-survival-kit\Modelfile
      D:\sirvival\offline-survival-kit\qwen2.5-1.5b.gguf

    Option B — Use the full path in Modelfile:
      Edit Modelfile, change this line:
        FROM ./qwen2.5-1.5b.gguf
      To the full path where your .gguf is:
        FROM D:\sirvival\offline-survival-kit\{scripts,ui,config,assets}\qwen2.5-1.5b.gguf

    NOTE: Your .gguf is currently in a folder with a weird name:
      {scripts,ui,config,assets}
    This happened because Linux brace expansion doesn't work on
    Windows CMD. The folder was created literally with that name.
    RECOMMENDATION: Move the .gguf to the kit root folder to keep
    things simple:
      move "{scripts,ui,config,assets}\qwen2.5-1.5b.gguf" .

  ── STEP 3: Create the model in Ollama ─────────────────────────

    Open CMD in the folder containing Modelfile and the .gguf:
      cd D:\sirvival\offline-survival-kit

    Run this command (only needed ONCE):
      ollama create survival-ai -f Modelfile

    Wait — it loads the model (may take 1–2 minutes).
    You should see: "success" at the end.

    Verify it was created:
      ollama list
      (you should see  survival-ai  in the list)

  ── STEP 4: Test in terminal ────────────────────────────────────

    Quick chat test:
      ollama run survival-ai

    Type your question and press Enter.
    Type  /bye  to exit.

  ── STEP 5: Expose to network ──────────────────────────────────

    By default Ollama only listens on localhost (127.0.0.1).
    To let other devices use it, set this BEFORE running:

    CMD:
      set OLLAMA_HOST=0.0.0.0
      ollama serve

    PowerShell:
      $env:OLLAMA_HOST="0.0.0.0"
      ollama serve

    Now other devices can reach Ollama at:
      http://YOUR_IP:11434

  ── STEP 6: Start the proxy (easier for browsers) ───────────────

    In a separate CMD window:
      python scripts\ollama_proxy.py

    This adds CORS headers and a /health endpoint that the
    ollama_ui.html needs to work properly from any browser.

  ── STEP 7: Use the AI from any device ─────────────────────────

    Open ui\ollama_ui.html in any browser.
    Enter your server IP (e.g. 192.168.1.5)
    Port: 11435
    Click CONNECT & LOAD MODELS
    Select  survival-ai  and start chatting.

    Other devices on the network use the same URL:
      http://192.168.1.5:8080/ui/ollama_ui.html
    (if web server is also running)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MODELFILE EXPLAINED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  The Modelfile (in the kit root) configures how Ollama uses your
  qwen2.5-1.5b.gguf model. Key settings you can change:

  FROM ./qwen2.5-1.5b.gguf
    → Path to the .gguf model file. Change if file is elsewhere.

  PARAMETER num_ctx 4096
    → How much conversation the AI remembers at once.
      2048 = faster/less RAM,  8192 = more memory/slower.

  PARAMETER temperature 0.7
    → Creativity level. 0.0 = always same answer, 1.0 = random.
      0.7 is a good balance for a survival assistant.

  PARAMETER num_predict 512
    → Max length of each response. 512 = short, -1 = no limit.

  SYSTEM """..."""
    → The personality/instructions for the AI.
      Edit this to change what the AI focuses on.

  After editing Modelfile, re-run:
    ollama create survival-ai -f Modelfile
  to apply changes.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OLLAMA COMMAND REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ollama list                       List all installed models
  ollama create survival-ai -f Modelfile   Create from Modelfile
  ollama run survival-ai            Chat in terminal
  ollama rm survival-ai             Delete the model
  ollama show survival-ai           Show model info
  ollama ps                         Show running models
  ollama serve                      Start Ollama server
  ollama pull llama3.2:1b           Download a model (needs internet)

  STORAGE LOCATION (Windows):
    Models are stored at:  C:\Users\USERNAME\.ollama\models
    Change with:  set OLLAMA_MODELS=D:\my-models

  OLLAMA_HOST options:
    set OLLAMA_HOST=0.0.0.0         Listen on all interfaces (LAN)
    set OLLAMA_HOST=127.0.0.1       Localhost only (default)
    set OLLAMA_HOST=0.0.0.0:8080    Different port


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  IMPORTANT — RENAME THE WEIRD FOLDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Your current folder is named exactly:  {scripts,ui,config,assets}
  This is a Linux shell trick that Windows took literally as a name.

  To move the .gguf to the kit root (recommended):
    cd D:\sirvival\offline-survival-kit
    move "{scripts,ui,config,assets}\qwen2.5-1.5b.gguf" .

  Then rename the empty folder (optional cleanup):
    rename "{scripts,ui,config,assets}" models

  After this, the Modelfile's  FROM ./qwen2.5-1.5b.gguf  will work
  without any path changes.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  "ollama: command not found"
    → Restart CMD after installing Ollama. Or use full path:
      C:\Users\USERNAME\AppData\Local\Programs\Ollama\ollama.exe

  "Error: open ./qwen2.5-1.5b.gguf: no such file"
    → Modelfile and .gguf must be in the same folder.
      Run  ollama create  from that folder, or use full path in FROM.

  "Other devices can't reach the AI"
    → Make sure you ran:  set OLLAMA_HOST=0.0.0.0  BEFORE ollama serve
    → Check Windows Firewall — allow port 11434 and 11435:
      netsh advfirewall firewall add rule name="Ollama" dir=in action=allow protocol=TCP localport=11434-11435

  "Ollama UI shows no models"
    → Make sure ollama_proxy.py is running (separate CMD window)
    → Make sure you created the model:  ollama create survival-ai -f Modelfile

  "Very slow responses"
    → Normal for CPU-only. Qwen2.5-1.5B should take 5–15 seconds.
    → Close other apps to free RAM.
    → Reduce num_ctx in Modelfile (try 2048).

  "Out of memory error"
    → Lower num_ctx to 2048 in Modelfile, then recreate the model.
    → Make sure you have at least 4GB free RAM.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PYTHON DEPENDENCIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Install all:
    pip install pyftpdlib websockets flask flask-cors requests

  Or use the requirements file:
    pip install -r config\requirements.txt

  For offline install (no internet):
    First download while online:
      pip download pyftpdlib websockets flask flask-cors requests -d .\offline-packages
    Then install offline:
      pip install --no-index --find-links=.\offline-packages pyftpdlib websockets flask flask-cors requests


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SUPPORTED DEVICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Any device with a browser can access all web UIs.
  FTP works on Windows, Linux, macOS, Android (with file manager app).
  Ollama only runs on the server machine (Windows/Linux/Mac).
  Android can run servers via Termux — see manual Chapter 10.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  LICENSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Kit scripts and UIs: Free for personal use. No warranty.
  Qwen2.5 model: Qwen License (Alibaba Cloud). Personal/research use.
  Designed for legitimate offline/disaster-recovery use only.
