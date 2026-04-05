#!/usr/bin/env python3
"""
Luna - Simple Twilio Voice Response
Minimal working version for incoming calls
"""

from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Luna Phone System - Online", 200

@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    """Handle incoming calls"""
    from_number = request.form.get("From", "unknown")
    call_sid = request.form.get("CallSid", "unknown")
    
    logger.info(f"Incoming call from {from_number} (SID: {call_sid})")
    
    response = VoiceResponse()
    response.say("Hallo, du erreichst Luna, den virtuellen Assistenten von Christopher.", language="de")
    response.pause(length=1)
    response.say("Leider kann ich gerade nicht sprechen. Bitte versuche es später noch einmal.", language="de")
    
    return str(response), 200

@app.route("/status", methods=["GET"])
def status():
    return {"status": "online", "service": "Luna"}, 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
