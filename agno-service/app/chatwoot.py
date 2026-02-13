import requests
import io
import logging

logger = logging.getLogger(__name__)

def upload_audio_to_chatwoot(
    account_id: str,
    conversation_id: str,
    token: str,
    audio_bytes: bytes,
    text_content: str = "Audio Message"
):
    """
    Uploads audio bytes to Chatwoot conversation.
    """
    try:
        url = f"http://chatwoot_web:3000/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
        
        # Prepare multipart payload
        files = {
            'attachments[]': ('response.mp3', io.BytesIO(audio_bytes), 'audio/mpeg')
        }
        data = {
            'content': text_content,
            'message_type': 'outgoing'
        }
        headers = {
            'api_access_token': token
        }

        response = requests.post(url, headers=headers, data=data, files=files)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Chatwoot upload error: {e}")
        raise e
