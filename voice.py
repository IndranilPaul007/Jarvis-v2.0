import os
import uuid
import asyncio
import edge_tts
import pygame
from config import VOICE_MODEL

pygame.mixer.init()
is_speaking = False

async def speak(text: str):
    """Generates and plays assistant voice lines entirely asynchronously."""
    global is_speaking
    if not text or not text.strip():
        return

    is_speaking = True
    
    # 🔧 FIX 1: Generate a strict absolute path so Pygame never loses the file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, f"temp_{uuid.uuid4().hex}.mp3")
    
    try:
        print(f"🤖 Jarvis: {text}")
        
        # Async synthesis stream
        communicate = edge_tts.Communicate(text, VOICE_MODEL)
        await communicate.save(filename)
        
        # 🔧 FIX 2: Verify the file actually saved and isn't empty (0 bytes)
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            print("\n❌ [Voice Engine Error]: Edge-TTS failed to download the audio data.")
            return
        
        # Non-blocking audio execution
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Await completion without locking the background systems
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.05)
            
        pygame.mixer.music.unload()
            
    except Exception as e:
        print(f"\n❌ [Voice Engine Error]: {e}")
    finally:
        is_speaking = False
        # Clean up the temp file
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except OSError:
                pass
