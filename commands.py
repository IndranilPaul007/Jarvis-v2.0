import os
import subprocess
import requests
import shutil
import base64
import io
from datetime import datetime
from urllib.parse import quote
from PIL import ImageGrab
from config import APP_MAPPING, CLOSE_MAPPING, OLLAMA_URL, VISION_MODEL

# -----------------------------------------------------------------------------
# 🛠️ UNIVERSAL AUTOMATION UTILITIES & VISUAL CORTEX
# -----------------------------------------------------------------------------

def analyze_screen_context(query: str = "Describe what is on the screen.") -> str:
    """Takes a silent screenshot, resizes it for speed, and sends it to the vision model."""
    try:
        print("📸 [Vision Engine]: Capturing screen frame...")
        screenshot = ImageGrab.grab()
        
        # 🔧 Downscale to max 720p bounding box to shrink the network payload size by 80%
        screenshot.thumbnail((1280, 720))
        
        buffered = io.BytesIO()
        screenshot.save(buffered, format="JPEG", quality=75)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        print(f"🧠 [Vision Engine]: Sending frame to {VISION_MODEL} for analysis...")
        
        payload = {
            "model": VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": query,
                    "images": [img_str]
                }
            ],
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        
        result_text = response.json().get("message", {}).get("content", "I could not analyze the image.")
        return f"Visual Analysis Complete: {result_text}"

    except Exception as e:
        return f"Failed to execute visual analysis pipeline: {e}"


def report_utility_count() -> str:
    """Returns the total number of primary tools currently registered in the manifest."""
    total_tools = len(TOOLS_MANIFEST)
    return f"I currently have exactly {total_tools} master utility channels fully operational and registered in my system manifest, Boss."


def play_spotify_media(search_query: str) -> str:
    """Uses the Windows URI scheme to launch Spotify and directly execute a media search query."""
    if not search_query or not search_query.strip():
        return "Please specify a song, artist, or album title for me to play."
    
    try:
        safe_query = quote(search_query.strip())
        os.system(f"start spotify:search:{safe_query}")
        return f"Executing local media override. Launching Spotify client and playing: {search_query}."
    except Exception as e:
        return f"Failed to interface with the local Spotify media pipeline: {e}"


def execute_universal_app(app_name: str) -> str:
    """Universal application launcher. Tries known aliases first, then attempts raw system execution."""
    target = app_name.lower().strip()
    
    if target in APP_MAPPING:
        cmd = APP_MAPPING[target]
    else:
        cmd = f"start {target}"
        
    try:
        subprocess.Popen(cmd, shell=True)
        return f"System command executed successfully. Initializing application/task: '{target}'."
    except Exception as e:
        return f"Failed to universally launch the requested process: {e}"


def terminate_universal_app(app_name: str) -> str:
    """Universal process killer. Attempts to force-terminate any application window or process name."""
    target = app_name.lower().strip()
    
    if target in CLOSE_MAPPING:
        cmd = CLOSE_MAPPING[target]
    else:
        if not target.endswith(".exe"):
            cmd = f"taskkill /f /im {target}.exe"
        else:
            cmd = f"taskkill /f /im {target}"
            
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        if "SUCCESS" in stdout or process.returncode == 0:
            return f"Successfully sent termination signals. Process '{target}' has been stopped."
        return f"System executed termination routine for '{target}', but the process may not be actively running."
    except Exception as e:
        return f"Error encountered during process termination loop: {e}"


