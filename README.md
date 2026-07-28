<h1 align="center">🤖 Jarvis v2.0</h1>

<p align="center">
  <b>A local, asynchronous AI agent assistant powered by Qwen 2.5 & Vision Core</b>
</p>

<p align="center">
  <img src="jarvis-v20-video_compressed-gif-optimized.gif" width="100%" alt="Jarvis v2.0 Demo" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Engine-Qwen--2.5--3B-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Vision-MiniCPM--V-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Privacy-100%25_Local-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge" />
</p>

---

### 🚀 Overview
**Jarvis v2.0** is an autonomous, agentic AI desktop assistant designed to run entirely locally on consumer-grade hardware (optimized for NVIDIA RTX GPUs). Moving away from rigid, hardcoded scripts, Jarvis uses a **dynamic tool-calling architecture** that allows him to interpret natural user intent and execute complex local system operations, browse the web, play media, and even "see" your screen natively.

---

### ✨ Key Capabilities
* **🧠 Agentic Dynamic Reasoning:** Uses function-calling loops via local Ollama models to bridge natural language requests directly to system actions.
* **👁️ Visual Cortex (Screen Awareness):** Equipped with `minicpm-v` to capture, resize, and analyze your monitor in real time to read errors, text, or UI elements.
* **🎵 Direct Media Playback:** Automatically hooks into the local Spotify desktop app via URI protocols to search and play tracks on demand.
* **💻 Universal OS Control:** 
  * Launch or force-terminate *any* application or background process on your machine.
  * Silently install or uninstall software packages via the native Windows Package Manager (`winget`).
* **🌐 Isolated Browser Automation:** Controls Google Chrome specifically for web searches and navigation, bypassing default browser conflicts.
* **🎙️ Voice-Activated Pipeline:** Listens passively through local Whisper acoustic models and responds using asynchronous text-to-speech engines.
* **🔒 100% Local Privacy:** Zero cloud telemetry, zero API keys required, and full offline functionality.

---

### 🛠 Tech Stack & Architecture

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Primary Brain** | `Qwen 2.5:3b-instruct` | Core logic, reasoning, and tool selection |
| **Visual Cortex** | `minicpm-v` | High-speed local OCR and screen analysis |
| **Acoustic Engine** | `faster-whisper` | Local real-time speech-to-text conversion |
| **Voice Output** | `edge-tts` | High-fidelity synthetic speech synthesis |
| **Environment** | Python 3.10+ / Windows | Native OS automation wrapper (`subprocess`, `PIL`) |

---

### 📂 Project Structure
```text
Jarvis-v2.0/
│
├── main.py              # Main asynchronous event loop & orchestration
├── brain.py             # Core cognitive loop & dynamic tool execution router
├── commands.py          # Universal system utilities & tool manifests
├── config.py            # System parameters, app registries, and model endpoints
├── requirements.txt     # Complete Python package dependency manifest
└── README.md            # Project documentation
```

### 📦 Quick Start Guide

1. Prerequisites
Ollama installed locally on your machine (Download Ollama).
Pull the required local models in your terminal:
```bash
ollama pull qwen2.5:3b-instruct
ollama pull minicpm-v
```

2. Clone the Repository
```bash
git clone [https://github.com/IndranilPaul007/Jarvis-v2.0.git](https://github.com/IndranilPaul007/Jarvis-v2.0.git)
cd Jarvis-v2.0
```

3. Install Python Dependencies
Install all required packages (including PyAudio/SoundDevice and Imaging tools via pillow):
```bash
pip install -r requirements.txt
```

4. Boot Up Jarvis
Open a terminal window and start the Ollama backend server bound to local IPv4:
```bash
ollama serve
```
Open a second terminal window, navigate to the project directory, and launch Jarvis:
```bash
python main.py
```

💡 Example Voice Commands
"Jarvis, play Judas by Lady Gaga."

"What is the weather like in Kolkata?"

"Jarvis, look at my screen. What error is showing here?"

"Open Visual Studio Code and Google Chrome."

"Install vlc quietly in the background."

"How many tools do you currently have registered?"

🌐 Repository Link & Git Clone
To clone or access the repository directly:

```bash
git clone https://github.com/IndranilPaul007/Jarvis-v2.0.git
```

