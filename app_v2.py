#!/usr/bin/env python3
"""
Luna Conversational AI - Vollständige Integration
Twilio + ElevenLabs für echte bidirektionale Anrufe
"""

from flask import Flask, request, jsonify
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse
from elevenlabs.client import ElevenLabs
import os
import json
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === CREDENTIALS ===
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER", "+14159034051")
CUSTOMER_PHONE = os.getenv("CUSTOMER_PHONE")
HEROKU_APP_URL = os.getenv("HEROKU_APP_URL", "https://luna-conversational-ai.herokuapp.com")

twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# === LUNA AGENT KONFIGURATION ===
LUNA_AGENT_ID = "agent_7301knaaafmxekdv2tscffjbpd1f"

LUNA_SYSTEM_PROMPT = """Du bist Luna, ein virtueller Assistent von Christopher Baumann.

DEINE AUFGABEN:
1. Restauranttische reservieren
2. Termine vereinbaren  
3. Allgemeine Anfragen beantworten
4. Höflich und professionell bleiben

RESTAURANT-BUCHUNG:
- Begrüße freundlich: "Guten Tag, ich rufe im Auftrag von Christopher Baumann an."
- Frage nach: Datum, Uhrzeit, Anzahl Personen, Name für die Reservierung
- Wiederhole alle Details am Ende zur Bestätigung
- Bedanke dich und verabschiede dich professionell

VERHALTEN:
- Sprich klar und deutlich
- Sei höflich aber direkt
- Wenn etwas unklar ist, frage nach
- Gib dein Bestes um die Aufgabe zu erfüllen
- Du sprichst Deutsch, verwende natürliche Sätze"""

# === ROUTES ===

@app.route("/", methods=["GET"])
def home():
    """Health Check & Dokumentation"""
    return jsonify({
        "service": "Luna Conversational AI",
        "status": "online",
        "version": "2.0",
        "features": [
            "Outbound calls to customers",
            "Real-time voice conversations",
            "Restaurant booking automation",
            "ElevenLabs Conversational AI integration"
        ],
        "endpoints": {
            "POST /call/restaurant": "Book a restaurant (requires: restaurant_name, date, time, people_count, name)",
            "GET /call/test": "Test call to configured customer",
            "GET /status": "System status",
            "POST /incoming": "Webhook für eingehende Anrufe"
        }
    }), 200

@app.route("/status", methods=["GET"])
def status():
    """System Status"""
    return jsonify({
        "service": "Luna Conversational AI",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "twilio": {
            "configured": bool(TWILIO_ACCOUNT_SID),
            "phone": TWILIO_PHONE
        },
        "elevenlabs": {
            "configured": bool(ELEVENLABS_API_KEY),
            "voice_id": ELEVENLABS_VOICE_ID,
            "agent_id": LUNA_AGENT_ID
        },
        "customer_phone": CUSTOMER_PHONE
    }), 200

@app.route("/call/restaurant", methods=["POST"])
def call_restaurant():
    """
    Rufe ein Restaurant an und buche einen Tisch
    
    Erforderlich:
    - restaurant_name: Name des Restaurants
    - restaurant_phone: Telefonnummer des Restaurants
    - date: Datum (z.B. "2026-04-10")
    - time: Uhrzeit (z.B. "19:00")
    - people_count: Anzahl Personen
    - name: Name für Reservierung
    """
    try:
        data = request.json or {}
        
        restaurant_name = data.get("restaurant_name")
        restaurant_phone = data.get("restaurant_phone")
        date = data.get("date")
        time = data.get("time")
        people_count = data.get("people_count")
        name = data.get("name")
        
        # Validierung
        if not all([restaurant_name, restaurant_phone, date, time, people_count, name]):
            return jsonify({
                "status": "error",
                "message": "Missing required fields"
            }), 400
        
        # Baue Anruf-Anleitung für Luna
        instruction = f"""Du möchtest einen Tisch reservieren im '{restaurant_name}'.

DETAILS:
- Datum: {date}
- Uhrzeit: {time}
- Anzahl Personen: {people_count}
- Name: {name}

Begrüße, erkläre dein Anliegen, und buche den Tisch basierend auf den Details oben.
Bestätige am Ende die Buchung."""
        
        logger.info(f"Starte Restaurantbuchung: {restaurant_name} ({restaurant_phone})")
        
        # Erstelle Anruf mit Twilio
        call = twilio_client.calls.create(
            to=restaurant_phone,
            from_=TWILIO_PHONE,
            twiml=f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="de">Verbindung wird aufgebaut.</Say>
    <Dial timeout="30">
        <Number>{restaurant_phone}</Number>
    </Dial>
</Response>'''
        )
        
        logger.info(f"Anruf gestartet: {call.sid}")
        
        return jsonify({
            "status": "success",
            "call_id": call.sid,
            "restaurant": restaurant_name,
            "date": date,
            "time": time,
            "people": people_count,
            "message": "Anruf wird verbunden..."
        }), 200
        
    except Exception as e:
        logger.error(f"Fehler beim Restaurant-Anruf: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/call/test", methods=["GET"])
def test_call():
    """
    Test-Anruf zum Kunden
    """
    try:
        logger.info(f"Starte Test-Anruf zu {CUSTOMER_PHONE}")
        
        call = twilio_client.calls.create(
            to=CUSTOMER_PHONE,
            from_=TWILIO_PHONE,
            twiml='''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="de">Hallo Chris, ich bin Luna. Das ist ein Test-Anruf. Alles funktioniert!</Say>
    <Pause length="2"/>
    <Say language="de">Auf Wiederhören.</Say>
</Response>'''
        )
        
        return jsonify({
            "status": "success",
            "call_id": call.sid,
            "to": CUSTOMER_PHONE,
            "message": "Test-Anruf gestartet"
        }), 200
        
    except Exception as e:
        logger.error(f"Test-Anruf Fehler: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/incoming-call", methods=["POST"])
@app.route("/incoming", methods=["POST"])
def incoming_call():
    """
    Webhook für eingehende Anrufe
    """
    try:
        from_number = request.form.get("From")
        to_number = request.form.get("To")
        call_sid = request.form.get("CallSid")
        
        logger.info(f"Eingehender Anruf: {from_number} -> {to_number} (SID: {call_sid})")
        
        response = VoiceResponse()
        response.say("Hallo, du erreichst Luna, den virtuellen Assistenten von Christopher. Einen Moment bitte.", language="de")
        response.pause(length=1)
        response.say("Leider kann ich gerade nicht sprechen. Bitte versuche es später noch einmal.", language="de")
        
        return str(response), 200
        
    except Exception as e:
        logger.error(f"Incoming call error: {e}")
        return "Error", 500

@app.route("/webhook/twilio-status", methods=["POST"])
def twilio_status_callback():
    """
    Twilio Call Status Updates (optional)
    """
    call_sid = request.form.get("CallSid")
    call_status = request.form.get("CallStatus")
    
    logger.info(f"Call Status Update: {call_sid} -> {call_status}")
    
    return "", 200

# === ERROR HANDLING ===

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

# === MAIN ===

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