def manage_software_packages(action: str, package_name: str) -> str:
    """Uses the native Windows Package Manager (winget) to install or uninstall any desktop application."""
    target_action = action.lower().strip()
    target_package = package_name.strip()
    
    if not target_package:
        return "Package target validation failed. I need a clear application name."
        
    if not shutil.which("winget"):
        return "The Windows Package Manager ('winget') was not detected on this machine's environment path."
        
    try:
        if target_action == "install":
            cmd = f"winget install {target_package} --silent --accept-source-agreements --accept-package-agreements"
            subprocess.Popen(cmd, shell=True)
            return f"Deployment pipeline initialized. Downloading and installing '{target_package}' quietly in the background, Boss."
            
        elif target_action == "uninstall":
            cmd = f"winget uninstall {target_package} --silent"
            subprocess.Popen(cmd, shell=True)
            return f"Removal pipeline initialized. Uninstalling '{target_package}' cleanly from the local machine."
            
        return f"Package operation action '{action}' is completely unsupported."
    except Exception as e:
        return f"Package management subsystem failure: {e}"


def handle_browser_tabs(action: str, url: str = "") -> str:
    """Manages browser windows explicitly through Google Chrome to prevent OS defaults hijacking execution."""
    target_action = action.lower().strip()
    
    try:
        if target_action == "open":
            if not url:
                return "I need a valid destination web address to launch a new tab."
            parsed_url = url.strip()
            if not parsed_url.startswith(("http://", "https://")):
                parsed_url = "https://" + parsed_url
            
            # 🔧 Forces Google Chrome instead of OS defaults
            subprocess.Popen(f"start chrome {parsed_url}", shell=True)
            return f"Routing request to browser engine. Opening tab destination: {parsed_url}."
            
        elif target_action == "close":
            return terminate_universal_app("chrome")
            
        return f"Browser tab action '{action}' unrecognized."
    except Exception as e:
        return f"Browser pipeline disruption: {e}"


def get_system_time_date(context_type: str = "time") -> str:
    """Fetches the current system time or date string."""
    now = datetime.now()
    if "date" in context_type.lower():
        return f"Today's date is {now.strftime('%d %B %Y')}."
    return f"The current system time is {now.strftime('%H:%M')}."


def fetch_live_weather(city: str = "Raiganj") -> str:
    """Pulls current real-time weather and temperature metrics for a specified city location."""
    if not city or not city.strip():
        city = "Raiganj"
        
    safe_city = quote(city.strip())
    try:
        url = f"https://wttr.in/{safe_city}"
        response = requests.get(url, headers={"User-Agent": "curl"}, params={"format": "3"}, timeout=5)
        if response.status_code == 200 and "<html" not in response.text.lower():
            return f"Weather update for {city}: {response.text.strip()}"
        return f"Could not pull clean weather data updates for {city} right now."
    except Exception:
        return "Weather backend system timed out."


def search_internet_query(query_string: str) -> str:
    """Executes a Google Search engine query string explicitly forcing Google Chrome execution."""
    try:
        safe_query = quote(query_string.strip())
        target_url = f"https://google.com/search?q={safe_query}"
        
        # 🔧 Forces Google Chrome instead of OS defaults
        subprocess.Popen(f"start chrome {target_url}", shell=True)
        return f"Searching live internet databases for: {query_string}."
    except Exception as e:
        return f"Search routing error encountered: {e}"


def control_system_power(action: str) -> str:
    """Manages local Windows environment states including workstation locking and power suspend routines."""
    target_action = action.lower().strip()
    try:
        if target_action == "lock":
            subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
            return "System security lock engaged successfully."
        elif target_action == "sleep":
            subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
            return "Placing active computational hardware array into sleep standby."
        return f"Action directive '{action}' was not processed."
    except Exception as e:
        return f"Failed to execute environment state transition tool: {e}"


def manage_local_notes(action: str, note_content: str = "") -> str:
    """Provides file read, overwrite, and append actions to handle an integrated workspace scratchpad log."""
    file_path = os.path.join(os.getcwd(), "jarvis_notes.txt")
    target_action = action.lower().strip()
    try:
        if target_action == "read":
            if not os.path.exists(file_path):
                return "The current workspace notes file is completely empty."
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            return f"Current Saved Notes Content:\n{content}" if content else "The scratchpad file exists but contains zero text entries."
        elif target_action == "append":
            if not note_content: return "Note payload was empty."
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"\n{timestamp} {note_content.strip()}")
            return "Information appended successfully to local notes storage."
        elif target_action == "write":
            if not note_content: return "Note payload was empty."
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(note_content.strip())
            return "Workspace scratchpad overwritten successfully."
        return f"Action query type '{action}' unrecognized."
    except Exception as e:
        return f"Local disk storage I/O pipeline failure: {e}"

