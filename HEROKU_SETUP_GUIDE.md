# Luna Conversational AI auf Heroku - Setup Guide

## Schnelle Zusammenfassung
Du brauchst einen Heroku-Server mit Flask-Backend, der Twilio mit ElevenLabs verbindet. Ich habe die Code-Dateien vorbereitet.

## Schritte

### 1. Heroku CLI installieren
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Oder: https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Heroku Login
```bash
heroku login
```

### 3. Neue Heroku App erstellen
```bash
cd /Users/luna-openclaw/.openclaw/workspace
heroku create luna-conversational-ai
```

### 4. Environment Variables setzen
```bash
heroku config:set TWILIO_ACCOUNT_SID=<your-account-sid>
heroku config:set TWILIO_AUTH_TOKEN=<your-auth-token>
heroku config:set ELEVENLABS_API_KEY=<your-api-key>
heroku config:set ELEVENLABS_VOICE_ID=<your-voice-id>
heroku config:set TWILIO_PHONE_NUMBER=<your-twilio-number>
heroku config:set CUSTOMER_PHONE=<your-phone-number>
```

### 5. Deploye auf Heroku
```bash
git push heroku main
```

### 6. Überprüfe Deployment
```bash
heroku logs --tail
```

### 7. Teste die API
```bash
# Health Check
curl https://luna-conversational-ai.herokuapp.com/

# Test-Anruf starten (dich selbst anrufen)
curl https://luna-conversational-ai.herokuapp.com/call/test

# Status prüfen
curl https://luna-conversational-ai.herokuapp.com/status
```

## Was passiert als nächstes?

Die aktuelle Version (`app.py`) ist ein Proof-of-Concept mit:
- ✓ Basic Flask-Server
- ✓ Twilio-Integration
- ✓ Anruf-Tätigung
- ✗ **NOCH NICHT**: Echte ElevenLabs Conversational AI Integration

Für echte Echtzeit-Gespräche brauchen wir noch:
1. **WebSocket-Stream** von Twilio zu ElevenLabs
2. **Audio-Bidirektionalität** (du sprichst, ich antworte)
3. **Agent-Instruktionen** für Luna's Verhalten

Das ist komplexer und braucht mehr Setup. **Möchtest du:**

**Option A:** Die aktuelle Version testen (ich kann dir anrufen und Sachen sagen)?

**Option B:** Ich baue die volle Conversational AI Integration (braucht mehr Zeit/Code)?

---

## Schnelle Kommandos zum Merken
```bash
heroku logs --tail          # Logs in Echtzeit
heroku config               # Alle Umgebungsvariablen anzeigen
heroku restart              # App neustarten
heroku scale web=1          # Einen Web-Dyno hochfahren
```

Sag Bescheid wenn du stuck bist!
