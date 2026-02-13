from groq import Groq
from elevenlabs.client import ElevenLabs
import os
import requests
import tempfile
import logging

logger = logging.getLogger(__name__)

# Clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def transcribe_audio(audio_url: str) -> str:
    """
    Downloads audio from URL and transcribes using Groq (Distil-Whisper).
    """
    try:
        # Download audio to temp file
        response = requests.get(audio_url)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_audio:
            temp_audio.write(response.content)
            temp_audio_path = temp_audio.name

        with open(temp_audio_path, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(temp_audio_path, file.read()),
                # Groq has "whisper-large-v3" which is multilingual.
                model="whisper-large-v3",
                response_format="json",
                language="pt" # Force Portuguese for safety
            )
        
        os.unlink(temp_audio_path)
        return transcription.text
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise e

def generate_audio(text: str) -> bytes:
    """
    Generates audio from text using ElevenLabs.
    """
    try:
        # Voice ID: "Rachel" (American) or a custom cloned voice. 
        # Using a default Portuguese-friendly voice or "Rachel" for now.
        # Ideally, user should provide a VOICE_ID env var.
        voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Fallback to Rachel
        
        audio_stream = elevenlabs_client.generate(
            text=text,
            voice=voice_id,
            model="eleven_turbo_v2_5" # Low latency model
        )
        
        # Collect the stream into bytes
        audio_bytes = b"".join(audio_stream)
        return audio_bytes
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise e
