#!/usr/bin/env python3
"""
Luna Conversational AI Call Handler
Nutzt Twilio für Anrufe + ElevenLabs für Sprachverarbeitung
"""

from twilio.rest import Client
from elevenlabs.client import ElevenLabs
import json
import sys

def load_credentials():
    with open("/Users/luna-openclaw/.openclaw/workspace/.twilio_config.json") as f:
        return json.load(f)

def make_call_with_conversation(to_number, purpose="restaurant_booking"):
    """
    Tätige einen Anruf und führe ein Gespräch
    """
    config = load_credentials()
    twilio = Client(config["account_sid"], config["auth_token"])
    elevenlabs = ElevenLabs(api_key=config["elevenlabs_key"])
    
    from_number = "+14159034051"
    
    instructions = {
        "restaurant_booking": """Du bist Luna, ein virtueller Assistent. Du möchtest einen Tisch reservieren.
Frage nach: Datum, Uhrzeit, Anzahl Personen, Name.
Bestätige am Ende alle Details.""",
        "appointment": """Du bist Luna und möchtest einen Termin vereinbaren.
Frage nach bevorzugtem Datum und Uhrzeit.""",
        "general": """Du bist Luna, ein hilfreicher Assistent von Christopher Baumann.
Führe ein natürliches Gespräch."""
    }
    
    # Für jetzt: einfache Anrufe mit vorgesprochenen Prompts
    # Die echte Conversational AI braucht einen Server-Endpoint
    
    print(f"Rufe {to_number} an...")
    
    try:
        # Text-to-Speech für Begrüßung
        audio = elevenlabs.text_to_speech.convert(
            voice_id=config["elevenlabs_voice"],
            text="Hallo Chris, ich bin Luna. Ich rufe dich an um einen Restauranttisch zu reservieren. Drücke 1 um zu sprechen.",
            model_id="eleven_multilingual_v2"
        )
        
        # Speichere Audio
        with open("/tmp/luna_greeting.mp3", "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        # Starte Anruf
        call = twilio.calls.create(
            to=to_number,
            from_=from_number,
            twiml=f'''<Response>
                <Say language="de">Hallo, ich bin Luna, ein virtueller Assistent. Ich möchte einen Restauranttisch für dich reservieren.</Say>
                <Gather numDigits="1" timeout="5">
                    <Say language="de">Drücke 1 um fortzufahren.</Say>
                </Gather>
            </Response>'''
        )
        
        print(f"✓ Anruf gestartet: {call.sid}")
        print(f"Status: {call.status}")
        return call.sid
        
    except Exception as e:
        print(f"✗ Fehler: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 luna_call_handler.py <to_number> [purpose]")
        print("Example: python3 luna_call_handler.py +4915770368632 restaurant_booking")
        sys.exit(1)
    
    to_number = sys.argv[1]
    purpose = sys.argv[2] if len(sys.argv) > 2 else "restaurant_booking"
    
    make_call_with_conversation(to_number, purpose)
