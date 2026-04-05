#!/usr/bin/env python3
"""
Heroku Setup für Luna Conversational AI
"""

import subprocess
import os
import sys

def run(cmd):
    """Führe Shell-Befehl aus"""
    print(f"\n→ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ Fehler: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    print("=== Luna Conversational AI auf Heroku Setup ===\n")
    
    # 1. Heroku Login
    print("1. Heroku Login...")
    if not run("heroku login"):
        print("Bitte führe 'heroku login' manuell aus")
        return
    
    # 2. Erstelle Heroku App
    print("\n2. Erstelle Heroku App...")
    run("heroku create luna-conversational-ai")
    
    # 3. Setze Environment Variables
    print("\n3. Setze Credentials...")
    env_vars = {
        "TWILIO_ACCOUNT_SID": "<your-account-sid>",
        "TWILIO_AUTH_TOKEN": "<your-auth-token>",
        "ELEVENLABS_API_KEY": "<your-api-key>",
        "ELEVENLABS_VOICE_ID": "<your-voice-id>",
        "TWILIO_PHONE_NUMBER": "<your-twilio-number>",
        "CUSTOMER_PHONE": "<your-phone-number>"
    }
    
    for key, value in env_vars.items():
        run(f"heroku config:set {key}={value}")
    
    print("\n✓ Setup komplett!")
    print("Nächste Schritte:")
    print("  1. git push heroku main (um Code zu deployen)")
    print("  2. heroku logs --tail (um Logs zu sehen)")

if __name__ == "__main__":
    main()
