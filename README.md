<h1 align="center">🤖 Jarvis v2.0</h1>

<p align="center">
  <strong>A local-first, screen-aware Windows desktop agent powered by Ollama.</strong>
</p>

<p align="center">
  Use natural language to control apps, inspect what is on your screen, play music, and automate everyday desktop tasks—without paid AI API keys.
</p>

<p align="center">
  <img src="Jarvis v2.0 complete.gif" width="100%" alt="Jarvis v2.0 demo: local AI desktop agent" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge" alt="Project status: active" />
  <img src="https://img.shields.io/badge/engine-Qwen%202.5%203B-blue?style=for-the-badge" alt="Qwen 2.5 3B" />
  <img src="https://img.shields.io/badge/vision-MiniCPM--V-purple?style=for-the-badge" alt="MiniCPM-V" />
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=for-the-badge" alt="Windows" />
  <img src="https://img.shields.io/badge/API%20keys-none-success?style=for-the-badge" alt="No paid API keys required" />
</p>

> **What makes Jarvis different?** It is a local-first Windows agent that can reason over voice input, call desktop tools, and analyze your screen with local Ollama models.

## ✨ What Jarvis can do

- **Reason and act** — converts natural-language requests into tool calls using a local Qwen model.
- **See your screen** — captures and analyzes visible UI, text, and error messages with MiniCPM-V.
- **Control Windows apps** — opens applications and manages selected desktop processes.
- **Play music** — searches and opens tracks in the Spotify desktop app through Spotify URIs.
- **Browse with Chrome** — performs targeted searches and navigation in Google Chrome.
- **Listen and speak** — combines local speech-to-text with asynchronous text-to-speech.
- **Manage software** — can use Windows Package Manager (`winget`) for package operations.

## 🎬 Try these commands

~~~text
"Jarvis, look at my screen. What error is showing here?"
"Open Visual Studio Code and Google Chrome."
"Jarvis, play Judas by Lady Gaga."
"How many tools do you currently have registered?"
~~~

## 🧠 How it works

~~~text
Voice / text input
      ↓
Qwen 2.5 via Ollama → tool selection → Windows / Chrome / Spotify actions
      ↓                                      ↑
faster-whisper + MiniCPM-V ──────────────────┘
~~~

| Component | Technology | Purpose |
| --- | --- | --- |
| Agent brain | Qwen 2.5:3B Instruct | Reasoning and tool selection |
| Visual cortex | MiniCPM-V | Screen analysis and OCR |
| Speech-to-text | faster-whisper | Voice input |
| Voice output | edge-tts | Spoken responses |
| Runtime | Python 3.10+ / Windows | Desktop automation |

## 🚀 Quick start

### Requirements

- Windows 10 or 11
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- A microphone for voice commands
- An NVIDIA RTX GPU is recommended for responsive local vision; CPU execution may be slower
- Optional: Spotify desktop app, Google Chrome, and `winget` for their respective integrations

### Install

~~~bash
git clone https://github.com/IndranilPaul007/Jarvis-v2.0.git
cd Jarvis-v2.0

ollama pull qwen2.5:3b-instruct
ollama pull minicpm-v

pip install -r requirements.txt
~~~

Start Ollama in one terminal:

~~~bash
ollama serve
~~~

Then start Jarvis in another:

~~~bash
python main.py
~~~

## ⚠️ Permissions and privacy

Jarvis is **local-first**: its models run through your local Ollama installation and it does not require paid AI API keys. Some optional capabilities—such as web search, Spotify, weather, package management, and cloud-backed text-to-speech—may use external services or require an internet connection.

Jarvis can launch apps, manage processes, and invoke `winget`. Review requests carefully and run it only on a machine you control. Never use it to install unknown software or execute actions you do not understand.

## 📁 Project structure

~~~text
Jarvis-v2.0/
├── main.py          # Asynchronous app entry point
├── brain.py         # Agent loop and tool-execution router
├── commands.py      # Windows utilities and tool definitions
├── config.py        # Models, endpoints, and application settings
├── listen.py        # Audio-input handling
├── voice.py         # Text-to-speech handling
└── requirements.txt # Python dependencies
~~~

## 🛣️ Roadmap

- [ ] Safer confirmations and a dry-run mode for system-changing tools
- [ ] Guided setup and diagnostics
- [ ] More app integrations and user-contributed tools
- [ ] Automated tests and CI
- [ ] Support for additional local models and hardware profiles

## 🤝 Contributing

Ideas, bug reports, documentation improvements, and new tools are welcome. Please open an issue describing the use case, your environment, and the expected behavior before submitting a large change.

## 📄 License

This project is released under the repository's [LICENSE](LICENSE).

---

If Jarvis helps you, consider giving the repository a ⭐. It helps more people discover local-first AI tooling.
