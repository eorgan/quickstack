from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel
from app.agent import get_agent_response
from app.audio import transcribe_audio, generate_audio
from app.chatwoot import upload_audio_to_chatwoot
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agno Agent Service - Maya")

# --- Models ---
class ChatRequest(BaseModel):
    message: str
    user_id: str
    session_id: str = None
    is_audio: bool = False

class ChatResponse(BaseModel):
    response: str

class TranscribeRequest(BaseModel):
    audio_url: str

class TTSRequest(BaseModel):
    text: str

class SendAudioRequest(BaseModel):
    text: str
    account_id: str
    conversation_id: str
    token: str

# --- Endpoints ---

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received message from user {request.user_id}: {request.message} (Audio: {request.is_audio})")
        response = get_agent_response(request.message, request.user_id, request.session_id, is_audio=request.is_audio)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def transcribe(request: TranscribeRequest):
    try:
        text = transcribe_audio(request.audio_url)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tts")
async def tts(request: TTSRequest):
    try:
        audio_bytes = generate_audio(request.text)
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/send_audio_reply")
async def send_audio_reply(request: SendAudioRequest):
    try:
        # 1. Generate Audio
        audio_bytes = generate_audio(request.text)
        
        # 2. Upload to Chatwoot
        upload_audio_to_chatwoot(
            account_id=request.account_id,
            conversation_id=request.conversation_id,
            token=request.token,
            audio_bytes=audio_bytes,
            text_content=request.text # Send text as caption
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
