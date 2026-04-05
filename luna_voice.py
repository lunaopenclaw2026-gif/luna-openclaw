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

def make_gather(action="/respond"):
    """Erstelle Gather mit optimalen Einstellungen"""
    return Gather(
        input="speech",
        action=action,
        method="POST",
        language="de-DE",
        speech_timeout=2,
        timeout=10,
        action_on_empty_result=True
    )

def say(gather, text):
    """Spreche Text mit besserer Stimme"""
    gather.say(text, language="de-DE", voice="Polly.Vicki")

@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    """Eingehender Anruf — begrüße und starte Konversation"""
    global conversation_history
    conversation_history = []  # Reset bei neuem Anruf
    
    logger.info(f"Eingehender Anruf von {request.form.get('From')}")
    
    response = VoiceResponse()
    gather = make_gather()
    say(gather, "Hallo Chris, hier ist Luna. Wie kann ich dir helfen?")
    response.append(gather)
    response.redirect("/listen")
    
    return str(response), 200

@app.route("/listen", methods=["POST"])
def listen():
    """Warte auf Sprache ohne Greeting"""
    response = VoiceResponse()
    gather = make_gather()
    response.append(gather)
    response.redirect("/listen")
    return str(response), 200

@app.route("/respond", methods=["POST"])
def respond():
    """Was Chris gesagt hat → Claude → Antwort aussprechen → weiter"""
    global conversation_history
    
    speech_result = request.form.get("SpeechResult", "").strip()
    logger.info(f"Chris sagt: '{speech_result}'")
    
    if not speech_result:
        # Nichts gehört — weiter zuhören
        response = VoiceResponse()
        gather = make_gather()
        response.append(gather)
        response.redirect("/listen")
        return str(response), 200
    
    # Gesprächs-Ende erkennen
    if any(word in speech_result.lower() for word in ["tschüss", "auf wiedersehen", "bye", "ciao"]):
        response = VoiceResponse()
        response.say("Tschüss Chris! Bis bald.", language="de-DE", voice="Polly.Vicki")
        response.hangup()
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
        
        conversation_history.append({
            "role": "assistant",
            "content": luna_reply
        })
        
    except Exception as e:
        logger.error(f"Claude Fehler: {e}")
        luna_reply = "Entschuldigung, kurzer technischer Fehler. Was hast du gesagt?"
    
    # Antwort aussprechen und weiter zuhören
    response = VoiceResponse()
    gather = make_gather()
    say(gather, luna_reply)
    response.append(gather)
    response.redirect("/listen")
    
    return str(response), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
