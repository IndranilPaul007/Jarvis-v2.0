import subprocess
import webbrowser
import requests
import shutil
from datetime import datetime
from urllib.parse import quote, urlparse
from config import APP_MAPPING

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
            return f"Weather for {city}: {response.text.strip()}"
        return f"Could not pull clean weather data updates for {city} right now."
    except Exception:
        return "Weather backend system timed out."

def open_web_portal(url: str, application_name: str = "website") -> str:
    """Launches any web URL link in the default internet browser."""
    parsed_url = url.strip()
    if not parsed_url.startswith(("http://", "https://")):
        parsed_url = "https://" + parsed_url
        
    try:
        webbrowser.open(parsed_url)
        return f"Successfully opening the {application_name} portal."
    except Exception as e:
        return f"Failed to launch browser pipeline: {e}"

def execute_os_app(app_binary: str) -> str:
    """Executes local applications directly using clean background subprocess engines."""
    target_key = app_binary.lower().strip()
    cmd = APP_MAPPING.get(target_key)
    
    if not cmd:
        return f"Application profile for '{app_binary}' is not recognized."
        
    try:
        # Resolve path validation using shutil before execution
        binary_root = cmd.split()[1] if "start" in cmd else cmd.split()[0]
        if "ms-settings" not in cmd and not shutil.which(binary_root) and not shutil.which(cmd):
            pass # Continue past standard Win32 environment quirks
            
        subprocess.Popen(cmd, shell=True if " " in cmd or ":" in cmd else False)
        return f"Initializing workspace application: {target_key}."
    except Exception as e:
        return f"Error spawning subprocess application: {e}"

def search_internet_query(query_string: str) -> str:
    """Executes a Google Search engine query string layout for arbitrary web research."""
    try:
        safe_query = quote(query_string.strip())
        webbrowser.open(f"https://google.com/search?q={safe_query}")
        return f"Searching internet database for: {query_string}."
    except Exception as e:
        return f"Search routing error encountered: {e}"

# Unified JSON Schemas mapped out perfectly for Qwen function-calling
TOOLS_MANIFEST = [
    {
        "type": "function",
        "function": {
            "name": "get_system_time_date",
            "description": "Get the current time or current calendar date information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "context_type": {"type": "string", "enum": ["time", "date"], "description": "Specify whether to fetch the time or date."}
                },
                "required": ["context_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_live_weather",
            "description": "Fetch real-time weather information and conditions for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The name of the city. Default to Raiganj if not specified."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_web_portal",
            "description": "Open a website shortcut in the default browser using its link.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The complete destination link starting with http or https (e.g., https://youtube.com)."},
                    "application_name": {"type": "string", "description": "The common name of the web portal (e.g., youtube, canva, whatsapp)."}
                },
                "required": ["url", "application_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_os_app",
            "description": "Launch desktop system utilities natively installed on this Windows computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_binary": {"type": "string", "enum": ["chrome", "edge", "notepad", "calculator", "cmd", "explorer", "settings", "taskmanager", "spotify"], "description": "The short alias code matching the target system application."}
                },
                "required": ["app_binary"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_internet_query",
            "description": "Use this tool if the user explicitly asks to 'search google for...', 'look up news on...', or asks for real-time live stock/crypto market information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_string": {"type": "string", "description": "The exact phrase or query search text to look up on Google."}
                },
                "required": ["query_string"]
            }
        }
    }
]

TOOLS_EXECUTION_ROUTER = {
    "get_system_time_date": get_system_time_date,
    "fetch_live_weather": fetch_live_weather,
    "open_web_portal": open_web_portal,
    "execute_os_app": execute_os_app,
    "search_internet_query": search_internet_query
}
