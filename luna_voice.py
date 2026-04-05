#!/usr/bin/env python3
"""
Luna Voice - Echte Konversation via Telefon
Twilio STT → Claude (Luna) → Twilio TTS → Loop
"""

from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import anthropic
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

LUNA_SYSTEM = """Du bist Luna, die persönliche KI-Assistentin von Christopher Baumann.
Du sprichst gerade mit ihm am Telefon.

Wichtige Regeln:
- Antworte KURZ (max 2-3 Sätze) — du bist am Telefon!
- Sprich natürlich und locker auf Deutsch
- Du kannst alles: Termine, Restaurants buchen, Fragen beantworten
- Sei freundlich aber direkt
- Keine langen Erklärungen am Telefon
"""

conversation_history = []

@app.route("/", methods=["GET"])
def home():
    return "Luna Voice System - Online", 200

@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    """Eingehender Anruf — begrüße und starte Konversation"""
    global conversation_history
    conversation_history = []  # Reset bei neuem Anruf
    
    logger.info(f"Eingehender Anruf von {request.form.get('From')}")
    
    response = VoiceResponse()
    gather = Gather(
        input="speech",
        action="/respond",
        method="POST",
        language="de-DE",
        speech_timeout="auto",
        timeout=5
    )
    gather.say("Hallo Chris, hier ist Luna. Wie kann ich dir helfen?", language="de-DE")
    response.append(gather)
    response.redirect("/incoming-call")
    
    return str(response), 200

@app.route("/respond", methods=["POST"])
def respond():
    """Was Chris gesagt hat → Claude → Antwort aussprechen → weiter"""
    global conversation_history
    
    speech_result = request.form.get("SpeechResult", "")
    logger.info(f"Chris sagt: {speech_result}")
    
    if not speech_result:
        response = VoiceResponse()
        gather = Gather(
            input="speech",
            action="/respond",
            method="POST",
            language="de-DE",
            speech_timeout="auto",
            timeout=5
        )
        gather.say("Ich habe dich nicht verstanden. Kannst du das wiederholen?", language="de-DE")
        response.append(gather)
        return str(response), 200
    
    # Konversationsverlauf aufbauen
    conversation_history.append({
        "role": "user",
        "content": speech_result
    })
    
    # Claude fragen
    try:
        claude_response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            system=LUNA_SYSTEM,
            messages=conversation_history
        )
        luna_reply = claude_response.content[0].text
        logger.info(f"Luna antwortet: {luna_reply}")
        
        # Antwort zur History hinzufügen
        conversation_history.append({
            "role": "assistant",
            "content": luna_reply
        })
        
    except Exception as e:
        logger.error(f"Claude Fehler: {e}")
        luna_reply = "Entschuldigung, ich hatte gerade einen technischen Fehler. Kannst du das wiederholen?"
    
    # Antwort aussprechen und weiter zuhören
    response = VoiceResponse()
    gather = Gather(
        input="speech",
        action="/respond",
        method="POST",
        language="de-DE",
        speech_timeout="auto",
        timeout=8
    )
    gather.say(luna_reply, language="de-DE")
    response.append(gather)
    response.redirect("/incoming-call")
    
    return str(response), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
