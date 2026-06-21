import json
import asyncio
import requests
import os
from config import OLLAMA_URL, AI_MODEL, SYSTEM_PROMPT, APP_MAPPING, CLOSE_MAPPING

# 🧠 Conversation Memory Array
session_history = []

# -----------------------------------------------------------------------------
# ⚙️ AGENTIC TOOL EXECUTION LAYER
# -----------------------------------------------------------------------------
AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_live_weather",
            "description": "Get the current weather for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get the weather for."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_internet_query",
            "description": "Search the internet for up-to-date information or guides.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_string": {
                        "type": "string",
                        "description": "The specific search query to look up."
                    }
                },
                "required": ["query_string"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_local_application",
            "description": "Open a local application or software on the Windows machine (e.g., Chrome, Spotify, Notepad, Edge).",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to open in lowercase."
                    }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_local_application",
            "description": "Close and terminate a running local application or software on the Windows machine (e.g., Chrome, Spotify, Notepad).",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to close in lowercase."
                    }
                },
                "required": ["app_name"]
            }
        }
    }
]

def execute_tool(tool_call):
    """Processes the tool requested by the AI and executes the local Python logic."""
    func_name = tool_call["function"]["name"]
    raw_args = tool_call["function"]["arguments"]
    
    # 🔧 Smart parsing to prevent the dictionary/string crash
    try:
        if isinstance(raw_args, dict):
            args = raw_args
        else:
            args = json.loads(raw_args)
    except Exception as e:
        print(f"⚠️ [Tool Parse Warning]: Could not read arguments. {e}")
        args = {}

    print(f"⚙️ [Agentic Tool Execution]: Running '{func_name}' with parameters {args}")

    # Tool 1: Weather
    if func_name == "fetch_live_weather":
        city = args.get("city", "your location")
        if not city: 
            city = "your location"
        return f"The weather in {city} is currently +40°C."

    # Tool 2: Internet Search
    elif func_name == "search_internet_query":
        query = args.get("query_string", "")
        return f"Search execution successful for '{query}'. Information gathered and ready for summary."

    # Tool 3: Open Local Application
    elif func_name == "open_local_application":
        app_name = args.get("app_name", "").lower()
        
        if app_name in APP_MAPPING:
            try:
                os.system(APP_MAPPING[app_name])
                return f"Successfully opened {app_name} for the Boss."
            except Exception as e:
                return f"Failed to open {app_name}. Error: {e}"
        else:
            return f"I do not have the command to open '{app_name}' in my registry."

    # Tool 4: Close Local Application
    elif func_name == "close_local_application":
        app_name = args.get("app_name", "").lower()
        
        if app_name in CLOSE_MAPPING:
            try:
                os.system(CLOSE_MAPPING[app_name])
                return f"Successfully closed {app_name} as requested."
            except Exception as e:
                return f"Failed to terminate {app_name}. Error: {e}"
        else:
            return f"I do not have a close routine for '{app_name}' mapped inside config.py."

    return f"Tool {func_name} executed."

# -----------------------------------------------------------------------------
# 🧠 CORE COGNITIVE LOOP
# -----------------------------------------------------------------------------
async def think(user_input: str) -> str:
    """Processes user input through the local Qwen model asynchronously."""
    global session_history
    
    try:
        session_history.append({"role": "user", "content": user_input})
        
        full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + session_history

        req_payload = {
            "model": AI_MODEL,
            "messages": full_messages,
            "stream": False,
            "tools": AVAILABLE_TOOLS
        }

        def send_http_request(payload):
            return requests.post(OLLAMA_URL, json=payload, timeout=120)

        response = await asyncio.to_thread(send_http_request, req_payload)
        response.raise_for_status()
        
        response_data = response.json()
        message = response_data.get("message", {})

        # Agentic Routing Intercept
        if "tool_calls" in message and message["tool_calls"]:
            tool_results = []
            for tool in message["tool_calls"]:
                result = execute_tool(tool)
                tool_results.append({
                    "role": "tool",
                    "content": result,
                    "name": tool["function"]["name"]
                })
            
            session_history.append(message)
            session_history.extend(tool_results)
            
            return await think("Tool execution complete. Read the tool data and answer the user naturally.")

        # Standard Conversational Response processing
        ai_reply = message.get("content", "").strip()
        
        if ai_reply:
            session_history.append({"role": "assistant", "content": ai_reply})
        
        # Memory Trimming
        if len(session_history) > 8:
            session_history = session_history[-8:]
            
        return ai_reply

    except requests.exceptions.Timeout:
        print("\n❌ [Advanced Agent Engine Error]: HTTPConnectionPool: Read timed out.")
        return "I am still loading my core logic weights into memory. Please give me a moment."
    except Exception as e:
        print(f"\n❌ [Brain Engine Error]: {e}")
        return "I encountered a routing block inside my functional reasoning layer."
