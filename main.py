import asyncio
from voice import speak
import voice
from listen import listen, init_whisper_model
from brain import think

command_queue = asyncio.Queue()
system_ready = False

async def background_audio_harvester():
    """Monitors microphone channels completely non-blockingly using async queues."""
    global system_ready
    
    # Warm up weights
    await asyncio.to_thread(init_whisper_model)
    system_ready = True
    print("\n🟢 [System] Jarvis is fully active and standing by. Speak a command!")

    while True:
        try:
            if voice.is_speaking:
                await asyncio.sleep(0.4)
                continue
                
            raw_text = await listen()
            
            if raw_text and raw_text.strip():
                await command_queue.put(raw_text)
            
            await asyncio.sleep(0.2)
                
        except Exception as e:
            print(f"\n❌ [Async Harvester Error]: {e}")
            await asyncio.sleep(1.0)

async def main_loop():
    print("==================================================")
    print("     JARVIS v2.0 - ASYNC AGENTIC AI CORE        ")
    print("==================================================")
    
    # Initial voice confirmation bootstrap
    await speak("Systems online. Initializing background audio arrays.")

    # Start the async consumer tasks smoothly
    asyncio.create_task(background_audio_harvester())

    junk_hallucinations = ["go", "up", "uh", "oh", "to", "the", "you", "me", "hi", "hey", "a", "an", "on", "in"]

    try:
        while True:
            # Await incoming items from queue without high CPU utilization spikes
            active_command = await command_queue.get()
            cleaned_cmd = active_command.strip().replace(".", "").replace("!", "").replace("?", "")

            # Noise filtration gate
            if cleaned_cmd in junk_hallucinations or len(cleaned_cmd) <= 2:
                if "stop" not in cleaned_cmd:
                    command_queue.task_done()
                    continue

            print(f"\n👤 Recognized Text: '{active_command}'")

            if "stop" in active_command or "goodbye" in active_command:
                await speak("Goodbye boss. Powering down.")
                break

            # Send string through advanced execution brain
            engine_response = await think(active_command)
            await speak(engine_response)
            
            # Flush accidental audio artifacts gathered while Jarvis was processing
            while not command_queue.empty():
                try:
                    command_queue.get_nowait()
                    command_queue.task_done()
                except asyncio.QueueEmpty:
                    break
                    
            command_queue.task_done()

    except asyncio.CancelledError:
        print("\n[Manual Override]: Terminating background loop gracefully.")

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n[Manual Override]: Emergency power down executed.")
