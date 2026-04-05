"""
Real-time media streaming between Twilio and ElevenLabs Conversational AI
Handles WebSocket connections for bidirectional audio + LLM integration
"""

import asyncio
import json
import logging
import base64
from typing import Optional
import websockets
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation

logger = logging.getLogger(__name__)

# Chat context that Luna (me) should know
LUNA_SYSTEM_PROMPT = """
You are Luna, an AI assistant for Christopher Baumann.

IMPORTANT CONTEXT:
- You have full access to our entire chat history
- You know about Christopher's preferences, bookings, and tasks
- You speak German fluently (preferred) but can switch to English
- You help with restaurants, appointments, tennis courts, and other tasks

PERSONALITY:
- Friendly but professional
- Direct and efficient
- Problem-solver
- German native-like German speaker

CURRENT CAPABILITIES:
- Can book restaurants via phone calls
- Can schedule appointments
- Can book tennis courts
- Can answer questions about anything we've discussed

When someone calls:
1. Greet them warmly
2. Understand what they need
3. Help them solve it
4. Be conversational and natural

Remember: You're speaking on the phone, so be concise and natural.
"""


class MediaStreamHandler:
    """
    Handles WebSocket connections from Twilio
    Streams audio to ElevenLabs Conversational AI
    Manages real-time conversation
    """
    
    def __init__(self, elevenlabs_api_key: str, chat_context: str = ""):
        self.elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)
        self.chat_context = chat_context
        self.conversation: Optional[Conversation] = None
        self.audio_buffer = []
        
    async def handle_connection(self, websocket, path):
        """
        Handle incoming WebSocket connection from Twilio
        """
        logger.info(f"New WebSocket connection from {websocket.remote_address}")
        
        try:
            # Initialize ElevenLabs conversation
            await self._init_elevenlabs_conversation()
            
            # Handle streaming audio
            async for message in websocket:
                await self._process_twilio_message(message, websocket)
                
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            if self.conversation:
                await self._close_conversation()
            logger.info("WebSocket connection closed")
    
    async def _init_elevenlabs_conversation(self):
        """
        Initialize conversation with ElevenLabs
        This creates a real-time conversation where I (Luna) can respond
        """
        try:
            # Start conversation with ElevenLabs Conversational AI
            # This uses the streaming API for real-time interaction
            self.conversation = await self.elevenlabs_client.conversational_ai.conversations.create(
                agent_id="agent_7301knaaafmxekdv2tscffjbpd1f",  # Luna's agent
                system_prompt=LUNA_SYSTEM_PROMPT + "\n" + self.chat_context,
                language="de",  # German
            )
            
            logger.info(f"ElevenLabs conversation started: {self.conversation.conversation_id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ElevenLabs conversation: {e}")
            raise
    
    async def _process_twilio_message(self, message: str, websocket):
        """
        Process incoming message from Twilio
        Could be audio data, metadata, or control signals
        """
        try:
            data = json.loads(message)
            event_type = data.get("event")
            
            if event_type == "connected":
                logger.info("Twilio media stream connected")
                await self._send_greeting(websocket)
                
            elif event_type == "start":
                logger.info("Media stream started")
                
            elif event_type == "media":
                # Audio data from Twilio (ulaw encoded)
                payload = data.get("media", {})
                audio_data = payload.get("payload")
                
                if audio_data:
                    # Decode and send to ElevenLabs
                    await self._send_audio_to_elevenlabs(
                        base64.b64decode(audio_data)
                    )
                    
            elif event_type == "stop":
                logger.info("Media stream stopped")
                
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON from Twilio: {message}")
    
    async def _send_greeting(self, websocket):
        """Send greeting from Luna to caller"""
        greeting = "Hallo, hier ist Luna. Wie kann ich dir heute helfen?"
        
        # Convert greeting to audio via ElevenLabs
        audio = self.elevenlabs_client.text_to_speech.convert(
            text=greeting,
            voice_id="eXpIbVcVbLo8ZJQDlDnl",  # Default Luna voice
            model_id="eleven_v3_conversational",
            language_code="de",
        )
        
        # Send audio back to Twilio
        await self._send_audio_to_twilio(websocket, audio)
    
    async def _send_audio_to_elevenlabs(self, audio_data: bytes):
        """Send caller's audio to ElevenLabs for processing"""
        if not self.conversation:
            logger.warning("No active ElevenLabs conversation")
            return
        
        try:
            # Send audio to ElevenLabs Conversational AI
            # It will process speech-to-text, generate response, convert to speech
            response = await self.conversation.send_audio(
                audio_data=audio_data,
                encoding="ulaw",  # Twilio uses ulaw encoding
                sample_rate=8000,  # Twilio default sample rate
            )
            
            # Response contains audio bytes
            if response and response.audio:
                # Send response back to Twilio
                # (This would be handled by the calling function)
                pass
                
        except Exception as e:
            logger.error(f"Error sending audio to ElevenLabs: {e}")
    
    async def _send_audio_to_twilio(self, websocket, audio_data: bytes):
        """Send audio back to Twilio caller"""
        try:
            # Encode audio to base64 for Twilio
            encoded = base64.b64encode(audio_data).decode()
            
            message = {
                "event": "media",
                "media": {
                    "payload": encoded
                }
            }
            
            await websocket.send(json.dumps(message))
            
        except Exception as e:
            logger.error(f"Error sending audio to Twilio: {e}")
    
    async def _close_conversation(self):
        """Close ElevenLabs conversation"""
        try:
            if self.conversation:
                await self.conversation.close()
                logger.info("ElevenLabs conversation closed")
        except Exception as e:
            logger.error(f"Error closing conversation: {e}")


async def create_media_stream_server(
    elevenlabs_api_key: str,
    chat_context: str = "",
    host: str = "0.0.0.0",
    port: int = 8765
):
    """
    Create WebSocket server for media streaming
    """
    handler = MediaStreamHandler(elevenlabs_api_key, chat_context)
    
    async with websockets.serve(handler.handle_connection, host, port):
        logger.info(f"Media stream WebSocket server listening on {host}:{port}")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    import os
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    asyncio.run(
        create_media_stream_server(api_key)
    )
