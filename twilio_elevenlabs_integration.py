"""
Twilio + ElevenLabs Conversational AI Integration
Allows Christopher to call +14159034051 and speak with Luna (me) directly
with full chat context awareness
"""

from flask import Flask, request, session
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from elevenlabs import ElevenLabs
import os
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-prod")

# Initialize clients
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+14159034051")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
CHRISTOPHER_PHONE = os.getenv("CHRISTOPHER_PHONE", "+4915770368632")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Store conversation context
CHAT_CONTEXT = """
Christopher Baumann is my user. I am Luna, his AI assistant.
I help with:
- Restaurant reservations
- Tennis court bookings
- Appointments and scheduling
- General tasks and questions

I have full access to our chat history and can reference anything we've discussed.
I speak German fluently and can switch to English.
I'm friendly but professional.
"""


@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    """
    Webhook for incoming Twilio calls to +14159034051
    Routes call to WebSocket handler for real-time conversation with ElevenLabs
    """
    logger.info(f"Incoming call from {request.form.get('From')}")
    
    response = VoiceResponse()
    
    # Connect to WebSocket for real-time conversation
    response.connect(
        action="/call-status",
        method="POST"
    ).stream(
        url=f"wss://{request.host}/media-stream",
        track="inbound_track"
    )
    
    return str(response)


@app.route("/call-status", methods=["POST"])
def call_status():
    """Handle call status updates"""
    call_sid = request.form.get("CallSid")
    call_status = request.form.get("CallStatus")
    
    logger.info(f"Call {call_sid}: {call_status}")
    
    return "", 200


@app.route("/media-stream", methods=["POST"])
def media_stream():
    """
    WebSocket endpoint for real-time audio streaming
    Connects Twilio audio stream to ElevenLabs Conversational AI
    """
    logger.info("WebSocket media stream initiated")
    
    # This will be handled by a WebSocket upgrade
    # See media_stream_handler.py for actual implementation
    return "", 200


@app.route("/initiateCall", methods=["POST"])
def initiate_call():
    """
    Initiate outbound call from Luna to a phone number
    Used for restaurant reservations, appointments, etc.
    
    POST data:
    {
        "to": "+49...",
        "purpose": "restaurant_booking|appointment|general",
        "context": "additional context for the call"
    }
    """
    data = request.json
    to_number = data.get("to")
    purpose = data.get("purpose", "general")
    context = data.get("context", "")
    
    if not to_number:
        return {"error": "Missing 'to' parameter"}, 400
    
    try:
        call = twilio_client.calls.create(
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            url=f"https://{request.host}/outbound-call-handler",
            method="POST",
            record=True,  # Record calls for quality assurance
        )
        
        logger.info(f"Outbound call initiated: {call.sid} to {to_number}")
        
        return {
            "status": "initiated",
            "call_sid": call.sid,
            "to": to_number,
            "purpose": purpose,
            "context": context
        }, 200
        
    except Exception as e:
        logger.error(f"Error initiating call: {e}")
        return {"error": str(e)}, 500


@app.route("/outbound-call-handler", methods=["POST"])
def outbound_call_handler():
    """
    Handler for outbound calls
    Routes to ElevenLabs Conversational AI with context
    """
    call_sid = request.form.get("CallSid")
    to_number = request.form.get("To")
    
    logger.info(f"Outbound call handler: {call_sid} to {to_number}")
    
    response = VoiceResponse()
    
    # Connect to ElevenLabs Conversational AI via WebSocket
    response.connect(
        action="/call-status",
        method="POST"
    ).stream(
        url=f"wss://{request.host}/media-stream-outbound",
        track="outbound_track"
    )
    
    return str(response)


@app.route("/media-stream-outbound", methods=["POST"])
def media_stream_outbound():
    """WebSocket endpoint for outbound calls"""
    logger.info("Outbound media stream initiated")
    return "", 200


@app.route("/test-call", methods=["POST"])
def test_call():
    """
    Test endpoint: Make a test call to Christopher's number
    """
    try:
        call = twilio_client.calls.create(
            to=CHRISTOPHER_PHONE,
            from_=TWILIO_PHONE_NUMBER,
            url=f"https://{request.host}/test-call-handler",
            method="POST",
        )
        
        logger.info(f"Test call initiated: {call.sid}")
        return {"status": "success", "call_sid": call.sid}, 200
        
    except Exception as e:
        logger.error(f"Test call error: {e}")
        return {"error": str(e)}, 500


@app.route("/test-call-handler", methods=["POST"])
def test_call_handler():
    """Handler for test calls"""
    response = VoiceResponse()
    response.say("Hallo Christopher, das ist Luna. Der Test funktioniert.", voice="woman", language="de-DE")
    return str(response)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "twilio": "configured" if TWILIO_ACCOUNT_SID else "missing",
        "elevenlabs": "configured" if ELEVENLABS_API_KEY else "missing"
    }, 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
