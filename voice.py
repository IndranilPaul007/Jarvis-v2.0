import os
import uuid
import asyncio
import edge_tts
import pygame
import pyttsx3
from config import VOICE_MODEL

pygame.mixer.init()
is_speaking = False

def _fallback_pyttsx3(text: str):
    """Synchronous local fallback engine using Windows SAPI5 (100% offline)."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        voices = engine.getProperty('voices')
        for voice in voices:
            if "david" in voice.name.lower() or "zira" in voice.name.lower() or "english" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"\n❌ [Fallback Voice Error]: {e}")

async def speak(text: str):
    """Generates and plays assistant voice lines asynchronously with automatic offline fallback."""
    global is_speaking
    if not text or not text.strip():
        return

    is_speaking = True
    
    # Generate a strict absolute path so Pygame never loses the file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, f"temp_{uuid.uuid4().hex}.mp3")
    
    edge_success = False
    try:
        print(f"🤖 Jarvis: {text}")
        
        # Async synthesis stream (Edge-TTS)
        communicate = edge_tts.Communicate(text, VOICE_MODEL)
        await communicate.save(filename)
        
        # Verify the file actually saved and isn't empty (0 bytes)
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            # Non-blocking audio execution
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Await completion without locking the background systems
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.05)
                
            pygame.mixer.music.unload()
            edge_success = True
        else:
            print("\n⚠️ [Voice Engine]: Edge-TTS failed or network is offline. Switching to local voice...")
            
    except Exception as e:
        print(f"\n⚠️ [Voice Engine Notice]: Offline detected ({e}). Switching to local voice...")
        
    finally:
        # Clean up the temp file
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except OSError:
                pass

    # If online Edge-TTS failed or timed out, seamlessly trigger the local pyttsx3 backup
    if not edge_success:
        await asyncio.to_thread(_fallback_pyttsx3, text)
        
    is_speaking = False
