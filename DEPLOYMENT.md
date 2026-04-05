# Luna Conversational AI - Deployment auf Heroku

## Überblick

Luna ist jetzt bereit zum Deployment auf Heroku. Die aktuelle Version (`app_v2.py`) kann:

✅ Anrufe tätigen
✅ Restaurants anrufen
✅ Einfache Sprachausgabe (TTS)
⚠️ Echte Conversational AI (braucht noch erweiterte ElevenLabs-Integration)

## Quick Start

```bash
# 1. In den Workspace-Verzeichnis gehen
cd /Users/luna-openclaw/.openclaw/workspace

# 2. Heroku CLI installieren (falls noch nicht)
brew tap heroku/brew && brew install heroku

# 3. Bei Heroku anmelden
heroku login

# 4. Neue App erstellen ODER existing nutzen
heroku create luna-conversational-ai

# 5. Environment Variables setzen
heroku config:set TWILIO_ACCOUNT_SID=<your-account-sid>
heroku config:set TWILIO_AUTH_TOKEN=<your-auth-token>
heroku config:set ELEVENLABS_API_KEY=<your-api-key>
heroku config:set ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
heroku config:set TWILIO_PHONE_NUMBER=+14159034051
heroku config:set CUSTOMER_PHONE=<your-phone-number>
heroku config:set HEROKU_APP_URL=https://luna-conversational-ai.herokuapp.com

# 6. Code deployen
git add app_v2.py requirements.txt Procfile
git commit -m "Deploy Luna v2 with restaurant calling"
git push heroku main

# 7. Logs überprüfen
heroku logs --tail

# 8. Testen
curl https://luna-conversational-ai.herokuapp.com/
curl https://luna-conversational-ai.herokuapp.com/status
curl https://luna-conversational-ai.herokuapp.com/call/test
```

## API Endpoints

### `GET /`
Health Check & Dokumentation

### `GET /status`
System-Status anzeigen

### `GET /call/test`
Test-Anruf zu deiner Nummer (CUSTOMER_PHONE)

### `POST /call/restaurant`
Restauranttisch buchen

**Beispiel:**
```bash
curl -X POST https://luna-conversational-ai.herokuapp.com/call/restaurant \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_name": "Petit Fritz",
    "restaurant_phone": "+4989123456789",
    "date": "2026-04-10",
    "time": "19:00",
    "people_count": 2,
    "name": "Baumann"
  }'
```

## Nächste Schritte für Echte Conversational AI

Um Luna wirklich mit Menschen sprechen zu lassen (nicht nur Text-to-Speech), brauchst du:

1. **ElevenLabs Conversational AI WebSocket Integration**
   - Bidirektionaler Audio-Stream
   - Real-time Speech Recognition
   - Real-time TTS Response

2. **Twilio Voice Webhooks**
   - `/incoming` Endpoint für eingehende Anrufe
   - Audio-Streaming zu ElevenLabs

Das ist komplex aber machbar. Sag Bescheid wenn du das weiter aufbauen möchtest.

## Kosten

- **Heroku:** $7/Monat (1 Web Dyno)
- **Twilio:** ~$1-2 pro Anruf (abhängig von Länge)
- **ElevenLabs:** Kostenlos (Creator Plan mit TTS enthalten)

Insgesamt: ~$10-20/Monat für realistische Nutzung.

## Troubleshooting

### App startet nicht
```bash
heroku logs --tail
# Schau nach Python-Fehlern
```

### Anrufe funktionieren nicht
```bash
# Überprüfe Credentials
heroku config

# Teste Twilio direkt
curl https://luna-conversational-ai.herokuapp.com/call/test
```

### Zu viele Kosten?
- Begrenzte die Anrufanzahl
- Nutze nur während Geschäftszeiten

---

**Bereit zum Deployen?** Schreib mir Bescheid!
