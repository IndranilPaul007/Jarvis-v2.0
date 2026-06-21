import os
import time
import tempfile
import asyncio
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel
import voice
from config import (
    SAMPLERATE, MAX_DURATION, MIN_SPEECH_TIME, 
    SILENCE_THRESHOLD, SILENCE_SECONDS, MIC_DEVICE_INDEX
)

# Global model container
whisper_engine = None

def init_whisper_model():
    """Warm up the Whisper weights on standard memory channels strictly once."""
    global whisper_engine
    if whisper_engine is None:
        print("🧠 [System] Powering up Whisper local acoustic arrays...")
        try:
            # 🔧 Upgraded to base.en for Copilot-level accuracy
            whisper_engine = WhisperModel("base.en", device="cpu", compute_type="int8")
            print("🟢 [System] Acoustic models successfully mounted.")
        except Exception as e:
            print(f"❌ [Model Load Critical Failure]: {e}")

async def listen() -> str:
    """Listens continuously to physical mic registers and yields text strings."""
    init_whisper_model()
    
    try:
        audio_chunks = []
        loop_state = {"silence_time": 0.0, "speech_time": 0.0, "latest_volume": 0}
        start_time = time.time()

        def audio_callback(indata, frames, time_info, status):
            if voice.is_speaking:
                loop_state["latest_volume"] = 0
                return

            audio_chunks.append(indata.copy())
            volume = int(np.linalg.norm(indata) * 400)
            loop_state["latest_volume"] = volume
            duration = frames / SAMPLERATE

            if volume < SILENCE_THRESHOLD:
                loop_state["silence_time"] += duration
            else:
                loop_state["silence_time"] = 0.0
                loop_state["speech_time"] += duration

        # Native non-blocking stream context
        stream = sd.InputStream(
            device=MIC_DEVICE_INDEX, 
            samplerate=SAMPLERATE, 
            channels=1, 
            callback=audio_callback
        )
        
        with stream:
            while True:
                await asyncio.sleep(0.1)
                elapsed = time.time() - start_time

                # Anti-Feedback Mute Hatch
                if voice.is_speaking:
                    audio_chunks.clear()
                    print("🤫 [Mic Engine] Jarvis is speaking... Muting intake.", end="\r", flush=True)
                    while voice.is_speaking:
                        await asyncio.sleep(0.1)
                    return ""

                print(f"🎤 [Mic Monitoring] Vol: {loop_state['latest_volume']} | Talk: {loop_state['speech_time']:.1f}s | Mute: {loop_state['silence_time']:.1f}s   ", end="\r", flush=True)

                if loop_state["speech_time"] > MIN_SPEECH_TIME and loop_state["silence_time"] > SILENCE_SECONDS:
                    break
                    
                if loop_state["speech_time"] == 0.0 and loop_state["silence_time"] > SILENCE_SECONDS:
                    return ""
                    
                if elapsed > MAX_DURATION:
                    break

        if not audio_chunks:
            return ""

        print("\n⚡ [Whisper] Converting sound matrices to text data...")
        audio = np.concatenate(audio_chunks, axis=0).flatten()

        # Execute disk writing and transcription via worker thread
        def processing_pipeline():
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                wav.write(tmp_file.name, SAMPLERATE, audio)
                tmp_path = tmp_file.name
            
            try:
                segments, _ = whisper_engine.transcribe(tmp_path)
                text_output = "".join([seg.text for seg in segments]).strip().lower()
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            return text_output

        return await asyncio.to_thread(processing_pipeline)

    except Exception as e:
        print(f"\n❌ [Audio Pipeline Exception]: {e}")
        return ""
