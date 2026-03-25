╔══════════════════════════════════════════════════════════════════╗
║   NetBunker — AI MODEL FILE NOT INCLUDED                        ║
║   Download required before using the AI feature                 ║
╚══════════════════════════════════════════════════════════════════╝

  WHY IS THE MODEL NOT HERE?
  ─────────────────────────────────────────────────────────────────
  GitHub has a 100 MB file size limit.
  The AI model file (qwen2.5-1.5b.gguf) is ~986 MB (about 1 GB).
  It cannot be included in this repository.

  You need to download it ONCE and place it in THIS folder.


  WHAT TO DOWNLOAD
  ─────────────────────────────────────────────────────────────────
  File name  :  qwen2.5-1.5b.gguf  (or any Q4/Q5 variant)
  Size       :  ~986 MB
  From       :  https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/main


  HOW TO DOWNLOAD (step by step)
  ─────────────────────────────────────────────────────────────────

  STEP 1 — Open this link in your browser:
    https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/main

  STEP 2 — You will see a list of files. Look for:
    qwen2.5-1.5b-instruct-q4_k_m.gguf   ← RECOMMENDED (best balance)
    qwen2.5-1.5b-instruct-q5_k_m.gguf   ← Better quality, slightly larger
    qwen2.5-1.5b-instruct-q8_0.gguf     ← Best quality, needs more RAM

    If unsure → download  q4_k_m  (smallest, works on 4GB RAM)

  STEP 3 — Click the filename → click the ⬇ Download button

  STEP 4 — Save/move the downloaded .gguf file into THIS folder:
    NetBunker\
    └── {scripts,ui,config,assets}\
        └── qwen2.5-1.5b.gguf    ← place it HERE


  AFTER DOWNLOADING — LOAD INTO OLLAMA
  ─────────────────────────────────────────────────────────────────

  Make sure Ollama is installed first:
    https://ollama.com/download

  Then open Command Prompt in the NetBunker root folder:

    cd D:\path\to\NetBunker
    ollama create netbunker-ai -f Modelfile

  Wait for it to finish (1–3 minutes). You will see: "success"

  Test it:
    ollama run netbunker-ai

  To start AI for the whole network:
    set OLLAMA_HOST=0.0.0.0
    ollama serve

  Then in a second CMD window:
    python scripts\ollama_proxy.py

  Then open  ui\ollama_ui.html  in any browser.


  FILE SIZE COMPARISON (choose based on your RAM)
  ─────────────────────────────────────────────────────────────────

  Variant         Size      Min RAM   Quality
  ─────────────────────────────────────────────────────────────────
  q4_k_m          ~986 MB   4 GB      Good  ← Start here
  q5_k_m          ~1.1 GB   4 GB      Better
  q5_k_s          ~1.1 GB   4 GB      Better
  q8_0            ~1.6 GB   6 GB      Best (for this model size)
  ─────────────────────────────────────────────────────────────────

  All variants of Qwen2.5-1.5B are small enough to run on most
  computers and laptops made after 2015 with 4GB+ RAM.


  ALTERNATIVE MODELS (also work with Modelfile)
  ─────────────────────────────────────────────────────────────────
  If you want a different AI model, these also work great offline:

  Model             Link
  ──────────────────────────────────────────────────────────────────
  Gemma2 2B         https://huggingface.co/google/gemma-2-2b-it-GGUF
  Phi-3 Mini        https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
  Llama 3.2 1B      https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct-GGUF
  TinyLlama 1.1B    https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF

  After downloading any .gguf, update the first line of Modelfile:
    FROM ./your-model-filename.gguf
  Then re-run:
    ollama create netbunker-ai -f Modelfile


  DOWNLOAD WITH COMMAND LINE (faster for large files)
  ─────────────────────────────────────────────────────────────────

  Windows PowerShell:
    Invoke-WebRequest -Uri "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf" -OutFile "qwen2.5-1.5b.gguf"

  Linux / Mac / Termux:
    wget "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf" -O qwen2.5-1.5b.gguf

  Or install huggingface-hub and use:
    pip install huggingface-hub
    huggingface-cli download Qwen/Qwen2.5-1.5B-Instruct-GGUF qwen2.5-1.5b-instruct-q4_k_m.gguf --local-dir .


╔══════════════════════════════════════════════════════════════════╗
║  Once downloaded, this folder should contain:                   ║
║                                                                  ║
║  {scripts,ui,config,assets}\                                    ║
║  └── qwen2.5-1.5b.gguf        ← the model you just downloaded  ║
║  └── DOWNLOAD_MODEL.txt       ← this file                       ║
╚══════════════════════════════════════════════════════════════════╝
