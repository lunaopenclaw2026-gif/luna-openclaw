# Luna Phone System - Complete Setup

## What You Now Have

Ein komplettes System damit du mit Luna **per Telefon** sprechen kannst:

- 📱 **Incoming calls** — Ruf Luna an (+14159034051), sie antwortet
- 🤖 **Full context** — Luna kennt alles aus unseren Chats
- 🍴 **Restaurant booking** — Luna kann Restaurants anrufen und buchen
- 📅 **Appointments** — Luna kann Termine vereinbaren
- 🌍 **Anywhere** — Über Telefon, egal wo du bist

## Files Created

| File | Purpose |
|------|---------|
| `twilio_elevenlabs_integration.py` | Flask backend für Twilio + ElevenLabs |
| `media_stream_handler.py` | WebSocket handler für real-time audio |
| `luna_phone_system.py` | CLI + orchestration |
| `chat_context_manager.py` | Lädt unsere Chat-History für Luna |
| `HEROKU_DEPLOYMENT_GUIDE.md` | Step-by-step Deployment Anleitung |
| `requirements.txt` | Python dependencies |
| `Procfile` | Heroku process definition |

## Nächste Schritte

### 1. Deploy to Heroku (15 Minuten)

```bash
cd /Users/luna-openclaw/.openclaw/workspace

# Login zu Heroku
heroku login

# App erstellen
heroku create luna-phone-system

# Environment variables setzen
heroku config:set \
  TWILIO_ACCOUNT_SID="AC..." \
  TWILIO_AUTH_TOKEN="..." \
  TWILIO_PHONE_NUMBER="+14159034051" \
  ELEVENLABS_API_KEY="sk_b330d85b28e2cbb5449b75bea6b6cde92255c92ab33b577b" \
  CHRISTOPHER_PHONE="+4915770368632" \
  HEROKU_APP_URL="https://luna-phone-system.herokuapp.com" \
  FLASK_SECRET_KEY="$(openssl rand -hex 32)"

# Commit & Push
git add .
git commit -m "Deploy Luna phone system"
git push heroku main

# Check logs
heroku logs --tail
```

### 2. Test Call

```bash
heroku run python3 luna_phone_system.py test
```

Dein Telefon sollte klingeln → Luna antwortet!

### 3. Start using!

Ruf einfach an: **+14159034051**

Luna nimmt ab und spricht mit dir.

## Technical Architecture

```
┌─────────────┐
│ Du rufst an │
└──────┬──────┘
       │ (PSTN über Twilio)
       ↓
┌──────────────────────┐
│ Twilio               │
│ +14159034051         │
└──────┬───────────────┘
       │ (WebSocket)
       ↓
┌──────────────────────────────┐
│ Heroku App (Luna)            │
│ - Twilio handler             │
│ - WebSocket streaming        │
│ - ElevenLabs integration     │
│ - Chat context injection     │
└──────┬───────────────────────┘
       │ (API)
       ↓
┌──────────────────────────────┐
│ ElevenLabs Conversational AI │
│ - Speech-to-Text             │
│ - LLM (mein Denken)          │
│ - Text-to-Speech             │
└──────┬───────────────────────┘
       │ (Audio response)
       ↓
┌─────────────────────┐
│ Du hörst Lunas      │
│ Stimme (ElevenLabs) │
└─────────────────────┘
```

## What Makes This Different

### ❌ Das alte Luna-Agent-Setup:
- Luna = Fertiger Agent (wenig Kontext)
- Klingt robotisch
- Keine echte Konversation

### ✅ Das neue Setup:
- Luna = Ich (mit Twilio + ElevenLabs als Interface)
- Voller Chat-Kontext
- Echte, natürliche Konversationen
- Kann denken und entscheiden

## Important Notes

1. **ElevenLabs Stimme** — Das ist nicht deine echte Stimme, aber klingt naturalistisch
2. **Deutsch** — Luna spricht standardmäßig German, kann aber zu English switchen
3. **Latency** — ~500-1000ms Verzögerung ist normal (PSTN limitation)
4. **Recording** — Alle Calls werden recorded (optional in Procfile disablebar)
5. **Kosten** — ~€1-2/Monat für Telefon + ein paar Cent pro Anruf

## Customization

### Andere Stimme
```python
# In media_stream_handler.py
voice_id="eXpIbVcVbLo8ZJQDlDnl"  # Change this to another ElevenLabs voice
```

Available voices: https://elevenlabs.io/docs/voices

### Andere Sprache
```python
# In media_stream_handler.py
language="de"  # Change to "en", "fr", etc.
```

### Mehr Context
Edit `chat_context_manager.py` — add more memory files, adjust prompts, etc.

## Troubleshooting

**Incoming call, aber Luna antwortet nicht:**
- Überprüf `heroku logs --tail` auf Fehler
- Überprüf dass Twilio webhook URL richtig ist
- Überprüf Environment variables

**Schlechte Audio-Qualität:**
- Normal bei PSTN (8kHz). Nutze VoIP für bessere Qualität.

**Luna antwortet falsch:**
- Überprüf dass ElevenLabs API Key stimmt
- Überprüf dass chat_context_manager.py deine Memory files findet

## What's Next

- [ ] **Voice cloning** — Nutze deine eigene Stimme statt ElevenLabs
- [ ] **Inbound calls** — Restaurants können dich callback-en
- [ ] **Automated booking** — Luna bucht automatisch ohne zu fragen
- [ ] **Call recording** — Transkripte unserer Telefonate
- [ ] **Analytics** — Track successful bookings, etc.

---

**Ready to go live!** 🚀

Sag mir wenn du ready bist zum Deployen oder wenn du Fragen hast.