# -----------------------------------------------------------------------------
# ⚙️ UNRESTRICTED TOOL SCHEMAS MANIFEST
# -----------------------------------------------------------------------------

TOOLS_MANIFEST = [
    {
        "type": "function",
        "function": {
            "name": "analyze_screen_context",
            "description": "Trigger this tool whenever the user asks you to 'look at this', 'what is on my screen', 'read this error', or asks a question about something they are currently looking at on their monitor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The specific question the user is asking about the screen."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "report_utility_count",
            "description": "Call this tool whenever the user asks how many tools, utilities, functions, or capabilities you have.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_spotify_media",
            "description": "Directly search and play specific songs, music tracks, artists, or playlists on Spotify.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {"type": "string", "description": "The name of the song, artist, or music track to play."}
                },
                "required": ["search_query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_universal_app",
            "description": "Launch ANY application, game, program, or background task installed on this Windows laptop using its name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "The name or command of the system program to launch (e.g., chrome, code, vlc, discord)."}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "terminate_universal_app",
            "description": "Close, kill, or force-stop ANY running desktop program, window, or background application task on this machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "The name of the program window or process executable to kill (e.g., chrome, spotify, notepad)."}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "manage_software_packages",
            "description": "Download, install, or uninstall application programs directly to/from the Windows machine via the package manager engine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["install", "uninstall"], "description": "Choose whether to install or uninstall a software."},
                    "package_name": {"type": "string", "description": "The name of the application software to manage (e.g., vlc, git, zoom, steam)."}
                },
                "required": ["action", "package_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_browser_tabs",
            "description": "Open a brand new web tab with a destination link, or close active web browser processing loops.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["open", "close"], "description": "Whether to open a new tab or close browser windows."},
                    "url": {"type": "string", "description": "The web target link to open. Required if action is open."}
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_time_date",
            "description": "Get the current time or current calendar date information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "context_type": {"type": "string", "enum": ["time", "date"]}
                },
                "required": ["context_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_live_weather",
            "description": "Fetch real-time weather information for any specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_internet_query",
            "description": "Universally search the internet for live news, real-time events, definitions, articles, or arbitrary inquiries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_string": {"type": "string", "description": "The search parameters query phrase to send to Google."}
                },
                "required": ["query_string"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_system_power",
            "description": "Modify hardware power states (lock screen or sleep device).",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["lock", "sleep"]}
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "manage_local_notes",
            "description": "Handle reading, writing, or appending to your integrated notes storage scratchpad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["read", "write", "append"]},
                    "note_content": {"type": "string"}
                },
                "required": ["action"]
            }
        }
    }
]

# -----------------------------------------------------------------------------
# 🔀 DYNAMIC EXECUTION ROUTER MAP
# -----------------------------------------------------------------------------

TOOLS_EXECUTION_ROUTER = {
    "analyze_screen_context": analyze_screen_context,
    "report_utility_count": report_utility_count,
    "play_spotify_media": play_spotify_media,
    "execute_universal_app": execute_universal_app,
    "terminate_universal_app": terminate_universal_app,
    "manage_software_packages": manage_software_packages,
    "handle_browser_tabs": handle_browser_tabs,
    "get_system_time_date": get_system_time_date,
    "fetch_live_weather": fetch_live_weather,
    "search_internet_query": search_internet_query,
    "control_system_power": control_system_power,
    "manage_local_notes": manage_local_notes
}
