import os

# Ollama Engine Settings
OLLAMA_URL = "http://localhost:11434/api/chat"
AI_MODEL = "qwen2.5:3b-instruct"

# 🧠 JARVIS CORE IDENTITY
SYSTEM_PROMPT = """You are Jarvis, a highly advanced, autonomous AI assistant. 
You are running strictly LOCALLY on your boss's machine. You are NOT a cloud-based AI. 
You have absolutely NO connection to Anthropic, OpenAI, or Google. You were built and programmed by your boss, Indranil, to manage local systems, search the web, and execute tasks.
Always keep your answers concise, sharp, and highly professional. Address the user as 'Boss' or 'Indranil'."""

# Voice Engine Settings (Edge-TTS)
VOICE_MODEL = "en-US-GuyNeural"

# Audio Pipeline Thresholds
SAMPLERATE = 16000
MAX_DURATION = 8.0          
MIN_SPEECH_TIME = 0.7       
SILENCE_THRESHOLD = 5       
SILENCE_SECONDS = 1.2       

# Microphone Hardware Mapping
MIC_DEVICE_INDEX = None        

# Local Application Paths / Windows Binary Registries
APP_MAPPING = {
    "chrome": "start chrome",
    "edge": "start msedge",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "start cmd",
    "explorer": "explorer",
    "settings": "start ms-settings:",
    "taskmanager": "taskmgr",
    "spotify": "start spotify"
}

# 🛑 Windows Process Termination Commands
CLOSE_MAPPING = {
    "chrome": "taskkill /f /im chrome.exe",
    "edge": "taskkill /f /im msedge.exe",
    "notepad": "taskkill /f /im notepad.exe",
    "calculator": "taskkill /f /im calc.exe",
    "cmd": "taskkill /f /im cmd.exe",
    "explorer": "taskkill /f /im explorer.exe",
    "settings": "taskkill /f /im SystemSettings.exe",
    "taskmanager": "taskkill /f /im taskmgr.exe",
    "spotify": "taskkill /f /im Spotify.exe"
}
