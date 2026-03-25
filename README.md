# 🛡️ NetBunker
### *Your offline survival network — when the internet goes dark*

> **NetBunker** is a complete, self-contained local network kit for when internet access is lost — power outages, natural disasters, war, or any emergency. One computer becomes a server. Every phone, tablet, and laptop nearby gets AI, group chat, file sharing, and a full web manual — **no internet required, ever.**

---

<div align="center">

![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Android%20%7C%20Mac-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-yellow)
![Internet](https://img.shields.io/badge/Internet-NOT%20Required-brightgreen)
![Level](https://img.shields.io/badge/Level-Beginner%20Friendly-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

</div>

---

## 🤔 What is this for?

Imagine the internet goes down for days — or longer. No Google, no WhatsApp, no news, no maps. **NetBunker** lets you:

- 📡 **Talk to people nearby** — group chat works over WiFi with no internet
- 🤖 **Ask an AI anything** — medical, technical, survival questions answered locally
- 📁 **Share files between devices** — documents, photos, instructions
- 🌐 **Read a full survival manual** — in your browser, offline
- 🏠 **Host your own local website** — share information with your community

All of this works as long as you have **electricity and a WiFi router** (or even just one phone as a hotspot).

---

## 📋 Table of Contents

- [What's Inside](#-whats-inside)
- [Before the Emergency — Do This Now!](#-before-the-emergency--do-this-now)
- [Required Installs](#-required-installs)
- [Quick Start (5 minutes)](#-quick-start-5-minutes)
- [Setting Up the AI](#-setting-up-the-ai-ollama)
- [Connecting Other Devices](#-connecting-other-devices)
- [Recommended Offline Apps](#-recommended-offline-apps-install-now)
- [Offline Maps — Very Important](#-offline-maps--very-important)
- [Services Overview](#-services-overview)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq-for-beginners)

---

## 📦 What's Inside

```
NetBunker/
│
├── 📄 index.html                        ← The full survival manual (open in browser)
├── 📄 README.md                         ← This file (GitHub page)
├── 📄 README.txt                        ← Plain text quick reference
├── 📄 Modelfile                         ← AI personality + settings config
│
├── 📁 scripts/
│   ├── serve_site.py                    ← Web server    → shares the manual
│   ├── ftp_server.py                    ← File sharing  → like a local Dropbox
│   ├── chat_server.py                   ← Group chat    → like WhatsApp, offline
│   ├── ollama_proxy.py                  ← AI server     → makes AI work on all devices
│   └── setup_hosts.py                   ← Easy addresses → type "chat.local" instead of IPs
│
├── 📁 ui/
│   ├── chat_ui.html                     ← Open in browser to chat
│   └── ollama_ui.html                   ← Open in browser to talk to AI
│
├── 📁 config/
│   └── requirements.txt                 ← List of Python packages needed
│
└── 📁 {scripts,ui,config,assets}/       ← ⚠️ AI model folder (see note below)
    ├── DOWNLOAD_MODEL.txt               ← Instructions to get the AI model
    └── qwen2.5-1.5b.gguf               ← ❌ NOT INCLUDED — download manually
```

> ### ⚠️ About the `{scripts,ui,config,assets}` folder
> This folder has an unusual name because it was created on Linux where `{a,b,c}` is a shell shortcut that normally creates **multiple** folders. On Windows, it was created as a **single** folder with that exact name — that is intentional and fine. **Leave the folder name as-is.** Just place your downloaded `.gguf` file inside it.

---

> ### 🤖 AI Model Not Included (GitHub File Size Limit)
>
> GitHub has a **100 MB maximum file size limit**.  
> The AI brain file (`qwen2.5-1.5b.gguf`) is **~986 MB** and cannot be uploaded here.
>
> 📥 **Download it yourself (free, one time):**
>
> **➡️ [Click here to download from Hugging Face](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/main)**
>
> 1. Open the link above
> 2. Click `qwen2.5-1.5b-instruct-q4_k_m.gguf`
> 3. Click the ⬇ download button (~986 MB)
> 4. Move the file into the `{scripts,ui,config,assets}` folder
> 5. See `{scripts,ui,config,assets}/DOWNLOAD_MODEL.txt` for full instructions
>
> The folder `{scripts,ui,config,assets}/DOWNLOAD_MODEL.txt` already included in this repo explains everything step by step.

---

## ⚡ Before the Emergency — Do This Now!

> **⚠️ This section is the most important. Do everything here BEFORE you lose internet.**

### 🗺️ 1. Download Offline Maps

When the internet dies, so does Google Maps. Download your area **now**.

**Google Maps (Android & iPhone):**
1. Open Google Maps
2. Tap your profile picture → "Offline maps"
3. Tap "Select your own map"
4. Draw a box around:
   - Where you **live**
   - Where you **work**
   - Routes between them
   - The nearest hospital, pharmacy, and supermarket
5. Download each area (each is ~1–2 GB)
6. Do this for family members' phones too!

**Better option — OsmAnd (more detail, free):**
- Download from Play Store / App Store
- Go to Downloads → download your entire country/state
- Works fully offline, includes roads, buildings, pharmacies, hospitals

**Even better — Maps.me:**
- Download from Play Store / App Store
- Download your country — works 100% offline

---

### 💾 2. Install Required Software (Needs Internet — Do Now!)

#### Python (needed to run all servers)

1. Go to **https://python.org/downloads**
2. Download the latest Python 3 for your system
3. **IMPORTANT on Windows:** During install, check ✅ **"Add Python to PATH"**
4. Click Install

Verify it worked — open Command Prompt and type:
```
python --version
```
You should see something like `Python 3.11.4`

---

#### Ollama (needed for offline AI)

1. Go to **https://ollama.com/download**
2. Download for your system (Windows/Mac/Linux)
3. Run the installer — it's automatic
4. **Verify:** Open Command Prompt and type:
   ```
   ollama --version
   ```

---

#### Python Packages (all in one command)

The packages folder is already included in this kit. Install from it:

```bash
pip install --no-index --find-links=./packages pyftpdlib websockets flask flask-cors requests
```

Or if you still have internet, install normally:
```bash
pip install pyftpdlib websockets flask flask-cors requests
```

---

#### 3. Set Up the AI Model

You should have the file `qwen2.5-1.5b.gguf` in this folder.  
If not, download it now: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF

**Create the AI model (run once):**
```bash
# Open Command Prompt in this folder, then:
ollama create netbunker-ai -f Modelfile
```

Wait for it to finish (1–3 minutes). You'll see `success`.

Test it works:
```bash
ollama run netbunker-ai
```
Type a question, press Enter. Type `/bye` to exit.

---

## 🚀 Quick Start (5 minutes)

> Once everything above is installed, starting NetBunker is simple.

**Step 1 — Open Command Prompt** in the NetBunker folder

On Windows: Hold `Shift`, right-click inside the folder → "Open PowerShell window here"

**Step 2 — Start the web server:**
```bash
python scripts/serve_site.py
```

You'll see something like:
```
  NETWORK → http://192.168.1.5:8080
```

**Step 3 — Tell everyone that address.** Any phone or computer on the same WiFi can open it in their browser.

**That's it.** The full manual is now available to everyone on your network.

---

### To start ALL services at once (Windows):

Save this as `START-NETBUNKER.bat` and double-click it:

```bat
@echo off
echo Starting NetBunker...
start "Web Server"  python scripts\serve_site.py
start "FTP Server"  python scripts\ftp_server.py
start "Chat Server" python scripts\chat_server.py
echo.
echo =============================================
echo  NetBunker is running!
echo  Open your browser and go to:
echo  http://localhost:8080
echo =============================================
pause
```

### To start AI separately:

```bat
@echo off
set OLLAMA_HOST=0.0.0.0
start "Ollama AI" ollama serve
timeout /t 5
start "AI Proxy" python scripts\ollama_proxy.py
echo AI is starting... wait 30 seconds then open ollama_ui.html
pause
```

---

## 🤖 Setting Up the AI (Ollama)

The AI runs on **one computer** and all devices on the network can use it.

### Requirements for the AI computer:
| RAM | What you can run |
|-----|-----------------|
| 4 GB | qwen2.5:1.5b ✅ (included) |
| 6 GB | phi3:mini, gemma2:2b |
| 8 GB | mistral:7b, llama3:8b |
| 16 GB+ | llama3:70b (very smart) |

### Starting the AI:
```bash
# Step 1 — Start Ollama (exposed to your whole network)
# Windows CMD:
set OLLAMA_HOST=0.0.0.0
ollama serve

# Step 2 — In a NEW Command Prompt window:
python scripts/ollama_proxy.py
```

### Using the AI from another device:
1. Open `ui/ollama_ui.html` in any browser
2. Or go to `http://SERVER_IP:8080/ui/ollama_ui.html`
3. Enter the server's IP address
4. Port: `11435`
5. Select `netbunker-ai` and start chatting

> 💡 **What can the AI help with?** Medical questions, first aid, technical problems, cooking with limited ingredients, navigation, repairs, legal questions, translation, math, writing — anything you'd normally Google.

---

## 📱 Connecting Other Devices

### Android Phone / Tablet
1. Connect to the same WiFi as the server
2. Open Chrome or any browser
3. Go to: `http://SERVER_IP:8080`
4. That's it — full access to everything

### Another Windows/Linux Computer
Same as above — connect to WiFi, open browser, type the IP.

### iPhone / iPad
Same — connect to WiFi, open Safari, type the IP.

### No WiFi Router?
Your phone can BE the router:
- Android: Settings → Mobile Hotspot → Turn on
- Connect your computer to the phone's hotspot
- They are now on a local network together

---

## 📱 Recommended Offline Apps — Install Now!

> Install these on your phone and family members' phones **today**, while you have internet.

### 📤 File Sharing
| App | What it does | Platform |
|-----|-------------|----------|
| **LocalSend** ⭐ | Share files between any devices on WiFi — like AirDrop for everyone | Android, iPhone, Windows, Linux, Mac |
| **Snapdrop** | Browser-based file sharing, no app needed | Any browser |
| **Bluetooth File Transfer** | Share files without WiFi at all | Android |

**LocalSend is the most important one.** Download it now: https://localsend.org  
It lets you send photos, documents, and videos between your phone and any computer on the same WiFi — no internet, no accounts, completely free.

### 💬 Offline Communication
| App | What it does | Platform |
|-----|-------------|----------|
| **Briar** ⭐ | Encrypted chat over WiFi/Bluetooth/Tor. Works with NO internet | Android |
| **Meshtastic** | Chat over long-range LoRa radio (needs cheap hardware ~$20) | Android, iPhone |
| **Bridgefy** | Chat via Bluetooth mesh, no internet needed | Android, iPhone |

### 🗺️ Maps & Navigation
| App | What it does | Download |
|-----|-------------|----------|
| **OsmAnd** ⭐ | Full offline maps, navigation, POIs | Play Store / App Store |
| **Maps.me** | Simple offline maps | Play Store / App Store |
| **Google Maps** | Download your area offline | Built-in (see above) |
| **Organic Maps** | Clean, fast offline maps | Play Store / App Store |

### 📚 Knowledge & Reference
| App | What it does | Platform |
|-----|-------------|----------|
| **Kiwix** ⭐ | Full Wikipedia offline (20GB) + medical wikis, Stack Overflow | Android, Windows, Linux |
| **Wikipedia offline** | Download Wikipedia articles for your language | Android |
| **iFixit** | Device repair guides — download for offline | Android |
| **MyTherapy** | Medication reminders and tracker | Android, iPhone |

### 🏥 Medical
| App | What it does | Platform |
|-----|-------------|----------|
| **ICE Medical Standard** | Emergency medical info stored on your phone | Android, iPhone |
| **First Aid (Red Cross)** | Offline first aid guide | Android, iPhone |
| **Medscape** | Drug database, disease info — partially offline | Android, iPhone |

### 🔋 Utilities
| App | What it does | Platform |
|-----|-------------|----------|
| **Network Analyzer** | Find all devices and IPs on your network | Android |
| **Termux** | Full Linux terminal on Android — run Python scripts | Android (F-Droid) |
| **FX File Explorer** | FTP client + full file manager | Android |
| **Flashlight app** | Keep one that works offline | Any |

---

## 🗺️ Offline Maps — Very Important

**Do this for every family member's phone right now.**

### Priority download list:
- [ ] Your home neighborhood (detailed)
- [ ] Your city / town
- [ ] Routes to nearest hospital
- [ ] Routes to nearest pharmacy
- [ ] Your workplace area
- [ ] Family members' homes
- [ ] Nearest large supermarket / market
- [ ] Nearest fuel station
- [ ] Nearest police station / fire station
- [ ] If near a border — the route to safety

### Google Maps step by step:
```
1. Open Google Maps
2. Tap your profile photo (top right)
3. Tap "Offline maps"
4. Tap "Select your own map"
5. Zoom and drag to your area
6. Tap "Download"
7. Repeat for each important area
```

### Pro tip — OsmAnd for serious use:
OsmAnd lets you download an entire country for free. It includes:
- Every road and path
- Hospitals, pharmacies, shelters marked
- Works without ANY data connection
- No account needed
- Open source (free forever)

Download: https://osmand.net or search "OsmAnd" in Play Store

---

## 🌐 Services Overview

| Service | Port | Access | Purpose |
|---------|------|--------|---------|
| Web Server | 8080 | Browser → `http://IP:8080` | Manual, UIs, file browser |
| FTP Server | 2121 | File manager app | Upload/download files |
| Chat Server | 8765 | `chat_ui.html` in browser | Group chat, rooms |
| Ollama (internal) | 11434 | Server only | AI engine |
| Ollama Proxy | 11435 | `ollama_ui.html` in browser | AI for all devices |

### FTP Login details:
```
Username: survival
Password: offline123
Server:   YOUR_IP
Port:     2121
```

---

## 🔧 Troubleshooting

### ❌ "python is not recognized"
Python is not installed or not in PATH.
- Re-install Python from python.org
- **Check the box "Add Python to PATH"** during install
- Restart Command Prompt after installing

### ❌ "Other devices can't connect"
Windows Firewall is probably blocking. Run this in CMD as Administrator:
```
netsh advfirewall firewall add rule name="NetBunker" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="NetBunker FTP" dir=in action=allow protocol=TCP localport=2121
netsh advfirewall firewall add rule name="NetBunker Chat" dir=in action=allow protocol=TCP localport=8765
netsh advfirewall firewall add rule name="NetBunker AI" dir=in action=allow protocol=TCP localport=11435
```

### ❌ "ollama: command not found"
Restart your Command Prompt window after installing Ollama. If still broken:
- Windows: find it at `C:\Users\YOUR_NAME\AppData\Local\Programs\Ollama\ollama.exe`

### ❌ "AI is very slow"
Normal on CPU-only. Qwen2.5 1.5B takes about 10–30 seconds per response.
- Close other apps and browser tabs
- Responses get faster after the first one (model is cached in RAM)

### ❌ "No models found" in Ollama UI
Make sure you ran: `ollama create netbunker-ai -f Modelfile`  
And that ollama_proxy.py is running in a separate window.

### ❌ Can't find the server IP
Run this in CMD:
```
ipconfig
```
Look for "IPv4 Address" under your WiFi or Ethernet adapter. It starts with `192.168.` usually.

---

## ❓ FAQ (for Beginners)

**Q: Do I need technical skills to use this?**  
A: No. If you can follow these steps and type commands, you can run it. The hardest part is the first setup, which you do once now while you have internet.

**Q: What if I don't have electricity?**  
A: A phone hotspot + laptop on battery can keep the network running for hours. A powerbank keeps the phone going longer. A UPS (uninterruptible power supply) keeps your main computer running during short outages.

**Q: Can Android be the server?**  
A: Yes! Install Termux (from F-Droid), then run the Python scripts. Your phone becomes the server. It won't run Ollama AI though — that needs more RAM.

**Q: What is the range of this network?**  
A: As far as your WiFi router reaches — typically 20–50 meters indoors. With external antennas or multiple routers, much further. See Chapter 8 (Mesh Networking) in the manual.

**Q: Can I use this without a router?**  
A: Yes. Any phone's hotspot creates a local network. Connect all devices to that hotspot. Your phone is the router.

**Q: How do I update the AI's knowledge?**  
A: You can't add new training data, but you can edit the `SYSTEM` section in `Modelfile` to change its personality and focus areas. Re-run `ollama create netbunker-ai -f Modelfile` after changes.

**Q: Is this secure?**  
A: It's designed for trusted local networks (your home, your group). Don't run it exposed to the internet. FTP passwords are sent in plain text — fine locally, not fine over internet.

**Q: What's the minimum hardware to run this?**  
A: Any computer made after 2010 with 4GB RAM can run the web, FTP, and chat servers. 4GB+ RAM is needed for the AI (Qwen2.5 1.5B). A Raspberry Pi 4 (4GB) can run everything.

---

## 💡 General Survival Advice

> These suggestions cost nothing and could make a huge difference.

### 📥 Download before you need it
- [ ] Offline maps of everywhere you go regularly
- [ ] Kiwix + Wikipedia in your language (survival knowledge)
- [ ] This kit on every household computer and family member's phone
- [ ] PDF copies of important documents (ID, passport, insurance)
- [ ] First aid guide (Red Cross app or PDF)
- [ ] Your country's emergency frequency guide (HAM/CB radio)

### 🔋 Power planning
- A **powerbank** (20,000 mAh+) keeps phones running for days
- A **UPS** keeps your main computer running through short outages
- A **solar panel + battery** (available cheaply) keeps everything going indefinitely
- Know where your building's circuit breaker is

### 📞 Communication without internet
- **SMS and calls** still work without internet (while cell towers are up)
- **Walkie-talkies** work completely independently — buy a pair
- **Meshtastic LoRa devices** (~$25 each) create a mesh that spans kilometers
- Write down important phone numbers — don't rely on your phone being charged

### 🏠 Tell people about this
The whole point of a local network is that multiple people use it. Install this kit and tell your neighbors, family, and colleagues where to connect. The more people prepared, the more resilient your community is.

---

## 🙏 Contributing

Contributions welcome! Ideas for improvement:
- More languages in the manual
- Better mobile UI
- DNS server script (currently manual)
- Automatic network discovery
- Encrypted chat option

Open an issue or submit a pull request.

---

## 📜 License

**NetBunker scripts and UI:** MIT License — free to use, modify, and share.  
**Qwen2.5 model:** Qwen License by Alibaba Cloud — free for personal and research use.  
**No warranty.** Use responsibly. Designed for legitimate emergency preparedness only.

---

<div align="center">

**Stay connected. Stay informed. Stay safe.**  
*Built for the worst days. Tested for everyday use.*

⭐ Star this repo if it helped you — it helps others find it.

</div>
