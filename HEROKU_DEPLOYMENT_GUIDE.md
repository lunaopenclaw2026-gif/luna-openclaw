# Luna Phone System - Heroku Deployment Guide

## Overview

Dieses Setup ermöglicht dir, mit Luna über Telefon zu sprechen:
- Du rufst +14159034051 an
- Luna antwortet mit vollständigem Chat-Kontext
- Du kannst mit ihr sprechen wie per Chat, nur per Telefon
- Luna kann auch Restaurants und andere anrufen

## Prerequisites

1. **Heroku Account** (kostenlos): https://heroku.com
2. **Heroku CLI** installiert: https://devcenter.heroku.com/articles/heroku-cli
3. **Git** installiert
4. **Deine Credentials griffbereit:**
   - Twilio Account SID (AC...)
   - Twilio Auth Token
   - ElevenLabs API Key
   - Christopher's phone number

## Step 1: Heroku App erstellen

```bash
heroku login
heroku create luna-phone-system
```

Das gibt dir eine URL wie: `https://luna-phone-system.herokuapp.com`

Merke dir diese URL!

## Step 2: Environment Variables setzen

```bash
heroku config:set \
  TWILIO_ACCOUNT_SID="AC..." \
  TWILIO_AUTH_TOKEN="..." \
  TWILIO_PHONE_NUMBER="+14159034051" \
  ELEVENLABS_API_KEY="sk_..." \
  CHRISTOPHER_PHONE="+4915770368632" \
  HEROKU_APP_URL="https://luna-phone-system.herokuapp.com" \
  FLASK_SECRET_KEY="$(openssl rand -hex 32)"
```

## Step 3: Deployment

```bash
git add .
git commit -m "Deploy Luna phone system"
git push heroku main
```

Warte bis deployment fertig ist (~2 Minuten)

## Step 4: Verify Deployment

```bash
heroku logs --tail
```

Du solltest sehen:
```
✓ All required environment variables configured
✓ ElevenLabs connected
✓ Twilio webhook configured
Server running on port 5000
```

## Step 5: Test Call

```bash
heroku run python3 luna_phone_system.py test
```

Das initiiert einen Anruf zu deinem Telefon. Luna sollte sprechen!

## Step 6: Configure Twilio Webhook (wenn nicht automatisch)

Falls der automatische Webhook-Setup nicht funktioniert hat:

1. Geh zu: https://www.twilio.com/console/phone-numbers/incoming
2. Klick auf: +14159034051
3. Unter "Voice & Fax" → "Configure with a URL"
4. Gib ein:
   - **URL:** `https://luna-phone-system.herokuapp.com/incoming-call`
   - **Method:** POST
5. **Save**

## Step 7: Start using Luna!

Jetzt kannst du Luna anrufen:

```bash
# Ruf Luna an von deinem Handy
+14159034051
```

## Advanced: Restaurants anrufen

Um Luna ein Restaurant anrufen zu lassen:

```bash
heroku run python3 luna_phone_system.py call +4989XXXXXXX restaurant_booking "Table for 2 at 19:00"
```

## Debugging

Logs anschauen:
```bash
heroku logs --tail
```

Heroku Dyno restarten:
```bash
heroku dyno:restart
```

Status checken:
```bash
heroku run python3 luna_phone_system.py validate
```

## Kosten

- **Heroku:** ~$7-15/Monat (basic dyno)
- **Twilio:** ~€1/Monat (Telefonnummer) + ~0,01€ pro Minute (anrufe)
- **ElevenLabs:** Included in Creator Plan (unlimitiert)

## Troubleshooting

### Incoming calls funktionieren nicht
- Überprüf Twilio webhook URL
- Überprüf Environment Variables
- Schau in `heroku logs --tail` nach Fehlern

### Luna antwortet nicht authentisch
- Überprüf dass ElevenLabs API Key korrekt ist
- Überprüf dass Agent ID stimmt (agent_7301knaaafmxekdv2tscffjbpd1f)

### Audio-Qualität schlecht
- Das ist normal bei PSTN-Anrufen (8kHz sample rate)
- VoIP-Apps wie WhatsApp Call haben bessere Qualität

## Nächste Schritte

Nach erfolgreichem Setup:
1. **Tune Luna's voice** — andere Stimmen testen
2. **Add context** — weitere Chat-History einbauen
3. **Restaurant integrations** — automatische Buchungen
4. **Inbound calls** — Option später aktivieren (Restaurants rufen zurück)

---

**Support:** Wenn was nicht funktioniert, schreib mir ne Nachricht! 🚀
