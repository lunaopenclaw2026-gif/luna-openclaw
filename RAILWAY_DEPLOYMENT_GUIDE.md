# Luna Phone System - Railway Deployment Guide

## Why Railway?

- ✅ **Günstiger:** €5/Monat (vs. Heroku €15+)
- ✅ **Schneller:** Git push und deployment in 30 Sekunden
- ✅ **Einfacher:** Web UI statt CLI
- ✅ **Besser für kleine Apps:** Ideal für Luna
- ✅ **Kostenlos testen:** $5 credit pro Monat

## Step 1: Railway Account erstellen

1. Geh zu: https://railway.app
2. Klick "Sign up"
3. Mit GitHub anmelden (easiest)
4. Done!

## Step 2: Neues Project erstellen

1. Klick "Create New Project"
2. Wähle "Deploy from GitHub"
3. Authorize Railway auf GitHub
4. Wähle dein `luna-openclaw` Repo
5. Wähle Branch: `main`

Railway startet automatisch deployment! ✨

## Step 3: Environment Variables setzen

Railway UI:
1. Geh zu deinem Project
2. Klick "Variables" Tab
3. Füge diese hinzu:

```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+14159034051
ELEVENLABS_API_KEY=sk_b330d85b28e2cbb5449b75bea6b6cde92255c92ab33b577b
CHRISTOPHER_PHONE=+4915770368632
FLASK_SECRET_KEY=<random hex string>
```

Für FLASK_SECRET_KEY generieren:
```bash
openssl rand -hex 32
```

## Step 4: Domain/URL bekommen

Railway gibt dir automatisch eine URL:
```
https://luna-phone-system-production.up.railway.app
```

Diese brauchst du für Twilio Webhook!

## Step 5: Twilio Webhook konfigurieren

1. Geh zu: https://www.twilio.com/console/phone-numbers/incoming
2. Klick auf +14159034051
3. Unter "Voice & Fax" → "Configure with a URL"
4. Gib ein:
   - **URL:** `https://luna-phone-system-production.up.railway.app/incoming-call`
   - **Method:** POST
5. **Save**

## Step 6: Test Call

```bash
# Dein Telefon sollte sofort klingeln
# Warten... Luna antwortet!
```

Oder per Railway CLI:
```bash
# Terminal vom Railway Project öffnen
railway shell

# Test call ausführen
python3 luna_phone_system.py test
```

## Step 7: Profit!

Deine Luna Phone System läuft live auf Railway! 🚀

## Deployment Flow

Jetzt ist es super einfach:

```bash
# Make changes locally
vim twilio_elevenlabs_integration.py

# Commit & push
git add .
git commit -m "Update Luna phone system"
git push origin main

# Railway deployt automatisch in ~30 Sekunden
# Schau auf: https://railway.app
```

Keine `git push heroku` Befehle mehr!

## Monitoring

Railway Dashboard zeigt:
- ✅ Deployment status (live/failed)
- 📊 CPU/Memory usage
- 📝 Real-time logs
- 🔧 Environment variables
- 💰 Costs

## Troubleshooting

### Deployment failed?
1. Klick auf "Deployments" Tab
2. Schau "Build Logs" und "Deploy Logs"
3. Häufig: Environment variable fehlt

### Incoming call funktioniert nicht?
1. Überprüf Twilio Webhook URL ist korrekt gesetzt
2. Schau Railway logs in "Logs" Tab
3. Überprüf dass ELEVENLABS_API_KEY richtig ist

### App startet nicht?
1. Überprüf dass `Procfile` vorhanden ist
2. Überprüf dass `requirements.txt` alle Dependencies hat
3. Überprüf dass `twilio_elevenlabs_integration.py` syntax-valid ist

## Scaling (später)

Falls du später mehr brauchst:
- Railway zeigt Kosten in Echtzeit
- Unbegrenzte Bandbreite
- Auto-scaling wenn Traffic steigt

## Costs Breakdown

| Service | Cost |
|---------|------|
| Railway Server | €5/Monat (included in credit) |
| Twilio Phone | ~€1/Monat |
| Twilio Calls | ~0,01€/Min |
| ElevenLabs | Included (Creator Plan) |
| **Total** | ~€6-8/Monat |

(Viel billiger als Heroku!)

## Next Steps

1. ✅ Create Railway account
2. ✅ Connect GitHub repo
3. ✅ Set environment variables
4. ✅ Set Twilio webhook
5. ✅ Make test call
6. 🎉 Start using!

## Need Help?

Railway support ist super responsiv:
- Chat support in app
- Community Discord: https://discord.gg/railway

---

**That's it!** Railway ist so viel einfacher als Heroku. 🚀

Viel Erfolg beim Deployment!
