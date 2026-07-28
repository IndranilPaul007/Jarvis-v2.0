import json
import asyncio
import requests
from config import OLLAMA_URL, AI_MODEL, SYSTEM_PROMPT

# 🔗 Import the universal schemas and execution router from our new commands architecture
from commands import TOOLS_MANIFEST, TOOLS_EXECUTION_ROUTER

# 🧠 Conversation Memory Array
session_history = []

# -----------------------------------------------------------------------------
# ⚙️ AGENTIC TOOL EXECUTION LAYER
# -----------------------------------------------------------------------------

def execute_tool(tool_call):
    """Dynamically processes the tool requested by the AI using the commands.py router."""
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

    # 🚀 Dynamic Routing: Look up the function in commands.py and execute it
    if func_name in TOOLS_EXECUTION_ROUTER:
        try:
            # Unpack the dictionary arguments directly into the mapped Python function
            result = TOOLS_EXECUTION_ROUTER[func_name](**args)
            return str(result)
        except Exception as e:
            error_msg = f"Crash during execution of {func_name}: {e}"
            print(f"❌ {error_msg}")
            return error_msg
    else:
        return f"Tool '{func_name}' was requested but is not registered in the commands router."

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
            "tools": TOOLS_MANIFEST  # 🔗 Now pulling the massive 11-tool array from commands.py
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
        
        # Memory Trimming (Keeps him fast and prevents context overload)
        if len(session_history) > 8:
            session_history = session_history[-8:]
            
        return ai_reply

    except requests.exceptions.Timeout:
        print("\n❌ [Advanced Agent Engine Error]: HTTPConnectionPool: Read timed out.")
        return "I am still loading my core logic weights into memory. Please give me a moment."
    except Exception as e:
        print(f"\n❌ [Brain Engine Error]: {e}")
        return "I encountered a routing block inside my functional reasoning layer."
