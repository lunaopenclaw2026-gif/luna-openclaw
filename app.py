#!/usr/bin/env python3
"""
Luna Conversational AI - Heroku Backend
Verbindet Twilio mit ElevenLabs Conversational AI
"""

from flask import Flask, request, jsonify
from twilio.rest import Client
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
import os
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Credentials aus Umgebungsvariablen
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")
CUSTOMER_PHONE = os.getenv("CUSTOMER_PHONE")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Speichere aktive Konversationen
active_conversations = {}

@app.route("/", methods=["GET"])
def health():
    """Health Check"""
    return jsonify({
        "status": "ok",
        "service": "Luna Conversational AI",
        "version": "1.0"
    }), 200

@app.route("/call/start", methods=["POST"])
def start_call():
    """Starte einen ausgehenden Anruf"""
    try:
        data = request.json or {}
        to_number = data.get("to", CUSTOMER_PHONE)
        purpose = data.get("purpose", "restaurant_booking")
        
        logger.info(f"Starte Anruf zu {to_number} für {purpose}")
        
        # Erstelle TwiML für Anruf
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="de">Hallo, ich bin Luna. Ein Moment bitte während ich die Verbindung aufbaue.</Say>
    <Connect>
        <Stream url="wss://your-heroku-app.herokuapp.com/stream" />
    </Connect>
</Response>'''
        
        # Starte Anruf über Twilio
        call = twilio_client.calls.create(
            to=to_number,
            from_=TWILIO_PHONE,
            twiml=twiml
        )
        
        logger.info(f"Anruf gestartet: {call.sid}")
        
        return jsonify({
            "status": "success",
            "call_id": call.sid,
            "to": to_number
        }), 200
        
    except Exception as e:
        logger.error(f"Fehler beim Starten des Anrufs: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/stream", methods=["POST"])
def handle_stream():
    """Verarbeite WebSocket Stream von Twilio für ElevenLabs Conversational AI"""
    try:
        # Diese Route wird von Twilio mit WebSocket aufgerufen
        # Hier verbinden wir ElevenLabs Conversational AI
        logger.info("Stream-Anfrage empfangen")
        return "", 200
    except Exception as e:
        logger.error(f"Stream-Fehler: {e}")
        return "", 500

@app.route("/call/test", methods=["GET"])
def test_call():
    """Test-Anruf starten"""
    try:
        call = twilio_client.calls.create(
            to=CUSTOMER_PHONE,
            from_=TWILIO_PHONE,
            twiml='''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="de">Hallo Chris, ich bin Luna. Das ist ein Test-Anruf von Heroku.</Say>
</Response>'''
        )
        
        return jsonify({
            "status": "success",
            "call_id": call.sid,
            "message": "Test-Anruf gestartet"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/status", methods=["GET"])
def status():
    """Zeige System-Status"""
    return jsonify({
        "service": "Luna Conversational AI",
        "status": "active",
        "twilio_configured": bool(TWILIO_ACCOUNT_SID),
        "elevenlabs_configured": bool(ELEVENLABS_API_KEY),
        "phone": TWILIO_PHONE,
        "customer": CUSTOMER_PHONE
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
